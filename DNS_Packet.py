from DNS_Header import DNSHeader
from DNS_Question import DNSQuestion
from DNS_Record import DNSRecord
from record_type import RecordType

import random

class DNSPacket:

    def __init__(self, header, questions=[], answers=[], authority_entries=[], additional_entries=[]):
        self.header = header
        self.questions = questions
        self.answers = answers
        self.authority_entries = authority_entries
        self.additional_entries = additional_entries

    """
    Decode DNS Packet information from bytes
    """
    @classmethod
    def getDNSPacketFromBuffer(cls, buffer):
        offset = 0
        header = cls.decodeHeaderSection(buffer)
        offset += header.size
        questions, offset = cls.decodeQuestionSection(buffer, offset, header.questions)
        answers, offset = cls.decodeAnswerSection(buffer, offset, header.answers)
        authority_entries, offset = cls.decodeAuthoritySection(buffer, offset, header.authoritative_entries)
        additional_entries, offset = cls.decodeAdditionalSection(buffer, offset, header.resource_entries)
        
        return DNSPacket(header, questions, answers, authority_entries, additional_entries)


    """
    Decode Header Section of DNS Packet from bytes
    """
    @classmethod
    def decodeHeaderSection(cls, buffer):
        return DNSHeader.getDNSHeaderFromBuffer(buffer)

    """
    Decode Question Section of DNS Packet from bytes
    """
    @classmethod
    def decodeQuestionSection(cls, buffer, offset, numQuestions):

        questions = []
        # Running for number of questions.
        for _ in range(numQuestions):

            question, offset = DNSQuestion.getDNSQuestionFromBuffer(buffer, offset)
            questions.append(question)
        
        return questions, offset

    """
    Decode Answer Section of DNS Packet from bytes
    """
    @classmethod
    def decodeAnswerSection(cls, buffer, offset, numAnswers):

        answers = []
        # Running for number of questions.
        for _ in range(numAnswers):

            answer, offset = DNSRecord.getDNSRecordFromBuffer(buffer, offset)
            answers.append(answer)
        
        return answers, offset

    """
    Decode Authority Section of DNS Packet from bytes
    """
    @classmethod
    def decodeAuthoritySection(cls, buffer, offset, numAuthEntries):

        authority_entries = []
        # Running for number of questions.
        for _ in range(numAuthEntries):

            entry, offset = DNSRecord.getDNSRecordFromBuffer(buffer, offset)
            authority_entries.append(entry)
        
        return authority_entries, offset

    """
    Decode Additional Section of DNS Packet from bytes
    """
    @classmethod
    def decodeAdditionalSection(cls, buffer, offset, numAdditionalEntries):

        additional_entries = []
        # Running for number of questions.
        for _ in range(numAdditionalEntries):

            entry, offset = DNSRecord.getDNSRecordFromBuffer(buffer, offset)
            additional_entries.append(entry)
        
        return additional_entries, offset

    """
    Encode Question Section of DNS Packet to bytes
    """
    def encodeQuestionSection(self):
        ques_bytes = b""
        for question in self.questions:
            ques = question.toBytes()
            if ques is not None:
                ques_bytes += ques
        
        return ques_bytes

    """
    Encode Answer Section of DNS Packet to bytes
    """
    def encodeAnswerSection(self):
        ans_bytes = b""
        for answer in self.answers:
            ans = answer.toBytes()
            if ans is not None:
                ans_bytes += ans
        
        return ans_bytes

    """
    Encode Authority Section of DNS Packet to bytes
    """
    def encodeAuthoritySection(self):
        authority_bytes = b""
        for entry in self.authority_entries:
            authority = entry.toBytes()
            if authority is not None:
                authority_bytes += authority
        
        return authority_bytes

    """
    Encode Additional Section of DNS Packet to bytes
    """
    def encodeAdditionalSection(self):
        additional_bytes = b""
        for entry in self.additional_entries:
            additional = entry.toBytes()
            if additional is not None:
                additional_bytes += additional
        
        return additional_bytes

    """
    Encode DNS Packet to bytes
    """
    def encodeDNSPacket(self):
        buffer = self.header.toBytes()

        buffer += self.encodeQuestionSection()
        buffer += self.encodeAnswerSection()
        buffer += self.encodeAuthoritySection()
        buffer += self.encodeAdditionalSection()
        return buffer

    """
    Returns true if record type is known to the application,
    false otherwise
    """
    def filterUnknownRecordType(self, record):
        if(record.recordType == RecordType.UNKNOWN):
            return False
        return True

    """
    Filters out Unsupported Record Types from the DNS Packet
    """
    def filterUnsupportedRecords(self):
        self.answers = list(filter(self.filterUnknownRecordType, self.answers))
        self.authority_entries = list(filter(self.filterUnknownRecordType, self.authority_entries))
        self.additional_entries = list(filter(self.filterUnknownRecordType, self.additional_entries))

        # Update number of records in the header section
        self.header.answers = len(self.answers)
        self.header.authoritative_entries = len(self.authority_entries)
        self.header.resource_entries = len(self.additional_entries)


    """
    Returns a random IP address (from answer records) of the DNS Packet
    This is used to query a random authoritative server.
    """
    def getRandomIPv4AnswerRecord(self):
        ipv4AnswerRecords = list(filter(lambda record : record.recordType == RecordType.A, self.answers))

        if len(ipv4AnswerRecords) == 0:
            return None

        random_record = random.choice(ipv4AnswerRecords)
        return random_record.ip_addr

    """
    Returns a list of tuples of the form (domain, hostname) from the
    NS Records in the authority section.
    """
    def get_ns_tuples(self, ques_domain_name):
        ns_records = filter(lambda record : record.recordType == RecordType.NS, self.authority_entries)
        ns_tuples = map(lambda record : (record.domain, record.host), ns_records)

        return list(ns_tuples)

    """
    Returns a random IP address (from additional records) of the DNS Packet
    matching a random NS record from the authority section.
    """
    def getNSRecordIpAddress(self, ques_domain_name):
        ns_tuples = self.get_ns_tuples(ques_domain_name)
        
        if len(ns_tuples) == 0:
            return None

        for (_, host) in ns_tuples:
            ip_records = list(filter(lambda record : record.recordType == RecordType.A and record.domain == host, self.additional_entries))
            if len(ip_records) > 0:
                return ip_records[0].ip_addr
        
        return None
    
    """
    Returns a random (domain, hostname) tuple from NS records in the 
    authority section.
    """
    def getUnresolvedNS(self, ques_domain_name):
        ns_tuples = self.get_ns_tuples(ques_domain_name)

        if len(ns_tuples) == 0:
            return None
        return ns_tuples[0]
            