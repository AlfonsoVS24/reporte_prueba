import streamlit as st
import plotly.express as px


def mostrar_tabla(datos):

    st.markdown("---")

    st.subheader("👥 Detalle de asesores")

    datos = datos.copy()

    # ======================
    # Estado
    # ======================

    datos["Estado"] = datos["Entrada"].apply(
        lambda x: "🔴 Retardo" if x > 555 else "🟢 Puntual"
    )

    # ======================
    # Minutos excedidos
    # ======================

    datos["Exceso Retardo"] = datos["Entrada"].apply(
        lambda x: max(0, x - 555)
    )

    datos["Exceso Comida"] = datos["Comida"].apply(
        lambda x: max(0, x - 60)
    )

    datos["Exceso Baño"] = datos["Baño"].apply(
        lambda x: max(0, x - 30)
    )

    datos["Total Excedido"] = (
        datos["Exceso Retardo"]
        + datos["Exceso Comida"]
        + datos["Exceso Baño"]
    )

    # ======================
    # Gráfica
    # ======================

    st.subheader("📊 Tiempo excedido por asesor")

    grafica = datos[
        [
            "Asesor",
            "Exceso Retardo",
            "Exceso Comida",
            "Exceso Baño",
        ]
    ].melt(
        id_vars="Asesor",
        var_name="Tipo",
        value_name="Minutos"
    )

    # Eliminar filas sin exceso
    grafica = grafica[grafica["Minutos"] > 0]

    # Cambiar nombres
    grafica["Tipo"] = grafica["Tipo"].replace({
        "Exceso Retardo": "⏰ Retardo",
        "Exceso Comida": "🍔 Comida",
        "Exceso Baño": "🚻 Baño",
    })

    # Ordenar por mayor tiempo excedido
    orden = (
        datos.sort_values("Total Excedido", ascending=False)["Asesor"]
        .tolist()
    )

    fig = px.bar(
        grafica,
        x="Asesor",
        y="Minutos",
        color="Tipo",
        text="Minutos",
        category_orders={"Asesor": orden},
        color_discrete_map={
            "⏰ Retardo": "#d62728",
            "🍔 Comida": "#f1c40f",
            "🚻 Baño": "#ff7f0e",
        },
    )

    fig.update_layout(
        barmode="stack",
        height=420,
        xaxis_title="",
        yaxis_title="Minutos excedidos",
        legend_title="",
    )

    fig.update_traces(textposition="inside")

    st.plotly_chart(fig, use_container_width=True)

    # ======================
    # Formato de horas
    # ======================

    datos["Entrada"] = datos["Entrada"].apply(
        lambda x: f"{x//60:02d}:{x%60:02d}"
    )

    datos["Salida"] = datos["Salida"].apply(
        lambda x: f"{x//60:02d}:{x%60:02d}"
    )

    # ======================
    # Tabla
    # ======================

    columnas = [
        "Asesor",
        "Estado",
        "Entrada",
        "Salida",
        "Comida",
        "Baño",
        "Exceso Retardo",
        "Exceso Comida",
        "Exceso Baño",
        "Total Excedido",
    ]

    st.data_editor(
        datos[columnas],
        use_container_width=True,
        disabled=True,
        hide_index=True,
    )