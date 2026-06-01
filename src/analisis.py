
# Aqui se almacenan las funciones que se reusan pero no hacen parte directa de la logica
import datetime as dt
import csv
import json
import os

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd

def buscar_dataframe(df, criterio, exacta=True):

    if exacta:
        try:
            valor = float(criterio)
        except ValueError:
            raise ValueError(
                "La búsqueda exacta requiere un valor numérico."
            )

        mask = (df == valor).any(axis=1)

    else:
        criterio = str(criterio)

        mask = df.astype(str).apply(
            lambda col: col.str.contains(criterio, regex=False, na=False)
        ).any(axis=1)

    return df[mask]

def filtrar_por_valor(df, columna, criterio):
    criterio = float(criterio)

    if columna not in df.columns:
        return 1, f"La columna '{columna}' no existe"

    try:
        resultado = df[df[columna] > criterio].sort_values(by=columna)
    except TypeError:
        return 1, f"No se puede comparar la columna '{columna}' con el criterio {criterio}", None

    filtrados = len(df) - len(resultado)

    return 0, resultado, filtrados

def estadisticas_pandas(datos, columna):
    if datos is None or len(datos) == 0:
        return 1, "Error: Dataset vacío o no cargado."
        
    if columna not in datos.columns:
        return 1, f"Error: La columna '{columna}' no existe."
        
    try:
        lista_filas = datos[columna].values.tolist()
        
        valores_numericos = [
            float(valor) for valor in lista_filas 
            if str(valor).replace('.', '', 1).isdigit() or (isinstance(valor, (int, float)))
        ]

        if len(valores_numericos) > 0:
            # Cálculos estadísticos 
            maximo = max(valores_numericos)
            minimo = min(valores_numericos)
            promedio = round(sum(valores_numericos) / len(valores_numericos), 2)
            contador = len(valores_numericos)
            lineas_reporte = [
                "==================================================",
                f"  REPORTE ESTADÍSTICO DE LA COLUMNA: {columna}",
                "==================================================\n",
                f" · Valor Mínimo: {minimo}",
                f" · Valor Máximo: {maximo}",
                f" · Promedio:     {promedio}\n",
                f" Total de registros válidos procesados: {contador} filas.",
                "=================================================="
            ]
            
            cadena_resultado = "\n".join(lineas_reporte)
            #info_historial = f"Max: {maximo} | Min: {minimo} | Prom: {promedio} | Cant: {contador}"
            #guardar_historial(3, columna, info_historial)
            
            return 0, cadena_resultado
        else:
            return 1, f"La columna '{columna}' no contiene datos numéricos válidos."
            
    except Exception as e:
        return 1, f"Error en la comprensión de listas o join: {e}"



def estadisticas_basicas():
    '''imprime el valor maximo, minimo y promedio de la columna seleccionada'''

    global dataset

    maximo = None
    minimo = None
    suma = 0
    contador = 0

    print("\nElegiste ESTADÍSTICAS BÁSICAS\n")

    columna = cli.menu_estadisticas()

    for fila in dataset:
        try:
            valor = float(fila[columna])
        except:
            continue

        if maximo is None or valor > maximo:
            maximo = valor
        if minimo is None or valor < minimo:
            minimo = valor 

        suma += valor 
        contador += 1

    if contador > 0:
        promedio = suma/contador
        print(f"Máximo: {maximo} · Mínimo: {minimo} · Promedio: {round(promedio,1)}")
    else:
        print("No hay datos en la columna")

    util.guardar_historial(3,columna,f"Maximo: {maximo} | media: {promedio} | minimo: {minimo} | {contador}")



def visualizar_historial():
    """ 
     Lee el archivo del historial y lo imprime formateado 
     (funcion obligatoria Entrega 2) 
    """

    with open(os.path.join(DIR_RAIZ, RUTA_HISTORIAL), mode='r', encoding='utf-8') as archivo:
        datos = csv.reader(archivo, delimiter=",")
        cli.imprimir_historial(datos)
        return True
    
def resumen_dataset(datos):

    if len(datos)<2:
        print("Error: dataset muy corto para calcular resumen")
        return 1, "Error: dataset muy corto para calcular resumen"
    
    try:
        resumen = datos.agg(['min', 'max', 'mean']).T
        return 0, resumen
    except Exception as e:
        return 1, f"Fallo analisis del dataset: {e}"


def guardar_historial(opcion: int, valor, resultados):
    
    
    match opcion:
        case 1:
            t = 'Cargar dataset'
        case 2:
            t = 'Buscar coincidencia'
        case 3:
            t = 'Estadisticas basicas'
        case 4:
            t = 'Filtrar por'
        case 5:
            t = 'Seleccion dataset'
        case _:
            raise ValueError("Opcion no definida")
    

    resultados = str(resultados) + " resultados"
    
    cadena = [dt.datetime.now().strftime("%Y-%m-%d %H:%M"), t, valor, resultados]

    with open(os.path.join(DIR, "resultados/historial.csv"), mode='a', encoding='utf-8') as hist:

        guardar = csv.writer(hist, delimiter=",")
        guardar.writerow(cadena)

def guardar_dataset(datos):
    while True:
        archivo = input("Digite el nombre del archivo a guardar sin extension: ")
        if "." in archivo:
            print("No utilice puntos ni caracteres especiales")
            continue
        else:
            archivo += ".csv"
            ruta = os.path.join(DIR, f"resultados\\{archivo}")
            with open(ruta, mode='w', newline='', encoding='utf-8') as busqueda:
                headers = list(datos[0].keys())
                #print(headers) #Linea de prueba
                wr = csv.DictWriter(busqueda, headers, delimiter=",")
                wr.writeheader()
                wr.writerows(datos)
                return True
        return False

def guardar_stadisticas_dataset(datos):
    ruta = os.path.join(DIR, f"resultados\\resumen.json")
    
    with open(ruta, 'w', encoding='utf-8') as aw:
        json.dump(datos, aw, indent=4)
        