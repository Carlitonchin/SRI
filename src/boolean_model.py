from src.text_processing import cleansing_query

def get_query(query):
    included = []
    not_included = []
    words = {}
    # query_ = query_processing(query)
    query_ = query.split(' ')
    query_ = cleansing_query(query_)
    not_bool = False
    for word in query_:
        if word.lower() == 'no':
            not_bool = True
            continue
        if not_bool:
            not_bool = False
            not_included.append(word)
            words[word] = 0
        else:
            included.append(word)
            words[word] = 1
    return words
class Document:
    def __init__(self, title, num):
        self.title = title
        self.num = num
    
    def __str__(self):
        return self.title

class BooleanModel:
    def __init__(self, documents_dic):
        self.documents_dict = documents_dic
        # self.max_per_document, self.count_words = _calculateMaxs(documents_dict)
        self.total_documents = len(documents_dic)

    def search(self, query):
        retrieved, relevants = self.boolean_retrieve(query)
        retrieved_docs = []
        for tittle in retrieved:
            retrieved_docs.append(Document(tittle, self.documents_dict[tittle]["num"]))
        relevants_docs = []
        relevants = sorted(relevants, key=lambda a: -relevants[a])
        for tittle in relevants:
            relevants_docs.append(Document(tittle, self.documents_dict[tittle]["num"]))
        return retrieved_docs, relevants_docs
    
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

# boolean_retrieve('./Cran/dataset.json', 'similarity')
# boolean_retrieve('./Cran/dataset.json', 'what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft .')