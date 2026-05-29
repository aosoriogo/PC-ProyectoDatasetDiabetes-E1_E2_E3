
# Aqui se almacenan las funciones que se reusan pero no hacen parte directa de la logica
import datetime as dt
import csv
import json
import os

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#Funciones de la logica del programa
def cargar_dataset_completo():
    """
    Permite al usuario seleccionar un dataset entre el original y una busqueda guardada previamente
    y lo carga como una lista de diccionarios
    """
    global dataset
    dataset.clear()

    a = cli.selecionar_dataset()
    if a == 1:
        ruta = os.path.join(DIR_RAIZ, RUTA_DATASET)
    else:
        carpeta = os.path.join(DIR_RAIZ, "resultados")
        print("\n\nLista de archivos guardados: ")
        for j in os.listdir(carpeta):
            print(f"\t{j}")
        
        archivo = input("Digite nombre del archivo sin extension: ")
        if archivo == "historial":
            print("Acceso denegado, elija otro archivo")
            return False
        archivo += ".csv"
        ruta = os.path.join(carpeta, archivo)
        

    try:
        with open(ruta, mode='r', encoding='utf-8') as archivo:
            # DictReader convierte cada fila en un diccionario
            lector = csv.DictReader(archivo)
            for fila in lector:
                for campo in ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]:
                    fila[campo] = float(fila[campo]) if fila[campo] else 0

                fila["Outcome"] = int(fila["Outcome"]) if fila["Outcome"] else 0
                dataset.append(fila)
        
        cli.imprimir_dataset(dataset)
        print(f"Carga exitosa: {len(dataset)} registros.")
        util.guardar_historial(5,ruta.split("\\")[-1],len(dataset))

        return True
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo en la ruta: {ruta}")
        return []
    except Exception as err:
        print(f"Error carga dataset: {err}")
        return []
    
def buscar():
    '''
        busca un valor en el dataset e imprime todas las columnas que lo contienen junto con la cantidad de veces que se encontro
        permite elegir si buscar coincidencias exactas o cualquier coincidencia
    '''

    global dataset

    #tomar entradas del usuario
    busqueda = []
    print("\nElegiste BUSCAR\n")

    a = input("digite criterio busqueda: ")
    b = input("digite 1 para busqueda exacta y 2 para busqueda extendida: ")
    
    #realizar busquedas y agregar coincidencias a nueva lista
    if b == "1": 
        for linea in dataset:
            for celda in linea.values():
                try:
                    if float(a) == float(celda):
                        busqueda.append(linea)
                        break
                except:
                    print("Fila erronea, pasando a la siguiente")
                    continue
    else:
        for linea2 in dataset:
            w = [str(v) for v in linea2.values()]
            r = " ".join(w)

            if a in r:
                busqueda.append(linea2)

    
    #Imprimir resultados y numero de coincidencias totales
    if len(busqueda) == 0:
        print("\nNo se encontraron coincidencias\n")
        return
    
    print(f"\nSe encontraron {len(busqueda)} resultados\n") 
    cli.imprimir_dataset(busqueda)

    util.guardar_historial(2, a, len(busqueda))
    cli.save_dataset(busqueda)

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
    
def resumen_dataset():
    global dataset

    if len(dataset)<2:
        print("Error: dataset muy corto para calcular resumen")
        return False

    cols = list(dataset[0].keys())
    externo = dict()

    for dato in cols:
        max = None
        min = None
        cont = 0
        acum = 0
        for fila in dataset:
            try:
                x = float(fila[dato])

                if  max == None or max < x:
                    max = x 
                if  min == None or min > x:
                    min = x

                acum += x
                cont += 1

            except Exception as e:
                print(f"Saltando fila {e}") #Linea de prueba
                continue

        if cont > 1:
            avg = round(acum/cont,2)

            interno = {'max':max, 'media':avg, 'min':min}
        else:
            interno = {'error': 'columna no computable'}
        externo.update({dato: interno})
    
    cli.imprimir_resumen(externo)
    util.guardar_stadisticas_dataset(externo)


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
        case '2':
            t = 'Pacientes en riesgo'
        case '3':
            t = 'Guardar filtro'
        case '4':
            t = 'Cargar resultados'
        case '5':
            t = 'Visualizar historial'
        case '6':
            t = 'Funcionalidad opcional'
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
        