import tkinter as tk
from tkinter import ttk, messagebox, filedialog 
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

import ctypes  # <--- AÑADIDO: Para acceder a funciones de sistema

# --- AÑADIDO ---
# Aumento de resolución de la UI
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass
# --- FIN AÑADIDO ---

class AppPrincipal:
<<<<<<< HEAD

=======
    
    
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
    def __init__(self, root):
        
        self.root = root
        self.root.title("Creador de Modelos - Regresión Lineal")
        self.root.state("zoomed") #Inicia maximizado
        
        # === Variables de Datos ===
        self.df = None
        self.df_procesado = None

        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
        self.model = None
        self.descripcion_modelo = ""

        # === NUEVO: Para modelos cargados ===
        self.modelo_cargado = False
        self.features = []
        self.target = None
        self.metricas = None  # Para métricas cargadas

        # === Flags de Estado (Control del Wizard) ===
        #Variables controlan si el usuario puede avanzar al siguiente paso
        self.archivo_cargado = False
        self.variables_seleccionadas = False
        self.preprocesado_aplicado = False
        self.division_realizada = False
        self.modelo_creado = False

        # === Variables UI y Navegación ===
        self.paso_actual = 0
        self.frames_pasos = []  # Lista para almacenar los frames de cada paso
        self.status_var = tk.StringVar(value="Listo.")
        
        # === Variables de Control (Inputs) ===
        self.metodo_var = tk.StringVar(value="eliminar")
        self.test_split_var = tk.DoubleVar(value=20.0)
        self.seed_var = tk.StringVar(value="42")

        # Variables para gráficos
        self.canvas_widget = None
        self.toolbar_widget = None

        # === NUEVO: Para UI de Predicción ===
        self.frame_prediccion = None
        self.entries_prediccion = {}  # Diccionario: feature -> Entry
        self.label_salida = None
        self.btn_prediccion = None

        self.crear_interfaz()

    def mostrar_mensaje(self, texto):
        
        self.status_var.set(texto)
        print(f"[INFO] {texto}")

    # === Método Auxiliar: Ejecución con Ventana de Carga ===
    # Bloquea la UI y muestra un spinner mientras se ejecuta una función
    def ejecutar_con_carga(self, funcion, mensaje, *args, **kwargs):
       
        ventana_carga = tk.Toplevel(self.root)
        ventana_carga.title("Procesando...")
        ventana_carga.geometry("300x100")
        ventana_carga.resizable(False, False)
        
        # Centrar ventana
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 150
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 50
        ventana_carga.geometry(f"+{x}+{y}")
        
        ventana_carga.transient(self.root)
        ventana_carga.grab_set()  # Bloquear interacción con ventana principal
        
        ttk.Label(ventana_carga, text=mensaje, anchor="center").pack(pady=10)
        pb = ttk.Progressbar(ventana_carga, mode="indeterminate")
        pb.pack(fill="x", padx=20, pady=5)
        pb.start(10)
        
        self.root.update_idletasks()
        
        try:
            funcion(*args, **kwargs)
        except Exception as e:
            self.mostrar_mensaje(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))
        finally:
            ventana_carga.destroy()

    def crear_interfaz(self):
        # === Estructura Principal ===
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 1. Header (Título del paso actual)
<<<<<<< HEAD
        self.header_label = ttk.Label(main_frame, 
                                      text="Paso 0: Bienvenida",
                                        font=("Helvetica", 16, "bold"))
