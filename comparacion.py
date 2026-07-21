import streamlit as st
import pandas as pd
import plotly.express as px

from data import generar_datos


def calcular_excesos(df):

    return {
        "Retardo": (df["Entrada"] - 555).clip(lower=0).sum(),
        "Comida": (df["Comida"] - 60).clip(lower=0).sum(),
        "Baño": (df["Baño"] - 30).clip(lower=0).sum(),
    }


def mostrar_comparacion():

    carteras = ["BBVA1", "BBVA2", "BBVA3", "BBVA4", "BBVA5"]

    resumen = []

    for cartera in carteras:

        datos = generar_datos(cartera)

        excesos = calcular_excesos(datos)

        resumen.append({
            "Cartera": cartera,
            "Retardo": excesos["Retardo"],
            "Comida": excesos["Comida"],
            "Baño": excesos["Baño"],
        })

    resumen = pd.DataFrame(resumen)

    resumen["Total"] = (
        resumen["Retardo"]
        + resumen["Comida"]
        + resumen["Baño"]
    )

    # ============================
    # KPIs
    # ============================

    c1, c2, c3, c4 = st.columns(4)

    peor_total = resumen.loc[resumen["Total"].idxmax()]
    peor_retardo = resumen.loc[resumen["Retardo"].idxmax()]
    peor_comida = resumen.loc[resumen["Comida"].idxmax()]
    peor_baño = resumen.loc[resumen["Baño"].idxmax()]

    c1.metric("🏆 Mayor tiempo perdido", peor_total["Cartera"])
    c2.metric("⏰ Más retardos", peor_retardo["Cartera"])
    c3.metric("🍔 Más comida", peor_comida["Cartera"])
    c4.metric("🚻 Más baño", peor_baño["Cartera"])

    st.markdown("---")

    # ============================
    # Gráfica
    # ============================

    grafica = resumen.melt(
        id_vars="Cartera",
        value_vars=["Retardo", "Comida", "Baño"],
        var_name="Tipo",
        value_name="Minutos"
    )

    fig = px.bar(
        grafica,
        x="Cartera",
        y="Minutos",
        color="Tipo",
        text="Minutos",
        color_discrete_map={
            "Retardo": "#d62728",
            "Comida": "#f1c40f",
            "Baño": "#ff7f0e",
        }
    )

    fig.update_layout(
        barmode="stack",
        height=550,
        xaxis_title="",
        yaxis_title="Minutos excedidos",
        legend_title=""
    )

    fig.update_traces(textposition="inside")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("Resumen por cartera")

    st.dataframe(
        resumen,
        use_container_width=True,
        hide_index=True
    )