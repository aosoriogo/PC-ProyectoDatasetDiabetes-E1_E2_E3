# MIGRACIÓN DE CARGA A PANDAS
import pandas as pd

def cargar_csv(ruta):  # Carga un archivo CSV y retorna un DataFrame.
    try:
        df = pd.read_csv(ruta)
        print("Archivo CSV cargado correctamente.")
        return df

    except FileNotFoundError:
        print("Error: el archivo no fue encontrado.")
        return None

    except Exception as e:
        print(f"Error al cargar el archivo CSV: {e}")
        return None

def cargar_json(ruta):  # Carga un archivo JSON y retorna un DataFrame.
    try:
        df = pd.read_json(ruta)
        print("Archivo JSON cargado correctamente.")
        return df

    except FileNotFoundError:
        print("Error: el archivo JSON no fue encontrado.")
        return None

    except Exception as e:
        print(f"Error al cargar el archivo JSON: {e}")
        return None

def limpiar_datos(df):  # Limpia duplicados, nulos y espacios innecesarios.
    if df is None:
        print("No hay datos para limpiar.")
        return None
    try:
        df = df.drop_duplicates()  # Elimina duplicados
        df = df.dropna()  # Elimina filas vacías
        columnas_texto = df.select_dtypes(include='object').columns  # Selecciona columnas de texto

        for columna in columnas_texto:
            df[columna] = df[columna].astype(str).str.strip()  # Limpia espacios

        print("Datos limpiados correctamente.")
        return df

    except Exception as e:
        print(f"Error al limpiar los datos: {e}")
        return None

def cargar_y_limpiar(ruta):  # Carga el dataset y luego lo limpia automáticamente.
    df = cargar_csv(ruta)

    if df is not None:
        df = limpiar_datos(df)
    return df

def mostrar_info(df):  # Muestra información básica del dataset.
    if df is None:
        print("No hay datos cargados.")
        return

    print("\n========== INFORMACIÓN DEL DATASET ==========")
    print(df.info())
    print("\n========== PRIMERAS 5 FILAS ==========")
    print(df.head())

def exportar_csv(df, nombre_archivo):  # Exporta un DataFrame a CSV.
    if df is None:
        print("No hay datos para exportar.")
        return

    try:
        df.to_csv(nombre_archivo, index=False)
        print(f"Archivo exportado correctamente como: {nombre_archivo}")

    except Exception as e:
        print(f"Error al exportar CSV: {e}")

def exportar_json(df, nombre_archivo):  # Exporta un DataFrame a JSON.
    if df is None:
        print("No hay datos para exportar.")
        return

    try:
        df.to_json(nombre_archivo, orient="records", indent=4)
        print(f"Archivo exportado correctamente como: {nombre_archivo}")

    except Exception as e:
        print(f"Error al exportar JSON: {e}")



# PRUEBA RÁPIDA DEL MÓDULO
# SOLO SE EJECUTA SI SE CORRE archivos.py DIRECTAMENTE

if __name__ == "__main__":

    ruta_dataset = "../Data/diabetes_COMPLETO.csv"  # Ruta del dataset completo
    datos = cargar_y_limpiar(ruta_dataset)  # Carga y limpieza de datos

    if datos is not None:
        mostrar_info(datos)  # Muestra información general
        exportar_csv(datos, "../Data/diabetes_limpio.csv")  # Exporta CSV limpio
        exportar_json(datos, "../Data/diabetes_limpio.json")  # Exporta JSON limpio
        print("\nProceso finalizado correctamente.")
