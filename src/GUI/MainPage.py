import os
import sys
from time import sleep
import traceback
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow
from src.BIPy import BIPy
from PyQt5.QtCore import *

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

    def __init__(self, processador: BIPy):
        super().__init__()
        self.processador = processador

        self.dict_assemblador = processador.dict_assemblador
        self.dict_assemblador_inv = processador.dict_assemblador_inv

        comandos = list(processador.dict_assemblador.keys())

        uic.loadUi(resource_path('src/GUI/main.ui'), self)
        self.show()

        self.threadpool = QThreadPool()

        self.refresh_displays()

        self.ui_dados = Mem_Dados(memoria_de_dados=self.processador.pega_memoria_de_dados(
        ), altera_memoria_de_dados=self.altera_memoria_de_dados)
        self.ui_programa = Mem_Programa(memoria_de_programa=self.processador.pega_memoria_de_programa(
        ), altera_memoria_de_programa=self.altera_memoria_de_programa, comandos=comandos)

        self.pushButton.clicked.connect(self.show_popup_mem_dados)
        self.pushButton_2.clicked.connect(self.show_popup_mem_programa)
        self.reset_button.clicked.connect(self.reset)
        self.step_button.clicked.connect(self.step)
        self.halt_check.clicked.connect(self.halt)
        self.actionSetar_Clock.triggered.connect(self.set_clock)
        self.clock = 1

    def altera_memoria_de_dados(self, endereco, valor):
        self.processador.memoria_de_dados.altera_celula(endereco, valor.upper())

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
        worker = Worker(self.halted, self.clock)
        self.threadpool.start(worker)

    def halted(self, clock):
        while self.halt_check.isChecked():
            self.step()
            sleep(clock)

    def reset(self):
        try:
            self.processador.reset()
            self.refresh_displays()
        except:
            print("Memoria de dados não iniciada")

    def step(self):
        self.processador.executa_comando()
        self.refresh_displays()
        self.ui_dados.preenche_tabela(self.processador.pega_memoria_de_dados())

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

    def show_popup_mem_dados(self):
        self.ui_dados.show()

    def show_popup_mem_programa(self):
        self.ui_programa.show()


class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
