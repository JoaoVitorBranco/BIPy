import os
import sys
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtGui

class WarningMessageBox(QMessageBox):
    
    def resource_path(self,relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def __init__(self, title: str, message: str):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon(self.resource_path('src/GUI/assets/icone.ico')))
        self.setWindowTitle(title)
        self.setIcon(QMessageBox.Warning)
        self.setText(message)
        self.exec_()