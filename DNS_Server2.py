import socket
from DNS_Packet import DNSPacket
from DNS_Header import DNSHeader
from res_code import ResCode


host = '0.0.0.0'
port = 3000


def query_other_dns_server(dns_query_packet):
    server = ('8.8.8.8', 53)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto(dns_query_packet, server)

    response_packet, addr = sock.recvfrom(1024)

    print("PRINTING DIRECTLY WHATS COMING")
    print(''.join('{:02x} '.format(x) for x in response_packet))
    print("ENDING")

    return DNSPacket.getDNSPacketFromBuffer(response_packet)



def handleQuery(sock):
    # Receiving dns question query from client.
    request, addr = sock.recvfrom(1024)
    
    dns_request_packet = DNSPacket.getDNSPacketFromBuffer(request)

    dns_response_packet = query_other_dns_server(request)

    # Create and initialize a response packet
    dns_response_header = DNSHeader(
        id = dns_request_packet.header.id,
        opcode = dns_request_packet.header.opcode,
        recursion_desired = dns_request_packet.header.recursion_desired,
        recursion_available = True,
        is_truncated = False,
        is_authoritative = False,
        is_response = True,
        rescode = dns_response_packet.header.rescode,
        z = dns_response_packet.header.z,
        questions = len(dns_response_packet.questions),
        answers = len(dns_response_packet.answers),
        authoritative_entries = len(dns_response_packet.authority_entries),
        resource_entries = len(dns_response_packet.additional_entries),
    )

    # dns_response_packet.header = dns_response_header
    dns_response_packet.header.id = dns_request_packet.header.id

    encoded_response = dns_response_packet.encodeDNSPacket()

    # print(''.join('{:02x} '.format(x) for x in request))

    # print()
    # print()
    # print(dns_response_packet.header.rescode)
    # print(len(dns_response_packet.questions))
    # print(len(dns_response_packet.answers))
    # print(len(dns_response_packet.authority_entries))
    # print(len(dns_response_packet.additional_entries))
    print("PRINTING ENCODED RESPONSE")
    print(''.join('{:02x} '.format(x) for x in encoded_response))

    dns_response_packet.header.printHeaderInfo()
    dns_response_packet.questions[0].printQuestionInfo()
    # dns_response_packet.answers[0].printRecordInfo()
    # dns_response_packet.additional_entries[0].printRecordInfo()

    for answer in dns_response_packet.answers:
        answer.printRecordInfo()

    sock.sendto(encoded_response, addr)


if __name__ == '__main__':
    # Bind a UDP Socket to listen for DNS requests
    server = (host, port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))

    while True:
        handleQuery(sock)