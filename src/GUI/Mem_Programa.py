import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from MemInterface import Mem_Interface

comandos = ["HLT ", "STO ", "LD ", "LDI ", "ADD ", "ADDI ", "SUB ", "SUBI ", "NOP ", "JUMP ", "CMP ","JL ","JG "]


class Mem_Programa(Mem_Interface):
    def __init__(self):
        super().__init__(UI_string='MemoriaPrograma')

        for i in range(self.num_colunas):
            delegate = StyledItemDelegate(self.tableWidget)
            self.tableWidget.setItemDelegateForColumn(i, delegate)

        

class StyledItemDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QtWidgets.QLineEdit):
            regex = f"^({'|'.join(comandos).replace(' ','')}) [0-9A-Fa-f]{'{3}'}$"
            regex = r"{}".format(regex)
            validator = QtGui.QRegExpValidator(
                QtCore.QRegExp(regex,cs=QtCore.Qt.CaseInsensitive), editor,
            )
            editor.setValidator(validator)
    
        completer = QtWidgets.QCompleter(comandos, editor)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        editor.setCompleter(completer)
        

        return editor

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    UIWindow = Mem_Programa()
    app.exec_()