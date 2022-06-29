from text_processing import cleansing_query

class Document:
    def __init__(self, title, num):
        self.title = title
        self.num = num
    
    def __str__(self):
        return self.title

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