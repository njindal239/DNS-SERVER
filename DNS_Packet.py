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

        # Filter out unssupported records from the DNS packet
        # self.filterUnsupportedRecords()


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


    @classmethod
    def decodeHeaderSection(cls, buffer):
        return DNSHeader.getDNSHeaderFromBuffer(buffer)

    @classmethod
    def decodeQuestionSection(cls, buffer, offset, numQuestions):

        questions = []
        # Running for number of questions.
        for _ in range(numQuestions):

            question, offset = DNSQuestion.getDNSQuestionFromBuffer(buffer, offset)
            questions.append(question)
        
        return questions, offset

    @classmethod
    def decodeAnswerSection(cls, buffer, offset, numAnswers):

        answers = []
        # Running for number of questions.
        for _ in range(numAnswers):

            answer, offset = DNSRecord.getDNSRecordFromBuffer(buffer, offset)
            answers.append(answer)
        
        return answers, offset

    @classmethod
    def decodeAuthoritySection(cls, buffer, offset, numAuthEntries):

        authority_entries = []
        # Running for number of questions.
        for _ in range(numAuthEntries):

            entry, offset = DNSRecord.getDNSRecordFromBuffer(buffer, offset)
            authority_entries.append(entry)
        
        return authority_entries, offset

    @classmethod
    def decodeAdditionalSection(cls, buffer, offset, numAdditionalEntries):

        additional_entries = []
        # Running for number of questions.
        for _ in range(numAdditionalEntries):

            entry, offset = DNSRecord.getDNSRecordFromBuffer(buffer, offset)
            additional_entries.append(entry)
        
        return additional_entries, offset

    def encodeQuestionSection(self):
        ques_bytes = b""
        for question in self.questions:
            ques = question.toBytes()
            if ques is not None:
                ques_bytes += ques
        
        return ques_bytes

    def encodeAnswerSection(self):
        ans_bytes = b""
        for answer in self.answers:
            ans = answer.toBytes()
            if ans is not None:
                ans_bytes += ans
        
        return ans_bytes

    def encodeAuthoritySection(self):
        authority_bytes = b""
        for entry in self.authority_entries:
            authority = entry.toBytes()
            if authority is not None:
                authority_bytes += authority
        
        return authority_bytes

    def encodeAdditionalSection(self):
        additional_bytes = b""
        for entry in self.additional_entries:
            additional = entry.toBytes()
            if additional is not None:
                additional_bytes += additional
        
        return additional_bytes

    def encodeDNSPacket(self):
        buffer = self.header.toBytes()

        buffer += self.encodeQuestionSection()
        buffer += self.encodeAnswerSection()
        buffer += self.encodeAuthoritySection()
        buffer += self.encodeAdditionalSection()
        return buffer

    def filterUnknownRecordType(self, record):
        if(record.recordType == RecordType.UNKNOWN):
            return False
        return True

    def filterUnsupportedRecords(self):
        self.answers = list(filter(self.filterUnknownRecordType, self.answers))
        self.authority_entries = list(filter(self.filterUnknownRecordType, self.authority_entries))
        self.additional_entries = list(filter(self.filterUnknownRecordType, self.additional_entries))

        # Update number of records in the header section
        self.header.answers = len(self.answers)
        self.header.authoritative_entries = len(self.authority_entries)
        self.header.resource_entries = len(self.additional_entries)


    def getRandomIPv4AnswerRecord(self):
        ipv4AnswerRecords = list(filter(lambda record : record.recordType == RecordType.A, self.answers))

        if len(ipv4AnswerRecords) == 0:
            return None

        random_record = random.choice(ipv4AnswerRecords)
        return random_record.ip_addr

    def get_ns_tuples(self, ques_domain_name):
        ns_records = filter(lambda record : record.recordType == RecordType.NS, self.authority_entries)
        ns_tuples = map(lambda record : (record.domain, record.host), ns_records)

        # Now, we discard any servers that are not authoritative to our query
        ## We will see this later
        return list(ns_tuples)

    
    def getNSRecordIpAddress(self, ques_domain_name):
        ns_tuples = self.get_ns_tuples(ques_domain_name)
        
        if len(ns_tuples) == 0:
            return None

        for (_, host) in ns_tuples:
            ip_records = list(filter(lambda record : record.recordType == RecordType.A and record.domain == host, self.additional_entries))
            if len(ip_records) > 0:
                return ip_records[0].ip_addr
        
        return None
    
    def getUnresolvedNS(self, ques_domain_name):
        ns_tuples = self.get_ns_tuples(ques_domain_name)

        if len(ns_tuples) == 0:
            return None
        return ns_tuples[0]
            