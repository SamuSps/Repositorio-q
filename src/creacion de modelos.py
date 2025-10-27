import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar, MULTIPLE
import pandas as pd

class CreadorModelosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Creador de Modelos - Selección de Columnas")
        self.data = None
        self.selected_features = []
        self.selected_target = None
        self.setup_ui()

    def setup_ui(self):
        # Etiqueta de bienvenida
        title_label = tk.Label(self.root, text="Selecciona las columnas de entrada y salida para crear tu modelo", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Botón para cargar datos
        load_btn = tk.Button(self.root, text="Cargar Datos (CSV)", command=self.load_data, bg="lightblue", font=("Arial", 10))
        load_btn.pack(pady=5)

        # Frame para selección de features (entrada múltiple)
        feature_frame = tk.LabelFrame(self.root, text="Columnas de Entrada (Features) - Selecciona múltiples", font=("Arial", 10, "bold"))
        feature_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Listbox para features con scrollbar
        list_frame = tk.Frame(feature_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.feature_listbox = Listbox(list_frame, selectmode=MULTIPLE, height=8, font=("Arial", 9))
        scrollbar_f = Scrollbar(list_frame, orient="vertical")
        self.feature_listbox.config(yscrollcommand=scrollbar_f.set)
        scrollbar_f.config(command=self.feature_listbox.yview)

        self.feature_listbox.pack(side="left", fill="both", expand=True)
        scrollbar_f.pack(side="right", fill="y")

        # Instrucción
        feature_label = tk.Label(feature_frame, text="Mantén Ctrl para seleccionar múltiples columnas", font=("Arial", 8, "italic"))
        feature_label.pack()

        # Frame para target (salida única)
        target_frame = tk.LabelFrame(self.root, text="Columna de Salida (Target) - Selecciona una", font=("Arial", 10, "bold"))
        target_frame.pack(pady=10, padx=20, fill="x")

        self.target_var = tk.StringVar()
        self.target_label = tk.Label(target_frame, text="Selecciona la columna de salida:", font=("Arial", 9))
        self.target_label.pack(pady=5)

        self.target_menu = tk.OptionMenu(target_frame, self.target_var, "")
        self.target_menu.config(font=("Arial", 9))
        self.target_menu.pack(pady=5)

        # Botón de confirmación
        confirm_btn = tk.Button(self.root, text="Confirmar Selección", command=self.confirm_selection, bg="lightgreen", font=("Arial", 12, "bold"))
        confirm_btn.pack(pady=20)

    def load_data(self):
        file_path = filedialog.askopenfilename(
            title="Selecciona un archivo CSV",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                columns = list(self.data.columns)

                # Limpiar y poblar listbox de features
                self.feature_listbox.delete(0, tk.END)
                for col in columns:
                    self.feature_listbox.insert(tk.END, col)

                # Limpiar y poblar menú de target
                self.target_menu['menu'].delete(0, 'end')
                self.target_var.set("")
                for col in columns:
                    self.target_menu['menu'].add_command(label=col, command=tk._setit(self.target_var, col))

                messagebox.showinfo("Éxito", f"Datos cargados correctamente. Columnas disponibles: {len(columns)}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")

    def confirm_selection(self):
        if self.data is None:
            messagebox.showerror("Error", "Debe cargar los datos primero.")
            return

        # Obtener features seleccionadas
        selection = self.feature_listbox.curselection()
        if len(selection) == 0:
            messagebox.showerror("Error", "Debe seleccionar al menos una columna de entrada (features).")
            return

        self.selected_features = [self.feature_listbox.get(i) for i in selection]

        # Obtener target
        target = self.target_var.get()
        if not target:
            messagebox.showerror("Error", "Debe seleccionar una columna de salida (target).")
            return

        self.selected_target = target

        # Verificar si target está en features (advertencia opcional)
        if target in self.selected_features:
            if not messagebox.askyesno("Advertencia", "¿Está seguro? La columna de salida está seleccionada como entrada. ¿Continuar?"):
                return

        # Mensaje de éxito
        features_str = ", ".join(self.selected_features)
        messagebox.showinfo(
            "Selección Confirmada",
            f"¡Selecciones registradas exitosamente!\n\n"
            f"Columnas de Entrada (Features):\n{features_str}\n\n"
            f"Columna de Salida (Target):\n{target}\n\n"
            f"Puedes proceder a crear el modelo."
        )

        # Aquí puedes agregar lógica para crear el modelo, por ejemplo:
        # self.crear_modelo()

    def crear_modelo(self):
        # Placeholder: Lógica para entrenar el modelo con las selecciones
        # Por ejemplo, usando scikit-learn (no incluido en el entorno, pero extensible)
        print(f"Creando modelo con features: {self.selected_features}, target: {self.selected_target}")
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = CreadorModelosGUI(root)
    root.mainloop()