=======
        self.header_label = ttk.Label(main_frame, text="Paso 0: Bienvenida",
                                       font=("Helvetica", 16, "bold"))
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
        self.header_label.pack(pady=(0, 10))

        # === FIX: Canvas con Scrollbar para Content Area ===
        # Frame contenedor para canvas y scrollbar
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(fill="both", expand=True, pady=(0, 10))

        self.canvas = tk.Canvas(canvas_frame, bg="white")
        self.scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            self.on_frame_configure
        )

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # 2. Content Area (Ahora dentro del scrollable_frame)
        self.content_frame = ttk.Frame(self.scrollable_frame)
        self.content_frame.pack(fill="both", expand=True)

        self.frames_pasos = []
        # Inicialización de todos los pasos
        self.crear_paso_bienvenida()       # Paso 0
        self.crear_paso_carga()            # Paso 1
        self.crear_paso_configuracion()    # Paso 2 (NUEVO UNIFICADO)
        self.crear_paso_modelo()           # Paso 3 (Antes era el 5)

        # 3. Footer (Botones de Navegación + Barra de Estado)
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill="x", pady=10)

        self.btn_anterior = ttk.Button(footer_frame, text="< Anterior",
                                        command=lambda: self.navegar(-1),
                                          state="disabled")
        self.btn_anterior.pack(side="left")

        self.btn_siguiente = ttk.Button(footer_frame, text="Siguiente >", 
                                        command=lambda: self.navegar(1))
        self.btn_siguiente.pack(side="right")

        # Barra de Estado
        status_frame = ttk.LabelFrame(main_frame, text="Estado")
        status_frame.pack(fill="x", pady=(5, 0))
        self.lbl_status = ttk.Label(status_frame, 
                                    textvariable=self.status_var, 
                                    foreground="blue")
        self.lbl_status.pack(fill="x", padx=5, pady=5)

        # Iniciar en el primer paso
        self.mostrar_paso(0)

    # === FIX: Métodos para Scroll (Actualizados para evitar espacio vacío) ===
    def on_frame_configure(self, event=None):
        # Actualizar tamaños con update para asegurar cálculos precisos
        self.canvas.update_idletasks()
        self.scrollable_frame.update_idletasks()
        
        # Actualizar scrollregion
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        # Ajustar tamaño de la ventana del canvas
        canvas_width = self.canvas.winfo_width()
        content_height = self.scrollable_frame.winfo_reqheight()
        self.canvas.itemconfig(self.canvas_window, 
                               width=canvas_width,
                               height=content_height)
        
        # FIX PRINCIPAL: Si el contenido es más corto que el canvas, redimensionar el canvas para eliminar espacio vacío
        canvas_height = self.canvas.winfo_height()
        if content_height < canvas_height:
            self.canvas.configure(height=content_height)

    def on_canvas_configure(self, event=None):
        # Ajustar ancho de la ventana del canvas al ancho del canvas
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        # Reconfigurar scroll y heights si es necesario
        self.on_frame_configure()

    # === PASO 0: Bienvenida ===
    def crear_paso_bienvenida(self):
        
        frame = ttk.Frame(self.content_frame)
        self.frames_pasos.append(frame)
        
        lbl = ttk.Label(frame, text="Bienvenido al Asistente", 
                        font=("Helvetica", 14))
        lbl.pack(pady=20)
        
        msg = (
            "Este asistente le guiará paso a paso para crear un modelo de Regresión Lineal.\n\n"
            "1. Carga de Datos: Importe su archivo CSV o Excel.\n"
            "2. Selección de Variables: Elija qué predecir (Target) y con qué (Features).\n"
            "3. Preprocesamiento: Gestione los valores faltantes.\n"
            "4. División: Separe sus datos en entrenamiento y prueba.\n"
            "5. Modelo: Entrene, evalúe y guarde su modelo.\n\n"
            "Haga clic en 'Siguiente' para comenzar."
        )
        ttk.Label(frame, text=msg, justify="center").pack(pady=10)

        # === NUEVO: Botón para cargar modelo existente ===
        btn_cargar_modelo = ttk.Button(frame, 
                                       text="Cargar Modelo Existente", 
                                       command=self.cargar_modelo_existente)
        btn_cargar_modelo.pack(pady=10)

    # === NUEVO: Método para cargar modelo existente ===
    def cargar_modelo_existente(self):
        archivo = filedialog.askopenfilename(
            title="Cargar Modelo de Regresión Lineal",
            defaultextension=".pkl",
            filetypes=[
                ("Archivos Pickle/Joblib", "*.pkl *.joblib"),
                ("Todos los archivos", "*.*")
            ]
        )
        if not archivo:
            return

        try:
            datos = joblib.load(archivo)

            # Validación básica
            if "modelo" not in datos or "features" not in datos or "target" not in datos:
                raise ValueError("El archivo no contiene un modelo válido.")

            # Cargar datos
            self.model = datos["modelo"]
            self.features = datos["features"]
            self.target = datos["target"]
            self.metricas = datos.get("metricas", {})  # Guardar métricas
            self.modelo_cargado = True

            # Actualizar fórmula (usar la guardada)
            self.label_formula.config(text=f"Fórmula: {datos.get('formula', 'N/A')}")

            # Actualizar métricas (usar las guardadas)
            metrics = self.metricas
            metrics_str = "Métricas (R²: Coef. Determinación | ECM: Error Cuadrático Medio):\n"
            metrics_str += f"  [Entrenamiento]\t R²: {metrics.get('train_r2', 'N/A'):.4f}\t | ECM: {metrics.get('train_mse', 'N/A'):.4f}\n"
            metrics_str += f"  [Test]\t\t R²: {metrics.get('test_r2', 'N/A'):.4f}\t | ECM: {metrics.get('test_mse', 'N/A'):.4f}"
            self.label_metrics.config(text=metrics_str)

            # Cargar descripción
            self.cargar_descripcion(datos.get("descripcion", ""))

            # Limpiar gráfico y mostrar mensaje
            for widget in self.frame_plot.winfo_children():
                widget.destroy()
            ttk.Label(self.frame_plot, 
                      text="Gráfico no disponible para modelos cargados.\n(Se muestra fórmula, métricas y descripción.)",
                      justify="center").pack(expand=True, padx=10, pady=10)

            # Deshabilitar creación y navegación
            self.btn_crear_modelo.config(state="disabled")
            self.btn_guardar_modelo.config(state="normal")  # Permitir re-guardar si se edita desc.

            # === NUEVO: Habilitar Predicción ===
            self.crear_ui_prediccion()

            # Navegar al Paso 3 y bloquear navegación
            self.mostrar_paso(3)
            self.btn_anterior.config(state="disabled")
            self.btn_siguiente.config(state="disabled", text="Modelo Cargado")

            # Confirmación
            messagebox.showinfo("Éxito", "El modelo ha sido recuperado exitosamente.")
            self.mostrar_mensaje(f"Modelo cargado desde: {archivo}")

            # FIX: Actualizar scroll después de cargar
            self.on_frame_configure()

        except Exception as e:
            error_msg = f"Error al cargar el modelo: {str(e)}\n\nEl archivo podría estar corrupto o no ser válido.\nIntente con otro archivo."
            messagebox.showerror("Error de Carga", error_msg)
            self.mostrar_mensaje(f"Error en carga: {str(e)}")

    # === NUEVO: Crear UI de Predicción Dinámica ===
    def crear_ui_prediccion(self):
        if self.frame_prediccion:
            # Limpiar si existe
            for widget in self.frame_prediccion.winfo_children():
                widget.destroy()
            self.entries_prediccion.clear()

        features = self.features if self.modelo_cargado else self.obtener_features()

        if not features or self.model is None:
            return

        # Frame para predicción
        self.frame_prediccion = ttk.LabelFrame(self.frame_left, text="Predicción con el Modelo", padding=10)
        self.frame_prediccion.pack(pady=10, padx=10, fill="x")

        # Campos dinámicos
        for feat in features:
            row_frame = ttk.Frame(self.frame_prediccion)
            row_frame.pack(fill="x", pady=2)
            ttk.Label(row_frame, text=f"{feat}:", width=20, anchor="w").pack(side="left")
            entry = ttk.Entry(row_frame, width=15)
            entry.pack(side="right", padx=5)
            self.entries_prediccion[feat] = entry

        # Botón de predicción
        self.btn_prediccion = ttk.Button(self.frame_prediccion, text="Realizar Predicción",
                                         command=self.realizar_prediccion)
        self.btn_prediccion.pack(pady=10)

        # Label para salida
        self.label_salida = ttk.Label(self.frame_prediccion, text="Salida predicha: N/A",
                                      font=("Helvetica", 12, "bold"), foreground="green")
        self.label_salida.pack(pady=5)

        # === FIX: Actualizar scroll después de agregar contenido dinámico ===
        self.root.update_idletasks()
        self.on_frame_configure()

    # === NUEVO: Realizar Predicción ===
    def realizar_prediccion(self):
        features = self.features if self.modelo_cargado else self.obtener_features()
        if not features or self.model is None:
            messagebox.showwarning("Sin modelo", "No hay modelo disponible para predecir.")
            return

        # Recopilar valores
        valores = []
        for feat in features:
            valor_str = self.entries_prediccion[feat].get().strip()
            try:
                valor = float(valor_str)
                valores.append(valor)
            except ValueError:
                messagebox.showerror("Error de Entrada", f"Valor inválido para '{feat}': debe ser un número.")
                return

        if len(valores) != len(features):
            messagebox.showerror("Error de Entrada", "Por favor, ingrese todos los valores de entrada.")
            return

        try:
            # Predecir
            X_pred = np.array(valores).reshape(1, -1)
            y_pred = self.model.predict(X_pred)[0]

            # Mostrar salida
            self.label_salida.config(text=f"{self.target} predicha: {y_pred:.4f}")
            self.mostrar_mensaje(f"Predicción realizada: {y_pred:.4f}")

        except Exception as e:
            messagebox.showerror("Error en Predicción", f"Error al calcular: {str(e)}")
            self.mostrar_mensaje(f"Error en predicción: {str(e)}")

    # === PASO 1: Carga de Datos ===
    def crear_paso_carga(self):
        
        frame = ttk.Frame(self.content_frame)
        self.frames_pasos.append(frame)
        
        # Botón Abrir Archivo
        self.btn_abrir = ttk.Button(frame, 
<<<<<<< HEAD
                                    text="Cargar Archivo de Datos", 
                                    command=lambda: self.ejecutar_con_carga(
                                        self.cargar_archivo,
                                        "Cargando archivo..."))
