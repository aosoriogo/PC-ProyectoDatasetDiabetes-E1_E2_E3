import sys
import os

from PyQt5.QtWidgets import (QCheckBox, QTextBrowser, QComboBox, QMainWindow, QLineEdit, QMessageBox, QDialog, QWidget, QPushButton, QTextEdit, QLabel, QVBoxLayout, QHBoxLayout, QApplication)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from tabulate import tabulate

import analisis as utils
import archivos


dataset = []
aux = []

#Funciones de interaccion con el usuario
def obtener_dataset():
    dialog = SelectorDataset()

    if dialog.exec_():
        return dialog.status, dialog.resultado

    return 1, "ERROR: fallo la captura del nombre del archivo"

def guardar_dataset():
    dialog = DialogoFiltro()
    if dialog.exec_():
        return dialog.status, dialog.resultado, dialog.filtrados


def resultado_busqueda():
    dialog = DialogoBusqueda()

    if dialog.exec_():
        return dialog.status, dialog.resultado
    return 1, "ERROR: fallo la busqueda"

def resultado_filtro():
    dialog = DialogoFiltro()
    if dialog.exec_():
        return dialog.status, dialog.resultado, dialog.filtrados
    return 1, "Error inesperado en el filtro", None

def resultado_estadisticas():
    dialog = DialogoEstadisticas()

    if dialog.exec_():
        return dialog.status, dialog.resultado
    return 1, "ERROR: fallo las estadisticas"


#FUNCIONES DE VENTANAS EMERGENTES (alertas y preguntas)
class SelectorDataset(QDialog):
    def __init__(self):
        super().__init__()

        self.resultado = None
        self.status = 0

        self.setWindowTitle("Seleccionar Dataset")
        self.resize(600, 250)

        layout = QVBoxLayout(self)

        info = QTextBrowser()
        
        _, lista_de_archivos = archivos.lista_archivos()
        listado = "ARCHIVOS DISPONIBLES:\n\n" + "\n".join(lista_de_archivos)
        info.setPlainText(listado)
        info.setMaximumHeight(200)

        layout.addWidget(info)

        layout.addWidget(QLabel("Nombre o ruta del archivo:"))

        self.txt_archivo = QLineEdit()
        layout.addWidget(self.txt_archivo)

        btn_archivo = QPushButton("Cargar archivo")
        btn_archivo.clicked.connect(self.usar_archivo)
        layout.addWidget(btn_archivo)

        btn_principal = QPushButton("Cargar dataset principal")
        btn_principal.clicked.connect(self.usar_principal)
        layout.addWidget(btn_principal)

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.reject)
        layout.addWidget(btn_cerrar)

    def usar_archivo(self):
        self.resultado = os.path.join(archivos.DIR_AUXILIARES, self.txt_archivo.text().strip())
        self.accept()

    def usar_principal(self):
        self.resultado = archivos.DATASET_PRINCIPAL
        self.accept()

