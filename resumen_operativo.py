import pandas as pd


def segundos_hora(segundos):

    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)

    return f"{horas:02}:{minutos:02}"


def crear_tabla_operativa(df):

    # quitar filas basura
    df = df.iloc[7:].copy()

    df["Inicio"] = pd.to_datetime(df["Inicio"])
    df["Fin"] = pd.to_datetime(df["Fin"])

    resumen = []

    for agente, datos in df.groupby("Agente"):

        entrada = datos["Inicio"].min()

        salida = datos["Fin"].max()

        conexion = (salida - entrada).total_seconds()

        comida = datos.loc[
            datos["Subestatus"] == "COMIDA",
            "Duracion"
        ].sum()

        wc = datos.loc[
            datos["Subestatus"] == "WC",
            "Duracion"
        ].sum()

        resumen.append({

            "Agente": agente,

            "Entrada": entrada,

            "Salida": salida,

            "Conexión": conexion,

            "Comida": comida,

            "Baño": wc

        })

    return pd.DataFrame(resumen)