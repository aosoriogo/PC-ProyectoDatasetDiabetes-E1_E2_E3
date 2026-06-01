import os

import analisis as util
import interfaz as cli


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




#funcion principal
def app():
    while True:
        #verificando que haya un dataset cargado, si no lo hay obliga a cargar uno si lo hay muestra el menu
        if dataset == None or len(dataset)<=1:
            opcion = 1
        else:
            opcion = cli.menu_interactivo()

        #Toma la opcion seleccionada en el menu y corre la funcion correspondien
        match opcion:
            case 1:
                cargar_dataset_completo() # extendida para implementar la funcion de carga de archivo guardado 
                resumen_dataset() # Funcion opcional entrega 2
            case 2:
                buscar()
            case 3:
                estadisticas_basicas()
            case 4:
                filtro()
            case 5:
                visualizar_historial()
            case 6:
                print("Elegiste SALIR DEL PROGRAMA")
                break
            case 'e':
                print("Error: Solo se aceptan valores numericos")
            case _:
                print("Opción no válida. Intenta nuevamente.")


from PyQt5.QtWidgets import QApplication
from interfaz import VentanaPrincipal
import sys

if __name__ == '__main__':
    app_qt = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app_qt.exec_())