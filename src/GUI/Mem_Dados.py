import sys
from PyQt5 import QtCore, QtWidgets, QtGui
import os

from src.GUI.MemInterface import Mem_Interface


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Mem_Dados(Mem_Interface):
    altera_memoria_de_dados: callable
    def __init__(self, memoria_de_dados: dict, altera_memoria_de_dados):
        super().__init__(UI_string='MemoriaDados', memoria=memoria_de_dados)

        self.altera_memoria_de_dados = altera_memoria_de_dados

        for i in range(self.num_colunas):
            delegate = StyledItemDelegate(self.tableWidget)
            self.tableWidget.setItemDelegateForColumn(i, delegate)
        
        self.actionZero.triggered.connect(self.zerar_memoria)
        self.actionSalvar.triggered.connect(self.salvar_arquivo)
        self.actionCarregar.triggered.connect(self.carregar_arquivo)

    def on_changed(self, item):
        linha = item.row()
        coluna = item.column()
        valor = item.text()
        celula = f'0x{linha:02X}{coluna:X}'

        self.altera_memoria_de_dados(celula, valor)

    def zerar_memoria(self):
            msg = QtWidgets.QMessageBox()
            msg.setWindowIcon(QtGui.QIcon(resource_path('src/GUI/assets/icone.ico')))
            msg.setWindowTitle("Zerar memória")
            msg.setIcon(QtWidgets.QMessageBox.Question)
            msg.addButton('Sim', QtWidgets.QMessageBox.YesRole)
            msg.addButton('Não', QtWidgets.QMessageBox.NoRole)        
            msg.setText('Certeza que quer zerar a memória? ')
            msg.exec_()
            resposta     = msg.buttonRole(msg.clickedButton())

            if resposta == QtWidgets.QMessageBox.YesRole:
                '''
                ZERAR MEMORIA
                '''
                qm = QtWidgets.QMessageBox()
                qm.setWindowTitle("Zerar memória")
                qm.setText("Memória zerada")
                qm.setWindowIcon(QtGui.QIcon(resource_path('src/GUI/assets/icone.ico')))
                qm.setIcon(QtWidgets.QMessageBox.Information)
                qm.exec_()
            
            elif resposta == QtWidgets.QMessageBox.NoRole:
                qm = QtWidgets.QMessageBox()
                qm.setText("Operação cancelada. Memória permanece inalterada.")
                qm.setWindowIcon(QtGui.QIcon(resource_path('src/GUI/assets/icone.ico')))
                qm.setIcon(QtWidgets.QMessageBox.Information)
                qm.setWindowTitle("Zerar memória")
                qm.exec_()

    def salvar_arquivo(self):
        nome = QtWidgets.QFileDialog.getSaveFileName(self, 'Salvar Arquivo')
        arquivo = open(nome[0], 'w')
        texto = 'fodase'
        arquivo.write(texto)
        arquivo.close()

    def carregar_arquivo(self):
        nome = QtWidgets.QFileDialog.getOpenFileName(self, 'Abrir Arquivo')
        arquivo = open(nome[0], 'r')
    
        with arquivo:
            texto = arquivo.read()
        print(texto)

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
