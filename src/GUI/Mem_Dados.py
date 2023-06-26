import sys
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtWidgets import QMainWindow

class Mem_Dados(QMainWindow):
    def __init__(self):
        super(Mem_Dados, self).__init__()

        uic.loadUi('src/GUI/MemoriaDados.ui', self)

        self.show()

        self.num_linhas = 256
        self.num_colunas = 16
        self.diminui_colunas()
        self.formata_colunas()
        self.formata_linhas()
        self.preenche_tabela()



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
 
    def preenche_tabela(self):
        for i in range(self.num_linhas):
            for j in range(self.num_colunas):
                item = QtWidgets.QTableWidgetItem()
                item.setText("0000")
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(i, j, item)
        

# class StyledItemDelegate(QtWidgets.QStyledItemDelegate):
#     def createEditor(self, parent, option, index):
#         editor = super().createEditor(parent, option, index)
#         if isinstance(editor, QtWidgets.QLineEdit):
#             regex = r"^[0-9A-Fa-f]{4}$"
#             validator = QtGui.QRegExpValidator(
#                 QtCore.QRegExp(regex,cs=QtCore.Qt.CaseInsensitive), editor,
#             )
#             editor.setValidator(validator)           
        
#         return editor

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    UIWindow = Mem_Dados()
    app.exec_()