=======
         text="Cargar Archivo de Datos", 
         command=lambda: self.ejecutar_con_carga
         (self.cargar_archivo, "Cargando archivo..."))
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
        self.btn_abrir.pack(pady=10)
        
        # Etiqueta Ruta
        self.label_ruta = ttk.Label(frame, 
<<<<<<< HEAD
                                    text="Ruta: Ningún archivo seleccionado", 
                                    foreground="gray")
=======
        text="Ruta: Ningún archivo seleccionado", foreground="gray")
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
        self.label_ruta.pack(pady=5)

        # Tabla de Previsualización
        frame_tabla = ttk.Frame(frame)
        frame_tabla.pack(pady=10, fill="both", expand=True)
        
        self.tabla = ttk.Treeview(frame_tabla, show="headings")
<<<<<<< HEAD
        scroll_y = ttk.Scrollbar(frame_tabla, 
                                 orient="vertical", 
                                 command=self.tabla.yview)
        scroll_x = ttk.Scrollbar(frame_tabla,
                                  orient="horizontal",
                                    command=self.tabla.xview)
=======
        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical",
                                  command=self.tabla.yview)
        scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal",
                                  command=self.tabla.xview)
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
        self.tabla.configure(yscrollcommand=scroll_y.set,
                              xscrollcommand=scroll_x.set)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tabla.pack(fill="both", expand=True)

<<<<<<< HEAD
    # === PASO 2 UNIFICADO: Configuración Completa ===
    def crear_paso_configuracion(self):
=======
    # === PASO 2: Selección de Variables ===
    def crear_paso_seleccion(self):

>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
        frame = ttk.Frame(self.content_frame)
        self.frames_pasos.append(frame)
        
        # Contenedor principal con un poco de margen interno
        main_layout = ttk.Frame(frame)
        main_layout.pack(fill="both", expand=True, padx=20, pady=10)

