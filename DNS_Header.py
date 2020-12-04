import struct

from res_code import ResCode

class DNSHeader:
    DNS_HEADER_FORMAT = struct.Struct("!6H")
    
    def __init__(self, id, opcode, recursion_desired, recursion_available, is_truncated,
            is_authoritative, is_response, rescode, z, questions, answers,
            authoritative_entries, resource_entries):

        self.id = id
        self.opcode = opcode
        self.recursion_desired = recursion_desired
        self.recursion_available = recursion_available
        self.is_truncated = is_truncated
        self.is_authoritative = is_authoritative
        self.is_response = is_response
        self.rescode = ResCode.getResCode(rescode)
        self.z = z
        self.size = DNSHeader.DNS_HEADER_FORMAT.size
        

        self.questions = questions
        self.answers = answers
        self.authoritative_entries = authoritative_entries
        self.resource_entries = resource_entries


    """
    Decode DNS Header information from bytes
    """
    @classmethod
    def getDNSHeaderFromBuffer(cls, buffer):
        id, misc, qdcount, ancount, nscount, arcount = DNSHeader.DNS_HEADER_FORMAT.unpack_from(buffer)

        qr = (misc & 0x8000) != 0
        opcode = (misc & 0x7800) >> 11
        aa = (misc & 0x0400) != 0
        tc = (misc & 0x200) != 0
        rd = (misc & 0x100) != 0
        ra = (misc & 0x80) != 0
        z = (misc & 0x70) >> 4
        rcode = misc & 0xF

        return DNSHeader(id=id, opcode=opcode, recursion_desired=rd, recursion_available=ra,
            is_truncated=tc, is_authoritative=aa, is_response=qr, rescode=rcode, z=z,
            questions=qdcount, answers=ancount, authoritative_entries=nscount, resource_entries=arcount)

    """
    Decode DNS Header information into bytes
    """
    def toBytes(self):
        headerBytes = self.id.to_bytes(2, "big")
       
        # Encode first byte
        firstByte = self.recursion_desired | (self.is_truncated << 1) | (self.is_authoritative << 2) | (self.opcode << 3) | (self.is_response << 7)
        headerBytes += firstByte.to_bytes(1, "big")

        # Encode second byte
        secondByte = self.rescode.value | (self.z << 4) | (self.recursion_available << 7)
        headerBytes += secondByte.to_bytes(1, "big")

        # Encoding remaining 8 bytes
        headerBytes += self.questions.to_bytes(2, "big")
        headerBytes += self.answers.to_bytes(2, "big")
        headerBytes += self.authoritative_entries.to_bytes(2, "big")
        headerBytes += self.resource_entries.to_bytes(2, "big")

        return headerBytes


    """
    Dump DNS Header to screen
    """
    def printHeaderInfo(self):
        result = {"id": self.id,
            "is_response": self.is_response,
            "opcode": self.opcode,
            "is_authoritative": self.is_authoritative,
            "is_truncated": self.is_truncated,
            "recursion_desired": self.recursion_desired,
            "recursion_available": self.recursion_available,
            "reserved": self.z,
            "response_code": self.rescode,
            "question_count": self.questions,
            "answer_count": self.answers,
            "authority_count": self.authoritative_entries,
            "additional_count": self.resource_entries,
        }

        print(result)
