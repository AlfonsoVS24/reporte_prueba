import streamlit as st
from data import generar_datos
from tabla import mostrar_tabla

def mostrar_dashboard():

    # Título
    st.title("📊 Dashboard Operativo")

    st.markdown("---")

    st.subheader("Selecciona una cartera")

    # Botones
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("🏦\n\nBBVA1", use_container_width=True):
            st.session_state["cartera"] = "BBVA1"

    with col2:
        if st.button("💳\n\nBBVA2", use_container_width=True):
            st.session_state["cartera"] = "BBVA2"

    with col3:
        if st.button("🏛️\n\nBBVA3", use_container_width=True):
            st.session_state["cartera"] = "BBVA3"

    with col4:
        if st.button("💰\n\nBBVA4", use_container_width=True):
            st.session_state["cartera"] = "BBVA4"

    with col5:
        if st.button("🏢\n\nBBVA5", use_container_width=True):
            st.session_state["cartera"] = "BBVA5"

    st.markdown("---")

    if "cartera" not in st.session_state:
        st.info("Selecciona una cartera para comenzar.")
        return

    st.success(f"Cartera seleccionada: **{st.session_state['cartera']}**")

    # A partir de aquí ya sabemos que hay una cartera seleccionada
    datos = generar_datos(st.session_state["cartera"])

    retardos = (datos["Entrada"] > 555).sum()
    comida = (datos["Comida"] > 60).sum()
    baño = (datos["Baño"] > 30).sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👥 Asesores", len(datos))
    col2.metric("⏰ Retardos", retardos)
    col3.metric("🍔 Exceso comida", comida)
    col4.metric("🚻 Exceso baño", baño)

    st.markdown("---")

    st.subheader("🚨 Alertas")

    for _, fila in datos.iterrows():

        if fila["Entrada"] > 555:

            hora = f"{fila['Entrada']//60:02d}:{fila['Entrada']%60:02d}"

            st.error(f"{fila['Asesor']} llegó a las {hora}")

        if fila["Comida"] > 60:

            st.warning(f"{fila['Asesor']} excedió comida ({fila['Comida']} min)")

        if fila["Baño"] > 30:

            st.warning(f"{fila['Asesor']} excedió baño ({fila['Baño']} min)")
    mostrar_tabla(datos)
