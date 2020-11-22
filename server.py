import socket
from DNS_Packet import DNSPacket
from DNS_Header import DNSHeader
from DNS_Question import DNSQuestion
from res_code import ResCode
from record_type import RecordType
from cache_manager import CacheManager
from threading import Thread
from constants import HOST, DEFAULT_PORT, RANDOM_REQUEST_HEADER, ROOT_DNS_SERVER, CACHE_FILE_NAME

def create_final_response_packet(request, rescode, answer_records=None):

    dns_response_header = DNSHeader(
        id = request.header.id,
        opcode = 0,
        recursion_desired = request.header.recursion_desired,
        recursion_available = True,
        is_truncated = False,
        is_authoritative = False,
        is_response = True,
        rescode = rescode,
        z = 0,
        questions = request.header.questions,
        answers = len(answer_records),
        authoritative_entries = 0,
        resource_entries = 0
    )

    final_response_packet = DNSPacket(
        header=dns_response_header,
        questions=[],
        answers=[],
        authority_entries=[],
        additional_entries=[]
    )


    for question in request.questions:
        final_response_packet.questions.append(question)

    for answer in answer_records:
        final_response_packet.answers.append(answer)

    return final_response_packet



def query_authoritative_dns_server(ques_domain_name, ques_type, server):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    dns_request_header = DNSHeader(
        id = RANDOM_REQUEST_HEADER,
        opcode = 0,
        recursion_desired = False,
        recursion_available = False,
        is_truncated = False,
        is_authoritative = False,
        is_response = False,
        rescode = 0,
        z = 0,
        questions = 1,
        answers = 0,
        authoritative_entries = 0,
        resource_entries = 0
    )

    dns_request_packet = DNSPacket(
        header=dns_request_header,
        questions=[],
        answers=[],
        authority_entries=[],
        additional_entries=[]
    )

    dns_question = DNSQuestion(
        ques_name = ques_domain_name,
        ques_type = ques_type,
        ques_class = 1
    )
    dns_request_packet.questions.append(dns_question)

    encoded_request_packet = dns_request_packet.encodeDNSPacket()

    sock.sendto(encoded_request_packet, server)

    response_packet, _ = sock.recvfrom(1024)

    return DNSPacket.getDNSPacketFromBuffer(response_packet)


def recursive_lookup(ques_domain_name, ques_type):
    # Starting with a.root-servers.net
    ns = ROOT_DNS_SERVER

    while True:
        print("Looking up now: " + ques_domain_name + " in " + ns)

        ns_copy = ns

        server = (ns_copy, 53)
        response = query_authoritative_dns_server(ques_domain_name, ques_type, server)

        # If there are entries in the answer section, and no errors, we are done!
        if len(response.answers) > 0 and response.header.rescode == ResCode.NOERROR:
            # Here we need to check if the type of returned answer is CNAME
            if all(ans.recordType == RecordType.CNAME for ans in response.answers):
                recursive_cname_response = recursive_lookup(response.answers[0].host, ques_type)
                for answer in recursive_cname_response.answers:
                    response.answers.append(answer)
                    response.header.answers += 1
            return response

        # We might also get a `NXDOMAIN` reply, which is the authoritative name servers
        # way of telling us that the name doesn't exist.
        if response.header.rescode == ResCode.NXDOMAIN:
            return response

        # Otherwise, we'll try to find a new nameserver based on NS and a corresponding A
        # record in the additional section. If this succeeds, we can switch name server
        # and retry the loop.
        nsRecordIpAddress = response.getNSRecordIpAddress(ques_domain_name)
        if nsRecordIpAddress is not None:
            ns = nsRecordIpAddress
            continue

        # If not, we'll have to resolve the ip of a NS record. If no NS records exist,
        # we'll go with what the last server told us.
        nsRecord = response.getUnresolvedNS(ques_domain_name)
        if nsRecord is None:
            return response
        
        # Here we go down the rabbit hole by starting _another_ lookup sequence in the
        # midst of our current one. Hopefully, this will give us the IP of an appropriate
        # name server.
        recursive_response = recursive_lookup(nsRecord[1], 1)

        # Finally, we pick a random ip from the result, and restart the loop. If no such
        # record is available, we again return the last result we got.
        nsRecordIpAddress = recursive_response.getRandomIPv4AnswerRecord()
        
        if nsRecordIpAddress is None:
            return response
        ns = nsRecordIpAddress


def handleQuery(sock, cache_manager, request, addr):
    
    dns_request_packet = DNSPacket.getDNSPacketFromBuffer(request)

    requested_domain = dns_request_packet.questions[0].ques_name
    request_ques_type = dns_request_packet.questions[0].ques_type

    # Check if the request can be served through cache
    cached_value = cache_manager.get_cache_entry(requested_domain, request_ques_type)
    if (cached_value is None):
        dns_response_packet = recursive_lookup(requested_domain, request_ques_type)
        res_code = dns_response_packet.header.rescode
        answer_records = dns_response_packet.answers
        if (len(answer_records) > 0):
            cache_manager.add_cache_entry(requested_domain, request_ques_type, answer_records)
    else:
        res_code = ResCode.NOERROR
        answer_records = cached_value
    

    final_response_packet = create_final_response_packet(dns_request_packet, res_code, answer_records)
    encoded_response = final_response_packet.encodeDNSPacket()

    sock.sendto(encoded_response, addr)


if __name__ == '__main__':
    # Bind a UDP Socket to listen for DNS requests
    server = (HOST, DEFAULT_PORT)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((HOST, DEFAULT_PORT))

        cache_manager = CacheManager(cacheFileName=CACHE_FILE_NAME)

        while True:
            # Receiving dns question query from client.
            request, addr = sock.recvfrom(1024)

            ## Start the thread
            t = Thread(target=handleQuery, args=(
                sock, cache_manager, request, addr))
            t.start()

    except KeyboardInterrupt:
        # Saving catched data in persistance storage if server is killed explicitly.
        cache_manager.save_to_file(CACHE_FILE_NAME)
        sock.close()

    except Exception as error:
        # Saving catched data in persistance storage if server is killed by unknown error.
        cache_manager.save_to_file(CACHE_FILE_NAME)
        print(error)
        sock.close()
