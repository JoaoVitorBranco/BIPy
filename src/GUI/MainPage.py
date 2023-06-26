from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow
from src.BIPy import BIPy

from src.GUI.Mem_Dados import Mem_Dados
from src.GUI.Mem_Programa import Mem_Programa


class Ui_MainPage(QMainWindow):
    processador: BIPy

    def __init__(self, processador: BIPy):
        super().__init__()
        self.processador = processador

        uic.loadUi('src/GUI/main.ui', self)
        self.show()

        self.pushButton.clicked.connect(self.show_popup_mem_dados)
        self.pushButton_2.clicked.connect(self.show_popup_mem_programa)
        self.reset_button.clicked.connect(self.reset)
        self.step_button.clicked.connect(self.step)

    def show_popup_mem_dados(self):
        self.window_dados = QtWidgets.QMainWindow()
        self.ui_dados = Mem_Dados(
            memoria_de_dados=self.processador.pega_memoria_de_dados())

    def show_popup_mem_programa(self):
        self.window_programa = QtWidgets.QMainWindow()
        self.ui_programa = Mem_Programa(
            memoria_de_programa=self.processador.pega_memoria_de_programa())

    def reset(self):
        try:
            self.ui_dados.tableWidget.clearContents()
            self.program_counter.display(0)
        except:
            print("Memoria de dados não iniciada")

    def step(self):
        valor = self.program_counter.intValue()
        valor += 1
        self.program_counter.display(valor)

    def closeEvent(self, event):
        try:
            self.ui_dados.close()
        except AttributeError:
            print("Memoria de dados não iniciada")
        try:
            self.ui_programa.close()
        except AttributeError:
            print("Memoria de programa não iniciada")