<<<<<<< HEAD
        # === ZONA 1: SELECCIÓN (Arriba, ocupa más espacio) ===
        lbl_sel = ttk.LabelFrame(main_layout,
            text=" 1. Selección de Variables (Obligatorio)", padding=10)
        lbl_sel.pack(side="top", fill="both", expand=True, pady=(0, 10))
        
        # Grid para poner features a la izquierda y target a la derecha
        lbl_sel.columnconfigure(0, weight=1)
        lbl_sel.columnconfigure(1, weight=1)
        lbl_sel.rowconfigure(1, weight=1)

        ttk.Label(lbl_sel, 
                  text="Variables para predecir (Features):",
                    font=("bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(lbl_sel, 
                  text="Variable a adivinar (Target):",
                    font=("bold")).grid(row=0, column=1, sticky="w")

        self.listbox_features = tk.Listbox(lbl_sel, 
                                           selectmode="multiple", 
                                           exportselection=False, height=6)
        self.listbox_features.grid(row=1, column=0, 
                                   sticky="nsew", padx=(0, 5), pady=5)
=======
        # Columnas de Entrada (Features)
        frame_izq = ttk.LabelFrame(frame_sel, 
                                   text="Variables Predictoras (Features)")
        frame_izq.pack(side="left", fill="both", expand=True, padx=5)
        self.listbox_features = tk.Listbox(frame_izq, selectmode="multiple",
                                            exportselection=False)
        self.listbox_features.pack(fill="both", expand=True, padx=5, pady=5)
        # Bind para actualizar estado del botón siguiente
        self.listbox_features.bind("<<ListboxSelect>>", lambda e: 
                                   self.actualizar_estado_navegacion())

        # Columna de Salida (Target)
        frame_der = ttk.LabelFrame(frame_sel,
                                    text="Variable Objetivo (Target)")
        frame_der.pack(side="right", fill="both", expand=True, padx=5)
        self.listbox_target = tk.Listbox(frame_der, exportselection=False)
        self.listbox_target.pack(fill="both", expand=True, padx=5, pady=5)
        # Bind para actualizar estado del botón siguiente
        self.listbox_target.bind("<<ListboxSelect>>", lambda e:
                                  self.actualizar_estado_navegacion())

    # === PASO 3: Preprocesamiento ===
    def crear_paso_preprocesado(self):

        frame = ttk.Frame(self.content_frame)
        self.frames_pasos.append(frame)
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
        
        self.listbox_target = tk.Listbox(lbl_sel, 
                                         exportselection=False, height=6)
        self.listbox_target.grid(row=1, column=1, 
                                 sticky="nsew", padx=(5, 0), pady=5)

        # === ZONA 2: CONFIGURACIÓN TÉCNICA (Abajo) ===
        bottom_panel = ttk.Frame(main_layout)
        bottom_panel.pack(side="bottom", fill="x")

        # -- Limpieza --
        lbl_clean = ttk.LabelFrame(bottom_panel, 
                                   text=" 2. Limpieza de Vacíos ", padding=10)
        lbl_clean.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
<<<<<<< HEAD
        ttk.Radiobutton(lbl_clean, text="Eliminar filas", 
                        variable=self.metodo_var, value="eliminar").pack(anchor="w")
        ttk.Radiobutton(lbl_clean, text="Rellenar (Media)", 
                        variable=self.metodo_var, value="media").pack(anchor="w")
        
        f_const = ttk.Frame(lbl_clean)
        f_const.pack(anchor="w", pady=2)
        ttk.Radiobutton(f_const, text="Valor fijo:", 
                        variable=self.metodo_var, value="constante").pack(side="left")
        self.entry_constante = ttk.Entry(f_const, width=6)
        self.entry_constante.pack(side="left", padx=5)

        # -- División --
        lbl_split = ttk.LabelFrame(bottom_panel, 
                                   text=" 3. Tamaño del Test ", padding=10)
        lbl_split.pack(side="right",
                        fill="both", expand=True, padx=(5, 0))
        
        ttk.Label(lbl_split, 
                  text="¿Cuánto separar para probar?").pack(pady=(0, 5))
        
        f_slider = ttk.Frame(lbl_split)
        f_slider.pack(fill="x")
        self.label_split_pct = ttk.Label(f_slider, text="20 %", width=6)
        self.label_split_pct.pack(side="right")
        
        self.slider_split = ttk.Scale(f_slider, from_=5, to=50,
                                      variable=self.test_split_var, 
                                      command=lambda v: 
                                      self.label_split_pct.config(
                                          text=f"{float(v):.0f} %"))
        self.slider_split.pack(side="left", fill="x", expand=True)
=======
        ttk.Radiobutton(frame_opts, text="Eliminar filas con nulos", 
            variable=self.metodo_var,
            value="eliminar").pack(anchor="w", padx=10, pady=5)
        ttk.Radiobutton(frame_opts, text="Rellenar con Media",
            variable=self.metodo_var, 
            value="media").pack(anchor="w", padx=10, pady=5)
        ttk.Radiobutton(frame_opts, text="Rellenar con Mediana", 
            variable=self.metodo_var, 
            value="mediana").pack(anchor="w", padx=10, pady=5)
        
        # Opción Constante
        f_const = ttk.Frame(frame_opts)
        f_const.pack(anchor="w", padx=10, pady=5)
        ttk.Radiobutton(f_const, text="Rellenar con Valor:",
            variable=self.metodo_var, value="constante").pack(side="left")
        self.entry_constante = ttk.Entry(f_const, width=10)
        self.entry_constante.pack(side="left", padx=5)

        self.btn_procesar = ttk.Button(frame, text="Aplicar Preprocesamiento",
            command=lambda: self.ejecutar_con_carga(self.aplicar_preprocesado,
                                                 "Procesando datos..."))
        self.btn_procesar.pack(pady=20)
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)

        # === BOTÓN DE ACCIÓN ===
        self.btn_procesar_todo = ttk.Button(frame, 
            text="APLICAR CONFIGURACIÓN Y PREPARAR MODELO", 
            command=lambda: self.ejecutar_con_carga(self.procesar_todo_en_uno,
                                                     "Procesando..."))
        self.btn_procesar_todo.pack(fill="x", padx=30, pady=20)

    def procesar_todo_en_uno(self):
        # 1. Validar Selección
        features = self.obtener_features()
        target = self.obtener_target()
        
<<<<<<< HEAD
        if not features or not target:
            messagebox.showwarning("Faltan datos", 
                                   "Por favor selecciona Features y Target.")
            return

        # 2. Aplicar Preprocesamiento (Copiado de tu lógica anterior)
        try:
            metodo = self.metodo_var.get()
            valor = self.entry_constante.get().strip()
            valor_constante = float(valor) if valor else None
            
            columnas_modelo = features + [target]
            df_temp = self.df.copy()
            
            # Llamada a tu función importada
            self.df_procesado = preprocesar_datos(df_temp, 
                                                  metodo, 
                                                  columnas_modelo,
                                                  valor_constante)
            
        except Exception as e:
            raise Exception(f"Error en Limpieza: {e}")

        # 3. Aplicar División (Copiado de tu lógica anterior)
        try:
            if len(self.df_procesado) < 5:
                raise Exception("Datos insuficientes tras la limpieza.")
                
            test_size = self.test_split_var.get() / 100.0
            seed = int(self.seed_var.get()) if self.seed_var.get().isdigit() else 42
            
            X = self.df_procesado[features]
            y = self.df_procesado[target]
            
            self.X_train, self.X_test, \
            self.y_train, self.y_test = train_test_split(
                X, y, test_size=test_size, random_state=seed
            )
            
            # ÉXITO TOTAL
            self.division_realizada = True  # Usamos este flag como "Todo listo"
            self.actualizar_estado_navegacion()
            self.mostrar_mensaje(f"Proceso completo. Train: {len(self.X_train)} | Test: {len(self.X_test)}")
            messagebox.showinfo("Éxito", 
                "Datos procesados y divididos.\nPuedes avanzar.")
            
        except Exception as e:
            raise Exception(f"Error en División: {e}")

    # === PASO 3: Creación y Evaluación del Modelo ===
