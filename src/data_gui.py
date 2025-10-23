import tkinter as tk
from tkinter import ttk, messagebox
from importacion_de_modulos import importar_datos, seleccionar_archivo
import pandas as pd

class DataGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Importador de Datos")
        self.root.geometry("600x400")  # Tamaño inicial
        
        # Label para mostrar ruta
        self.label_ruta = ttk.Label(root, text="Ruta del archivo: No seleccionado")
        self.label_ruta.pack(pady=10)
        
        # Botón para cargar archivo
        self.btn_cargar = ttk.Button(root, text="Cargar Archivo", command=self.cargar_datos)
        self.btn_cargar.pack(pady=5)
        
        # Frame para la tabla con scroll
        self.frame_tabla = ttk.Frame(root)
        self.frame_tabla.pack(pady=10, fill="both", expand=True)
        
        # Treeview (tabla) con barras de scroll
        self.tabla = ttk.Treeview(self.frame_tabla, show="headings")
        self.scroll_y = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla.yview)
        self.scroll_x = ttk.Scrollbar(self.frame_tabla, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        
        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")
        self.tabla.pack(fill="both", expand=True)
        
    def cargar_datos(self):
        # Seleccionar archivo con diálogo filtrado
        ruta = seleccionar_archivo()
        if not ruta:
            messagebox.showwarning("Advertencia", "No seleccionaste ningún archivo.")
            return
        
        # Actualizar label con ruta
        self.label_ruta.config(text=f"Ruta del archivo: {ruta}")
        
        try:
            # Importar datos
            df = importar_datos(ruta)
            if df is None or df.empty:
                messagebox.showerror("Error", "No se encontraron datos en el archivo.")
                return
            
            # Limpiar tabla previa
            self.tabla.delete(*self.tabla.get_children())
            self.tabla["columns"] = list(df.columns)
            
            # Configurar encabezados
            for col in df.columns:
                self.tabla.heading(col, text=col)
                self.tabla.column(col, width=100, anchor="center")
            
            # Insertar todas las filas
            for _, row in df.iterrows():
                self.tabla.insert("", "end", values=list(row))
            
            messagebox.showinfo("Éxito", "Datos cargados correctamente.")
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")

def main():
    root = tk.Tk()
    app = DataGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()