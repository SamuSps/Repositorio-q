import tkinter as tk
from tkinter import ttk, messagebox, filedialog  # <-- AÑADIDO: filedialog
from importacion_de_modulos import (
    seleccionar_archivo, importar_datos, 
    detectar_valores_faltantes, preprocesar_datos
)
import pandas as pd
import joblib  # <-- AÑADIDO: para guardar el modelo
from datetime import datetime  # <-- AÑADIDO: timestamp

# --- MODIFICADO: Añadir más importaciones ---
try:
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error, r2_score
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    import numpy as np

except ImportError as e:
    messagebox.showerror(
        "Error de Dependencia", 
        f"No se encontró una librería necesaria: {e}.\nPor favor, instálala (ej: pip install scikit-learn matplotlib joblib)"
    )
    exit()
# --- FIN MODIFICADO ---


class AppPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Creador de Modelos - Regresión Lineal")
        self.root.geometry("1200x900")
        
        self.df = None
        self.df_procesado = None

        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
        self.model = None
        self.canvas_widget = None
        self.toolbar_widget = None
        self.canvas = None
        self.scrollable_frame = None
        self.scrollable_frame_window = None

        self.descripcion_modelo = ""

        self.crear_interfaz()

    def crear_interfaz(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # === 1. Botón Abrir Archivo ===
        self.btn_abrir = ttk.Button(self.scrollable_frame, text="Abrir Archivo", command=self.cargar_archivo)
        self.btn_abrir.pack(pady=10, anchor="center")

        # === 2. Ruta del archivo ===
        self.label_ruta = ttk.Label(self.scrollable_frame, text="Ruta: Ningún archivo seleccionado", foreground="gray")
        self.label_ruta.pack(pady=5, fill="x", padx=20)

        # === 3. Tabla ===
        frame_tabla = ttk.Frame(self.scrollable_frame)
        frame_tabla.pack(pady=10, fill="both", expand=True, padx=20)

        self.tabla = ttk.Treeview(frame_tabla, show="headings")
        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tabla.pack(fill="both", expand=True)

        # === 4. Selección de columnas ===
        frame_seleccion = ttk.Frame(self.scrollable_frame)
        frame_seleccion.pack(pady=10, fill="x", padx=20)

        frame_izq = ttk.LabelFrame(frame_seleccion, text="Columnas de Entrada (Features)")
        frame_izq.pack(side="left", padx=10, fill="both", expand=True)
        self.listbox_features = tk.Listbox(frame_izq, selectmode="multiple", exportselection=False)
        self.listbox_features.pack(fill="both", expand=True, padx=5, pady=5)

        frame_der = ttk.LabelFrame(frame_seleccion, text="Columna de Salida (Target)")
        frame_der.pack(side="right", padx=10, fill="both", expand=True)
        self.listbox_target = tk.Listbox(frame_der, exportselection=False)
        self.listbox_target.pack(fill="both", expand=True, padx=5, pady=5)

        # === 5. Preprocesamiento ===
        frame_pre = ttk.LabelFrame(self.scrollable_frame, text="Preprocesamiento de Valores Faltantes")
        frame_pre.pack(pady=10, fill="x", padx=20)
        self.metodo_var = tk.StringVar(value="eliminar")
        ttk.Radiobutton(frame_pre, text="Eliminar filas", variable=self.metodo_var, value="eliminar").grid(row=0, column=0, padx=5, pady=5)
        ttk.Radiobutton(frame_pre, text="Rellenar con Media", variable=self.metodo_var, value="media").grid(row=0, column=1, padx=5, pady=5)
        ttk.Radiobutton(frame_pre, text="Rellenar con Mediana", variable=self.metodo_var, value="mediana").grid(row=0, column=2, padx=5, pady=5)
        ttk.Radiobutton(frame_pre, text="Rellenar con Valor:", variable=self.metodo_var, value="constante").grid(row=1, column=0, padx=5, pady=5)
        self.entry_constante = ttk.Entry(frame_pre, width=10)
        self.entry_constante.grid(row=1, column=1, padx=5, pady=5)
        self.btn_procesar = ttk.Button(frame_pre, text="Aplicar Preprocesado", command=self.aplicar_preprocesado)
        self.btn_procesar.grid(row=1, column=3, padx=10, pady=5)

        # === 6. División de Datos ===
        frame_division = ttk.LabelFrame(self.scrollable_frame, text="División de Datos (Train/Test)")
        frame_division.pack(pady=10, fill="x", padx=20)
        ttk.Label(frame_division, text="Porcentaje de Test:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.test_split_var = tk.DoubleVar(value=20.0) 
        self.label_split_pct = ttk.Label(frame_division, text="20.0 %")
        def actualizar_label_split(valor):
            self.label_split_pct.config(text=f"{float(valor):.1f} %")
        self.slider_split = ttk.Scale(frame_division, from_=5.0, to=50.0, orient="horizontal", variable=self.test_split_var, command=actualizar_label_split)
        self.slider_split.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.label_split_pct.grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(frame_division, text="Semilla (Seed):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.seed_var = tk.StringVar(value="42")
        self.entry_seed = ttk.Entry(frame_division, textvariable=self.seed_var, width=10)
        self.entry_seed.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.btn_dividir = ttk.Button(frame_division, text="Dividir Datos", command=self.aplicar_division)
        self.btn_dividir.grid(row=1, column=3, padx=10, pady=5, sticky="e")
        frame_division.columnconfigure(1, weight=1)

        # === 7. Modelo ===
        frame_modelo_main = ttk.LabelFrame(self.scrollable_frame, text="Creación y Evaluación del Modelo")
        frame_modelo_main.pack(pady=10, fill="both", expand=True, padx=20)
        frame_modelo_main.rowconfigure(0, weight=1)
        frame_modelo_main.columnconfigure(1, weight=1)

        # Controles
        frame_controles_modelo = ttk.Frame(frame_modelo_main)
        frame_controles_modelo.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        self.btn_crear_modelo = ttk.Button(frame_controles_modelo, text="Crear Modelo", command=self.crear_modelo)
        self.btn_crear_modelo.pack(pady=10)

        # --- NUEVO: Botón Guardar Modelo ---
        self.btn_guardar_modelo = ttk.Button(
            frame_controles_modelo,
            text="Guardar Modelo",
            command=self.guardar_modelo,
            state="disabled"
        )
        self.btn_guardar_modelo.pack(pady=8)
        # --- FIN NUEVO ---

        # Área de descripción
        frame_desc = ttk.LabelFrame(frame_controles_modelo, text="Descripción del Modelo (Opcional)")
        frame_desc.pack(pady=10, fill="both", expand=True)
        self.text_descripcion = tk.Text(frame_desc, height=6, wrap="word", font=("TkDefaultFont", 9))
        self.text_descripcion.pack(fill="both", expand=True, padx=5, pady=5)
        scroll_desc = ttk.Scrollbar(frame_desc, command=self.text_descripcion.yview)
        scroll_desc.pack(side="right", fill="y")
        self.text_descripcion.config(yscrollcommand=scroll_desc.set)
        ttk.Label(frame_desc, text="Describe el propósito o características del modelo, etc.", 
                 foreground="gray", font=("TkDefaultFont", 8, "italic")).pack(anchor="w", padx=5, pady=(0,5))

        # Resultados
        frame_resultados = ttk.Frame(frame_modelo_main)
        frame_resultados.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        frame_resultados.rowconfigure(0, weight=1)
        frame_resultados.columnconfigure(0, weight=1)

        self.frame_plot = ttk.Frame(frame_resultados, relief="sunken", borderwidth=1)
        self.frame_plot.grid(row=0, column=0, sticky="nsew")
        ttk.Label(self.frame_plot, text="El gráfico del modelo aparecerá aquí.").pack(padx=10, pady=10)

        frame_texto_resultados = ttk.Frame(frame_resultados)
        frame_texto_resultados.grid(row=1, column=0, sticky="ew", pady=10)
        self.label_formula = ttk.Label(frame_texto_resultados, text="Fórmula: N/A", font=("TkDefaultFont", 10, "bold"), wraplength=700, justify="left")
        self.label_formula.pack(anchor="w")
        self.label_metrics = ttk.Label(frame_texto_resultados, text="Métricas:\n  Train R²: N/A | Test R²: N/A\n  Train MSE: N/A | Test MSE: N/A", justify="left")
        self.label_metrics.pack(anchor="w", pady=5)

        # Mensajes
        self.text_mensajes = tk.Text(self.scrollable_frame, height=4, state="disabled", background="#f0f0f0")
        self.text_mensajes.pack(pady=10, fill="x", padx=20)

    # === NUEVO: Guardar Modelo ===
    def guardar_modelo(self):
        if self.model is None:
            messagebox.showwarning("Sin modelo", "Primero debe crear un modelo antes de guardarlo.")
            return

        archivo = filedialog.asksaveasfilename(
            title="Guardar Modelo de Regresión Lineal",
            defaultextension=".pkl",
            filetypes=[
                ("Archivos Pickle", "*.pkl"),
                ("Archivos Joblib", "*.joblib"),
                ("Todos los archivos", "*.*")
            ]
        )
        if not archivo:
            return

        try:
            features = self.obtener_features()
            target = self.obtener_target()
            descripcion = self.obtener_descripcion()

            # Recalcular métricas
            y_train_pred = self.model.predict(self.X_train)
            y_test_pred = self.model.predict(self.X_test)
            train_r2 = r2_score(self.y_train, y_train_pred)
            test_r2 = r2_score(self.y_test, y_test_pred)
            train_mse = mean_squared_error(self.y_train, y_train_pred)
            test_mse = mean_squared_error(self.y_test, y_test_pred)

            # Fórmula legible
            intercept = self.model.intercept_
            coefs = self.model.coef_
            formula_str = f"{target} = {intercept:.6f}"
            for feat, coef in zip(features, coefs):
                signo = " + " if coef >= 0 else " - "
                formula_str += f"{signo}{abs(coef):.6f} * {feat}"

            # Datos a guardar
            datos_modelo = {
                "modelo": self.model,
                "features": features,
                "target": target,
                "formula": formula_str,
                "descripcion": descripcion,
                "metricas": {
                    "train_r2": float(train_r2),
                    "test_r2": float(test_r2),
                    "train_mse": float(train_mse),
                    "test_mse": float(test_mse)
                },
                "fecha_guardado": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "version_app": "1.0"
            }

            joblib.dump(datos_modelo, archivo)
            self.mostrar_mensaje(f"Modelo guardado correctamente:\n{archivo}")
            messagebox.showinfo("Éxito", f"Modelo guardado en:\n{archivo}")

        except Exception as e:
            error_msg = f"Error al guardar el modelo:\n{str(e)}"
            self.mostrar_mensaje(error_msg)
            messagebox.showerror("Error", error_msg)

    # === MODIFICADO: Activar botón al crear modelo ===
    def crear_modelo(self):
        if self.X_train is None or self.y_train is None:
            messagebox.showwarning("Advertencia", "Primero debe dividir los datos en conjuntos de entrenamiento y test.")
            self.mostrar_mensaje("Error: Datos no divididos.")
            return

        descripcion = self.obtener_descripcion()
        if not descripcion:
            self.mostrar_mensaje("Modelo creado sin descripción (opcional).")
        else:
            self.mostrar_mensaje(f"Modelo creado. Descripción guardada ({len(descripcion)} caracteres).")
            
        try:
            self.model = LinearRegression()
            self.model.fit(self.X_train, self.y_train)
            self.actualizar_resultados_modelo()
            self.actualizar_grafico()

            # Activar botón de guardar
            self.btn_guardar_modelo.config(state="normal")

        except Exception as e:
            messagebox.showerror("Error al crear modelo", str(e))
            self.mostrar_mensaje(f"Error: {str(e)}")

    # === MODIFICADO: resetar también desactiva botón ===
    def resetar_resultados_modelo(self):
        self.model = None
        self.btn_guardar_modelo.config(state="disabled")  # Desactiva

        self.label_formula.config(text="Fórmula: N/A")
        self.label_metrics.config(text="Métricas:\n  Train R²: N/A | Test R²: N/A\n  Train MSE: N/A | Test MSE: N/A")
        
        if self.canvas_widget:
            self.canvas_widget.destroy()
            self.canvas_widget = None
        if self.toolbar_widget:
            self.toolbar_widget.destroy()
            self.toolbar_widget = None
            
        for widget in self.frame_plot.winfo_children():
            widget.destroy()
            
        ttk.Label(self.frame_plot, text="El gráfico del modelo aparecerá aquí.").pack(padx=10, pady=10)
        
        self.text_descripcion.delete("1.0", tk.END)
        self.descripcion_modelo = ""

    # === Resto de métodos sin cambios (cargar_archivo, etc.) ===
    def cargar_archivo(self):
        ruta = seleccionar_archivo()
        if not ruta:
            return

        self.label_ruta.config(text=f"Ruta: {ruta}", foreground="black")
        self.mostrar_mensaje("Cargando datos...")

        try:
            self.df = importar_datos(ruta)
            self.df_procesado = None
            self.X_train = self.X_test = self.y_train = self.y_test = None
            self.resetar_resultados_modelo()

            self.actualizar_tabla(self.df)
            self.actualizar_listboxes()
            self.mostrar_mensaje(f"Datos cargados: {self.df.shape[0]} filas, {self.df.shape[1]} columnas.")
            self.mostrar_mensaje(detectar_valores_faltantes(self.df))
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.mostrar_mensaje(f"Error: {str(e)}")

    # ... (todos los demás métodos quedan exactamente igual: actualizar_tabla, aplicar_preprocesado, etc.)

    def obtener_descripcion(self):
        texto = self.text_descripcion.get("1.0", tk.END).strip()
        self.descripcion_modelo = texto
        return texto

    def cargar_descripcion(self, texto):
        self.text_descripcion.delete("1.0", tk.END)
        if texto:
            self.text_descripcion.insert("1.0", texto)
        self.descripcion_modelo = texto or ""

    def obtener_features(self):
        seleccion = self.listbox_features.curselection()
        return [self.listbox_features.get(i) for i in seleccion]

    def obtener_target(self):
        seleccion = self.listbox_target.curselection()
        return self.listbox_target.get(seleccion[0]) if seleccion else None

    def mostrar_mensaje(self, texto):
        self.text_mensajes.config(state="normal")
        self.text_mensajes.delete("1.0", tk.END)
        self.text_mensajes.insert("1.0", texto)
        self.text_mensajes.config(state="disabled")

    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event=None):
        if self.scrollable_frame_window:
            self.canvas.itemconfig(self.scrollable_frame_window, width=event.width)

    # === Métodos faltantes (copiados tal cual) ===
    def actualizar_tabla(self, df):
        self.tabla.delete(*self.tabla.get_children())
        self.tabla["columns"] = list(df.columns)
        for col in df.columns:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120, anchor="center")
        for _, row in df.iterrows():
            self.tabla.insert("", "end", values=[str(v) for v in row])

    def actualizar_listboxes(self):
        if self.df is None:
            return
        columnas = list(self.df.columns)
        self.listbox_features.delete(0, tk.END)
        self.listbox_target.delete(0, tk.END)
        for col in columnas:
            self.listbox_features.insert(tk.END, col)
            self.listbox_target.insert(tk.END, col)

    def aplicar_preprocesado(self):
        if self.df is None:
            messagebox.showwarning("Advertencia", "Primero carga un archivo.")
            return

        metodo = self.metodo_var.get()
        valor = self.entry_constante.get().strip()
        valor_constante = float(valor) if valor else None

        try:
            features = self.obtener_features()
            target = self.obtener_target()
            if not target:
                raise ValueError("Selecciona una columna de salida (Target).")
            if not features:
                raise ValueError("Selecciona al menos una columna de entrada (Features).")
            
            self.X_train = self.X_test = self.y_train = self.y_test = None
            self.resetar_resultados_modelo()

            columnas_modelo = features + [target]
            df_temp = self.df.copy()
            df_procesado_parcial = preprocesar_datos(
                df_temp, metodo, columnas_modelo, valor_constante
            )
            self.df_procesado = df_procesado_parcial.copy()

            self.actualizar_tabla(self.df_procesado)
            self.mostrar_mensaje("Preprocesado aplicado correctamente (solo en columnas del modelo).")
            self.mostrar_mensaje(detectar_valores_faltantes(self.df_procesado))

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.mostrar_mensaje(f"Error: {str(e)}")

    def aplicar_division(self):
        if self.df_procesado is None:
            messagebox.showwarning("Advertencia", "Primero debe aplicar el preprocesamiento de datos.")
            return
        if len(self.df_procesado) < 5:
            messagebox.showerror("Error", "No hay suficientes datos para realizar la división (se requieren al menos 5 filas).")
            return

        try:
            self.resetar_resultados_modelo()
            
            test_size_pct = self.test_split_var.get()
            test_size_float = test_size_pct / 100.0
            seed = int(self.seed_var.get()) if self.seed_var.get().isdigit() else 42
            if self.seed_var.get() == "": self.seed_var.set("42")

            features = self.obtener_features()
            target = self.obtener_target()
            if not target or not features:
                messagebox.showerror("Error", "Asegúrese de tener features y target seleccionados.")
                return

            X = self.df_procesado[features]
            y = self.df_procesado[target]

            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                X, y, test_size=test_size_float, random_state=seed
            )

            msg_total = f"Datos divididos correctamente (Semilla={seed})."
            msg_train = f"Conjunto de Entrenamiento: {len(self.X_train)} filas."
            msg_test = f"Conjunto de Test: {len(self.X_test)} filas."
            self.mostrar_mensaje(f"{msg_total}\n{msg_train}\n{msg_test}")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.mostrar_mensaje(f"Error en la división: {str(e)}")

    def actualizar_resultados_modelo(self):
        if self.model is None:
            return

        features = self.obtener_features()
        target = self.obtener_target()
        
        try:
            intercept = self.model.intercept_
            coefs = self.model.coef_
            
            formula_str = f"{target} = "
            for i, (feat, coef) in enumerate(zip(features, coefs)):
                signo = "+" if i > 0 and coef >= 0 else ""
                formula_str += f" {signo} ({coef:.4f} * {feat})"
            
            signo_intercept = "+" if intercept >= 0 else ""
            formula_str += f" {signo_intercept} {intercept:.4f}"
            
            self.label_formula.config(text=f"Fórmula: {formula_str}")
        except Exception as e:
            self.label_formula.config(text=f"Fórmula: Error al generar - {e}")

        try:
            y_train_pred = self.model.predict(self.X_train)
            train_r2 = r2_score(self.y_train, y_train_pred)
            train_mse = mean_squared_error(self.y_train, y_train_pred)
            
            y_test_pred = self.model.predict(self.X_test)
            test_r2 = r2_score(self.y_test, y_test_pred)
            test_mse = mean_squared_error(self.y_test, y_test_pred)

            metrics_str = "Métricas (R²: Coef. Determinación | ECM: Error Cuadrático Medio):\n"
            metrics_str += f"  [Entrenamiento]\t R²: {train_r2:.4f}\t | ECM: {train_mse:.4f}\n"
            metrics_str += f"  [Test]\t\t R²: {test_r2:.4f}\t | ECM: {test_mse:.4f}"
            
            self.label_metrics.config(text=metrics_str)
            
        except Exception as e:
            self.label_metrics.config(text=f"Métricas: Error al calcular - {e}")

    def actualizar_grafico(self):
        if self.canvas_widget:
            self.canvas_widget.destroy()
        if self.toolbar_widget:
            self.toolbar_widget.destroy()
        for widget in self.frame_plot.winfo_children():
            widget.destroy()

        features = self.obtener_features()
        target = self.obtener_target()

        if len(features) > 1:
            ttk.Label(self.frame_plot, text="No se puede graficar: Múltiples features (entradas).\nEl modelo fue creado, pero no es visualizable en 2D.").pack(padx=10, pady=10)
            self.mostrar_mensaje("Gráfico no generado (múltiples features).")
            return
            
        try:
            fig = Figure(figsize=(6, 4), dpi=100)
            ax = fig.add_subplot(111)

            feature_name = features[0]
            ax.scatter(self.X_train[feature_name], self.y_train, color='blue', label='Entrenamiento', alpha=0.7)
            ax.scatter(self.X_test[feature_name], self.y_test, color='red', label='Test', alpha=0.7)

            X_all_series = pd.concat([self.X_train[feature_name], self.X_test[feature_name]])
            X_line = np.linspace(X_all_series.min(), X_all_series.max(), 100).reshape(-1, 1)
            X_line_df = pd.DataFrame(X_line, columns=[feature_name])
            y_line = self.model.predict(X_line_df)
            
            ax.plot(X_line, y_line, color='green', linewidth=3, label='Recta de Regresión')
            ax.set_xlabel(feature_name)
            ax.set_ylabel(target)
            ax.set_title("Regresión Lineal: Ajuste del Modelo")
            ax.legend()
            ax.grid(True)
            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.frame_plot)
            self.canvas_widget = canvas.get_tk_widget()
            self.canvas_widget.pack(fill='both', expand=True)

            toolbar = NavigationToolbar2Tk(canvas, self.frame_plot)
            toolbar.update()
            self.toolbar_widget = toolbar
            self.toolbar_widget.pack(side='bottom', fill='x')
            canvas.draw()
            
        except Exception as e:
            ttk.Label(self.frame_plot, text=f"Error al generar gráfico: {e}").pack(padx=10, pady=10)
            self.mostrar_mensaje(f"Error al graficar: {e}")


# === INICIO DE LA APLICACIÓN ===
if __name__ == "__main__":
    root = tk.Tk()
    app = AppPrincipal(root)
    root.mainloop()