import streamlit as st
import pandas as pd
from src.model import BooleanModel
from src.evaluation import recover_mean, precision_mean
import json

def get_metricas(model_recovered: BooleanModel, model_relevant: BooleanModel):
    '''
    docs es una lista de Documents, la clase
    
    Formato de métricas:
    Precisión: {value}
    Recobrado: {value}
    ... otras que quieras añadir
    '''
    metricas = ''
    
    # Your code here
    '''
    Calculas la Precisión.
    '''
    metricas += f'Precisión de recuperados estricto: {precision_mean(model_recovered)}\n'
    metricas += f'Precisión de recuperados por partes: {precision_mean(model_relevant)}\n'
    
    
    '''
    Calculas la Recobrado.
    '''
    metricas += f'Recobrado de recuperados estricto: {recover_mean(model_recovered)}\n'
    metricas += f'Recobrado de recuperados por partes: {recover_mean(model_relevant)}\n'
    
    '''
    Otras que quieras añadir
    '''
    
    return metricas
def bln():
    st.title("Modelo Booleano")
    st.header("Introduzca los datos necesarios para su cómputo")

    query = st.text_input("Consulta", help=
        'Una expresión en el lenguaje natural.',
        value = "experimental investigation aerodynamics wing slipstream"
    )
    dataset = st.selectbox("Dataset", ('Cranfield', 'Vaswani'), 
                help= 'Elija un dataset para evaluar la query.')
    
    run = st.button("Computar")
    if run:
        placeholder = st.empty() # For displaying messages
        placeholder.success("Ejecutando...")
        dataset_path = './Cran/dataset.json' if dataset == 'Cranfield' else './vaswani/dataset.json'
        if query != '':
            try:
                with open(dataset_path, 'r') as data:
                    documents_dict = json.load(data)
            except:
                st.write("No se encuentra el archivo 'dataset.json' en la carpeta")
                exit(0)

            model_recovered = BooleanModel(documents_dict)
            model_relevant = BooleanModel(documents_dict, True)

            recovered = model_recovered.search(query)
            relevants = model_relevant.search(query)

            recovered_docs = []
            for doc in recovered:
                recovered_docs.append(f'Doc #{doc.num}: {doc.title}')
            relevant_docs = []
            for doc in relevants:
                relevant_docs.append(f'Doc #{doc.num}: {doc.title}')
            placeholder.empty()
            data = {'Documentos recuperados estricto' : recovered_docs}
            st.write(pd.DataFrame(data = data))
            data = {'Documentos recuperados por partes' : relevant_docs}
            st.write(pd.DataFrame(data = data))
            metrics = get_metricas(model_recovered, model_relevant)
            st.write(metrics)
        else:
            st.write("Necesitas escribir una consulta")
            
        placeholder.empty()
