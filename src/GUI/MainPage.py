import os
import sys
from threading import Thread
from time import sleep
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow
from src.BIPy import BIPy
from PyQt5.QtCore import pyqtSignal

from src.GUI.Mem_Dados import Mem_Dados
from src.GUI.Mem_Programa import Mem_Programa

import os


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
        uic.loadUi(resource_path(os.path.join('src', 'GUI', 'MainPage.ui')), self)

        self.setWindowIcon(QtGui.QIcon(resource_path(os.path.join('src', 'GUI', 'assets', 'icone.ico'))))
        self.show()

        self.ui_dados = Mem_Dados(memoria_de_dados=self.processador.pega_memoria_de_dados(
        ), altera_memoria_de_dados=self.altera_memoria_de_dados)
        self.ui_programa = Mem_Programa(memoria_de_programa=self.processador.pega_memoria_de_programa(
        ), altera_memoria_de_programa=self.altera_memoria_de_programa, comandos=comandos)

        self.refresh_displays()
        self.reset()
        self.pushButton.clicked.connect(self.show_popup_mem_dados)
        self.pushButton_2.clicked.connect(self.show_popup_mem_programa)
        self.reset_button.clicked.connect(self.reset)
        self.step_button.clicked.connect(self.step)
        self.halt_check.clicked.connect(self.halt)
        self.actionSetar_Clock.triggered.connect(self.set_clock)
        self.actionDecimal.triggered.connect(
            self.altera_acumulador_para_decimal)
        self.actionHexadecimal.triggered.connect(
            self.altera_acumulador_para_hexadecimal)
        self.clock = 1

        self.ui_refresh.connect(self.step)

    def altera_acumulador_para_decimal(self):
        self.acumulador.setDigitCount(5)
        self.acumulador.setDecMode()
        self.label_5.setStyleSheet("background:rgba(0, 71, 133, 0.4);")
        self.label_4.setStyleSheet("background:rgba(0, 71, 133, 0.1);")

    def altera_acumulador_para_hexadecimal(self):
        self.acumulador.setDigitCount(4)
        self.acumulador.setHexMode()
        self.label_4.setStyleSheet("background:rgba(0, 71, 133, 0.4);")
        self.label_5.setStyleSheet("background:rgba(0, 71, 133, 0.1);")

    def altera_memoria_de_dados(self, endereco, valor):
        self.processador.memoria_de_dados.altera_celula(
            endereco, valor.upper())

    def altera_memoria_de_programa(self, endereco, valor):
        split_valor = valor.upper().split(" ")
        valor = self.dict_assemblador[split_valor[0]] + split_valor[1]
        self.processador.memoria_de_programa.altera_celula(endereco, valor)

    def set_clock(self):

        msg = QtWidgets.QInputDialog()
        msg.setWindowIcon(QtGui.QIcon(
            resource_path('src/GUI/assets/icone.ico')))
        msg.setLabelText("Digite a frequência de clock desejada em Hz:")
        msg.setInputMode(QtWidgets.QInputDialog.DoubleInput)
        msg.setOkButtonText("Setar")
        msg.setDoubleValue(1/self.clock)
        msg.setDoubleRange(0.1, 15)
        msg.setDoubleStep(0.5)
        msg.setWindowTitle("Setar Clock")
        msg.exec_()

        try:
            self.clock = 1/msg.doubleValue()
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
        valor = self.processador.instrucao.valor

        linha = int(endereco[:-1], 16)
        coluna = int(endereco[-1], 16)

        self.set_selecionado_mem_programa(linha, coluna)
        self.set_selecionado_mem_dados(valor)

    def set_selecionado_mem_programa(self, linha, coluna):
        for i in range(self.ui_programa.tableWidget.rowCount()):
            for j in range(self.ui_programa.tableWidget.columnCount()):

                item = self.ui_programa.tableWidget.item(i, j)

                if i % 2 == 0:
                    color = QtGui.QColor(255, 255, 255)
                else:
                    color = QtGui.QColor(0, 71, 133)
                    color.setAlphaF(0.2)

                item.setBackground(color)
                item.setForeground(QtGui.QColor(0, 0, 0))

        item = self.ui_programa.tableWidget.item(linha, coluna)
        highlight = QtGui.QColor(0, 71, 133)
        highlight.setAlphaF(0.8)
        item.setBackground(highlight)

    def set_selecionado_mem_dados(self, valor):
        linha = int(valor[1:-1], 16)
        coluna = int(valor[-1], 16)

        for i in range(self.ui_dados.tableWidget.rowCount()):
            for j in range(self.ui_dados.tableWidget.columnCount()):
                item = self.ui_dados.tableWidget.item(i, j)

                if i % 2 == 0:
                    color = QtGui.QColor(255, 255, 255)
                else:
                    color = QtGui.QColor(0, 71, 133)
                    color.setAlphaF(0.2)

                item.setBackground(color)
                item.setForeground(QtGui.QColor(0, 0, 0))

        item = self.ui_dados.tableWidget.item(linha, coluna)
        highlight = QtGui.QColor(0, 71, 133)
        highlight.setAlphaF(0.8)
        item.setBackground(highlight)

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
        self.acumulador.display(int(self.processador.acc, 16))
        self.instruct_counter.display(
            self.processador.instrucao.pega_comando())
        self.set_selecionado_mem_programa(0, 0)

    def show_popup_mem_dados(self):
        self.ui_dados.show()

    def show_popup_mem_programa(self):
        self.ui_programa.show()
