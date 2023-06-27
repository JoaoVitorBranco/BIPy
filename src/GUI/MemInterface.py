import os
import sys
from PyQt5 import QtCore, QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QFont

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Mem_Interface(QMainWindow):
    memoria: dict

    def __init__(self, UI_string, memoria: dict):
        super().__init__()
        self.memoria = memoria

        uic.loadUi(f'src/GUI/{UI_string}.ui', self)
        self.setWindowIcon(QtGui.QIcon(resource_path('src/GUI/assets/icone.ico')))


        self.num_linhas = 256
        self.num_colunas = 16

        self.diminui_colunas()
        self.formata_colunas()
        self.formata_linhas()
        self.preenche_tabela(memoria)
        self.tableWidget.itemChanged.connect(self.on_changed)

    def diminui_colunas(self):
        for i in range(self.num_colunas):
            self.tableWidget.setColumnWidth(i, 60)

    def formata_colunas(self):
        _translate = QtCore.QCoreApplication.translate
        for i in range(self.num_colunas):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)
            item.setText(_translate("Form", hex(i)[-1].upper()))

    def formata_linhas(self):
        _translate = QtCore.QCoreApplication.translate
        for i in range(self.num_linhas):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(i, item)
            label = '0x' + hex(i).split('x')[1].upper().zfill(2) + 'X'
            item.setText(_translate("Form", label))

    def preenche_tabela(self, memoria):
        self.memoria = memoria
        for i in range(self.num_linhas):
            linha = '0x' + hex(i).split('x')[1].upper().zfill(2)
            for j in range(self.num_colunas):
                coluna = hex(j)[-1].upper()
                item = QtWidgets.QTableWidgetItem()
                font = QFont()
                font.setCapitalization(QFont.AllUppercase)
                item.setFont(font)
                item.setText(memoria.get(linha).get(coluna))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(i, j, item)

    def on_changed(self, item):
        pass
