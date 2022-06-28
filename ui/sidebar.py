import streamlit as st
# from modelo_booleano import bln
# from modelo_vectorial import vtl
from ui.welcome import welcome
import ui.modelo_booleano as mb
import ui.modelo_vectorial as mv

options = [
    "Decidiendo...",
    "Modelo Vectorial",
    "Modelo Booleano"
]

router = [
    welcome,
    mv.vtl,
    mb.bln
]


def callback():
    if "current" in st.session_state:
        del st.session_state[st.session_state.current]


def sidebar():
    with st.sidebar:
        st.header("Qué desea computar?")
        opt = st.radio("", options, on_change=callback)

        idx = options.index(opt)

        return router[idx]
