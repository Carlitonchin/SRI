import json
import re
import statistics
from src.model import Model

def recover_value(model: Model, query_number: int):
    rel_rec_docs = relevant_recovered_docs(model, query_number)
    rel_docs = relevant_docs(query_number)

    if len(rel_docs) == 0:
        return 1
    return len(rel_rec_docs) / len(rel_docs)

def recover_mean(model: Model):
    return statistics.mean([recover_value(model, i) for i in range(225)])

def precision_value(model: Model, query_number: int):
    rel_rec_docs = relevant_recovered_docs(model, query_number)
    rec_docs = recovered_docs(model, query_number)
    
    if len(rec_docs) == 0:
        return 1
    return len(rel_rec_docs) / len(rec_docs)

def precision_mean(model: Model):
    return statistics.mean([precision_value(model, i) for i in range(225)])

def f_value(model: Model, query_number: int, beta=1):
    p = precision_value(model, query_number)
    r = recover_value(model, query_number)
    
    if p == 0 or r == 0:
        return 0

    return (1 + beta**2) / ((1 / p) + (beta**2 / r))

def f_mean(model: Model, beta=1):
    return statistics.mean([f_value(model, i, beta) for i in range(225)])

def relevant_recovered_docs(model: Model, query_number: int) -> list:
    rel_docs = relevant_docs(query_number)
    rec_docs = recovered_docs(model, query_number)

    return list(set(rel_docs) & set(rec_docs)) # Intersection

def relevant_docs(query_number: int) -> list:
    rel_dict = read_rel_dic()
    rel_docs = rel_dict[str(query_number + 1)]['docs']
    return rel_docs

def recovered_docs(model: Model, query_number: int) -> list:
    query: str = read_queries()[query_number]
    query = ' '.join(query.split('\n'))
    
    rec_docs = model.search(query)
    return [str(rec_doc.num) for rec_doc in rec_docs]

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
