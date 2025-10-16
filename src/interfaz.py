import tkinter as tk
from tkinter import messagebox, scrolledtext
# Opcional: Integra tu importador (comenta si no lo tienes aún)
# from data_importer import importar_datos, preview_datos

def cargar_datos():
    ruta = entry_ruta.get()  # Obtiene texto del cuadro
    if not ruta:
        messagebox.showerror("Error", "Ingresa una ruta de archivo.")
        return
    
    try:
        # Simulación: Integra aquí tu función real
        # df = importar_datos(ruta)
        # preview = str(df.head(3)) if 'df' in locals() else "Datos cargados: Simulado preview."
        preview = f"Datos simulados de {ruta}:\nID | Nombre | Edad\n1 | Ana | 25\n2 | Bob | 30"
        
        # Muestra mensaje con preview
        messagebox.showinfo("Preview de Datos", preview)
        # Opcional: Inserta en text area abajo
        text_area.insert(tk.END, f"Cargado: {preview}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar: {str(e)}")

# Crear ventana principal
root = tk.Tk()
root.title("Importador de Datos - Prueba GUI")
root.geometry("400x300")  # Tamaño inicial

# Cuadro de texto para ruta
tk.Label(root, text="Ruta del archivo:").pack(pady=10)
entry_ruta = tk.Entry(root, width=50)
entry_ruta.pack(pady=5)

# Botón
btn_cargar = tk.Button(root, text="Cargar Datos", command=cargar_datos)
btn_cargar.pack(pady=10)

# Área de texto para logs (opcional, para más feedback)
text_area = scrolledtext.ScrolledText(root, width=50, height=10)
text_area.pack(pady=10)

# Iniciar loop de eventos
root.mainloop()
