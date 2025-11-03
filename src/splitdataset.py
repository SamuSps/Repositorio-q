import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import sqlite3
import os

class SeparadorDatosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Separador de Datos")
        self.dataset = None
        self.X_train = self.X_test = self.y_train = self.y_test = None

        # Botón para cargar dataset
        self.btn_cargar = tk.Button(root, text="Cargar dataset (CSV, Excel o DB)", command=self.cargar_dataset)
        self.btn_cargar.pack(pady=5)

        # Entrada para porcentaje de test
        tk.Label(root, text="Porcentaje de test (0-100):").pack()
        self.entry_test = tk.Entry(root)
        self.entry_test.insert(0, "20")
        self.entry_test.pack(pady=5)

        # Entrada para semilla
        tk.Label(root, text="Semilla (opcional):").pack()
        self.entry_seed = tk.Entry(root)
        self.entry_seed.insert(0, "42")
        self.entry_seed.pack(pady=5)

        # Botón para separar
        self.btn_separar = tk.Button(root, text="Separar datos", command=self.separar_datos)
        self.btn_separar.pack(pady=10)

        # Label para resultados
        self.lbl_resultados = tk.Label(root, text="", fg="blue")
        self.lbl_resultados.pack(pady=5)

        # Botón para guardar datasets separados
        self.btn_guardar = tk.Button(root, text="Guardar datasets separados", command=self.guardar_datasets)
        self.btn_guardar.pack(pady=5)

    def cargar_dataset(self):
        archivo = filedialog.askopenfilename(filetypes=[
            ("Excel files", "*.xlsx *.xls"),
            ("CSV files", "*.csv"),
            ("SQLite DB", "*.db")
        ])
        if archivo:
            try:
                if archivo.endswith(".csv"):
                    self.dataset = pd.read_csv(archivo)
                elif archivo.endswith((".xlsx", ".xls")):
                    self.dataset = pd.read_excel(archivo)
                elif archivo.endswith(".db"):
                    # Conexión a SQLite
                    conn = sqlite3.connect(archivo)
                    tablas = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
                    if tablas.empty:
                        messagebox.showerror("Error", "La base de datos no contiene tablas.")
                        return
                    tabla_name = tablas.iloc[0, 0]  # Usar la primera tabla
                    self.dataset = pd.read_sql(f"SELECT * FROM {tabla_name}", conn)
                    conn.close()
                else:
                    messagebox.showerror("Error", "Formato de archivo no soportado.")
                    return
                messagebox.showinfo("Éxito", f"Dataset cargado con {len(self.dataset)} filas.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")

    def separar_datos(self):
        if self.dataset is None:
            messagebox.showerror("Error", "No se ha cargado ningún dataset.")
            return

        if len(self.dataset) < 5:
            messagebox.showerror("Error", f"No hay suficientes filas ({len(self.dataset)}) para separar (mínimo 5).")
            return

        try:
            porcentaje_test = float(self.entry_test.get()) / 100
            if not 0 < porcentaje_test < 1:
                raise ValueError
            semilla = int(self.entry_seed.get())
        except ValueError:
            messagebox.showerror("Error", "Porcentaje de test inválido (0-100) o semilla inválida.")
            return

        # Mezclar aleatoriamente
        np.random.seed(semilla)
        df = self.dataset.sample(frac=1).reset_index(drop=True)

        # Calcular número de filas de test
        n_test = int(len(df) * porcentaje_test)
        if n_test < 1 or (len(df) - n_test) < 1:
            messagebox.showerror("Error", "El porcentaje de test seleccionado deja menos de 1 fila en entrenamiento o test.")
            return

        df_test = df.iloc[:n_test]
        df_train = df.iloc[n_test:]

        # Última columna como target
        self.X_train = df_train.iloc[:, :-1]
        self.y_train = df_train.iloc[:, -1]
        self.X_test = df_test.iloc[:, :-1]
        self.y_test = df_test.iloc[:, -1]

        self.lbl_resultados.config(
            text=f"Entrenamiento: {len(self.X_train)} filas\nTest: {len(self.X_test)} filas\n¡Separación realizada correctamente!"
        )

    def guardar_datasets(self):
        if self.X_train is None or self.X_test is None:
            messagebox.showerror("Error", "Primero realiza la separación de datos.")
            return

        try:
            # Guardar como CSV
            self.X_train.to_csv("X_train.csv", index=False)
            self.X_test.to_csv("X_test.csv", index=False)
            self.y_train.to_csv("y_train.csv", index=False)
            self.y_test.to_csv("y_test.csv", index=False)

            # También como Pickle opcional
            self.X_train.to_pickle("X_train.pkl")
            self.X_test.to_pickle("X_test.pkl")
            self.y_train.to_pickle("y_train.pkl")
            self.y_test.to_pickle("y_test.pkl")

            messagebox.showinfo("Éxito", "Datasets guardados en CSV y Pickle.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar los datasets:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SeparadorDatosApp(root)
    root.mainloop()