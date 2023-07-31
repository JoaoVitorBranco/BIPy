import os
import sys
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtWidgets import QMainWindow


class Ui_Consulta(QMainWindow):

    def __init__(self):
        super().__init__()

        uic.loadUi(f'src/GUI/assets/Consulta.ui', self)
        self.setWindowIcon(QtGui.QIcon(self.resource_path('src/GUI/assets/icone.ico')))

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)