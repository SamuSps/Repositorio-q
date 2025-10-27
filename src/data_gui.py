import tkinter as tk
from tkinter import ttk, messagebox
from importacion_de_modulos import importar_datos, seleccionar_archivo, detectar_nans, preprocesar_datos
import pandas as pd

class DataGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Importador de Datos")
        self.root.geometry("600x400")
        self.df = None  # DataFrame actual
        
        # Label para mostrar ruta
        self.label_ruta = ttk.Label(root, text="Ruta del archivo: No seleccionado")
        self.label_ruta.pack(pady=10)
        
        # Botón para cargar archivo
        self.btn_cargar = ttk.Button(root, text="Cargar Archivo", command=self.cargar_datos)
        self.btn_cargar.pack(pady=5)
        
        # Área de texto para NaN
        self.text_nans = tk.Text(root, height=4, width=50)
        self.text_nans.pack(pady=5)
        self.text_nans.config(state="disabled")
        
        # Menú desplegable para método
        self.label_metodo = ttk.Label(root, text="Método de preprocesamiento:")
        self.label_metodo.pack(pady=5)
        self.metodo_var = tk.StringVar(value="eliminar")
        self.metodo_menu = ttk.Combobox(root, textvariable=self.metodo_var, values=["eliminar", "media", "mediana", "constante"], state="readonly")
        self.metodo_menu.pack(pady=5)
        
        # Entrada para valor constante
        self.label_constante = ttk.Label(root, text="Valor constante (si aplica):")
        self.label_constante.pack(pady=5)
        self.entry_constante = ttk.Entry(root)
        self.entry_constante.pack(pady=5)
        
        # Botón para seleccionar columnas (simplificado)
        self.btn_columnas = ttk.Button(root, text="Seleccionar Columnas", command=self.seleccionar_columnas)
        self.btn_columnas.pack(pady=5)
        self.columnas_seleccionadas = None
        
        # Botón para confirmar preprocesamiento
        self.btn_procesar = ttk.Button(root, text="Procesar Datos", command=self.procesar_datos)
        self.btn_procesar.pack(pady=5)
        
        # Frame para tabla con scroll
        self.frame_tabla = ttk.Frame(root)
        self.frame_tabla.pack(pady=10, fill="both", expand=True)
        
        self.tabla = ttk.Treeview(self.frame_tabla, show="headings")
        self.scroll_y = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla.yview)
        self.scroll_x = ttk.Scrollbar(self.frame_tabla, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        
        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")
        self.tabla.pack(fill="both", expand=True)
    
    def cargar_datos(self):
        ruta = seleccionar_archivo()
        if not ruta:
            messagebox.showwarning("Advertencia", "No seleccionaste ningún archivo.")
            return
        
        self.label_ruta.config(text=f"Ruta del archivo: {ruta}")
        
        try:
            self.df = importar_datos(ruta)
            if self.df is None or self.df.empty:
                messagebox.showerror("Error", "No se encontraron datos en el archivo.")
                return
            
            # Mostrar NaN
            self.text_nans.config(state="normal")
            self.text_nans.delete("1.0", tk.END)
            self.text_nans.insert(tk.END, detectar_nans(self.df))
            self.text_nans.config(state="disabled")
            
            # Actualizar tabla
            self.tabla.delete(*self.tabla.get_children())
            self.tabla["columns"] = list(self.df.columns)
            for col in self.df.columns:
                self.tabla.heading(col, text=col)
                self.tabla.column(col, width=100, anchor="center")
            for _, row in self.df.iterrows():
                self.tabla.insert("", "end", values=list(row))
            
            messagebox.showinfo("Éxito", "Datos cargados correctamente.")
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")
    
    def seleccionar_columnas(self):
        # Simplificado: Selecciona todas o ingresa manualmente (puedes mejorar con GUI)
        columnas = list(self.df.columns) if self.df is not None else []
        self.columnas_seleccionadas = columnas  # Por ahora, usa todas
        messagebox.showinfo("Columnas", f"Seleccionadas: {', '.join(columnas)}")
    
    def procesar_datos(self):
        if self.df is None:
            messagebox.showerror("Error", "Carga un archivo primero.")
            return
        
        metodo = self.metodo_var.get()
        valor_constante = self.entry_constante.get() if metodo == "constante" else None
        
        try:
            if metodo == "constante" and not valor_constante:
                raise ValueError("Ingresa un valor constante.")
            df_procesado = preprocesar_datos(self.df, metodo, self.columnas_seleccionadas, valor_constante)
            
            # Actualizar tabla
            self.tabla.delete(*self.tabla.get_children())
            self.tabla["columns"] = list(df_procesado.columns)
            for col in df_procesado.columns:
                self.tabla.heading(col, text=col)
                self.tabla.column(col, width=100, anchor="center")
            for _, row in df_procesado.iterrows():
                self.tabla.insert("", "end", values=list(row))
            
            # Actualizar NaN
            self.text_nans.config(state="normal")
            self.text_nans.delete("1.0", tk.END)
            self.text_nans.insert(tk.END, detectar_nans(df_procesado))
            self.text_nans.config(state="disabled")
            
            self.df = df_procesado  # Actualizar DataFrame
            messagebox.showinfo("Éxito", "Datos preprocesados correctamente.")
        
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

def main():
    root = tk.Tk()
    app = DataGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()