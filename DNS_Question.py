import struct

from utils import decode_labels, encode_labels, combine_labels

class DNSQuestion:
    DNS_QUERY_SECTION_FORMAT = struct.Struct("!2H")
    
    def __init__(self, ques_name, ques_type=1, ques_class=1):
        self.ques_name = ques_name
        self.ques_type = ques_type
        self.ques_class = ques_class


    """
    Decode DNS Question information from bytes
    """
    @classmethod
    def getDNSQuestionFromBuffer(cls, message, offset):
        # Getting query name.
        ques_name_labels, offset = decode_labels(message, offset)
        ques_name = combine_labels(ques_name_labels)

        # Getting question type and class.
        ques_type, ques_class = DNSQuestion.DNS_QUERY_SECTION_FORMAT.unpack_from(message, offset)
        offset += DNSQuestion.DNS_QUERY_SECTION_FORMAT.size

        ques_name = ques_name
        ques_type = ques_type
        ques_class = ques_class

        return DNSQuestion(ques_name=ques_name, ques_type=ques_type, ques_class=ques_class), offset

    """
    Encode DNS Question information into bytes
    """
    def toBytes(self):
        ques_bytes = encode_labels(self.ques_name)
        ques_bytes += self.ques_type.to_bytes(2, byteorder='big')
        ques_bytes += self.ques_class.to_bytes(2, byteorder='big')

        return ques_bytes


    """
    Dump DNS Question to screen
    """
    def printQuestionInfo(self):
        result = {
            "Question Name": self.ques_name,
            "Question Type": self.ques_type,
            "Question Class": self.ques_class
        }
        print(result)
