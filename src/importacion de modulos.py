import pandas as pd
import sqlite3
import os

def importar_datos(ruta_archivo):
    """
    Importa datos desde un archivo CSV, Excel o base de datos SQLite.
    Muestra las primeras filas para confirmar la carga.
    """
    if not os.path.exists(ruta_archivo):
        print("Error: El archivo no existe.")
        return None

    extension = os.path.splitext(ruta_archivo)[1].lower()

    try:
        if extension == '.csv':
            print("Cargando datos desde archivo CSV...")
            df = pd.read_csv(ruta_archivo)

        elif extension in ['.xlsx', '.xls']:
            print("Cargando datos desde archivo Excel...")
            df = pd.read_excel(ruta_archivo)

        elif extension in ['.sqlite', '.db']:
            print("Cargando datos desde base de datos SQLite...")
            conn = sqlite3.connect(ruta_archivo)

            # Obtener el nombre de la tabla (asumiendo que solo hay una)
            tablas = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
            if tablas.empty:
                print("Error: No se encontró ninguna tabla en la base de datos.")
                return None

            nombre_tabla = tablas['name'][0]
            df = pd.read_sql_query(f"SELECT * FROM {nombre_tabla}", conn)
            conn.close()

        else:
            print("Error: Formato de archivo inválido.")
            return None

        # Mostrar vista previa
        print("\n Datos cargados correctamente. Vista previa:")
        print(df.head())

        # Mostrar tipos de datos detectados
        print("\n Tipos de datos detectados:")
        print(df.dtypes)

        return df

    except ValueError as e:
        print(f" Error de formato o conversión: {e}")
    except sqlite3.DatabaseError as e:
        print(f" Error en la base de datos SQLite: {e}")
    except Exception as e:
        print(f" Ocurrió un error inesperado: {e}")

    return None


# === Ejemplo de uso ===
if __name__ == "__main__":
    # Cambia esta ruta por el archivo que quieras probar
    rutas = [
        "C:/Users/Elena/Documents/UDC/2IA/Software/Repositorio-q/docs/housing.csv",
        "C:/Users/Elena/Documents/UDC/2IA/Software/Repositorio-q/docs/housing.xlsx",
        "C:/Users/Elena/Documents/UDC/2IA/Software/Repositorio-q/docs/housing.db"
    ]

    for ruta in rutas:
        print("\n" + "="*80)
        importar_datos(ruta)
