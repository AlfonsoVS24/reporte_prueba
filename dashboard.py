import streamlit as st

from data import generar_datos
from tabla import mostrar_tabla
from comparacion import mostrar_comparacion


def mostrar_dashboard():

    # ==========================
    # Título
    # ==========================

    st.title("📊 Dashboard Operativo")

    st.markdown("---")

    st.subheader("Selecciona una cartera")

    # ==========================
    # Botones
    # ==========================

    col1, col2, col3, col4, col5, col6 = st.columns(6)

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

    with col6:
        if st.button("📊\n\nComparación", use_container_width=True):
            st.session_state["cartera"] = "Comparación"

    st.markdown("---")

    # ==========================
    # Validación
    # ==========================

    if "cartera" not in st.session_state:
        st.info("Selecciona una cartera para comenzar.")
        return

    # ==========================
    # Vista comparación
    # ==========================

    if st.session_state["cartera"] == "Comparación":

        st.success("📊 Comparación entre carteras")

        mostrar_comparacion()

        return

    # ==========================
    # Dashboard de cartera
    # ==========================

    st.success(
        f"Cartera seleccionada: **{st.session_state['cartera']}**"
    )

    datos = generar_datos(st.session_state["cartera"])

    retardos = (datos["Entrada"] > 555).sum()
    comida = (datos["Comida"] > 60).sum()
    baño = (datos["Baño"] > 30).sum()

    # ==========================
    # KPIs
    # ==========================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👥 Asesores", len(datos))
    col2.metric("⏰ Retardos", retardos)
    col3.metric("🍔 Exceso comida", comida)
    col4.metric("🚻 Exceso baño", baño)

    st.markdown("---")

    # ==========================
    # Tabla + Alertas
    # ==========================

    col_tabla, col_alertas = st.columns([4, 1])

    with col_tabla:

        mostrar_tabla(datos)

    with col_alertas:

        st.subheader("🚨 Alertas")

        contenedor = st.container(border=True)

        with contenedor:

            hay_alertas = False

            for _, fila in datos.iterrows():

                if fila["Entrada"] > 555:

                    hora = f"{fila['Entrada']//60:02d}:{fila['Entrada']%60:02d}"

                    st.markdown(
                        f"🔴 **{fila['Asesor']}**<br>"
                        f"<span style='font-size:12px'>Retardo ({hora})</span>",
                        unsafe_allow_html=True,
                    )

                    hay_alertas = True

                if fila["Comida"] > 60:

                    st.markdown(
                        f"🟡 **{fila['Asesor']}**<br>"
                        f"<span style='font-size:12px'>Comida ({fila['Comida']} min)</span>",
                        unsafe_allow_html=True,
                    )

                    hay_alertas = True

                if fila["Baño"] > 30:

                    st.markdown(
                        f"🟠 **{fila['Asesor']}**<br>"
                        f"<span style='font-size:12px'>Baño ({fila['Baño']} min)</span>",
                        unsafe_allow_html=True,
                    )

                    hay_alertas = True

            if not hay_alertas:
                st.success("✅ Sin alertas")