=======
        frame_div = ttk.LabelFrame(frame,
        text="Configuración de Entrenamiento/Test")
        frame_div.pack(pady=20, padx=20, fill="x")
        
        # Slider Porcentaje
        f_slider = ttk.Frame(frame_div)
        f_slider.pack(fill="x", padx=10, pady=10)
        ttk.Label(f_slider, text="Tamaño Test (%):").pack(side="left")
        
        def actualizar_label_split(valor):

            self.label_split_pct.config(text=f"{float(valor):.1f} %")
            
        self.slider_split = ttk.Scale(f_slider, from_=5.0, to=50.0,
            orient="horizontal", variable=self.test_split_var,
            command=actualizar_label_split)
        self.slider_split.pack(side="left", fill="x", expand=True, padx=10)
        self.label_split_pct = ttk.Label(f_slider, text="20.0 %")
        self.label_split_pct.pack(side="left")

        # Semilla
        f_seed = ttk.Frame(frame_div)
        f_seed.pack(fill="x", padx=10, pady=10)
        ttk.Label(f_seed, text="Semilla Aleatoria:").pack(side="left")
        self.entry_seed = ttk.Entry(f_seed, textvariable=self.seed_var,
                                     width=10)
        self.entry_seed.pack(side="left", padx=10)

        self.btn_dividir = ttk.Button(frame, text="Dividir Datos", 
            command=lambda: self.ejecutar_con_carga(self.aplicar_division,
                                                     "Dividiendo datos..."))
        self.btn_dividir.pack(pady=20)

    # === PASO 5: Creación y Evaluación del Modelo ===
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
    def crear_paso_modelo(self):

        frame = ttk.Frame(self.content_frame)
        self.frames_pasos.append(frame)
        
        # División: Controles (Izq) vs Resultados (Der)
        paned = ttk.PanedWindow(frame, orient="horizontal")
        paned.pack(fill="both", expand=True)
        
        self.frame_left = ttk.Frame(paned)  # <-- MODIFICADO: self para acceder
        frame_right = ttk.Frame(paned)
        paned.add(self.frame_left, weight=1)
        paned.add(frame_right, weight=3)

        # Controles
<<<<<<< HEAD
        self.btn_crear_modelo = ttk.Button(self.frame_left, text="Crear Modelo",
=======
<<<<<<< HEAD
        self.btn_crear_modelo = ttk.Button(frame_left, text="Crear Modelo",
>>>>>>> 67a6751 (revision de codigo y aplicar PEP 8)
                                        command=lambda: 
                                        self.ejecutar_con_carga(
                                            self.crear_modelo,
                                            "Creando modelo..."))
=======
        self.btn_crear_modelo = ttk.Button(frame_left,
            text="Entrenar Modelo", command=lambda: 
            self.ejecutar_con_carga(self.crear_modelo, "Entrenando modelo.."))
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
        self.btn_crear_modelo.pack(pady=20, padx=10, fill="x")
        
        # Botón Guardar Modelo
<<<<<<< HEAD
        self.btn_guardar_modelo = ttk.Button(self.frame_left,
=======
        self.btn_guardar_modelo = ttk.Button(frame_left,
<<<<<<< HEAD
>>>>>>> 67a6751 (revision de codigo y aplicar PEP 8)
                                            text="Guardar Modelo",
                                            command=self.guardar_modelo,
                                            state="disabled")
=======
            text="Guardar Modelo", 
            command=self.guardar_modelo, state="disabled")
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
        self.btn_guardar_modelo.pack(pady=10, padx=10, fill="x")

        # Descripción
        lbl_desc = ttk.Label(self.frame_left, text="Descripción (Opcional):")
        lbl_desc.pack(pady=(20, 5), padx=10, anchor="w")
<<<<<<< HEAD
        self.text_descripcion = tk.Text(self.frame_left, height=10, width=20,
=======
<<<<<<< HEAD
        self.text_descripcion = tk.Text(frame_left, height=10, width=20,
>>>>>>> 67a6751 (revision de codigo y aplicar PEP 8)
                                        font=("Segoe UI", 10),
                                        bd=1, relief="solid")
=======
        self.text_descripcion = tk.Text(frame_left, height=10, width=20, 
            font=("Segoe UI", 10), bd=1, relief="solid")
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
        self.text_descripcion.pack(pady=5, padx=10, fill="both", expand=True)

        # === NUEVO: Frame para Predicción (se creará dinámicamente) ===
        # Se inicializa en None, se crea al tener modelo

        # Resultados (Gráfico y Métricas)
        self.frame_plot = ttk.Frame(frame_right, relief="sunken")
        self.frame_plot.pack(fill="both", expand=True, padx=10, pady=10)
        ttk.Label(self.frame_plot,
<<<<<<< HEAD
                  text="El gráfico aparecerá aquí").pack(expand=True)
        
        self.label_formula = ttk.Label(frame_right, text="Fórmula: -",
                                        wraplength=500)
=======
            text="El gráfico aparecerá aquí").pack(expand=True)
        
        self.label_formula = ttk.Label(frame_right, 
                                       text="Fórmula: -", wraplength=500)
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
        self.label_formula.pack(fill="x", padx=10)
        
        self.label_metrics = ttk.Label(frame_right, text="Métricas: -")
        self.label_metrics.pack(fill="x", padx=10, pady=10)

    # === (Mostrar/Ocultar Frames) ===
    def mostrar_paso(self, indice):
        # Ocultar todos
        for f in self.frames_pasos:
            f.pack_forget()
        
        # Mostrar el actual
        if 0 <= indice < len(self.frames_pasos):
            self.frames_pasos[indice].pack(fill="both", expand=True)
            self.paso_actual = indice
            
            # === FIX: Actualizar scroll con update_idletasks y reconfig ===
            self.root.update_idletasks()
            self.content_frame.update_idletasks()
            self.scrollable_frame.update_idletasks()
            self.canvas.itemconfig(self.canvas_window, width=self.canvas.winfo_width())
            self.on_frame_configure()
            
            titulos = [
                "Paso 0: Bienvenida",
                "Paso 1: Carga de Datos",
                "Paso 2: Configuración y Procesamiento",  # <--- CAMBIO
                "Paso 3: Creación del Modelo"             # <--- CAMBIO
            ]
            self.header_label.config(text=titulos[indice])
            self.actualizar_estado_navegacion()

    def navegar(self, delta):
<<<<<<< HEAD
        # === MODIFICADO: Bloquear si modelo cargado ===
        if self.modelo_cargado:
            return  # No permitir navegación en modo cargado
=======
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)

        nuevo_paso = self.paso_actual + delta
        if 0 <= nuevo_paso < len(self.frames_pasos):
            self.mostrar_paso(nuevo_paso)

    # === Navegación ===
    def actualizar_estado_navegacion(self):
        # === MODIFICADO: Si cargado, bloquear todo ===
        if self.modelo_cargado:
            self.btn_anterior.config(state="disabled")
            self.btn_siguiente.config(state="disabled")
            return

        # Botón Anterior
        state_ant = "normal" if self.paso_actual > 0 else "disabled"
        self.btn_anterior.config(state=state_ant)

        # Botón Siguiente
        puede_avanzar = False
        
        if self.paso_actual == 0:    # Bienvenida
            puede_avanzar = True
        elif self.paso_actual == 1:  # Carga
            puede_avanzar = self.archivo_cargado
        elif self.paso_actual == 2:  # Configuración (Nuevo paso unificado)
            # Avanzamos solo si se ha ejecutado la división correctamente
            puede_avanzar = self.division_realizada 
        elif self.paso_actual == 3:  # Modelo (Fin)
            self.btn_siguiente.config(text="Finalizar", state="disabled")
            return

        state_sig = "normal" if puede_avanzar else "disabled"
        self.btn_siguiente.config(state=state_sig, text="Siguiente >")

    # === Guardar Modelo ===
    def guardar_modelo(self):
