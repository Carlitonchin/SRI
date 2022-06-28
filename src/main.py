from src.vectorial_model import VectorialModel
from src.evaluation import recover_mean, precision_mean
import json

def print_recovereds(docs):
    if docs:
        print(f"\nDocumentos recuperados ({len(docs)}):\n")
        for doc in docs:
            print(f'Doc #{doc.num}: {doc.title}')

    else:
        print("No se recuperaron documentos para esa consulta\n")


try:
    with open('./Cran/dataset.json', 'r') as data:
        documents_dict = json.load(data)
except:
    print("No se encuentra el archivo 'dataset.json' en la carpeta cran")
    exit(0)

model = VectorialModel(documents_dict)

#print("Recover mean:", recover_mean(model))
#print("Precision mean:", precision_mean(model))

while True:
    query = input("Escribe una query y presiona enter:\n")
    recovereds = model.search(query)
    print_recovereds(recovereds)