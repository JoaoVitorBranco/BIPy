import os
import sys
from threading import Thread
from time import sleep
import traceback
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow
from src.BIPy import BIPy
from PyQt5.QtCore import pyqtSignal

from src.GUI.Mem_Dados import Mem_Dados
from src.GUI.Mem_Programa import Mem_Programa


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Ui_MainPage(QMainWindow):
    processador: BIPy
    dict_assemblador: dict
    dict_assemblador_inv: dict
    ui_refresh = pyqtSignal()

    def __init__(self, processador: BIPy):
        super().__init__()
        self.processador = processador

        self.dict_assemblador = processador.dict_assemblador
        self.dict_assemblador_inv = processador.dict_assemblador_inv

        comandos = list(processador.dict_assemblador.keys())

        uic.loadUi(resource_path('src/GUI/main.ui'), self)
        self.show()

        self.ui_dados = Mem_Dados(memoria_de_dados=self.processador.pega_memoria_de_dados(
        ), altera_memoria_de_dados=self.altera_memoria_de_dados)
        self.ui_programa = Mem_Programa(memoria_de_programa=self.processador.pega_memoria_de_programa(
        ), altera_memoria_de_programa=self.altera_memoria_de_programa, comandos=comandos)

        self.refresh_displays()
        self.pushButton.clicked.connect(self.show_popup_mem_dados)
        self.pushButton_2.clicked.connect(self.show_popup_mem_programa)
        self.reset_button.clicked.connect(self.reset)
        self.step_button.clicked.connect(self.step)
        self.halt_check.clicked.connect(self.halt)
        self.actionSetar_Clock.triggered.connect(self.set_clock)
        self.clock = 1

        self.ui_refresh.connect(self.step)

    def altera_memoria_de_dados(self, endereco, valor):
        self.processador.memoria_de_dados.altera_celula(
            endereco, valor.upper())

    def altera_memoria_de_programa(self, endereco, valor):
        split_valor = valor.split(" ")
        valor = self.dict_assemblador[split_valor[0].upper()] + split_valor[1]
        self.processador.memoria_de_programa.altera_celula(endereco, valor)

    def set_clock(self):
        msg = QtWidgets.QInputDialog()

        msg.setLabelText("Digite o clock desejado")
        msg.setWindowTitle("Setar Clock")
        msg.exec_()
        try:
            self.clock = 1/int(msg.textValue())
        except:
            pass

    def halt(self):
        t = Thread(target=self.halted)
        t.daemon = True
        t.start()

    def halted(self):
        while self.halt_check.isChecked():
            self.ui_refresh.emit()
            sleep(self.clock)

    def reset(self):
        self.processador.reset()
        self.refresh_displays()

    def step(self):
        self.processador.executa_comando()
        self.refresh_displays()
        self.ui_dados.preenche_tabela(self.processador.pega_memoria_de_dados())

        endereco = self.processador.instrucao.endereco

        linha = int(self.processador.instrucao.endereco[:-1], 16)
        coluna = int(self.processador.instrucao.endereco[-1], 16)

        self.set_selecionado_mem_programa(linha, coluna)

    def set_selecionado_mem_programa(self, linha, coluna):
        for i in range(self.ui_programa.tableWidget.rowCount()):
            for j in range(self.ui_programa.tableWidget.columnCount()):
                item = self.ui_programa.tableWidget.item(i, j)
                item.setBackground(QtGui.QColor(255, 255, 255))
                item.setForeground(QtGui.QColor(0, 0, 0))

        item = self.ui_programa.tableWidget.item(linha, coluna)
        item.setBackground(QtGui.QColor(255, 0, 0))

    def closeEvent(self, event):
        try:
            self.ui_dados.close()
        except AttributeError:
            print("Memoria de dados não iniciada")
        try:
            self.ui_programa.close()
        except AttributeError:
            print("Memoria de programa não iniciada")

    def refresh_displays(self):
        self.program_counter.display(self.processador.instrucao.endereco)
        self.acumulador.display(self.processador.acc)
        self.instruct_counter.display(
            self.processador.instrucao.pega_comando())
        self.set_selecionado_mem_programa(0, 0)

    def show_popup_mem_dados(self):
        self.ui_dados.show()

    def show_popup_mem_programa(self):
        self.ui_programa.show()