<<<<<<< HEAD
        # === MODIFICADO: Usar features/target cargados si aplica ===
        features = self.features if self.modelo_cargado else self.obtener_features()
        target = self.target if self.modelo_cargado else self.obtener_target()

        if self.model is None:
            messagebox.showwarning("Sin modelo", 
=======

        if self.model is None:
            messagebox.showwarning("Sin modelo",
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
                "Primero debe crear un modelo antes de guardarlo.")
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
            descripcion = self.obtener_descripcion()

            # Si no cargado, recalcular métricas y fórmula
            if not self.modelo_cargado:
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

                metricas_dict = {
                    "train_r2": float(train_r2),
                    "test_r2": float(test_r2),
                    "train_mse": float(train_mse),
                    "test_mse": float(test_mse)
                }
            else:
                # Usar las métricas cargadas
                formula_str = self.label_formula.cget("text").replace("Fórmula: ", "").strip()
                metricas_dict = self.metricas

            # Datos a guardar
            datos_modelo = {
                "modelo": self.model,
                "features": features,
                "target": target,
                "formula": formula_str,
                "descripcion": descripcion,
                "metricas": metricas_dict,
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

    def crear_modelo(self):

        if self.X_train is None or self.y_train is None:
            messagebox.showwarning("Advertencia", 
<<<<<<< HEAD
                "Primero debe dividir los datos " \
                "en conjuntos de entrenamiento y test.")
=======
                "Primero debe dividir los datos" \
                " en conjuntos de entrenamiento y test.")
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
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
            
            # === NUEVO: Habilitar Predicción ===
            self.crear_ui_prediccion()
            
            # Actualizar flag y navegación
            self.modelo_creado = True
            self.actualizar_estado_navegacion()

            # FIX: Actualizar scroll después de crear modelo
            self.root.update_idletasks()
            self.on_frame_configure()

        except Exception as e:
            messagebox.showerror("Error al crear modelo", str(e))
            self.mostrar_mensaje(f"Error: {str(e)}")

    # === Resetear Variables y UI ===
    def resetar_resultados_modelo(self):

        self.model = None
        self.btn_guardar_modelo.config(state="disabled")

        self.label_formula.config(text="Fórmula: N/A")
        self.label_metrics.config(text="Métricas:\n  Train R²: N/A | Test R²: N/A\n  Train MSE: N/A | Test MSE: N/A")
        
        # Limpiar gráfico
        for widget in self.frame_plot.winfo_children():
            widget.destroy()
<<<<<<< HEAD
        ttk.Label(self.frame_plot, 
=======
        ttk.Label(self.frame_plot,
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
            text="El gráfico aparecerá aquí.").pack(padx=10, pady=10)
        
        self.text_descripcion.delete("1.0", tk.END)
        self.descripcion_modelo = ""

        # === NUEVO: Ocultar Predicción ===
        if self.frame_prediccion:
            self.frame_prediccion.pack_forget()
            self.frame_prediccion = None
            self.entries_prediccion.clear()

        # === FIX: Actualizar scroll después de reset ===
        self.root.update_idletasks()
        self.on_frame_configure()

    # === Funcionalidad: Cargar Archivo ===
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
            
            # Actualizar flag y navegación
            self.archivo_cargado = True
            self.actualizar_estado_navegacion()
            
            self.mostrar_mensaje(f"Datos cargados: {self.df.shape[0]} filas, {self.df.shape[1]} columnas.")
            self.mostrar_mensaje(detectar_valores_faltantes(self.df))

            # FIX: Actualizar scroll después de cargar datos
            self.root.update_idletasks()
            self.on_frame_configure()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.mostrar_mensaje(f"Error: {str(e)}")

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
<<<<<<< HEAD
        # === MODIFICADO: Usar cargados si aplica ===
        if self.modelo_cargado:
            return self.features
=======

>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
        seleccion = self.listbox_features.curselection()
        return [self.listbox_features.get(i) for i in seleccion]

    def obtener_target(self):
<<<<<<< HEAD
        # === MODIFICADO: Usar cargado si aplica ===
        if self.modelo_cargado:
            return self.target
=======

>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
        seleccion = self.listbox_target.curselection()
        return self.listbox_target.get(seleccion[0]) if seleccion else None

<<<<<<< HEAD
=======
    def on_frame_configure(self, event=None):

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event=None):

        if self.scrollable_frame_window:
            self.canvas.itemconfig(self.scrollable_frame_window,
<<<<<<< HEAD
                                   width=event.width)
=======
                                    width=event.width)
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)

