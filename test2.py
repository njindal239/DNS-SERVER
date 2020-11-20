import socket

print("Hello world")

ip_addr = "2607:f8b0:400a:801::200e"
print(ip_addr)

bytes_form = socket.inet_pton(socket.AF_INET6, ip_addr)

print(bytes_form)

print(''.join('{:02x} '.format(x) for x in bytes_form))