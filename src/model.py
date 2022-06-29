from typing import List
from src.model_utils import Document, get_query, _calculateMaxs, _wordFrequencyQuery
import math
from src.text_processing import query_processing

class Model:
    def __init__(self, documents_dict):
        self.documents_dict = documents_dict
        self.max_per_document, self.count_words = _calculateMaxs(documents_dict)
        self.total_documents = len(documents_dict)
    
    def search(self, query) -> List:
        pass

class BooleanModel(Model):
    def __init__(self, documents_dict, retrieve_relevants=False):
        super().__init__(documents_dict)
        self.retrieve_relevants = retrieve_relevants

    def search(self, query) -> List:
        retrieved, relevants = self.boolean_retrieve(query)
        retrieved_docs = []
        for tittle in retrieved:
            retrieved_docs.append(Document(tittle, self.documents_dict[tittle]["num"]))
        relevants_docs = []
        relevants = sorted(relevants, key=lambda a: -relevants[a])
        for tittle in relevants:
            relevants_docs.append(Document(tittle, self.documents_dict[tittle]["num"]))
        
        if self.retrieve_relevants:
            return relevants_docs
        return retrieved_docs
    
    def boolean_retrieve(self, query):
        query_dic = get_query(query)
        retrieved_docs = []
        relevant_docs = {}

        for tittle in self.documents_dict:
            doc = self.documents_dict[tittle]
            doc_words = doc["words"]
            valid = True
            relevance = 0
            for word in query_dic:
                if (doc_words.__contains__(word) and query_dic[word] == 1) or (not doc_words.__contains__(word) and query_dic[word] == 0):
                    relevance += 1
                    # valid = True
                else:
                    valid = False
                    # break
            if valid:
                retrieved_docs.append(tittle)
            if relevance != 0:
                relevant_docs[tittle] = relevance

        return retrieved_docs, relevant_docs

class VectorialModel(Model):
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

    def search(self,query) -> List:
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