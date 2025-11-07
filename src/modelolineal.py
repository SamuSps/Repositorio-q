# ==============================================
# 1. Importar librerías necesarias
# ==============================================
import pandas as pd
import numpy as np
import os
import sqlite3
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# ==============================================
# 2. Cargar el dataset (desde CSV, XLSX o DB)
# ==============================================
csv_file = r"C:\Users\Elena\Downloads\housing.csv"
xlsx_file = r"C:\Users\Elena\Downloads\housing.xlsx"
db_file = r"C:\Users\Elena\Downloads\housing.db"

data = None

if os.path.exists(csv_file):
    print(" Cargando datos desde CSV...")
    data = pd.read_csv(csv_file)
elif os.path.exists(xlsx_file):
    print(" Cargando datos desde Excel...")
    data = pd.read_excel(xlsx_file)
elif os.path.exists(db_file):
    print(" Cargando datos desde Base de Datos SQLite...")
    conn = sqlite3.connect(db_file)
    tablas = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
    print(" Tablas disponibles:", tablas)
    data = pd.read_sql("SELECT * FROM housing;", conn)
    conn.close()
else:
    raise FileNotFoundError(" No se encontró ningún archivo housing (.csv, .xlsx o .db) en la carpeta de Descargas.")

# ==============================================
# 3. Mostrar información básica
# ==============================================
print("\n Datos cargados correctamente.")
print(" Columnas disponibles:", list(data.columns))
print("\nPrimeras filas del dataset:")
print(data.head())

# ==============================================
# 4. Selección de variables (ajustada al dataset real)
# ==============================================
X = data[['median_income']]
y = data['median_house_value']

# ==============================================
# 5. División de los datos en entrenamiento y prueba
# ==============================================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ==============================================
# 6. Entrenamiento del modelo
# ==============================================
model = LinearRegression()
model.fit(X_train, y_train)

# ==============================================
# 7. Evaluación del modelo
# ==============================================
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n===== Resultados del Modelo =====")
print(f"Coeficiente (pendiente): {model.coef_[0]:.2f}")
print(f"Intersección: {model.intercept_:.2f}")
print(f"Error cuadrático medio (MSE): {mse:.2f}")
print(f"Coeficiente de determinación (R²): {r2:.2f}")

# ==============================
# 8. Visualización optimizada
# ==============================
# Tomar una muestra de 1000 puntos (o menos si el test es más pequeño)
sample = X_test.join(y_test).sample(min(1000, len(X_test)), random_state=42)

plt.figure(figsize=(8, 5))
plt.scatter(sample['median_income'], sample['median_house_value'], 
            color="blue", alpha=0.5, label="Datos reales")
# Predicción de la muestra
y_pred_sample = model.predict(sample[['median_income']])
plt.plot(sample['median_income'], y_pred_sample, color="red", linewidth=2, label="Predicción (modelo lineal)")
plt.title("Regresión Lineal: Ingreso medio vs Valor medio de vivienda")
plt.xlabel("Ingreso medio (median_income)")
plt.ylabel("Valor medio de la vivienda (median_house_value)")
plt.legend()
plt.grid(True)
plt.show()  

