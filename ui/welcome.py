import streamlit as st


def welcome():
    st.title("Proyecto de Sistema de Recuperación de Información")
    st.header("Implementar dos modelos diferentes y realizar experimentos en dos escenarios (datasets) distintos")

    st.subheader("Desarrollado por:")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("- Richard García De la Osa C-512")
        st.markdown("- Carlos Alejandro Arrieta Montes de Oca C-512")
        st.markdown("- Luis Alejandro Lara Rojas C-512")


    st.markdown(
        "## Para comenzar seleccione que programa desea ejecutar en el menú lateral 👈"
    )
