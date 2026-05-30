from PyQt5.QtWidgets import (QWidget, QPushButton, QTextEdit, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from archivos import cargar_y_limpiar, exportar_csv, guardar_historial, cargar_historial

class VentanaPrincipal(QWidget):

    def __init__(self):
        self.df = None
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
        layout_principal.addWidget(self.area_texto) # CAJA DE BUSQUEDA
        # Caja de Busqueda
        self.caja_busqueda = QLineEdit()
        self.caja_busqueda.setPlaceholderText("Ingrese un valor para buscar")
        layout_principal.addWidget(self.caja_busqueda)
        # SELECTOR DE COLUMNA
        self.combo_columna = QComboBox()
        self.combo_columna.addItems(["Pregnancies", "Glucose", "BloodPressure","SkinThickness","Insulin","BMI","DiabetesPedigreeFunction","Age","Outcome"])
        layout_principal.addWidget(self.combo_columna)
        # AREA DE RESULTADOS
        self.area_texto = QTextEdit()
        self.area_texto.setMaximumHeight(180)
        layout_principal.addWidget(self.area_texto)
        # Botones
        layout_botones = QHBoxLayout()
        self.boton_cargar = QPushButton("Cargar Dataset")
        self.boton_buscar = QPushButton("Buscar")
        self.boton_estadisticas = QPushButton("Estadísticas")
        self.boton_filtrar = QPushButton("Filtrar")
        self.boton_historial = QPushButton("Historial")
        self.boton_salir = QPushButton("Salir")
        boton_exportar = QPushButton("Exportar CSV")
        layout_botones.addWidget(boton_exportar)
        boton_exportar.clicked.connect(self.exportar)
        layout_botones.addWidget(self.boton_cargar)
        layout_botones.addWidget(self.boton_buscar)
        layout_botones.addWidget(self.boton_estadisticas)
        layout_botones.addWidget(self.boton_filtrar)
        layout_botones.addWidget(self.boton_historial)
        layout_botones.addWidget(self.boton_salir)
        layout_principal.addLayout(layout_botones)
        # Área gráfica vacía
        self.figura = Figure()
        self.canvas = FigureCanvas(self.figura)
        layout_principal.addWidget(self.canvas)
        # Asignar layout
        self.setLayout(layout_principal)
        # CONEXIÓN DE SEÑALES
        self.boton_cargar.clicked.connect(self.cargar_dataset)
        self.boton_buscar.clicked.connect(self.buscar)
        self.boton_estadisticas.clicked.connect(self.estadisticas)
        self.boton_filtrar.clicked.connect(self.filtrar)
        self.boton_historial.clicked.connect(self.historial)
        self.boton_salir.clicked.connect(self.close)

    # FUNCIONES CONECTORAS
    def cargar_dataset(self):
        self.df = cargar_y_limpiar("../Data/diabetes_COMPLETO.csv")
        if self.df is not None:
            self.area_texto.setText("Dataset cargado correctamente")
        guardar_historial("Dataset cargado")
    else:
        self.area_texto.setText("Error al cargar dataset")

    def buscar(self):
        if self.df is None:
            self.area_texto.setText("Primero cargue el dataset")
            return
        valor = self.caja_busqueda.text()

        if valor == "":
            self.area_texto.setText("Ingrese un valor para buscar")
            return
        resultados = self.df[self.df.astype(str).apply(lambda fila:fila.str.contains(valor,case=False).any(),axis=1)]
        if len(resultados) == 0:
            self.area_texto.setText("No se encontraron coincidencias")
        else:
            self.area_texto.setText(resultados.head(20).to_string())

    def estadisticas(self):
        if self.df is None:
            self.area_texto.setText("Primero cargue el dataset")
            return
        columna = self.combo_columna.currentText()
        estadisticas = self.df[columna].describe()
        self.area_texto.setText(str(estadisticas))

    def filtrar(self):
        self.area_texto.setText("Función lista para integrar con el módulo de análisis.")

    def historial(self):
    df_historial = cargar_historial()

    if df_historial is not None and not df_historial.empty:
        texto = df_historial.to_string(index=False)
        self.area_texto.setText(texto)
    else:
        self.area_texto.setText("No hay historial disponible")
    
    def exportar(self):
    if self.df is not None:
        nombre = "resultados/datos_exportados.csv"
        exportar_csv(self.df, nombre)
        self.area_texto.setText(f"Datos exportados en {nombre}")
        guardar_historial("Exportación a CSV")
    else:
        self.area_texto.setText("No hay datos para exportar")
