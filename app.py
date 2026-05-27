# =========================================================
# STREAMLIT APP - RESTAURANTE
# =========================================================

import joblib
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="Sistema Predictivo Restaurante",
    page_icon="📈",
    layout="wide"
)

# =========================================================
# TÍTULO
# =========================================================

st.title("📈 Sistema Predictivo de Ventas Restaurante")

st.markdown("---")

# =========================================================
# RUTAS
# =========================================================

ruta_dataset = "DATA/DATASET_LIMPIO.csv"

ruta_modelo = "MODELO/modelo_ols_linear.pkl"

# =========================================================
# CARGAR DATASET
# =========================================================

data = pd.read_csv(
    ruta_dataset,
    sep=';',
    encoding='latin-1'
)

data['FECHA'] = pd.to_datetime(
    data['FECHA']
)

# =========================================================
# CARGAR MODELO
# =========================================================

modelo = joblib.load(
    ruta_modelo
)

# =========================================================
# MOSTRAR DATASET
# =========================================================

st.subheader("Dataset Histórico")

st.dataframe(data)

# =========================================================
# GRÁFICO HISTÓRICO
# =========================================================

st.subheader("Ventas Históricas")

fig, ax = plt.subplots(figsize=(14,5))

ax.plot(
    data['FECHA'],
    data['VENTAS']
)

ax.set_title("Serie Temporal Ventas")

ax.set_xlabel("Fecha")

ax.set_ylabel("Ventas")

ax.grid(True)

st.pyplot(fig)

# =========================================================
# PRONÓSTICO
# =========================================================

siguiente_x = data.shape[0] + 1

X_futuro = pd.DataFrame({
    "const": [1],
    "x1": [siguiente_x]
})

pronostico = modelo.predict(
    X_futuro
)[0]

ultima_fecha = data['FECHA'].max()

fecha_futura = (
    ultima_fecha + pd.offsets.MonthEnd(1)
)

# =========================================================
# KPI PRONÓSTICO
# =========================================================

st.subheader("Pronóstico Próximo Mes")

st.metric(
    label=f"Ventas estimadas {fecha_futura.strftime('%Y-%m')}",
    value=f"$ {pronostico:,.0f}"
)

# =========================================================
# PLANIFICACIÓN OPERATIVA
# =========================================================

st.subheader("Planificación Operativa")

if pronostico <= 3000000:

    nivel_operacion = "Baja demanda"
    meseros = 2
    cocina = 2

elif pronostico <= 6000000:

    nivel_operacion = "Demanda media"
    meseros = 2
    cocina = 3

elif pronostico <= 9000000:

    nivel_operacion = "Alta demanda"
    meseros = 3
    cocina = 3

else:

    nivel_operacion = "Demanda extraordinaria"
    meseros = 3
    cocina = 4

col1, col2, col3 = st.columns(3)

col1.metric(
    "Nivel Operativo",
    nivel_operacion
)

col2.metric(
    "Meseros",
    meseros
)

col3.metric(
    "Cocina",
    cocina
)

# =========================================================
# INSUMOS
# =========================================================

st.subheader("Insumos Estimados")

precio_promedio_plato = 25000

platos_estimados = (
    pronostico /
    precio_promedio_plato
)

df_insumos = pd.DataFrame({

    "Insumo": [

        "Arroz (kg)",
        "Pollo (kg)",
        "Carne (kg)",
        "Pescado (kg)",
        "Granos (kg)"

    ],

    "Cantidad Estimada": [

        round(platos_estimados * 0.15, 2),
        round(platos_estimados * 0.12, 2),
        round(platos_estimados * 0.20, 2),
        round(platos_estimados * 0.012, 2),
        round(platos_estimados * 0.05, 2)

    ]

})

st.dataframe(df_insumos)

# =========================================================
# COSTOS OPERATIVOS
# =========================================================

st.subheader("Resumen Financiero")

DIAS_LABORALES = 22

precio_kg_arroz = 4000
precio_kg_pollo = 12000
precio_kg_carne = 10000
precio_kg_pescado = 16000
precio_kg_granos = 20000

costo_total = (

    (platos_estimados * 0.15 * precio_kg_arroz) +
    (platos_estimados * 0.12 * precio_kg_pollo) +
    (platos_estimados * 0.20 * precio_kg_carne) +
    (platos_estimados * 0.012 * precio_kg_pescado) +
    (platos_estimados * 0.05 * precio_kg_granos)

)

salario_diario = 60000

empleados = meseros + cocina

costo_personal = (
    empleados *
    salario_diario *
    DIAS_LABORALES
)

gastos_fijos = 500000

costo_operativo = (
    costo_total +
    costo_personal +
    gastos_fijos
)

utilidad = (
    pronostico -
    costo_operativo
)

df_financiero = pd.DataFrame({

    "Concepto": [

        "Pronóstico Ventas",
        "Costo Inventario",
        "Costo Personal",
        "Gastos Fijos",
        "Costo Operativo",
        "Utilidad Estimada"

    ],

    "Valor": [

        round(pronostico, 2),
        round(costo_total, 2),
        round(costo_personal, 2),
        round(gastos_fijos, 2),
        round(costo_operativo, 2),
        round(utilidad, 2)

    ]

})

df_financiero["Valor"] = (
    df_financiero["Valor"]
    .map(lambda x: f"$ {x:,.0f}")
)

st.dataframe(df_financiero)

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "Modelo Predictivo OLS Linear Regression"
)