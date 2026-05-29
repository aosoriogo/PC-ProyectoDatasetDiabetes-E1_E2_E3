from PyQt5.QtWidgets import (QWidget, QPushButton, QTextEdit, QLabel, QVBoxLayout, QHBoxLayout, QApplication)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys

class VentanaPrincipal(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Proyecto Dataset Diabetes")
        self.setGeometry(100, 100, 1000, 700)
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
    def cargar_dataset(self):
        self.area_texto.setText("Botón cargar dataset conectado")
    def buscar(self):
        self.area_texto.setText("Botón buscar conectado")
    def estadisticas(self):
        self.area_texto.setText("Botón estadísticas conectado")
    def filtrar(self):
        self.area_texto.setText("Botón filtro conectado")
    def historial(self):
        self.area_texto.setText("Botón historial conectado")