#FUNCIONES DE VENTANAS EMERGENTES (alertas y preguntas)
class DialogoBusqueda(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.df = aux
        self.resultado = None
        self.status = 0

        self.setWindowTitle("Buscar")
        self.setModal(True)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Criterio de búsqueda"))

        self.txt_criterio = QLineEdit()
        layout.addWidget(self.txt_criterio)

        self.chk_exacta = QCheckBox("Búsqueda exacta")
        self.chk_exacta.setChecked(True)
        layout.addWidget(self.chk_exacta)

        botones = QHBoxLayout()

        self.btn_buscar = QPushButton("Buscar")
        self.btn_cancelar = QPushButton("Cancelar")

        botones.addWidget(self.btn_buscar)
        botones.addWidget(self.btn_cancelar)

        layout.addLayout(botones)

        self.setLayout(layout)

        self.btn_buscar.clicked.connect(self.buscar)
        self.btn_cancelar.clicked.connect(self.reject)

    def buscar(self):

        criterio = self.txt_criterio.text().strip()
        if aux == None or len(aux<1):
            self.resultado = "Es neceario realizar primero una busqueda o filtrado"
            self.status = 1
            return

        if not criterio:
            QMessageBox.warning(self, "Error", "Ingrese un criterio de búsqueda")
            self.resultado = "Error, no se ingreso nombre archivo"
            self.status = 1
            return 

        try:
            self.resultado = archivos.exportar_csv(self.df, criterio)
            self.status = 0

            self.accept()

        except Exception as e:
            self.resultado = f"Error: {e}"
            self.status = 1

class DialogoFiltro(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.df = dataset
        self.resultado = None
        self.filtrados = None
        self.status = 0

        self.setWindowTitle("Filtrar datos")
        self.setModal(True)

        layout = QVBoxLayout()

        # --- Selector de columna ---
        layout.addWidget(QLabel("Selecciona la columna"))

        self.combo_columnas = QComboBox()
        self.combo_columnas.addItems(list(self.df.columns))
        layout.addWidget(self.combo_columnas)

        # --- Criterio ---
        layout.addWidget(QLabel("Criterio"))

        self.txt_criterio = QLineEdit()
        layout.addWidget(self.txt_criterio)

        # --- Botones ---
        botones = QHBoxLayout()

        self.btn_ok = QPushButton("Filtrar")
        self.btn_cancel = QPushButton("Cancelar")

        botones.addWidget(self.btn_ok)
        botones.addWidget(self.btn_cancel)

        layout.addLayout(botones)

        self.setLayout(layout)

        # --- eventos ---
        self.btn_ok.clicked.connect(self.filtrar)
        self.btn_cancel.clicked.connect(self.reject)

    def filtrar(self):

        columna = self.combo_columnas.currentText()
        criterio = self.txt_criterio.text().strip()

        if not criterio:
            QMessageBox.warning(self, "Error", "Debe ingresar un criterio")
            self.resultado = "Error: criterio vacío"
            self.status = 1
            return
        else:
            self.status, self.resultado, self.filtrados = utils.filtrar_por_valor(self.df, columna, criterio)
            self.accept()

class DialogoEstadisticas(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        global dataset
        self.df = dataset
        self.resultado = None
        self.status = 0

        self.setWindowTitle("Estadísticas por Columna")
        self.setModal(True)
        self.resize(350, 150)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Selecciona la columna a analizar:"))
        self.combo_columnas = QComboBox()
        self.combo_columnas.addItems(list(self.df.columns) if len(self.df) > 0 else [])
        layout.addWidget(self.combo_columnas)

        botones = QHBoxLayout()
        self.btn_ok = QPushButton("Calcular")
        self.btn_cancel = QPushButton("Cancelar")

        botones.addWidget(self.btn_ok)
        botones.addWidget(self.btn_cancel)
        layout.addLayout(botones)

        self.setLayout(layout)

        self.btn_ok.clicked.connect(self.procesar)
        self.btn_cancel.clicked.connect(self.reject)

    def procesar(self):
        columna = self.combo_columnas.currentText()

        if not columna:
            QMessageBox.warning(self, "Error", "El dataset no posee columnas válidas para operar.")
            self.resultado = "Error: Sin columnas válidas"
            self.status = 1
            return
        else:
            self.status, self.resultado = utils.estadisticas_pandas(self.df, columna)
            self.accept()



class DialogoGuardar(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.df = aux
        self.resultado = None
        self.status = 0

        self.setWindowTitle("Guardar busqueda")
        self.setModal(True)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Nombre archivo (sin extension): "))

        self.txt_criterio = QLineEdit()
        layout.addWidget(self.txt_criterio)

        botones = QHBoxLayout()

        self.btn_buscar = QPushButton("Guardar")
        self.btn_cancelar = QPushButton("Cancelar")

        botones.addWidget(self.btn_buscar)
        botones.addWidget(self.btn_cancelar)

        layout.addLayout(botones)

        self.setLayout(layout)

        self.btn_buscar.clicked.connect(self.guardar)
        self.btn_cancelar.clicked.connect(self.reject)

    def guardar(self):

        criterio = self.txt_criterio.text().strip()
        criterio = criterio + ".csv"

        if not criterio:
            QMessageBox.warning(self, "Error", "Ingrese un nombre de archivo")
            self.resultado = "Error, no se ingreso nonbre archivo"
            self.status = 1
            return 

        try:
            self.resultado = archivos.exportar_csv(self.df, criterio)
            self.status = 0

            self.accept()

        except Exception as e:
            self.resultado = f"Error: {e}"
            self.status = 1

#ventana principal
class VentanaPrincipal(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Proyecto Dataset Diabetes")
        self.setGeometry(100, 100, 1200, 700)
        self.crear_ui()


    def crear_ui(self):

        # Layout principal
        layout_principal = QVBoxLayout()
        # Título
        titulo = QLabel("Proyecto Dataset Diabetes - Insuline_Logic")
        layout_principal.addWidget(titulo)
        # Área de texto
        self.area_texto = QTextEdit()
        layout_principal.addWidget(self.area_texto)
        # Layout botones
        layout_botones = QHBoxLayout()
        # Botones
        boton_cargar = QPushButton("Cargar Dataset")
        boton_buscar = QPushButton("Buscar")
        boton_estadisticas = QPushButton("Estadísticas")
        boton_filtro = QPushButton("Filtrar")
        boton_graficar = QPushButton("Graficar")
        boton_guardar = QPushButton("Guardar resultados")
        boton_historial = QPushButton("Historial")
        boton_salir = QPushButton("Salir")
        # Agregar botones
        layout_botones.addWidget(boton_cargar)
        layout_botones.addWidget(boton_buscar)
        layout_botones.addWidget(boton_estadisticas)
        layout_botones.addWidget(boton_filtro)
        layout_botones.addWidget(boton_graficar)
        layout_botones.addWidget(boton_guardar)
        layout_botones.addWidget(boton_historial)
        layout_botones.addWidget(boton_salir)
        layout_principal.addLayout(layout_botones)

        # Área gráfica vacía
        self.figura = Figure()
        self.canvas = FigureCanvas(self.figura)
        layout_principal.addWidget(self.canvas)

        # Asignar layout
        self.setLayout(layout_principal)

        # CONEXIÓN DE SEÑALES
        boton_cargar.clicked.connect(self.cargar_dataset)
        boton_buscar.clicked.connect(self.buscar)
        boton_estadisticas.clicked.connect(self.estadisticas)
        boton_filtro.clicked.connect(self.filtrar)
        boton_graficar.clicked.connect(self.graficar)
        boton_guardar.clicked.connect(self.guardar)
        boton_historial.clicked.connect(self.historial)
        boton_salir.clicked.connect(self.close)

    # FUNCIONES CONECTORAS
    def mostrar_error(self, texto):
        QMessageBox.critical(self, "Error!", texto, QMessageBox.Ok)

    def cargar_dataset(self):

        status, donde = obtener_dataset()

        if status == 0:
            status, df = archivos.cargar_y_limpiar(donde)
        else:
            status = 1
            texto = "Falla de captura nombre archivo"
        
        if status == 0:
            global dataset
            dataset = df
            if len(dataset) > 1:
                status, texto = utils.resumen_dataset(dataset)
                if status == 0:
                    cadena = f"Total datos: {len(dataset)}\n\n" + tabulate(texto, headers='keys', tablefmt='psql')
                    self.area_texto.setText(cadena)
                    self.graficar()
                else:
                    self.mostrar_error(texto)
            else:
                self.area_texto.setText("Dataset invalido")
        else:
            print(texto)
            self.mostrar_error(texto)
            

    def buscar(self):
        status, procesado = resultado_busqueda()

        if status == 0 and len(procesado)>1:
            global aux
            aux = procesado
            cadena = tabulate(procesado, headers='keys', tablefmt='psql') + f"\n\n Coincidencias encontradas: {len(procesado)}"
            self.area_texto.setText(cadena)

        else:
            try:
                self.area_texto.setText(str(procesado))
            except:
                self.area_texto.setText("Error en la busqueda")

    def estadisticas(self):
        status, texto = resultado_estadisticas()
        if status == 0:
            self.area_texto.setText(texto)
        else:
            self.area_texto.setText("Error en procesamiento de estadisticas")
        
    def filtrar(self):
        status, procesado, filtrados = resultado_filtro()
        if status == 0 and len(procesado)>1:
            global aux
            aux = procesado
            cadena = tabulate(procesado, headers='keys', tablefmt='psql') + f"\n\n Elementos filtrados: {filtrados}"
            self.area_texto.setText(cadena)
        else:
            try:
                self.area_texto.setText(str(procesado))
            except:
                self.area_texto.setText("Error en el filtro")


    def guardar():
        _, texto = guardar_dataset()
        self.area_texto.setText(texto)
        
    def historial(self):
        _, texto = utils.visualizar_historial()
        self.area_texto.setText(texto)

    def graficar(self):
        global dataset
        if dataset is None or len(dataset) == 0:
            return
        
        categorias, prom_glucosa = utils.datos_grafico_glucosa_outcome(dataset)
        edades, prom_bmi = utils.datos_grafico_bmi_edad(dataset)

        self.figura.clear()

        # ax1 = Gráfico de barras| ax2 = Gráfico de línea 
        ax1 = self.figura.add_subplot(1, 2, 1)
        ax2 = self.figura.add_subplot(1, 2, 2)

        # GRÁFICO 1: Barras - Promedio de Glucosa según Diagnóstico 
        if categorias and prom_glucosa:
            colores = ['skyblue', 'salmon']
            barras = ax1.bar(categorias, prom_glucosa, color=colores, edgecolor='black', width=0.5)
            
            ax1.set_title("Promedio de Glucosa por Diagnóstico", fontsize=10, fontweight='bold')
            ax1.set_ylabel("Glucosa (mg/dL)", fontsize=8)
            ax1.set_ylim(0, max(prom_glucosa) * 1.2) 
        
            for barra in barras:
                yval = barra.get_height()
                ax1.text(barra.get_x() + barra.get_width()/2.0, yval + 2, f"{yval}", ha='center', va='bottom', fontsize=8, fontweight='bold')
        else:
            ax1.text(0.5, 0.5, "Sin datos de Glucosa/Outcome", ha='center', va='center')

        # GRÁFICO 2: Línea - Tendencia del BMI según la Edad 
        if edades and prom_bmi:
            ax2.plot(edades, prom_bmi, color='purple', marker='.', linewidth=1.5, linestyle='-')
            ax2.set_title("Tendencia del BMI Promedio por Edad", fontsize=10, fontweight='bold')
            ax2.set_xlabel("Edad (Años)", fontsize=8)
            ax2.set_ylabel("BMI (Índice de Masa Corporal)", fontsize=8)
            ax2.grid(True, linestyle=':', alpha=0.6) 
        else:
            ax2.text(0.5, 0.5, "Sin datos de Edad/BMI", ha='center', va='center')

        self.figura.tight_layout()
        self.canvas.draw()
