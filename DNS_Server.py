import socket
from DNS_Packet import DNSPacket
from DNS_Header import DNSHeader
from DNS_Question import DNSQuestion
from DNS_Record import DNSRecord

if __name__ == '__main__':
    print("INSIDE DNS SERVER")

    domain = "en.wikipedia.org"
    qtype = 15


    proxy_server = ("8.8.8.8", 53)
    host = "0.0.0.0"
    port = 3000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))

    # Build a DNS packet
    # with open("query_packet.txt", "rb") as f:
    #     content = f.read()

    # print(''.join('{:02x} '.format(x) for x in content))

    # dnsPacket = DNSPacket.getDNSPacketFromBuffer(content)

    dnsHeader = DNSHeader(id=34234, opcode=0, recursion_desired=1, recursion_available=0,
            is_truncated=0, is_authoritative=0, is_response=0, rescode=0, z=0,
            questions=1, answers=0, authoritative_entries=0, resource_entries=0)
    
    dnsQuestions = [DNSQuestion(ques_name=domain, ques_type=qtype, ques_class=1)]

    dnsPacket = DNSPacket(header=dnsHeader, questions=dnsQuestions, answers=[], authority_entries=[], additional_entries=[])

    content = dnsPacket.encodeDNSPacket()
    print("printing raw sending data")
    print(''.join('{:02x} '.format(x) for x in content))


    sock.sendto(content, proxy_server)

    data = sock.recv(1024)
    print("printing raw return data")
    print(''.join('{:02x} '.format(x) for x in data))

    dnsPacket2 = DNSPacket.getDNSPacketFromBuffer(data)

    encodedPacket = dnsPacket2.encodeDNSPacket()

    dnsPacket2 = DNSPacket.getDNSPacketFromBuffer(encodedPacket)
    
    print("PRINTING HEADER INFO")
    dnsPacket2.header.printHeaderInfo()

    print()
    print()

    print("PRINTING QUESTION INFO")

    for ques in dnsPacket2.questions:
        ques.printQuestionInfo()

    print()
    print()


    print("PRINTING ANSWER INFO")

    for ans in dnsPacket2.answers:
        ans.printRecordInfo()

    print()
    print()