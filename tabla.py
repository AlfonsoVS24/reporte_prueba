import streamlit as st

def mostrar_tabla(datos):

    st.markdown("---")

    st.subheader("👥 Detalle de asesores")

    datos = datos.copy()

    datos["Estado"] = datos["Entrada"].apply(
        lambda x: "🔴 Retardo" if x > 555 else "🟢 Puntual"
    )

    datos["Entrada"] = datos["Entrada"].apply(
        lambda x: f"{x//60:02d}:{x%60:02d}"
    )

    datos["Salida"] = datos["Salida"].apply(
        lambda x: f"{x//60:02d}:{x%60:02d}"
    )

    st.data_editor(
        datos,
        use_container_width=True,
        disabled=True,
        hide_index=True
    )