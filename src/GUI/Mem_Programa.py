import sys
from PyQt5 import QtCore, QtWidgets, QtGui

from src.GUI.MemInterface import Mem_Interface


class Mem_Programa(Mem_Interface):
    comandos: list
    altera_memoria_de_programa: callable

    def __init__(self, memoria_de_programa: dict, altera_memoria_de_programa: callable, comandos: list):
        super().__init__(UI_string='MemoriaPrograma', memoria=memoria_de_programa)

        self.comandos = [i+" " for i in comandos]
        self.altera_memoria_de_programa = altera_memoria_de_programa

        for i in range(self.num_colunas):
            delegate = StyledItemDelegate(
                parent=self.tableWidget, comandos=self.comandos)
            self.tableWidget.setItemDelegateForColumn(i, delegate)

    def on_changed(self, item):
        linha = item.row()
        coluna = item.column()
        valor = item.text()
        celula = f'0x{linha:02X}{coluna:X}'

        self.altera_memoria_de_programa(celula, valor)


class StyledItemDelegate(QtWidgets.QStyledItemDelegate):
    comandos: list

    def __init__(self, comandos: list, parent=None):
        super().__init__(parent)
        self.comandos = comandos

    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QtWidgets.QLineEdit):
            regex = f"^({'|'.join(self.comandos).replace(' ','')}) [0-9A-Fa-f]{'{3}'}$"
            regex = r"{}".format(regex)
            validator = QtGui.QRegExpValidator(
                QtCore.QRegExp(regex, cs=QtCore.Qt.CaseInsensitive), editor,
            )
            editor.setValidator(validator)

        completer = QtWidgets.QCompleter(self.comandos, editor)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        editor.setCompleter(completer)

        return editor