>>>>>>> 67a6751 (revision de codigo y aplicar PEP 8)
    def actualizar_tabla(self, df):

        self.tabla.delete(*self.tabla.get_children())
        self.tabla["columns"] = list(df.columns)
        for col in df.columns:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120, anchor="center")
        for _, row in df.iterrows():
            self.tabla.insert("", "end", values=[str(v) for v in row])

        # FIX: Actualizar scroll después de actualizar tabla
        self.root.update_idletasks()
        self.on_frame_configure()

    def actualizar_listboxes(self):

        if self.df is None:
            return
        columnas = list(self.df.columns)
        self.listbox_features.delete(0, tk.END)
        self.listbox_target.delete(0, tk.END)
        for col in columnas:
            self.listbox_features.insert(tk.END, col)
            self.listbox_target.insert(tk.END, col)

    # === Funcionalidad: Preprocesamiento ===
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
<<<<<<< HEAD
                raise ValueError("Selecciona mínimo una columna de entrada.")
=======
                raise ValueError("Selecciona al menos una columna de entrada.")
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
            
            self.X_train = self.X_test = self.y_train = self.y_test = None
            self.resetar_resultados_modelo()

            columnas_modelo = features + [target]
            df_temp = self.df.copy()
            df_procesado_parcial = preprocesar_datos(
                df_temp, metodo, columnas_modelo, valor_constante
            )
            self.df_procesado = df_procesado_parcial.copy()

            self.actualizar_tabla(self.df_procesado)
            
            # Actualizar flag y navegación
            self.preprocesado_aplicado = True
            self.actualizar_estado_navegacion()
            
            self.mostrar_mensaje("Preprocesado aplicado correctamente"
            " (solo en columnas del modelo).")
<<<<<<< HEAD
            self.mostrar_mensaje(detectar_valores_faltantes(
                self.df_procesado))
=======
            self.mostrar_mensaje(detectar_valores_faltantes
                                 (self.df_procesado))
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.mostrar_mensaje(f"Error: {str(e)}")

    # === Funcionalidad: División de Datos ===
    def aplicar_division(self):

        if self.df_procesado is None:
<<<<<<< HEAD
            messagebox.showwarning("Advertencia", 
                "Primero debe aplicar el preprocesamiento de datos.")
            return
        if len(self.df_procesado) < 5:
            messagebox.showerror("Error", 
                "No hay suficientes datos para realizar la división"
                " (se requieren al menos 5 filas).")
