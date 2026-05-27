#CARGAR LIBRERIAS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# CARGAR DATASET

df = pd.read_csv(
    "D:\\Documents\\ESP. ANALITICA DE DATOS\\TESIS ESPECIALIZACION ANALITICA DE DATOS\\DESPLIEGUE\\DATA\\DATASET_COMPLETO_3.0.csv",
    encoding='latin-1',
    sep=';'
)


# LIMPIEZA DE ESPACIOS Y FORMATO DE COLUMNAS

df.columns = (
    df.columns
    .str.strip()
    .str.replace('\ufeff', '')
    .str.replace('\n', '')
    .str.upper()
)


df['CREDITOS'] = (
    df['CREDITOS']
    .astype(str)
    .str.replace('.', '', regex=False)
    .str.replace(',', '.', regex=False)
    .astype(float)
)


df['FECHA'] = pd.to_datetime(
    df['FECHA'],
    dayfirst=True,
    format='%Y-%m-%d',
    errors='coerce'
)

# ELIMINAR NULOS Y CAMBIAR CREDITOS A VENTAS
df = df.dropna(subset=['FECHA'])

df_mensual = (
    df
    .set_index('FECHA')
    .resample('ME')['CREDITOS']
    .sum()
    .reset_index()
    .rename(columns={'CREDITOS': 'VENTAS'})
)


# =========================================================
# GUARDAR DATASET LIMPIO
# =========================================================

df_mensual.to_csv(
    "D:\\Documents\\ESP. ANALITICA DE DATOS\\TESIS ESPECIALIZACION ANALITICA DE DATOS\\DESPLIEGUE\\DATA\\DATASET_LIMPIO.csv",
    index=False,
    encoding='latin-1',
    sep=';'
)

print("Dataset limpio guardado exitosamente.")