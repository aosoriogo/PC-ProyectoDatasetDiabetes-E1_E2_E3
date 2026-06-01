import sys

from PyQt5.QtWidgets import QApplication
from interfaz import VentanaPrincipal

import interfaz as cli

if __name__ == '__main__':
    app_qt = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app_qt.exec_())