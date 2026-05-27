# =========================================================
# PLANIFICACIÓN OPERATIVA Y FINANCIERA
# =========================================================

import joblib
import numpy as np
import pandas as pd

# =========================================================
# 1. RUTAS
# =========================================================

ruta_dataset = r"D:\Documents\ESP. ANALITICA DE DATOS\TESIS ESPECIALIZACION ANALITICA DE DATOS\DESPLIEGUE\DATA\DATASET_LIMPIO.csv"

ruta_modelo = r"D:\Documents\ESP. ANALITICA DE DATOS\TESIS ESPECIALIZACION ANALITICA DE DATOS\DESPLIEGUE\MODELO\modelo_ols_linear.pkl"

# =========================================================
# 2. CARGAR DATASET
# =========================================================

data = pd.read_csv(
    ruta_dataset,
    sep=';',
    encoding='latin-1'
)

# =========================================================
# 3. CONVERTIR FECHA
# =========================================================

data['FECHA'] = pd.to_datetime(
    data['FECHA']
)

# =========================================================
# 4. CARGAR MODELO
# =========================================================

modelo = joblib.load(
    ruta_modelo
)

# =========================================================
# 5. PRONÓSTICO MES SIGUIENTE
# =========================================================

siguiente_x = data.shape[0] + 1

X_futuro = pd.DataFrame({
    "const": [1],
    "x1": [siguiente_x]
})

pronostico_mes = modelo.predict(
    X_futuro
)[0]

ultima_fecha = data['FECHA'].max()

fecha_futura = (
    ultima_fecha + pd.offsets.MonthEnd(1)
)

# =========================================================
# 6. MOSTRAR PRONÓSTICO
# =========================================================

print("\n============================")
print("PRONÓSTICO MES SIGUIENTE")
print("============================")

print(f"Fecha pronosticada : {fecha_futura.date()}")

print(f"Ventas estimadas   : ${pronostico_mes:,.2f}")

# =========================================================
# 7. PLANIFICACIÓN OPERATIVA
# =========================================================

print("\n============================")
print("PLANIFICACIÓN OPERATIVA")
print("============================")

pronostico_mayo_num = float(pronostico_mes)

# Clasificación operacional
if pronostico_mayo_num <= 5000000:

    nivel_operacion = "Baja demanda"
    meseros = 2
    cocina = 2

elif pronostico_mayo_num <= 10000000:

    nivel_operacion = "Demanda media"
    meseros = 2
    cocina = 3

elif pronostico_mayo_num <= 17000000:

    nivel_operacion = "Alta demanda"
    meseros = 3
    cocina = 3

else:

    nivel_operacion = "Demanda extraordinaria"
    meseros = 3
    cocina = 4

print(f"Nivel operativo      : {nivel_operacion}")

print(f"Meseros requeridos   : {meseros} diarios")

print(f"Personal de cocina   : {cocina} diarios")

# =========================================================
# 8. INSUMOS ESTIMADOS
# =========================================================

print("\n============================")
print("INSUMOS ESTIMADOS")
print("============================")

DIAS_LABORALES = 22

precio_promedio_plato = 25000

MES_EVALUADO = fecha_futura.month

# volumen de platos
platos_estimados_mes = (
    pronostico_mayo_num /
    precio_promedio_plato
)

# recetas
kg_arroz_mes = platos_estimados_mes * 0.15

kg_pollo_mes = platos_estimados_mes * 0.12

kg_granos_mes = platos_estimados_mes * 0.05

kg_carne_mes = platos_estimados_mes * 0.20

kg_pescado_mes = kg_pollo_mes * 0.10

# gaseosas
gaseosas_consumo_mes = 30

gaseosas_compra_mes = (
    60 if MES_EVALUADO % 2 == 0 else 0
)

