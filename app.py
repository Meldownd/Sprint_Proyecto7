import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# ----------------------------------------------------------------------#
# CARGA DEL DATASET
# ----------------------------------------------------------------------#
df = pd.read_csv("../csv/vehicles_us.csv")


def cleaning(data):
    """
    Limpieza básica del dataset de vehículos.

    Pasos:
    1. Rellenar valores faltantes (fillna) según el tipo de columna.
    2. Estandarizar formatos y tipos de datos.
    3. Aplicar correcciones específicas por columna.
    """

    # ----------------------------------------------------------------------#
    # 1️⃣ RELLENAR VALORES FALTANTES
    # ----------------------------------------------------------------------#
    # Sustituye 1 → 'Yes' y NaN → 'No' en columna 'is_4wd'
    data['is_4wd'] = data['is_4wd'].replace({1: 'Yes', np.nan: 'No'})

    # Completa odometer, cylinders y model_year con 0 si están vacíos
    data['odometer'] = data['odometer'].fillna(0)
    data['cylinders'] = data['cylinders'].fillna(0)
    data['model_year'] = data['model_year'].fillna(0)

    # Completa paint_color con un valor genérico
    data['paint_color'] = data['paint_color'].fillna('random')

    # Rellena 'cylinders' según el modo de cada modelo (si falta y existe)
    data['cylinders'] = data.groupby("model")['cylinders'].transform(
        lambda x: x.fillna(x.mode()[0] if not x.mode().empty else np.nan)
    )

    # ----------------------------------------------------------------------#
    # 2️⃣ CAMBIOS DE TIPO DE DATO
    # ----------------------------------------------------------------------#
    # Convierte fechas y números a su tipo correcto
    data['date_posted'] = pd.to_datetime(data['date_posted'])
    data['odometer'] = data['odometer'].astype(int)
    data['cylinders'] = data['cylinders'].astype(int)
    data['model_year'] = data['model_year'].astype(int)

    # ----------------------------------------------------------------------#
    # 3️⃣ RETORNAR DATA LIMPIA
    # ----------------------------------------------------------------------#
    return data


# ----------------------------------------------------------------------#
# LIMPIEZA DE DATOS
# ----------------------------------------------------------------------#
df_clean = cleaning(df)

st.title("📊 Análisis de Datos de Vehículos")
st.write("Dataset procesado y limpio listo para análisis visual.")


# ----------------------------------------------------------------------#
# 🔹 GRÁFICA 1: DISPERSIÓN (Kilometraje vs Precio)
# ----------------------------------------------------------------------#
def plot_scatter(data):
    """
    Muestra la relación entre kilometraje, precio y condición del vehículo.

    Parámetros:
    - data (DataFrame): Dataset limpio.

    Descripción:
    1. Eje X → 'odometer' (kilometraje recorrido)
    2. Eje Y → 'price' (precio del vehículo)
    3. Color → 'condition' (estado general)
    4. Tamaño → 'model_year' (año del modelo)
    5. Hover → 'model' y 'type' (información adicional)
    """
    fig = px.scatter(
        data,
        x="odometer",
        y="price",
        color="condition",
        size="model_year",
        hover_data=["model", "type"],
        title="Relación entre kilometraje, precio y condición del vehículo",
        labels={
            "odometer": "Kilometraje recorrido",
            "price": "Precio (USD)",
            "condition": "Condición del vehículo",
            "model_year": "Año del modelo"
        },
        opacity=0.6
    )
    return fig


if st.button("Mostrar gráfica de dispersión"):
    st.plotly_chart(plot_scatter(df_clean), use_container_width=True)


# ----------------------------------------------------------------------#
# 🔹 GRÁFICA 2: PRECIO PROMEDIO SEGÚN CONDICIÓN
# ----------------------------------------------------------------------#
def plot_condition_mean(data):
    """
    Muestra el precio promedio agrupado por condición del vehículo.

    Pasos:
    1. Agrupar por 'condition' y calcular el precio medio.
    2. Generar gráfico de barras con colores personalizados.
    """
    cond_mean = data.groupby("condition", as_index=False)["price"].mean()
    fig = px.bar(
        cond_mean,
        x="condition",
        y="price",
        title="Precio promedio según condición del vehículo",
        labels={"condition": "Condición", "price": "Precio promedio (USD)"},
    )
    fig.update_traces(marker_color="skyblue")
    return fig


if st.button("Mostrar gráfica de precio promedio por condición"):
    st.plotly_chart(plot_condition_mean(df_clean), use_container_width=True)


# ----------------------------------------------------------------------#
# 🔹 GRÁFICA 3: PRECIO PROMEDIO POR TIPO DE VEHÍCULO
# ----------------------------------------------------------------------#
def plot_type_mean(data):
    """
    Muestra el precio promedio agrupado por tipo de vehículo.

    Pasos:
    1. Agrupar por 'type' y calcular el precio medio.
    2. Mostrar un gráfico de barras horizontal para mejor lectura.
    """
    type_mean = data.groupby("type", as_index=False)["price"].mean()
    fig = px.bar(
        type_mean,
        x="price",
        y="type",
        orientation="h",
        title="Precio promedio por tipo de vehículo",
        labels={"type": "Tipo de vehículo", "price": "Precio promedio (USD)"},
    )
    fig.update_traces(marker_color="coral")
    return fig


if st.button("Mostrar gráfica de precio promedio por tipo"):
    st.plotly_chart(plot_type_mean(df_clean), use_container_width=True)
