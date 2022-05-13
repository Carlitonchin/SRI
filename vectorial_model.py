def _calculateMaxs(documents_dict):
    max_per_document = {}
    count_words = {}

    for title in documents_dict:
        localMax = 0

        for w in documents_dict[title]["words"]:
            localMax = max(localMax, documets_dict[title]["words"][w])
            try:
                count_words[w] += 1
            except KeyError:
                count_words[w] = 1

        max_per_document[title] = localMax

    return max_per_document, N




class VectorialModel:
    def __init__(self, documents_dict):
        self.documents_dict = documents_dict
        self.max_per_document, self.count_words = _calculateMaxs(documents_dict)
        self.total_documents = len(document_dict)

    def tf(self, document, word):
        try:
            f = self.documents_dict[document]["words"][word]
            return f/self.max_per_document[document]
        except KeyError:
            return 0

    def idf(word):
        math.log(self.total_documents/(self.count_words[word]))


