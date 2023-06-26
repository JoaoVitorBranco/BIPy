import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from MemInterface import Mem_Interface

class Mem_Dados(Mem_Interface):
    def __init__(self):
        super().__init__(UI_string='MemoriaDados')
        for i in range(self.num_colunas):
            delegate = StyledItemDelegate(self.tableWidget)
            self.tableWidget.setItemDelegateForColumn(i, delegate)

        

class StyledItemDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QtWidgets.QLineEdit):
            regex = f"^[0-9]{'{4}'}$"
            regex = r"{}".format(regex)
            validator = QtGui.QRegExpValidator(
                QtCore.QRegExp(regex,cs=QtCore.Qt.CaseInsensitive), editor,
            )
            editor.setValidator(validator)           
        
    
        complete = QtWidgets.QCompleter(editor)
        editor.setCompleter(complete)
        

        return editor


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    UIWindow = Mem_Dados()
    app.exec_()