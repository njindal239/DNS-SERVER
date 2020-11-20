import struct
import socket

from utils import decode_labels, encode_labels, combine_labels
from record_type import RecordType

class DNSRecord:

    def __init__(self, domain, recordTypeNum, recordClass, ttl, length, ip_addr=None, host=None, priority=None):
        self.domain = domain
        self.recordTypeNum = recordTypeNum
        self.recordClass = recordClass
        self.recordType = RecordType.getRecordType(self.recordTypeNum)
        self.ttl = ttl
        self.length = length

        # Extra fields for different types of records
        self.ip_addr = ip_addr # for record type A, AAAA
        self.host = host # for record type NS, CNAME, MX
        self.priority = priority # for MX


    @classmethod
    def getDNSRecordFromBuffer(cls, message, offset):

       # Getting length of domain
        length, = struct.unpack_from("!B", message, offset)
        offset += 1

        # calling recursively if it points to another address else calling it normally.
        if length & 0xC0 != 0:
            name, _ = decode_labels(message, message[offset])
            offset += 1
        else:
            name, offset = decode_labels(message, offset-1)

        # Saving name in ans dictionary.
        domain = (b".".join(name)).decode()

        # Getting and saving class type
        recordTypeNum, = struct.Struct("!H").unpack_from(message[offset:offset+2])
        recordType = RecordType.getRecordType(recordTypeNum)
        offset += 2

        # Getting class and saving class.
        cls, = struct.Struct("!H").unpack_from(message[offset:offset+2])
        offset += 2
        recordClass = cls

        # Getting ttl.
        ttl, = struct.Struct("!I").unpack_from(message[offset:offset+4])
        offset += 4

        # Getting response data length. 
        length, = struct.Struct("!H").unpack_from(message[offset:offset+2])
        offset += 2

        # baking up the offset.
        org_offset = int(offset)

        ip_addr = None
        host = None
        priority = None
        decompressed_length = length
        if (recordType == RecordType.A):
            ip_addr = socket.inet_ntop(socket.AF_INET, message[offset:offset+4])
        elif (recordType == RecordType.AAAA): # check it ipv6 is not complete yet
            ip_addr = socket.inet_ntop(socket.AF_INET6, message[offset:offset+16])
        elif (recordType == RecordType.NS):
            host_labels, offset = decode_labels(message, offset)
            host = combine_labels(host_labels)
            decompressed_length = len(host) + 2
        elif (recordType == RecordType.CNAME):
            host_labels, offset = decode_labels(message, offset)
            host = combine_labels(host_labels)
            decompressed_length = len(host) + 2
        elif (recordType == RecordType.MX):
            priority, = struct.Struct("!H").unpack_from(message[offset:offset+2])
            offset += 2
            host_labels, offset = decode_labels(message, offset)
            host = combine_labels(host_labels)
            decompressed_length = 2 + len(host) + 2

        offset = org_offset + length
        length = decompressed_length
        
        return DNSRecord(
            domain=domain,
            recordTypeNum=recordTypeNum,
            recordClass=recordClass,
            ttl=ttl,
            length=length,
            ip_addr=ip_addr,
            host = host,
            priority=priority
        ), offset

    
    def toBytes(self):

        if (self.recordType == RecordType.UNKNOWN):
            # Unsupported Record Type
            return None

        record_bytes = encode_labels(self.domain)
        record_bytes += self.recordTypeNum.to_bytes(2, byteorder='big')
        record_bytes += self.recordClass.to_bytes(2, byteorder='big')
        record_bytes += self.ttl.to_bytes(4, byteorder='big')
        record_bytes += self.length.to_bytes(2, byteorder='big')

        if (self.recordType == RecordType.A):
            ip_array = self.splitIpIntoInts()
            for ip in ip_array:
                record_bytes += ip.to_bytes(1, 'big')
        elif (self.recordType == RecordType.AAAA):
            record_bytes += socket.inet_pton(socket.AF_INET6, self.ip_addr)
        elif (self.recordType == RecordType.NS):
            record_bytes += encode_labels(self.host)
        elif (self.recordType == RecordType.CNAME):
            record_bytes += encode_labels(self.host)
        elif (self.recordType == RecordType.MX):
            record_bytes += self.priority.to_bytes(2, 'big')
            record_bytes += encode_labels(self.host)
        
        return record_bytes


    def printRecordInfo(self):
        result = {
            "Domain Name": self.domain,
            "Record Type": self.recordType,
            "Record Type Num": self.recordTypeNum,
            "Record Class": self.recordClass,
            "Record TTL": self.ttl,
            "Record Len": self.length,
            "Record IP": self.ip_addr,
            "Record Host": self.host,
            "priority": self.priority
        }
        print(result)

    def splitIpIntoInts(self):
        ip_array = []

        splits = self.ip_addr.split('.')
        for split in splits:
            ip_array.append(int(split))
        
        return ip_array
