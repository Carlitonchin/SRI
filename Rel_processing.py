import json
from text_processing import dataset_processing

'''
el primer path es el del dataset osea el cran.all.1400
el segundo path es el del cranrel el documento que brinda las relevancias
based_md es el modelo q utiliza spacy que esta por defecto si no se recibe
override es para realizar todo el procesamiento de nuevo
'''
# TODO: revisar el path de los .json que talvés den mal si se ejecuta desde donde no es
def final_text_processing(path, path_, based_md= 'en_core_web_sm', override=False):
    dataset = dataset_processing(path, based_md, override)
    rel_dic = {}
    try:
        with open('./Cran/rel_dic.json', 'r') as settings:
                rel_dic = json.load(settings)
        if override:
            dataset, rel_dic = relevancy(path_, dataset)
    except:
        dataset, rel_dic = relevancy(path_, dataset)
    
    json_object = json.dumps(dataset, indent = 4)
    with open('./dataset.json', 'w') as settings:
        settings.write(json_object)
    json_object = json.dumps(rel_dic, indent = 4)
    with open('./Cran/rel_dic.json', 'w') as settings:
        settings.write(json_object)
    return dataset, rel_dic


def relevancy(path, dataset):
    rel_dic = {}
    doc = ''
    with open(path) as file2:
                doc =  file2.read()
    splitted_doc = doc.split('\n')

    for i, row in enumerate(splitted_doc):
        if row == '':
            continue
        splitted_row = row.split(' ')
        this_row_doc = 'there is no relevancy'
        for d in dataset.values():
            if d['num'] == int(splitted_row[1]):
                this_row_doc = d['tittle']
        if this_row_doc != 'there is no relevancy':
            try:
                if not splitted_row[0] in dataset[this_row_doc]['relevant_queries']:
                    dataset[this_row_doc]['relevant_queries'].append(splitted_row[0])
            except:
                dataset[this_row_doc]['relevant_queries'] = [splitted_row[0]]

        try:
            rel_dic[splitted_row[0]]['docs'].append(splitted_row[1])
        except:
            rel_dic[splitted_row[0]] = {'docs': [splitted_row[1]]}

        try:
            rel_dic[splitted_row[0]]['relevancy_scale'].append(splitted_row[2])
        except:
            rel_dic[splitted_row[0]]['relevancy_scale'] = [splitted_row[2]]
    return dataset, rel_dic
    
# final_text_processing('./Modelo_vectorial/Test Collections/Cran/cran.all.1400', './Modelo_vectorial/Test Collections/Cran/cranqrel')
# a = 0