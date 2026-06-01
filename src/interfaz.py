import sys
import os

from PyQt5.QtWidgets import (QCheckBox, QTextBrowser, QMainWindow, QLineEdit, QMessageBox, QDialog, QWidget, QPushButton, QTextEdit, QLabel, QVBoxLayout, QHBoxLayout, QApplication)
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

def resultado_busqueda():
    dialog = DialogoBusqueda()

    if dialog.exec_():
        return dialog.status, dialog.resultado
    return 1, "ERROR: fallo la busqueda"


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

        self.df = dataset
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

        if not criterio:
            QMessageBox.warning(self, "Error", "Ingrese un criterio de búsqueda")
            self.resultado = "Error, no se ingreso criterio"
            self.status = 1
            return 

        try:
            self.resultado = utils.buscar_dataframe(self.df, criterio, self.chk_exacta.isChecked())
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
            self.status, self.resultado = utils.filtrar_por_valor(self.df, columna, criterio)


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
        boton_historial = QPushButton("Historial")
        boton_salir = QPushButton("Salir")
        # Agregar botones
        layout_botones.addWidget(boton_cargar)
        layout_botones.addWidget(boton_buscar)
        layout_botones.addWidget(boton_estadisticas)
        layout_botones.addWidget(boton_filtro)
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
        self.area_texto.setText("Botón estadísticas conectado")
    def filtrar(self):
        self.area_texto.setText("Botón filtro conectado")
    def historial(self):
        self.area_texto.setText("Botón historial conectado")
