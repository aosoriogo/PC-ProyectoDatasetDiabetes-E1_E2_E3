# MIGRACIÓN DE CARGA A PANDAS
import os
import pandas as pd

RUTA_DATASET = "Data\\diabetes_COMPLETO.csv"
RUTA_HISTORIAL = "resultados\\historial.csv"
DIR_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATASET_PRINCIPAL = os.path.join(DIR_RAIZ, RUTA_DATASET)
DIR_AUXILIARES = os.path.join(DIR_RAIZ, "resultados")

def cargar_csv(ruta):  # Carga un archivo CSV y retorna un DataFrame.
    try:
        df = pd.read_csv(ruta)
        print("Archivo CSV cargado correctamente.")
        return 0, df

    except FileNotFoundError:
        print("Error: el archivo no fue encontrado.")
        return 1, "Error: el archivo no fue encontrado."

    except Exception as e:
        print(f"Error al cargar el archivo CSV: {e}")
        return 1, f"Error al cargar el archivo CSV: {e}"
    
def cargar_historial():  # Carga el archivo CSV del historial y retorna un DataFrame.
    try:
        df = pd.read_csv(os.path.join(DIR_RAIZ, RUTA_HISTORIAL))
        print("Archivo CSV cargado correctamente.")
        return 0, df

    except FileNotFoundError:
        print("Error: el archivo no fue encontrado.")
        return 1, "Error: el Historial no fue encontrado."

    except Exception as e:
        print(f"Error al cargar el archivo CSV: {e}")
        return 1, f"Error al cargar el archivo CSV: {e}"

def cargar_json(ruta):  # Carga un archivo JSON y retorna un DataFrame.
    try:
        df = pd.read_json(ruta)
        print("Archivo JSON cargado correctamente.")
        return 0, df

    except FileNotFoundError:
        print("Error: el archivo JSON no fue encontrado.")
        return 1, "Error: el archivo JSON no fue encontrado."

    except Exception as e:
        print(f"Error al cargar el archivo JSON: {e}")
        return 1, f"Error al cargar el archivo JSON: {e}"

def limpiar_datos(df):  # Limpia duplicados, nulos y espacios innecesarios.
    if df is None:
        print("No hay datos para limpiar.")
        return 1, "No hay datos para limpiar."
    try:
        df = df.drop_duplicates()  # Elimina duplicados
        df = df.dropna()  # Elimina filas vacías
        columnas_texto = df.select_dtypes(include='object').columns  # Selecciona columnas de texto

        for columna in columnas_texto:
            df[columna] = df[columna].astype(str).str.strip()  # Limpia espacios

        print("Datos limpiados correctamente.")
        return 0, df

    except Exception as e:
        print(f"Error al limpiar los datos: {e}")
        return 1, f"Error al limpiar los datos: {e}"

def cargar_y_limpiar(ruta):  # Carga el dataset y luego lo limpia automáticamente.
    status, df = cargar_csv(ruta)

    if df is not None and status == 0:
        status, df = limpiar_datos(df)

        if status == 0:
            return 0, df
        else:
            return 1, df
        
    else:
        return 1, df

def mostrar_info(df):  # Muestra información básica del dataset.
    if df is None:
        print("No hay datos cargados.")
        return 1, "No hay datos cargados."

    print("\n========== INFORMACIÓN DEL DATASET ==========")
    print(df.info())
    print("\n========== PRIMERAS 5 FILAS ==========")
    print(df.head())

def exportar_csv(df, nombre_archivo):  # Exporta un DataFrame a CSV.
    if df is None or len(df)<1:
        print("No hay datos para exportar.")
        return 1, "No hay datos para exportar."

    try:
        archivo = os.path.join(DIR_AUXILIARES, nombre_archivo)
        df.to_csv(archivo, index=False)
        print(f"Archivo exportado correctamente como: {nombre_archivo}")
        return 0, f"Archivo exportado correctamente como: {nombre_archivo}"

    except Exception as e:
        print(f"Error al exportar CSV: {e}")
        return 1, str(f"Error al exportar CSV: {e}")

def exportar_json(df, nombre_archivo):  # Exporta un DataFrame a JSON.
    if df is None:
        print("No hay datos para exportar.")
        return 1, "No hay datos para exportar."

    try:
        df.to_json(nombre_archivo, orient="records", indent=4)
        print(f"Archivo exportado correctamente como: {nombre_archivo}")
        return 0, f"Archivo exportado correctamente como: {nombre_archivo}"

    except Exception as e:
        print(f"Error al exportar JSON: {e}")
        return 1, str(f"Error al exportar JSON: {e}")

def lista_archivos():
    carpeta = os.path.join(DIR_RAIZ, "resultados")
    lista = []

    for j in os.listdir(carpeta):
        if j != "historial.csv" and j != "resumen.json":
            lista.append(j)

    

    if len(lista) >= 1:
        return 0, lista
    else:
        return 1, "No se encontraron archivos para cargar"

# PRUEBA RÁPIDA DEL MÓDULO
# SOLO SE EJECUTA SI SE CORRE archivos.py DIRECTAMENTE

if __name__ == "__main__":

    ARCHIVO_DATASET = "Data\\diabetes_COMPLETO.csv"
    ARCHIVO_CSV = "Data\\diabetes_limpio.csv"
    ARCHIVO_JSON = "Data\\diabetes_limpio.json"

    _, datos = cargar_y_limpiar(os.path.join(DIR_RAIZ, ARCHIVO_DATASET))  # Carga y limpieza de datos

    if datos is not None:
        mostrar_info(datos)  # Muestra información general
        _, _ = exportar_csv(datos, os.path.join(DIR_RAIZ, ARCHIVO_CSV))  # Exporta CSV limpio
        _, _ = exportar_json(datos, os.path.join(DIR_RAIZ, ARCHIVO_JSON))  # Exporta JSON limpio
        print("\nProceso finalizado correctamente.")
