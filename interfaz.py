import tkinter as tk
from tkinter import messagebox

def mostrar_mensaje():
    texto =entrada.get()
    messagebox.showinfo("Mensaje", f"Has escrito:{texto}")
ventana = tk.Tk()
ventana.title("Prueba de Interfaz Gráfica")
entrada=tk.Entry(ventana)

boton = tk.Button(ventana, text="Mostrar mensaje", command= mostrar_mensaje)
boton.pack(pady=10)

ventana.mainloop()
