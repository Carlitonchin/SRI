import ir_datasets
# dataset = ir_datasets.load('vaswani')
# Documents
# for doc in dataset.docs_iter():
#     print(doc)
# for i, doc in enumerate(dataset.docs_iter()):
#     print(doc)
    
#spaCy Code Initialization:
import spacy
import os
import json

Example_Sentence = """Patients who in late middle age have smoked 20 cigarettes a day since 
their teens constitute an at-risk group. One thing they’re clearly at risk for is the acute 
sense of guilt that a clinician can incite, which immediately makes a consultation tense."""


def processing_text(text : str, nlp_based : str):
    nlp = spacy.load(nlp_based)
    doc = nlp(text)
    token_listSC = []
    for token in doc:
        token_listSC.append(token.text)
        
    # Stemming
    lemma_list = []
    for token in doc:
        lemma_list.append(token.lemma_)
        
    # Filter the stopwords
    filtered_sentence = [] 
    for word in lemma_list:
        lexeme = nlp.vocab[word]
        if lexeme.is_stop == False:
            filtered_sentence.append(word)
            
    #Remove punctuation
    punctuations="?:!.,;"+'-+/\\*'
    for word in filtered_sentence:
        if word in punctuations:
            filtered_sentence.remove(word)
    
    others="\n"
    for word in filtered_sentence:
        if word in others:
            filtered_sentence.remove(word)
            
    return filtered_sentence

def read_docs(based_md, dataset):
    dataset_ = ir_datasets.load('vaswani')
    # Processing each document
    for i, doc in enumerate(dataset_.docs_iter()):
        print(doc)
        docDic = {}
        # Number of the Document
        docDic['num'] = i+1
        # Tittle of the Document
        docDic['tittle'] = str(doc.doc_id)
        # Authors of the Document
        docDic['authors'] = ''
        # B of the Document
        docDic['B'] = ''
        # Text Content of the Document
        docDic['content'] = doc.text
        # Dictionary of words to frequency in the Document
        docDic['words'] = {}
        # Split the text to process 10000 each time
        texts = []
        text = docDic['content']
        while len(text) > 10000:
            texts.append(text[: 10000])
            text =  text[10000:]
        texts.append(text)
        # Processing with spacy
        processed_text = []
        for text in texts:
            processed_text += processing_text(text, based_md)
        
        processed_text += processing_text(docDic['authors'], based_md)
        # Build the words dictionary
        for word in processed_text:
            try:
                docDic['words'][word] += 1
            except KeyError:
                docDic['words'][word] = 1
        # Save in dataset the document dictionary attached to his tittle
        dataset[docDic['tittle']] = docDic
    # json_object = json.dumps(dataset, indent = 4)
    # with open('./Modelo_vectorial/Test Collections/Cran/dataset.json', 'w') as settings:
    #     settings.write(json_object)
    return dataset


def dataset_processing(dataset_path, based_md, override=False):
    dataset = {}
    try:
        # with open('./Modelo_vectorial/Test Collections/Cran/dataset.json', 'r') as settings:
        with open(dataset_path, 'r') as settings:
                dataset = json.load(settings)
        if override:
            dataset = read_docs(based_md, dataset)
    except:
        dataset = read_docs(based_md, dataset)
    
    dataset = cleansing_dataset(dataset)
    json_object = json.dumps(dataset, indent = 4)
    # with open('./Modelo_vectorial/Test Collections/Cran/dataset.json', 'w') as settings:
    with open(dataset_path, 'w') as settings:
        settings.write(json_object)
    return dataset

def cleansing_dataset(dataset):
    for key in dataset:
        doc = dataset[key]
        words = doc['words']
        new_words = {}
        for s in words:
            if ' ' in s or '\n' in s or '/' in s:
                s_splitted = s.split(' ')
                new_s= ''
                for i in s_splitted:
                    new_s += i
                
                s_splitted = new_s.split('\n')
                new_s = ''
                for i in s_splitted:
                    new_s += i
                    
                s_splitted = new_s.split('/')
                new_s = ''
                for i in s_splitted:
                    new_s += i
                if new_s != '':
                    new_words[new_s] = words[s]
            elif ('.' in s or ',' in s or '('  in s or ')' in s) and len(s) == 1:
                pass
            # elif '/' in s:
            #     new_s = ''
            #     for c in s:
            #         if c != '/':
            #             new_s += c
            #     new_words[new_s] = words[s]
            else:
                new_words[s] = words[s]
        dataset[key]['words'] = new_words
    return dataset

def clean_dataset(path):
    with open(path, 'r') as settings:
        dataset = json.load(settings)
    for key in dataset:
        doc = dataset[key]
        words = doc['words']
        new_words = {}
        for s in words:
            if ' ' in s or '\n' in s or '/' in s:
                s_splitted = s.split(' ')
                new_s= ''
                for i in s_splitted:
                    new_s += i
                
                s_splitted = new_s.split('\n')
                new_s = ''
                for i in s_splitted:
                    new_s += i
                    
                s_splitted = new_s.split('/')
                new_s = ''
                for i in s_splitted:
                    new_s += i
                if new_s != '':
                    new_words[new_s] = words[s]
            elif s == '.' or s == ',' or s == '(' or s == ')':
                pass
            # elif '/' in s:
            #     new_s = ''
            #     for c in s:
            #         if c != '/':
            #             new_s += c
            #     new_words[new_s] = words[s]
            else:
                new_words[s] = words[s]
        dataset[key]['words'] = new_words
    json_object = json.dumps(dataset, indent = 4)
    with open(path, 'w') as settings:
        settings.write(json_object)

def query_processing(query, based_md):
    texts = []
    text = query
    while len(text) > 10000:
        texts.append(text[: 10000])
        text =  text[10000:]
    texts.append(text)
    # Processing with spacy
    processed_text = []
    for text in texts:
        processed_text += processing_text(text, based_md)
    return processed_text

# read_docs('./Modelo_vectorial/dataset1/', 'en_core_web_sm')
# read_docs('./Modelo_vectorial/Test Collections/Cran/cran.all.1400', 'en_core_web_sm', {})
# read_docs('./Test Collections/Cran/cran.all.1400', 'en_core_web_sm', {})
# dataset_processing('./vaswani.json', 'en_core_web_sm')
# dataset_processing('./Test Collections/Cran/cran.all.1400','./Test Collections/Cran/dataset.json', 'en_core_web_sm', True)
# clean_dataset('./Test Collections/Cran/dataset.json')