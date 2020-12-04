from enum import Enum

"""
This class specifies different type of records supported
by this DNS Server
"""
class RecordType(Enum):
    UNKNOWN = 0
    A = 1
    NS = 2
    CNAME = 5
    MX = 15
    AAAA = 28

    @classmethod
    def getRecordType(cls, num):
        return {
            1: RecordType.A,
            2: RecordType.NS,
            5: RecordType.CNAME,
            15: RecordType.MX,
            28: RecordType.AAAA
        }.get(num, RecordType.UNKNOWN)
