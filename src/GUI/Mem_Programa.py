import sys
import os
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox

from src.GUI.MemInterface import Mem_Interface

class Mem_Programa(Mem_Interface):
    comandos: list
    altera_memoria_de_programa: callable
    salva_memoria_de_programa: callable
    limpa_memoria: callable
    carrega_memoria_de_programa: callable
    tipos_de_arquivo = "CEDAR Memory files (*.cdm);; Arquivo de Texto (*.txt)"

    def __init__(self, memoria_de_programa: dict, altera_memoria_de_programa: callable, comandos: list, limpa_memoria, salva_memoria_de_programa, carrega_memoria_de_programa):
        super().__init__(titulo='Memoria de Programa', memoria=memoria_de_programa)

        self.comandos = [i+" " for i in comandos]
        self.altera_memoria_de_programa = altera_memoria_de_programa
        self.limpa_memoria = limpa_memoria
        self.salva_memoria_de_programa = salva_memoria_de_programa
        self.carrega_memoria_de_programa = carrega_memoria_de_programa

        for i in range(self.num_colunas):
            delegate = StyledItemDelegate(parent=self.tableWidget, comandos=self.comandos)
            self.tableWidget.setItemDelegateForColumn(i, delegate)

    # region Funções de controle

    def on_changed(self, item):
        linha = item.row()
        coluna = item.column()
        valor = item.text()
        celula = f'0x{linha:02X}{coluna:X}'

        self.altera_memoria_de_programa(celula, valor)
    
    def zerar_memoria(self):
        msg = QMessageBox()
        msg.setWindowIcon(QtGui.QIcon(self.resource_path('src/GUI/assets/icone.ico')))
        msg.setWindowTitle("Zerar memória")
        msg.setIcon(QMessageBox.Question)
        msg.addButton('Sim', QMessageBox.YesRole)
        msg.addButton('Não', QMessageBox.NoRole)        
        msg.setText('Certeza que quer zerar a memória? ')
        msg.exec_()
        reply = msg.buttonRole(msg.clickedButton())

        if reply == QMessageBox.YesRole:
            self.limpa_memoria()
            qm = QMessageBox()
            qm.setWindowTitle("Zerar memória")
            qm.setText("Memória zerada")
            qm.setWindowIcon(QtGui.QIcon(self.resource_path('src/GUI/assets/icone.ico')))
            qm.setIcon(QMessageBox.Information)
            qm.exec_()

    def salvar_arquivo(self):
        nome , tipo = QtWidgets.QFileDialog.getSaveFileName(self, 'Salvar arquivo', '', self.tipos_de_arquivo.split(';;')[0])
        self.salva_memoria_de_programa(nome, tipo)
    
    def carregar_arquivo(self):
        nome, tipo = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Abrir Arquivo', '', self.tipos_de_arquivo)
        try:
            arquivo = open(nome, 'r')
            cdm = list()
            with arquivo:
                texto = arquivo.read()

            cdm = texto.split('\n')
            cdm = list(filter(None, cdm))
            cdm = [x for x in cdm if not x.startswith('#')]
            self.carrega_memoria_de_programa(cdm, tipo)
        except (FileNotFoundError):
            print("Arquivo não encontrado")
    
    #endregion

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
