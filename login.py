import streamlit as st
from funcion_login import login
from dashboard import mostrar_dashboard

st.set_page_config(

    page_title="Dashboard Operativo",

    page_icon="📊",

    layout="wide"

)

if "login" not in st.session_state:
    st.session_state["login"] = False

if not st.session_state["login"]:

    login()

else:

    st.sidebar.success(
        f"Bienvenido {st.session_state['usuario']}"
    )

    mostrar_dashboard()