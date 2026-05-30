#NOTA: NO CAMBIAR O BORRAR ESTE ARCHIVO QUE YA NO SE USA (YO LO HAGO AL FINAL)

from tabulate import tabulate
import os

import analisis as util

def menu_interactivo():
    print("\n BIENVENIDOS AL MENÚ INTERACTIVO DE INSULINE_LOGIC!\n")
    print("Ingresa 1 si deseas SELECCIONAR DATASET (permite cargar resultados guardados)")
    print("Ingresa 2 si deseas BUSCAR")
    print("Ingresa 3 si deseas realizar ESTADÍSTICAS BÁSICAS")
    print("Ingresa 4 si deseas FILTRAR POR CONDICIÓN")
    print("Ingresa 5 si deseas VER HISTORIAL DE BUSQUEDAS")
    print("Ingresa 6 si deseas SALIR DEL PROGRAMA")

    try:
        opcion = int(input("\nIngresa una opción (1, 2, 3, 4, 5 o 6): "))
    except:
        return 'e'
    return opcion

def selecionar_dataset():
    while True:
        opcion = input("Digite '1' para cargar dataset principal o '2' para cargar Resultado almacenado: ")
        if opcion == '1':
            return 1
        elif opcion == '2':
            return 2
        else:
            print("Error: Opcion no valida!")

def save_dataset(datos):
    a = input("Digite 1 para guardar el resultado, 0 para volver: ")
    if a == '1':
        if util.guardar_dataset(datos):
            print("\nDatos guardados con exito!\n")
            return
        else:
            print("Error: No se guardaron los datos")
            return
    print("\nSalindo sin guardar\n")

     


def menu_estadisticas():
    while True:
        print("\n--- ESTADÍSTICAS BÁSICAS ---")
        print("Ingrese un número de acuerdo a la columna que desea analizar:")
        print("1: Embarazos")
        print("2: Glucosa")
        print("3: Presión arterial")
        print("4: Grosor de la piel")
        print("5: Insulina")
        print("6: IMC")
        print("7: Función de pedigrí de diabetes")
        print("8: Edad")
        print("9: Resultado")

        try:
            columna=int(input("Elige el número de columna: "))

            match columna:
                case 1:
                    return "Pregnancies"
                case 2:
                    return "Glucose"
                case 3:
                    return "BloodPressure"
                case 4:
                    return "SkinThickness"
                case 5:
                    return "Insulin"
                case 6:
                    return "BMI"
                case 7:
                    return "DiabetesPedigreeFunction"
                case 8:
                    return "Age"
                case 9:
                    return "Outcome"
                case _:
                    print("Digite un numero de columna entre 1 y 8")
        except:
            print("Entrada invalida, solo se aceptan numeros")

def menu_filtro():
    while True:
        print("\n--- ESTADÍSTICAS BÁSICAS ---")
        print("Ingrese un número de acuerdo a la columna que desea analizar:")
        print("1: Embarazos")
        print("2: Glucosa")
        print("3: Presión arterial")
        print("4: Grosor de la piel")
        print("5: Insulina")
        print("6: IMC")
        print("7: Función de pedigrí de diabetes")
        print("8: Edad")
        print("9: Resultado")

        try:
            columna=int(input("Elige el número de columna: "))
            valor_filtro = float(input('Digite desde que valor desea filtrar: '))

            match columna:
                case 1:
                    return "Pregnancies", valor_filtro
                case 2:
                    return "Glucose", valor_filtro
                case 3:
                    return "BloodPressure", valor_filtro
                case 4:
                    return "SkinThickness", valor_filtro
                case 5:
                    return "Insulin", valor_filtro
                case 6:
                    return "BMI", valor_filtro
                case 7:
                    return "DiabetesPedigreeFunction", valor_filtro
                case 8:
                    return "Age", valor_filtro
                case 9:
                    return "Outcome", valor_filtro
                case _:
                    print("Digite un numero de columna entre 1 y 8")

        except:
            print("Entrada invalida, solo se aceptan numeros")
        


def imprimir_dataset(dataset):
    if dataset == None or len(dataset)<1:
        print("Error de data set, por favor cargue un conjunto valido")
        return False
    
    rows = []
    cont = 0

    #print(dataset) #Linea de prueba
    
    for fila in dataset:
        if cont == 0:
            headers = [k[:10] for k in fila.keys()]
        cont += 1

        rows.append(list(fila.values()))
        

    print(tabulate(rows, headers, tablefmt="grid"))
    #print(headers)

    
def imprimir_historial(datos: list):
    headers = ["Fecha", "Funcion", "Valor", "Resultados"]
    datos = list(datos)
    filtrados = [j for j in datos if len(j)>2]
    print(tabulate(filtrados, headers, tablefmt="grid"))


def listar_dir_archivos():
    ruta = os.path.dirname(os.path.abspath(__file__))
    os.listdir(ruta)

def imprimir_resumen(datos):
    print("\n\nResumen dataset cargado: \n")
    for k, v in datos.items():
        print(k, end='=> ')
        for key, val in v.items():
            print(key, ":", val, end=" ! ")
            pass
        
        print()