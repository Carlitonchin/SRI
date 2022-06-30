import streamlit as st
import pandas as pd
from src.model import VectorialModel
from src.evaluation import recover_mean, precision_mean, f_mean
import json

def get_metricas(RR, RN, DR, NR, Rel):
# def get_metricas(model: VectorialModel):
    '''
    RR: Recuperados Relevantes
    RR: Recuperados No Relevantes
    RR: Documentos Recuperados
    RR: Documentos NO Recuperados
    Rel: Documentos Relevantes a la query
    
    Formato de métricas:
    Precisión: {value}
    Recobrado: {value}
    ... otras que quieras añadir
    '''
    metricas = ''
    
    '''
    Precisión.
    '''
    precision = 0
    try:
        precision = RR/DR
    except:
        pass
    metricas += f'Precisión: {precision}\n'
    #precision = precision_mean(model)
    #metricas += f'Precisión: {precision}\n'
    
    '''
    Recobrado.
    '''
    recobrado = 0
    try:
        recobrado = RR/Rel
    except:
        pass
    metricas += f'Recobrado: {recobrado}\n'
    
    '''
    Calculas la F1.
    '''
    # F1 = 0
    # metricas += f'F1: {F1}\n'
    
    '''
    Otras que quieras añadir
    '''
    
    #recobrado = recover_mean(model)
    #metricas += f'Recobrado: {recobrado}\n'
    '''
    F. (Se le puede cambiar el Beta)
    '''
    #f = f_mean(model, beta=1)
    #metricas += f'F: {f}\n'
    
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
    
    query_rel_num = st.selectbox("Número de la consulta", tuple([i for i in range(365 if dataset == "Cranfield" else 93)]), 
                help= 'Elija el número de la consulta. El valor es 0 si no está entre las consultas recomendadas')
    
    run = st.button("Computar")
    if run:
        placeholder = st.empty() # For displaying messages
        placeholder.success("Ejecutando...")
        dataset_path = './Cran/dataset.json' if dataset == 'Cranfield' else './vaswani/dataset.json'
        qrel_path = './Cran/rel_dic.json' if dataset == 'Cranfield' else './vaswani/rel_dic.json'
        
        if query != '':
            try:
                with open(dataset_path, 'r') as _data:
                    documents_dict = json.load(_data)
            except:
                st.write("No se encuentra el archivo 'dataset.json' en la carpeta")
                exit(0)
            model = VectorialModel(documents_dict)
            recovered = model.search(query.lower())
            
            try:
                with open(qrel_path, 'r') as _data:
                    rel_dict = json.load(_data)
            except:
                st.write("No se encuentra el archivo 'rel_dic.json' en la carpeta")
                exit(0)
            
            placeholder.empty()

            recovered_docs = []
            
            if query_rel_num != 0:
                rel_docs_for_query = rel_dict[str(query_rel_num)]['docs']

                RR = 0
                for doc in recovered:
                    recovered_docs.append(f'Doc #{doc.num}: {doc.title}')
                    if doc.num in rel_docs_for_query:
                        RR+=1
                RN = len(recovered_docs) - RR
                DR = len(recovered_docs)
                NR = len(documents_dict) - DR
                Rel = len(rel_docs_for_query)
                
                metrics = get_metricas(RR, RN, DR, NR, Rel)
                st.write(metrics)
            else:    
                for doc in recovered:
                    recovered_docs.append(f'Doc #{doc.num}: {doc.title}')
            
            data = {'Documentos recuperados por el modelo' : recovered_docs}
            st.write(pd.DataFrame(data = data))
        else:
            st.write("Necesitas escribir una consulta")
            
        placeholder.empty()
