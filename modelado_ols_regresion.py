# =========================================================
# OLS LINEAR REGRESSION - MODELO FINAL
# =========================================================

import os
import joblib
import numpy as np
import pandas as pd
import statsmodels.api as sm

from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score
)

# =========================================================
# 1. RUTAS
# =========================================================

ruta_dataset = r"D:\Documents\ESP. ANALITICA DE DATOS\TESIS ESPECIALIZACION ANALITICA DE DATOS\DESPLIEGUE\DATA\DATASET_LIMPIO.csv"

ruta_modelo = r"D:\Documents\ESP. ANALITICA DE DATOS\TESIS ESPECIALIZACION ANALITICA DE DATOS\DESPLIEGUE\MODELO"

os.makedirs(ruta_modelo, exist_ok=True)

# =========================================================
# 2. CARGAR DATASET
# =========================================================

data = pd.read_csv(
    ruta_dataset,
    sep=';',
    encoding='latin-1'
)

# =========================================================
# 3. VALIDAR COLUMNA
# =========================================================

if "VENTAS" not in data.columns:
    raise ValueError(
        "La columna 'VENTAS' no existe."
    )

# =========================================================
# 4. PREPARAR DATOS
# =========================================================

y = data["VENTAS"]

x = np.linspace(
    1,
    data.shape[0],
    data.shape[0]
)

X = sm.add_constant(x)

# =========================================================
# 5. ENTRENAR MODELO
# =========================================================

modelo = sm.OLS(y, X)

modelo_fit = modelo.fit()

# =========================================================
# 6. PREDICCIONES
# =========================================================

predicciones = modelo_fit.predict(X)

# =========================================================
# 7. MÉTRICAS
# =========================================================

rmse = np.sqrt(
    mean_squared_error(y, predicciones)
)

mae = mean_absolute_error(
    y,
    predicciones
)

r2 = r2_score(
    y,
    predicciones
)

# =========================================================
# 8. RESULTADOS
# =========================================================

print(modelo_fit.summary())

print("\n============================")
print("MÉTRICAS DEL MODELO")
print("============================")

print(f"RMSE : {rmse:.4f}")
print(f"MAE  : {mae:.4f}")
print(f"R2   : {r2:.4f}")

# =========================================================
# 9. GUARDAR MODELO
# =========================================================

ruta_pkl = os.path.join(
    ruta_modelo,
    "modelo_ols_linear.pkl"
)

joblib.dump(modelo_fit, ruta_pkl)

print("\nMODELO GUARDADO EN:")
print(ruta_pkl)

# =========================================================
# 10. GUARDAR MÉTRICAS
# =========================================================

metricas_df = pd.DataFrame([{
    "Modelo": "OLS_Linear_Regression",
    "Optimizacion": "Ninguna",
    "Tipo_Backtesting": "Sin Backtesting",
    "RMSE": rmse,
    "MAE": mae,
    "R2": r2
}])

ruta_csv = os.path.join(
    ruta_modelo,
    "metricas_modelo_ols.csv"
)

metricas_df.to_csv(
    ruta_csv,
    index=False
)

print("\nCSV DE MÉTRICAS GUARDADO EN:")
print(ruta_csv)