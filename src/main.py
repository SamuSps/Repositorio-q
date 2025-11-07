import tkinter as tk
from tkinter import ttk, messagebox
from importacion_de_modulos import (
    seleccionar_archivo, importar_datos, 
    detectar_valores_faltantes, preprocesar_datos
)
import pandas as pd
# --- NUEVO ---
# Necesitamos esta librería para dividir los datos
try:
    from sklearn.model_selection import train_test_split
except ImportError:
    messagebox.showerror(
        "Error de Dependencia", 
        "No se encontró 'scikit-learn'.\nPor favor, instálalo con: pip install scikit-learn"
    )
    exit()
# --- FIN NUEVO ---


class AppPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Creador de Modelos - Regresión Lineal")
        self.root.geometry("1000x750") # Modificado: Aumenté un poco la altura
        self.df = None
        self.df_procesado = None

        # --- NUEVO ---
        # Atributos para guardar los conjuntos de datos divididos
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        # --- FIN NUEVO ---

        self.crear_interfaz()

    def crear_interfaz(self):
        # === 1. Botón Abrir Archivo (arriba) ===
        self.btn_abrir = ttk.Button(self.root, text="Abrir Archivo", command=self.cargar_archivo)
        self.btn_abrir.pack(pady=10, anchor="center")

        # === 2. Ruta del archivo ===
        self.label_ruta = ttk.Label(self.root, text="Ruta: Ningún archivo seleccionado", foreground="gray")
        self.label_ruta.pack(pady=5, fill="x", padx=20)

        # === 3. Tabla con scroll ===
        frame_tabla = ttk.Frame(self.root)
        frame_tabla.pack(pady=10, fill="both", expand=True, padx=20)

        self.tabla = ttk.Treeview(frame_tabla, show="headings")
        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tabla.pack(fill="both", expand=True)

        # === 4. Selección de columnas (debajo de la tabla) ===
        frame_seleccion = ttk.Frame(self.root)
        frame_seleccion.pack(pady=10, fill="x", padx=20)

        # Izquierda: Features
        frame_izq = ttk.LabelFrame(frame_seleccion, text="Columnas de Entrada (Features)")
        frame_izq.pack(side="left", padx=10, fill="both", expand=True)

        self.listbox_features = tk.Listbox(frame_izq, selectmode="multiple", exportselection=False)
        self.listbox_features.pack(fill="both", expand=True, padx=5, pady=5)

        # Derecha: Target
        frame_der = ttk.LabelFrame(frame_seleccion, text="Columna de Salida (Target)")
        frame_der.pack(side="right", padx=10, fill="both", expand=True)

        self.listbox_target = tk.Listbox(frame_der, exportselection=False)
        self.listbox_target.pack(fill="both", expand=True, padx=5, pady=5)

        # === 5. Preprocesamiento ===
        frame_pre = ttk.LabelFrame(self.root, text="Preprocesamiento de Valores Faltantes")
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
        
        # --- NUEVO: Frame para la División de Datos ---
        frame_division = ttk.LabelFrame(self.root, text="División de Datos (Train/Test)")
        frame_division.pack(pady=10, fill="x", padx=20)

        # Slider para Test %
        ttk.Label(frame_division, text="Porcentaje de Test:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.test_split_var = tk.DoubleVar(value=20.0) # Variable para el slider
        self.label_split_pct = ttk.Label(frame_division, text="20.0 %") # Etiqueta que muestra el valor
        
        # Función interna para actualizar la etiqueta del slider
        def actualizar_label_split(valor):
            self.label_split_pct.config(text=f"{float(valor):.1f} %")

        self.slider_split = ttk.Scale(
            frame_division, 
            from_=5.0, # Mínimo 5% para test
            to=50.0, # Máximo 50% para test
            orient="horizontal", 
            variable=self.test_split_var,
            command=actualizar_label_split
        )
        self.slider_split.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.label_split_pct.grid(row=0, column=2, padx=5, pady=5)

        # Semilla (Seed) para reproducibilidad
        ttk.Label(frame_division, text="Semilla (Seed):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.seed_var = tk.StringVar(value="42") # Variable para la semilla
        self.entry_seed = ttk.Entry(frame_division, textvariable=self.seed_var, width=10)
        self.entry_seed.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Botón Dividir
        self.btn_dividir = ttk.Button(frame_division, text="Dividir Datos", command=self.aplicar_division)
        self.btn_dividir.grid(row=1, column=3, padx=10, pady=5, sticky="e")
        
        frame_division.columnconfigure(1, weight=1) # Hacer que el slider se expanda
        frame_division.columnconfigure(3, weight=1) # Hacer que el botón se alinee a la derecha
        # --- FIN NUEVO ---

        # Área de mensajes (MODIFICADO: altura)
        self.text_mensajes = tk.Text(self.root, height=4, state="disabled", background="#f0f0f0")
        self.text_mensajes.pack(pady=10, fill="x", padx=20)

    def cargar_archivo(self):
        ruta = seleccionar_archivo()
        if not ruta:
            return

        self.label_ruta.config(text=f"Ruta: {ruta}", foreground="black")
        self.mostrar_mensaje("Cargando datos...")

        try:
            self.df = importar_datos(ruta)
            self.df_procesado = None
            
            # --- MODIFICADO ---
            # Reseteamos los datos de train/test si se carga un nuevo archivo
            self.X_train = None
            self.X_test = None
            self.y_train = None
            self.y_test = None
            # --- FIN MODIFICADO ---

            self.actualizar_tabla(self.df)
            self.actualizar_listboxes()
            self.mostrar_mensaje(f"Datos cargados: {self.df.shape[0]} filas, {self.df.shape[1]} columnas.")
            self.mostrar_mensaje(detectar_valores_faltantes(self.df))
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.mostrar_mensaje(f"Error: {str(e)}")

    def actualizar_tabla(self, df):
        self.tabla.delete(*self.tabla.get_children())
        self.tabla["columns"] = list(df.columns)
        for col in df.columns:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120, anchor="center")
        
        # --- MODIFICACIÓN ---
        # Quitado .head(1000) para iterar sobre TODAS las filas del dataframe
        for _, row in df.iterrows():
        # --- FIN MODIFICACIÓN ---
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
            
            
            # Reseteamos la división anterior, ya que los datos van a cambiar
            self.X_train = None
            self.X_test = None
            self.y_train = None
            self.y_test = None
            # --- FIN MODIFICADO ---

            columnas = features + [target]
            self.df_procesado = preprocesar_datos(
                self.df, metodo, columnas, valor_constante
            )
            self.actualizar_tabla(self.df_procesado)
            self.mostrar_mensaje("Preprocesado aplicado correctamente.")
            self.mostrar_mensaje(detectar_valores_faltantes(self.df_procesado))
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.mostrar_mensaje(f"Error: {str(e)}")

    # --- NUEVO: Método para dividir los datos ---
    def aplicar_division(self):
        # 1. (Restricción) Verificar si los datos están procesados
        if self.df_procesado is None:
            messagebox.showwarning("Advertencia", "Primero debe aplicar el preprocesamiento de datos.")
            self.mostrar_mensaje("Error: Datos no preprocesados.")
            return

        # 2. (Manejo de errores) Verificar si hay suficientes datos
        if len(self.df_procesado) < 5:
            messagebox.showerror("Error", "No hay suficientes datos para realizar la división (se requieren al menos 5 filas).")
            self.mostrar_mensaje("Error: No hay suficientes datos.")
            return

        try:
            # 3. Obtener parámetros de la UI
            test_size_pct = self.test_split_var.get()
            test_size_float = test_size_pct / 100.0

            seed_str = self.seed_var.get()
            if not seed_str.isdigit() or seed_str == "":
                self.seed_var.set("42") # Valor por defecto si está vacío
                seed = 42
            else:
                seed = int(seed_str)

            # 4. Obtener features y target (ya seleccionados en preprocesado)
            features = self.obtener_features()
            target = self.obtener_target()
            
            # Esto no debería pasar si df_procesado existe, pero por si acaso.
            if not target or not features:
                messagebox.showerror("Error", "Asegúrese de tener features y target seleccionados.")
                return

            X = self.df_procesado[features]
            y = self.df_procesado[target]

            # 5. (Separación) Realizar la división
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                X, y, 
                test_size=test_size_float, 
                random_state=seed # (Reproducibilidad)
            )

            # 6. (Visualización) Mostrar confirmación y tamaños
            msg_total = f"Datos divididos correctamente (Semilla={seed})."
            msg_train = f"Conjunto de Entrenamiento: {len(self.X_train)} filas."
            msg_test = f"Conjunto de Test: {len(self.X_test)} filas."
            
            self.mostrar_mensaje(f"{msg_total}\n{msg_train}\n{msg_test}")
            
            # (DoD) Los conjuntos quedan almacenados en self.X_train, self.X_test, etc.

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.mostrar_mensaje(f"Error en la división: {str(e)}")
    

    def obtener_features(self):
        seleccion = self.listbox_features.curselection()
        return [self.listbox_features.get(i) for i in seleccion]

    def obtener_target(self):
        seleccion = self.listbox_target.curselection()
        return self.listbox_target.get(seleccion[0]) if seleccion else None

    def mostrar_mensaje(self, texto):
        self.text_mensajes.config(state="normal")
        # --- MODIFICADO: Insertar al principio para ver el último mensaje ---
        self.text_mensajes.delete("1.0", tk.END) 
        self.text_mensajes.insert("1.0", texto)
        # --- FIN MODIFICADO ---
        self.text_mensajes.config(state="disabled")

# === INICIO DE LA APLICACIÓN ===
if __name__ == "__main__":
    root = tk.Tk()
    app = AppPrincipal(root)
    root.mainloop()