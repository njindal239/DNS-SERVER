from res_code import ResCode
from DNS_Header import DNSHeader
from DNS_Packet import DNSPacket
# import socket


# HOST = "127.0.0.1"
# PORT = 3000
# # print(ResCode.getResCode(0))
# # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# # sock.bind((HOST, PORT))

# # data, addr = sock.recvfrom(1024)
# # # dnsHeader = DNSHeader(data)
# # # dnsHeader.printHeaderInfo()
# # # print(data)

# # dnsPacket = DNSPacket(data)

# # print("PRINTING HEADER INFO")
# # dnsPacket.header.printHeaderInfo()

# # print()
# # print()

# # print("PRINTING QUESTION INFO")

# # for ques in dnsPacket.questions:
# #     ques.printQuestionInfo()

# # print()
# # print()

# # print("PRINTING ACTUAL DATA")
# # print(''.join('{:02x} '.format(x) for x in data))

# # print()
# # print()

# # str = ""
# # for ch in data:
# # 	str += hex(ord(ch))+" "
# # print(str)

# with open("response_packet.txt", "rb") as f:
#     content = f.read()

# print(''.join('{:02x} '.format(x) for x in content))

# dnsPacket = DNSPacket.getDNSPacketFromBuffer(content)

# print("PRINTING HEADER INFO")
# dnsPacket.header.printHeaderInfo()

# print()
# print()

# print("PRINTING QUESTION INFO")

# for ques in dnsPacket.questions:
#     ques.printQuestionInfo()

# print()
# print()


# print("PRINTING ANSWER INFO")

# for ans in dnsPacket.answers:
#     ans.printRecordInfo()

# print()
# print()

# # dnsPacket.header.toBytes()
# # dnsPacket.questions[0].toBytes()
# # dnsPacket.answers[0].toBytes()
# dnsPacket.encodeDNSPacket()


dnsPacket = DNSPacket(header=None)

print(dnsPacket.questions)
print(dnsPacket.answers)