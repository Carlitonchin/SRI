import streamlit as st
import pandas as pd
from src.model import BooleanModel
from src.evaluation import recover_mean, precision_mean, f_mean
import json

def get_metricas(RR, RN, DR, NR, Rel):
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
    #metricas += f'Precisión de recuperados estricto: {precision_mean(model_recovered)}\n'
    #metricas += f'Precisión de recuperados por partes: {precision_mean(model_relevant)}\n'
    
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
    # metricas += f'Recobrado de recuperados estricto: {recover_mean(model_recovered)}\n'
    # metricas += f'Recobrado de recuperados por partes: {recover_mean(model_relevant)}\n'

    '''
    F. (Se le puede cambiar el Beta)
    '''
    #metricas += f'F de recuperados estricto: {f_mean(model_recovered, beta=1)}\n'
    #metricas += f'F de recuperados por partes: {f_mean(model_relevant, beta=1)}\n'
    
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
    
    query_rel_num = st.selectbox("Dataset", tuple([i for i in range(365 if dataset == "Cranfield" else 93)]), 
                help= 'Elija el número de la consulta. El valor es 0 si no está entre las consultas recomendadas')
    
    run = st.button("Computar")
    if run:
        placeholder = st.empty() # For displaying messages
        placeholder.success("Ejecutando...")
        dataset_path = './Cran/dataset.json' if dataset == 'Cranfield' else './vaswani/dataset.json'
        qrel_path = './Cran/rel_dic.json' if dataset == 'Cranfield' else './vaswani/rel_dic.json'

        if query != '':
            try:
                with open(dataset_path, 'r') as data:
                    documents_dict = json.load(data)
            except:
                st.write("No se encuentra el archivo 'dataset.json' en la carpeta")
                exit(0)
            # model = BooleanModel(documents_dict)
            # recovered, relevants = model.search(query)
            
            

            model_recovered = BooleanModel(documents_dict)
            model_relevant = BooleanModel(documents_dict, True)

            recovered = model_recovered.search(query)
            relevants = model_relevant.search(query)

            try:
                with open(qrel_path, 'r') as _data:
                    rel_dict = json.load(_data)
            except:
                st.write("No se encuentra el archivo 'rel_dic.json' en la carpeta")
                exit(0)
            
            placeholder.empty()
            recovered_docs = []
            relevant_docs = []
            
            if query_rel_num != 0:
                rel_docs_for_query = rel_dict[str(query_rel_num)]['docs']
                
                RR1 = 0
                RR2 = 0
                for doc in recovered:
                    recovered_docs.append(f'Doc #{doc.num}: {doc.title}')
                    if doc.num in rel_docs_for_query:
                        RR1 += 1
                for doc in relevants:
                    relevant_docs.append(f'Doc #{doc.num}: {doc.title}')
                    if doc.num in rel_docs_for_query:
                        RR2 += 1
                    
                RN1 = len(recovered_docs) - RR1
                RN2 = len(recovered_docs) - RR2
                DR1 = len(recovered_docs)
                DR2 = len(recovered_docs)
                NR1 = len(documents_dict) - DR1
                NR2 = len(documents_dict) - DR2
                Rel1 = len(rel_docs_for_query)
                Rel2 = len(rel_docs_for_query)
                
                metrics1 = get_metricas(RR1, RN1, DR1, NR1, Rel1)
                metrics2 = get_metricas(RR2, RN2, DR2, NR2, Rel2)
                metrics = {'Métricas para el modelo estricto' : [metrics1], 'Métricas para el modelo relajado' : [metrics2]}
                st.write(pd.DataFrame(data =metrics))
            else:    
                for doc in recovered:
                    recovered_docs.append(f'Doc #{doc.num}: {doc.title}')
                for doc in relevants:
                    relevant_docs.append(f'Doc #{doc.num}: {doc.title}')
            
            data = {'Documentos recuperados estricto' : recovered_docs}
            st.write(pd.DataFrame(data = data))
            data = {'Documentos recuperados por partes' : relevant_docs}
            st.write(pd.DataFrame(data = data))
        else:
            st.write("Necesitas escribir una consulta")
            
        placeholder.empty()
