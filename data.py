import pandas as pd
import random

asesores = [
    "Juan",
    "María",
    "Pedro",
    "Luis",
    "Ana",
    "Carlos",
    "Fernanda",
    "José",
    "Andrea",
    "Miguel"
]

def generar_datos(cartera):

    datos = []

    for asesor in asesores:

        llegada = random.randint(530,565)

        salida = random.randint(1080,1110)

        comida = random.randint(45,80)

        baño = random.randint(10,40)

        datos.append({

            "Asesor":asesor,

            "Entrada":llegada,

            "Salida":salida,

            "Comida":comida,

            "Baño":baño

        })

    return pd.DataFrame(datos)