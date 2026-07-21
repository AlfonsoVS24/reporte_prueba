import streamlit as st
import pandas as pd
from data import generar_datos   # Cambia "datos" por el nombre de tu archivo


# ===========================
# Convierte segundos a HH:MM
# ===========================

def segundos_a_hora(segundos):

    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)

    return f"{horas:02d}:{minutos:02d}"


# ===========================
# Obtiene el resumen
# ===========================

def obtener_resumen(df):

    # Elimina las filas basura
    df = df[df["Agente"] != ""].copy()

    resumen = []

    for asesor in sorted(df["Agente"].unique()):

        datos = df[df["Agente"] == asesor]

        # Hora de llegada
        login = datos[datos["Estatus"] == "Log in"]["Inicio"].min()

        # Hora de salida
        logout = datos[datos["Estatus"] == "Logout"]["Fin"].max()

        # Tiempo de comida
        comida = datos[
            (datos["Estatus"] == "Not ready") &
            (datos["Subestatus"] == "COMIDA")
        ]["Duracion"].sum()

        # Tiempo de baño
        wc = datos[
            (datos["Estatus"] == "Not ready") &
            (datos["Subestatus"] == "WC")
        ]["Duracion"].sum()

        resumen.append({

            "Asesor": asesor,

            "Llegada": login.strftime("%H:%M"),

            "Salida": logout.strftime("%H:%M"),

            "Comida": segundos_a_hora(comida),

            "WC": segundos_a_hora(wc),

            "Retardo": login.time() > pd.Timestamp("09:15").time(),

            "Salida Temprana": logout.time() < pd.Timestamp("18:00").time(),

            "Comida Excedida": comida > 3600,

            "WC Excedido": wc > 1800

        })

    return pd.DataFrame(resumen)


# ===========================
# Colorea la tabla
# ===========================

def colorear_tabla(df):

    estilos = pd.DataFrame(
        "",
        index=df.index,
        columns=df.columns
    )

    for i in df.index:

        if df.loc[i, "Retardo"]:
            estilos.loc[i, "Llegada"] = "background-color:#ff9999"

        if df.loc[i, "Salida Temprana"]:
            estilos.loc[i, "Salida"] = "background-color:#ff9999"

        if df.loc[i, "Comida Excedida"]:
            estilos.loc[i, "Comida"] = "background-color:#ff9999"

        if df.loc[i, "WC Excedido"]:
            estilos.loc[i, "WC"] = "background-color:#ff9999"

    return estilos


# ===========================
# Página principal
# ===========================

def mostrar_cartera(nombre_cartera):

    st.title(f"📁 {nombre_cartera}")

    df = generar_datos(nombre_cartera)

    resumen = obtener_resumen(df)

    mostrar = resumen[
        ["Asesor", "Llegada", "Salida", "Comida", "WC"]
    ]

    st.dataframe(
        mostrar.style.apply(
            lambda _: colorear_tabla(resumen),
            axis=None
        ),
        use_container_width=True,
        hide_index=True
    )