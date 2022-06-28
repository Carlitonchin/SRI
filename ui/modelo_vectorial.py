import streamlit as st
import pandas as pd
from src.vectorial_model import VectorialModel
import json

def get_metricas(docs):
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
    precision = 0
    metricas += f'Precisión: {precision}\n'
    
    
    '''
    Calculas la Recobrado.
    '''
    recobrado = 0
    metricas += f'Recobrado: {recobrado}\n'
    
    '''
    Otras que quieras añadir
    '''
    
    return metricas

def vtl():
    st.title("Modelo Vectorial")
    st.header("Introduzca los datos necesarios para su cómputo")

    query = st.text_input("Consulta", help=
        'Una expresión en el lenguaje booleano.'
        ' Debe tener el formato: "Palabra o no Palabra".'
        ' Ejemplo: "avión no perro no gato caballo carro".',
        value = "experimental investigation of the aerodynamics of a wing in a slipstream"
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
            model = VectorialModel(documents_dict)
            recovered = model.search(query.lower())
            recovered_docs = []
            for doc in recovered:
                recovered_docs.append(f'Doc #{doc.num}: {doc.title}')
            
            placeholder.empty()
            data = {'Documentos' : recovered_docs}
            st.write(pd.DataFrame(data = data))
            metrics = get_metricas(recovered)
            st.write(metrics)
        else:
            st.write("Necesitas escribir una consulta")
            
        placeholder.empty()
