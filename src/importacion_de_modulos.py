import pandas as pd
import sqlite3
import os
import tkinter as tk
from tkinter import filedialog

def seleccionar_archivo():
    """Abre diálogo para seleccionar CSV, Excel o SQLite."""
    root = tk.Tk()
    root.withdraw()
    archivo = filedialog.askopenfilename(
        title="Selecciona un dataset",
        filetypes=[
            ("CSV", "*.csv"),
            ("Excel", "*.xlsx *.xls"),
            ("SQLite", "*.sqlite *.db"),
            ("Todos", "*.*")
        ]
    )
    root.destroy()
    return archivo if archivo else None

def importar_datos(ruta):
    """Importa datos desde CSV, Excel o SQLite."""
    if not os.path.exists(ruta):
        raise FileNotFoundError("Archivo no encontrado.")
    
    ext = os.path.splitext(ruta)[1].lower()
    
    try:
        if ext == '.csv':
            df = pd.read_csv(ruta)
        elif ext in ['.xlsx', '.xls']:
            df = pd.read_excel(ruta)
        elif ext in ['.sqlite', '.db']:
            conn = sqlite3.connect(ruta)
            tablas = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
            if tablas.empty:
                raise ValueError("No hay tablas en la base de datos.")
            nombre_tabla = tablas['name'].iloc[0]
            df = pd.read_sql_query(f"SELECT * FROM {nombre_tabla}", conn)
            conn.close()
        else:
            raise ValueError("Formato no soportado.")
        
        return df
    except Exception as e:
        raise ValueError(f"Error al cargar: {str(e)}")

def detectar_valores_faltantes(df):
    """Devuelve resumen de NaN por columna."""
    faltantes = df.isna().sum()
    total = faltantes.sum()
    if total == 0:
        return "No hay valores faltantes."
    resumen = f"Valores faltantes: {total}\n"
    for col, count in faltantes.items():
        if count > 0:
            resumen += f"  • {col}: {count}\n"
    return resumen

def preprocesar_datos(df, metodo, columnas=None, valor_constante=None):
    """Elimina o rellena NaN."""
    df = df.copy()
    if columnas:
        df = df[columnas + [df.columns[-1]]]  # Asegurar target
    
    try:
        if metodo == "eliminar":
            df = df.dropna()
        elif metodo == "media":
            df = df.fillna(df.mean(numeric_only=True))
        elif metodo == "mediana":
            df = df.fillna(df.median(numeric_only=True))
        elif metodo == "constante":
            if valor_constante is None:
                raise ValueError("Falta valor constante.")
            df = df.fillna(valor_constante)
        return df
    except Exception as e:
        raise ValueError(f"Error en preprocesado: {str(e)}")