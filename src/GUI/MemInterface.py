from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow

class Mem_Interface(QMainWindow):
    def __init__(self, UI_string):
        super().__init__()

        uic.loadUi(f'src/GUI/{UI_string}.ui', self)
  
        self.num_linhas = 256
        self.num_colunas = 16

        self.vazio = '0000' if UI_string == 'MemoriaDados' else 'HLT 000'

        self.diminui_colunas()
        self.formata_colunas()
        self.formata_linhas()
        self.preenche_tabela(UI_string)

        self.show()


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
            label = '0x'+ hex(i).split('x')[1].upper().zfill(2) + 'X'
            item.setText(_translate("Form", label))     

    def preenche_tabela(self, UI_string):
        for i in range(self.num_linhas):
            for j in range(self.num_colunas):
                item = QtWidgets.QTableWidgetItem()
                item.setText(self.vazio)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(i, j, item)
