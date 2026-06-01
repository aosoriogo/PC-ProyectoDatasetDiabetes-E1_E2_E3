
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

    if columna not in df.columns:
        return 1, f"La columna '{columna}' no existe"

    resultado = df[df[columna] == criterio].sort_values(by=columna)

    print(f"Se filtraron {len(df) - len(resultado)} resultados")

    return 0, resultado



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

    
def filtro():
    '''
        filtra los datos encontrando los valores de una columna mayores al valor 
        que ingrese el usuario.
    '''

    global dataset

    filtro_l = [] #cambie de filtro a filtro_l para evitar colision en la llamada recursiva

    print("\nElegiste FILTRAR POR CONDICIÓN\n")

    x, y = cli.menu_filtro()

    for fila in dataset:
        try:
            if float(fila[x]) >= y:
                filtro_l.append(fila)
        except:
            continue

    filtro_l.sort(key=lambda a: a[x])

    print(f"\nSe filtraron {len(dataset)-len(filtro_l)} resultados\n\n")
    
    cli.imprimir_dataset(filtro_l)

    util.guardar_historial(4, x, f"mayores a {y}: {len(filtro_l)}")

    if len(filtro_l) > 1:
        cli.save_dataset(filtro_l)


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
    """
    Correcciones realizadas:
        se movio la funcion de main.py a utilidades.py
        se cambio el if-elif-else por un match->case (No es recomendable usar if en cadenas de mas de 3 opciones)
        se agrego un caso por defecto al match->case que levanta un error indicando que no existe ese caso
        se movio la apertura del archivo hasta despues del match->case (El archivo debe abrirse y cerrarce en el menor numero de operaciones posibles)
    """
    
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
        