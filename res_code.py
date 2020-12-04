from enum import Enum

"""
This class specifies different types of return 
types for the DNS Packet
"""
class ResCode(Enum):
    NOERROR = 0
    FORMERR = 1
    SERVFAIL = 2
    NXDOMAIN = 3
    NOTIMP = 4
    REFUSED = 5

    @classmethod
    def getResCode(cls, num):
        return ResCode(num)
        