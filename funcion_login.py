import streamlit as st

# Usuarios simulados
USUARIOS = {
    "admin": "1234",
    "supervisor": "cobranza2026",
    "alfonso": "python2026"
}

def login():

    st.title("🔐 Sistema de Control Operativo")

    st.markdown("---")

    usuario = st.text_input("Usuario")

    contraseña = st.text_input(
        "Contraseña",
        type="password"
    )

    if st.button("Ingresar", use_container_width=True):

        if usuario in USUARIOS and USUARIOS[usuario] == contraseña:

            st.session_state["login"] = True
            st.session_state["usuario"] = usuario

            st.rerun()

        else:

            st.error("Usuario o contraseña incorrectos")