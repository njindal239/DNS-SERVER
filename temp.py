from DNS_Header import DNSHeader
from DNS_Question import DNSQuestion
from DNS_Record import DNSRecord

class DNSPacket:

    def __init__(self, header, questions, answers):
        self.header = header
        self.questions = questions
        self.answers = answers





        self.header = self.decodeHeaderSection(buffer)
        self.offset += self.header.size
        self.questions = []
        self.answers = []
        self.decodeQuestionSection(buffer, self.offset)
        self.decodeAnswerSection(buffer, self.offset)


    @classmethod
    def getDNSPacketFromBuffer(cls, buffer):
        offset = 0
        header = cls.decodeHeaderSection(buffer)


    @classmethod
    def decodeHeaderSection(cls, buffer):
        return DNSHeader.getDNSHeaderFromBuffer(buffer)

    @classmethod
    def decodeQuestionSection(cls, buffer, offset):

        # Running for number of questions.
        for _ in range(self.header.questions):

            question, offset = DNSQuestion.getDNSQuestionFromBuffer(buffer, offset)
            self.offset = offset

            self.questions.append(question)

    @classmethod
    def decodeAnswerSection(cls, buffer, offset):

        # Running for number of questions.
        for _ in range(self.header.answers):

            answer, offset = DNSRecord.getDNSRecordFromBuffer(buffer, offset)
            self.offset = offset

            self.answers.append(answer)

    def encodeQuestionSection(self):
        ques_bytes = b""
        for question in self.questions:
            ques_bytes += question.toBytes()
        
        return ques_bytes

    def encodeAnswerSection(self):
        ans_bytes = b""
        for answer in self.answers:
            ans_bytes += answer.toBytes()
        
        return ans_bytes

    def encodeDNSPacket(self):
        buffer = self.header.toBytes()

        buffer += self.encodeQuestionSection()
        buffer += self.encodeAnswerSection()
        print(''.join('{:02x} '.format(x) for x in buffer))
        return buffer