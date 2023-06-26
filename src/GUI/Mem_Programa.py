import sys
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtWidgets import QMainWindow
from MemInterface import Mem_Interface

class Mem_Programa(Mem_Interface):
    def __init__(self):
        super().__init__(UI_string='MemoriaPrograma')
        

        

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
    UIWindow = Mem_Programa()
    app.exec_()