df_insumos = pd.DataFrame({

    "Insumo": [

        "Arroz (kg)",
        "Pollo (kg)",
        "Carne (kg)",
        "Pescado (kg)",
        "Granos (kg)",
        "Gaseosas - Consumo Mes",
        "Gaseosas - Compra Real"

    ],

    "Cantidad_Estimada": [

        round(kg_arroz_mes, 2),
        round(kg_pollo_mes, 2),
        round(kg_carne_mes, 2),
        round(kg_pescado_mes, 2),
        round(kg_granos_mes, 2),
        gaseosas_consumo_mes,
        gaseosas_compra_mes

    ]

})

print(df_insumos.to_string(index=False))

# =========================================================
# 9. COSTOS INVENTARIO
# =========================================================

print("\n============================")
print("COSTOS DE INVENTARIO")
print("============================")

precio_kg_arroz = 4000

precio_kg_pollo = 12000

precio_kg_carne = 10000

precio_kg_pescado = 16000

precio_kg_granos = 20000

costo_especias_dia = 10000

VALOR_LOTE_GASEOSAS = 60000

# costos
costo_arroz_mes = (
    kg_arroz_mes *
    precio_kg_arroz
)

costo_pollo_mes = (
    kg_pollo_mes *
    precio_kg_pollo
)

costo_carne_mes = (
    kg_carne_mes *
    precio_kg_carne
)

costo_pescado_mes = (
    kg_pescado_mes *
    precio_kg_pescado
)

costo_granos_mes = (
    kg_granos_mes *
    precio_kg_granos
)

costo_especias_mes = (
    costo_especias_dia *
    DIAS_LABORALES
)

# gaseosas
costo_gaseosas_mes = (
    VALOR_LOTE_GASEOSAS
    if MES_EVALUADO % 2 == 0
    else 0
)

# costo total
costo_total_inventario_mes = (

    costo_arroz_mes +
    costo_pollo_mes +
    costo_carne_mes +
    costo_pescado_mes +
    costo_granos_mes +
    costo_especias_mes +
    costo_gaseosas_mes

)

df_costos = pd.DataFrame({

    "Concepto": [

        "Costo Arroz",
        "Costo Pollo",
        "Costo Carne",
        "Costo Pescado",
        "Costo Granos",
        "Costo Especias",
        "Costo Gaseosas",
        "COSTO TOTAL INVENTARIO"

    ],

    "Valor": [

        round(costo_arroz_mes, 2),
        round(costo_pollo_mes, 2),
        round(costo_carne_mes, 2),
        round(costo_pescado_mes, 2),
        round(costo_granos_mes, 2),
        round(costo_especias_mes, 2),
        round(costo_gaseosas_mes, 2),
        round(costo_total_inventario_mes, 2)

    ]

})

print(df_costos.to_string(index=False))

# =========================================================
# 10. RESUMEN FINANCIERO
# =========================================================

print("\n============================")
print("RESUMEN FINANCIERO")
print("============================")

# personal
salario_diario = 60000

total_empleados = meseros + cocina

costo_personal_mes = (
    total_empleados *
    salario_diario *
    DIAS_LABORALES
)

# gastos fijos
gastos_funcionamiento_mes = 500000

# costos totales
costo_operativo_total = (

    costo_total_inventario_mes +
    costo_personal_mes +
    gastos_funcionamiento_mes

)

# utilidad
utilidad_estimada = (
    pronostico_mayo_num -
    costo_operativo_total
)

df_resumen = pd.DataFrame({

    "Concepto": [

        "Pronóstico ventas",
        "Costo inventario",
        "Costo personal",
        "Gastos funcionamiento",
        "Costo operativo total",
        "Utilidad neta estimada"

    ],

    "Valor": [

        round(pronostico_mayo_num, 2),
        round(costo_total_inventario_mes, 2),
        round(costo_personal_mes, 2),
        round(gastos_funcionamiento_mes, 2),
        round(costo_operativo_total, 2),
        round(utilidad_estimada, 2)

    ]

})

df_resumen["Valor_Formateado"] = (
    df_resumen["Valor"]
    .map(lambda x: f"$ {x:,.2f}")
)

print(
    df_resumen[
        ["Concepto", "Valor_Formateado"]
    ].to_string(index=False)
)