=======
            messagebox.showwarning("Advertencia",
                "Primero debe aplicar el preprocesamiento de datos.")
            return
        if len(self.df_procesado) < 5:
            messagebox.showerror("Error",
                 "No hay suficientes datos para realizar la división (se requieren al menos 5 filas).")
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
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
<<<<<<< HEAD
                messagebox.showerror("Error", 
=======
                messagebox.showerror("Error",
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
                    "Asegúrese de tener features y target seleccionados.")
                return

            X = self.df_procesado[features]
            y = self.df_procesado[target]

<<<<<<< HEAD
            self.X_train, self.X_test, \
=======
            self.X_train, self.X_test,
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
            self.y_train, self.y_test = train_test_split(
                X, y, test_size=test_size_float, random_state=seed
            )

            msg_total = f"Datos divididos correctamente (Semilla={seed})."
            msg_train = f"Conjunto Entrenamiento: {len(self.X_train)} filas."
            msg_test = f"Conjunto Test: {len(self.X_test)} filas."
            
            # Actualizar flag y navegación
            self.division_realizada = True
            self.actualizar_estado_navegacion()
            
            self.mostrar_mensaje(f"{msg_total}\n{msg_train}\n{msg_test}")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.mostrar_mensaje(f"Error en la división: {str(e)}")

    def actualizar_resultados_modelo(self):
<<<<<<< HEAD
        # === MODIFICADO: Si cargado, no recalcular ===
        if self.modelo_cargado:
            return  # Ya se actualizó en cargar_modelo_existente

=======
        
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
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
            self.label_metrics.config(
                text=f"Métricas: Error al calcular - {e}")

    def actualizar_grafico(self):
        # === FIX: Actualizar scroll después de actualizar gráfico ===
        def update_after_graph():
            self.root.update_idletasks()
            self.on_frame_configure()

        # === MODIFICADO: Si cargado, omitir ===
        if self.modelo_cargado:
            update_after_graph()
            return
        
        if self.canvas_widget:
            try:
                self.canvas_widget.destroy()
            except: pass
            self.canvas_widget = None
        if hasattr(self, 'toolbar_widget') and self.toolbar_widget:
            try:
                self.toolbar_widget.destroy()
            except: pass
            self.toolbar_widget = None
            
        for widget in self.frame_plot.winfo_children():
            widget.destroy()

        features = self.obtener_features()
        target = self.obtener_target()

<<<<<<< HEAD
        if self.model is None or self.X_test is None or self.y_test is None:
=======
        if len(features) > 1:
<<<<<<< HEAD
>>>>>>> 67a6751 (revision de codigo y aplicar PEP 8)
            ttk.Label(self.frame_plot, 
                      text="Gráficos disponibles después de crear el modelo."
                      ).pack(padx=10, pady=10)
<<<<<<< HEAD
            update_after_graph()
=======
=======
            ttk.Label(self.frame_plot,
                text="No se puede graficar: Múltiples features (entradas).\n" \
                "El modelo fue creado, pero no es visualizable en 2D.").pack(padx=10, pady=10)
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
            self.mostrar_mensaje("Gráfico no generado (múltiples features).")
>>>>>>> 67a6751 (revision de codigo y aplicar PEP 8)
            return

        # Calcular predicciones para test
        y_test_pred = self.model.predict(self.X_test)

        try:
<<<<<<< HEAD
            # Figura con dos subplots lado a lado
            fig = Figure(figsize=(10, 4), dpi=120)
            
            # Subplot izquierdo: Gráfico de regresión (solo si una feature)
            ax1 = fig.add_subplot(121)
            if len(features) == 1:
                feature_name = features[0]
                ax1.scatter(self.X_train[feature_name], self.y_train, color='blue',
                            label='Entrenamiento', alpha=0.7)
                ax1.scatter(self.X_test[feature_name], self.y_test, color='red',
                            label='Test', alpha=0.7)

                X_all_series = pd.concat([self.X_train[feature_name], 
                                          self.X_test[feature_name]])
                X_line = np.linspace(X_all_series.min(), X_all_series.max(), 100
                                     ).reshape(-1, 1)
                X_line_df = pd.DataFrame(X_line, columns=[feature_name])
                y_line = self.model.predict(X_line_df)
                
                ax1.plot(X_line, y_line, color='green', linewidth=3,
                         label='Recta de Regresión')
                ax1.set_xlabel(feature_name)
                ax1.set_ylabel(target)
                ax1.set_title("Ajuste del Modelo")
                ax1.legend()
                ax1.grid(True)
            else:
                ax1.text(0.5, 0.5, 'Múltiples features\nNo visualizable en 2D', 
                         ha='center', va='center', transform=ax1.transAxes, fontsize=12)
                ax1.set_title("Gráfico de Regresión")
                ax1.set_xlabel("")
                ax1.set_ylabel("")

            # Subplot derecho: Actual vs Predicho (siempre)
            ax2 = fig.add_subplot(122)
            ax2.scatter(self.y_test, y_test_pred, color='red', alpha=0.7, label='Test Set')
            
            # Línea de predicción perfecta (y = x)
            min_y = min(self.y_test.min(), y_test_pred.min())
            max_y = max(self.y_test.max(), y_test_pred.max())
            ax2.plot([min_y, max_y], [min_y, max_y], 'k--', lw=2, label='Predicción Perfecta')
            
            ax2.set_xlabel('Valor Real (y)')
            ax2.set_ylabel('Valor Predicho (ŷ)')
            ax2.set_title("Conjunto Test: Real vs Predicho")
            ax2.legend()
            ax2.grid(True)
            
=======
            fig = Figure(figsize=(5, 3), dpi=120)
            ax = fig.add_subplot(111)

            feature_name = features[0]
<<<<<<< HEAD
            ax.scatter(self.X_train[feature_name], self.y_train, color='blue',
                        label='Entrenamiento', alpha=0.7)
            ax.scatter(self.X_test[feature_name], self.y_test, color='red',
                        label='Test', alpha=0.7)

            X_all_series = pd.concat([self.X_train[feature_name], 
                                      self.X_test[feature_name]])
            X_line = np.linspace(X_all_series.min(), X_all_series.max(), 100
                                 ).reshape(-1, 1)
            X_line_df = pd.DataFrame(X_line, columns=[feature_name])
            y_line = self.model.predict(X_line_df)
            
            ax.plot(X_line, y_line, color='green', linewidth=3,
                     label='Recta de Regresión')
=======
            ax.scatter(self.X_train[feature_name], self.y_train,
                        color='blue', label='Entrenamiento', alpha=0.7)
            ax.scatter(self.X_test[feature_name], self.y_test, 
                       color='red', label='Test', alpha=0.7)

            X_all_series = pd.concat([self.X_train[feature_name],
                                       self.X_test[feature_name]])
            X_line = np.linspace(X_all_series.min(), 
                                 X_all_series.max(), 100).reshape(-1, 1)
            X_line_df = pd.DataFrame(X_line, columns=[feature_name])
            y_line = self.model.predict(X_line_df)
            
            ax.plot(X_line, y_line, color='green', linewidth=3, 
                label='Recta de Regresión')
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
            ax.set_xlabel(feature_name)
            ax.set_ylabel(target)
            ax.set_title("Regresión Lineal: Ajuste del Modelo")
            ax.legend()
            ax.grid(True)
>>>>>>> 67a6751 (revision de codigo y aplicar PEP 8)
            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.frame_plot)
            self.canvas_widget = canvas.get_tk_widget()
            self.canvas_widget.pack(fill='both', expand=True)

            toolbar = NavigationToolbar2Tk(canvas, self.frame_plot)
            toolbar.update()
            self.toolbar_widget = toolbar
            self.toolbar_widget.pack(side='bottom', fill='x')
            canvas.draw()
            
            self.mostrar_mensaje("Gráficos actualizados: Ajuste del modelo y Real vs Predicho.")
            
            update_after_graph()
            
        except Exception as e:
            ttk.Label(self.frame_plot, 
<<<<<<< HEAD
                      text=f"Error al generar gráficos: {e}"
=======
<<<<<<< HEAD
                      text=f"Error al generar gráfico: {e}"
>>>>>>> 67a6751 (revision de codigo y aplicar PEP 8)
                      ).pack(padx=10, pady=10)
=======
                text=f"Error al generar gráfico: {e}").pack(padx=10, pady=10)
>>>>>>> b745d1f (revision de codigo y aplicar PEP 8)
            self.mostrar_mensaje(f"Error al graficar: {e}")
            update_after_graph()

# === INICIO DE LA APLICACIÓN ===
if __name__ == "__main__":
    root = tk.Tk()
    app = AppPrincipal(root)
    root.mainloop()