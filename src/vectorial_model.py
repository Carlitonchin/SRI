from src.text_processing import query_processing
import math

def _calculateMaxs(documents_dict):
    max_per_document = {}
    count_words = {}

    for title in documents_dict:
        localMax = 0

        for w in documents_dict[title]["words"]:
            localMax = max(localMax, documents_dict[title]["words"][w])
            try:
                count_words[w] += 1
            except KeyError:
                count_words[w] = 1

        max_per_document[title] = localMax

    return max_per_document, count_words


def _wordFrequencyQuery(query):
    maxW = 0
    frequency = {}

    for w in query:
        try:
            frequency[w] += 1
        except KeyError:
            frequency[w] = 1
        maxW = max(frequency[w], maxW)

    return frequency, maxW

class Document:
    def __init__(self, title, num):
        self.title = title
        self.num = num
    
    def __str__(self):
        return self.title

class VectorialModel:
    def __init__(self, documents_dict):
        self.documents_dict = documents_dict
        self.max_per_document, self.count_words = _calculateMaxs(documents_dict)
        self.total_documents = len(documents_dict)

    def tf(self, document, word):
        try:
            f = self.documents_dict[document]["words"][word]
            return f/self.max_per_document[document]
        except KeyError:
            return 0

    def idf(self, word):
        try:
            return math.log(self.total_documents/(self.count_words[word]))
        except KeyError:
            return 0

    def calculateWQuery(self, query, frequency, maxW):
        a = 0.5
        w = {}
        for word in query:
            wq = self.idf(word) * (a + (1-a) * (frequency[word]/maxW))
            w[word] = wq

        return w 

    def search(self,query):
        query = query_processing(query, 'en_core_web_sm')
        response = []
        for d in self.documents_dict:
            if self.sim(d, query) >= 0.6:
                response.append(Document(d, self.documents_dict[d]["num"]))
        return response

    def sim(self, document, query):
        frequency, maxW = _wordFrequencyQuery(query)
        wq = self.calculateWQuery(query, frequency, maxW)
        wjXwq = 0

        wqTotal2 = 0
        wjTotal2 = 0

        for w in query:
            wj = self.tf(document, w) * self.idf(w)
            try:
                wjXwq += wj * wq[w]
                wqTotal2 += wq[w]*wq[w]
            except KeyError:
                pass

        for w in self.documents_dict[document]["words"]:
            wj = self.tf(document, w) * self.idf(w)
            wjTotal2 = wj*wj

        den = math.sqrt(wjTotal2) * math.sqrt(wqTotal2)

        if den != 0:
            return wjXwq/den
        
        return 0

