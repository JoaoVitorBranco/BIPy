import sys
from PyQt5 import QtCore, QtWidgets, QtGui

from src.GUI.MemInterface import Mem_Interface


class Mem_Dados(Mem_Interface):
    altera_memoria_de_dados: callable
    def __init__(self, memoria_de_dados: dict, altera_memoria_de_dados):
        super().__init__(UI_string='MemoriaDados', memoria=memoria_de_dados)

        self.altera_memoria_de_dados = altera_memoria_de_dados

        for i in range(self.num_colunas):
            delegate = StyledItemDelegate(self.tableWidget)
            self.tableWidget.setItemDelegateForColumn(i, delegate)

    def on_changed(self, item):
        linha = item.row()
        coluna = item.column()
        valor = item.text()
        celula = f'0x{linha:02X}{coluna:X}'

        self.altera_memoria_de_dados(celula, valor)


class StyledItemDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QtWidgets.QLineEdit):
            regex = f"^[0-9A-Fa-f]{'{4}'}$"
            regex = r"{}".format(regex)
            validator = QtGui.QRegExpValidator(
                QtCore.QRegExp(regex, cs=QtCore.Qt.CaseInsensitive), editor,
            )
            editor.setValidator(validator)

        complete = QtWidgets.QCompleter(editor)
        editor.setCompleter(complete)

        return editor
