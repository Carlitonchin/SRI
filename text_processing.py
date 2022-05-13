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

def read_docs(path, based_md, dataset):
    file = path.split('/')[-1]

    try:
        with open(path) as file2:
            text =  file2.read()
    except IOError:
        print(f"Couldn't read this document{file}")
    # Processing each document
    splitted_text = text.split('.I')[1:]
    for i, doc in enumerate(splitted_text):
        docDic = {}
        # Number of the Document
        docDic['num'] = i+1
        splitted_doc = doc.split('.A')
        # Tittle of the Document
        docDic['tittle'] = splitted_doc[0].split('.T\n')[1]
        part_doc = splitted_doc[1]
        splitted_doc = part_doc.split('.B')
        # Authors of the Document
        docDic['authors'] = splitted_doc[0][1:]
        part_doc = splitted_doc[1]
        splitted_doc = part_doc.split('.W')
        # B of the Document
        docDic['B'] = splitted_doc[0][1:]
        # Text Content of the Document
        docDic['content'] = splitted_doc[1][1:]
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


'''
Este método recive 3 parámetros:
path -> el path del documento a procesar.
based_md -> modelo de spacy a utilizar.
override -> si existe el .json del dataset, sobreescribirlo

retorna un diccionario con la siguiente estructura:
un diccionario de título del documento a otro diccionario,
este segundo diccionario tiene los campos de tittle(título del documento), 
num(número del documento), authors(autores), B(supongo que es la editorial),
content(texto del documento), relevancy(una lista con las querys en las que es relevante)
y words que es un diccionario de palabra contra frecuencia en ese documento.
'''
def dataset_processing(path, based_md, override=False):
    dataset = {}
    try:
        with open('./Cran/dataset.json', 'r') as settings:
                dataset = json.load(settings)
        if override:
            dataset = read_docs(path, based_md, dataset)
    except:
        dataset = read_docs(path, based_md, dataset)
    
    json_object = json.dumps(dataset, indent = 4)
    with open('./Cran/dataset.json', 'w') as settings:
        settings.write(json_object)
    return dataset

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