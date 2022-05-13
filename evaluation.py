import json
import re
import statistics
from vectorial_model import VectorialModel

def recover_value(model: VectorialModel, query_number: int):
    rel_rec_docs = relevant_recovered_docs(model, query_number)
    rec_docs = recovered_docs(model, query_number)

    return len(rel_rec_docs) / len(rec_docs)

def recover_mean(model: VectorialModel):
    return statistics.mean([recover_value(model, i) for i in range(225)])

def precision_value(model: VectorialModel, query_number: int):
    rel_rec_docs = relevant_recovered_docs(model, query_number)
    rel_docs = relevant_docs(query_number)

    return len(rel_rec_docs) / len(rel_docs)

def precision_mean(model: VectorialModel):
    return statistics.mean([precision_value(model, i) for i in range(225)])

def relevant_recovered_docs(model: VectorialModel, query_number: int) -> list:
    rel_docs = relevant_docs(query_number)
    rec_docs = recovered_docs(model, query_number)

    return list(set(rel_docs) & set(rec_docs)) # Intersection

def relevant_docs(query_number: int) -> list:
    rel_dict = read_rel_dic()
    rel_docs = rel_dict[str(query_number)]["docs"]
    return rel_docs

def recovered_docs(model: VectorialModel, query_number: int) -> list:
    query: str = read_queries()[query_number]
    query = ' '.join(query.split('\n'))
    
    rec_docs = model.search(query)
    return rec_docs

def read_rel_dic() -> dict:
    try:
        with open('./Cran/rel_dic.json', 'r') as settings:
            return json.load(settings)
    except:
        return {}

def read_queries() -> list:
    try:
        with open('./Cran/cran.qry', 'r') as queries:
            queries_text = queries.read()
    except:
        return []

    return re.split('.I \d+\n.W', queries_text)[1:] # Regular expression to split queries file
