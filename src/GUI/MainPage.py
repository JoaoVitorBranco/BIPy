import os
import sys
import io
from threading import Thread
from time import sleep
from typing import List

from PyQt5 import QtGui, uic
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog, QShortcut, QWidget
from PyQt5.QtCore import pyqtSignal

from src.BIPy import BIPy
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

        # Inicialização de variáveis

        self.secret_feature = QShortcut(QKeySequence('Ctrl+Shift+U'), self)
        self.secret_feature.activated.connect(self.set_secret_feature)
        self.secret_feature_bool = self.secret_feature.isEnabled()
        self.processador = processador
        self.dict_assemblador = processador.dict_assemblador
        self.dict_assemblador_inv = processador.dict_assemblador_inv
        self.comandos = list(processador.dict_assemblador.keys())

        # Inicialização da UI da página

        self.setup_ui('MainPage')

    def setup_ui(self, ui_name: str):

        uic.loadUi(resource_path(os.path.join('src', 'GUI','assets', f'{ui_name}.ui')), self)
        self.setWindowIcon(QtGui.QIcon(
            resource_path('src/GUI/assets/icone.ico')))
        self.show()

        # Inicializando a tabela responsável pela memoria de programa e de dados

        self.ui_dados = Mem_Dados(memoria_de_dados=self.processador.pega_memoria_de_dados(
        ), altera_memoria_de_dados=self.altera_memoria_de_dados, limpa_memoria=self.limpa_memoria_de_dados, carrega_memoria_de_dados=self.carrega_memoria_de_dados, salva_memoria_de_dados=self.salva_memoria_de_dados)

        self.ui_programa = Mem_Programa(memoria_de_programa=self.processador.pega_memoria_de_programa(
        ), altera_memoria_de_programa=self.altera_memoria_de_programa, comandos=self.comandos, limpa_memoria=self.limpa_memoria_de_programa, salva_memoria_de_programa=self.salva_memoria_de_programa, carrega_memoria_de_programa=self.carrega_memoria_de_programa)

        # Inicialização geral da página
        self.refresh_displays()
        self.reset()
        self.clock = 1

        # region Designando funções aos botões da página

        self.pushButton.clicked.connect(self.show_popup_mem_dados)
        self.pushButton_2.clicked.connect(self.show_popup_mem_programa)
        self.reset_button.clicked.connect(self.reset)
        self.step_button.clicked.connect(self.step)
        self.halt_check.clicked.connect(self.halt)
        self.pushButton_3.clicked.connect(self.altera_acumulador_para_hexadecimal)
        self.pushButton_4.clicked.connect(self.altera_acumulador_para_decimal)

        # endregion

        # region Designando funções aos botões do menu

        self.actionSetar_Clock.triggered.connect(self.set_clock)
        self.actionDecimal.triggered.connect(self.altera_acumulador_para_decimal)
        self.actionHexadecimal.triggered.connect(self.altera_acumulador_para_hexadecimal)
        self.actionSobre.triggered.connect(self.exibe_creditos)
        self.actionConsulta.triggered.connect(self.abre_consulta)

        # endregion

        self.ui_refresh.connect(self.step)

    # region Funções de controle

    def set_clock(self):

        msg = QInputDialog()
        msg.setWindowIcon(QtGui.QIcon(
            resource_path('src/GUI/assets/icone.ico')))
        msg.setLabelText("Digite a frequência de clock desejada em Hz:")
        msg.setInputMode(QInputDialog.DoubleInput)
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

    def closeEvent(self, event):
        try:
            self.ui_dados.close()
        except AttributeError:
            print("Memoria de dados não iniciada")
        try:
            self.ui_programa.close()
        except AttributeError:
            print("Memoria de programa não iniciada")

        self.processador.salva_memorias()

    def altera_memoria_de_dados(self, endereco, valor):
        self.processador.memoria_de_dados.altera_celula(
            endereco, valor.upper())

    def altera_memoria_de_programa(self, endereco, valor):
        split_valor = valor.upper().split(" ")
        valor = self.dict_assemblador[split_valor[0]] + split_valor[1]
        self.processador.memoria_de_programa.altera_celula(endereco, valor)


    # endregion

    # region Funções dos botões que controlam o processador

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

        if(valor[0] == "0"):
            self.halt_check.setChecked(False)

        linha = int(endereco[:-1], 16)
        coluna = int(endereco[-1], 16)

        self.set_selecionado_mem_programa(linha, coluna)
        self.set_selecionado_mem_dados(valor)

    # endregion

    # region Funções que conttrolam a UI

    # region Altera a UI da MainPage

    def altera_acumulador_para_decimal(self):
        self.acumulador.setDigitCount(5)
        self.acumulador.setDecMode()
        self.pushButton_3.setStyleSheet(
            "background-color: rgb(50, 119, 185);border-width: 0.5%;")
        self.pushButton_4.setStyleSheet(
            "background-color: rgb(0, 69, 135);border-width: 2%;")

    def altera_acumulador_para_hexadecimal(self):
        self.acumulador.setDigitCount(4)
        self.acumulador.setHexMode()
        self.pushButton_3.setStyleSheet(
            "background-color: rgb(0, 69, 135);border-width: 2%;")
        self.pushButton_4.setStyleSheet(
            "background-color: rgb(50, 119, 185);border-width: 0.5%;")

    def refresh_displays(self):
        self.program_counter.display(self.processador.instrucao.endereco)
        self.acumulador.display(int(self.processador.acc, 16))
        self.instruct_counter.display(
            self.processador.instrucao.pega_comando())
        self.set_selecionado_mem_programa(0, 0)

        # Cria popups

    def exibe_creditos(self):
        msg = QMessageBox()
        arquivo = io.open(resource_path(r'src\GUI\assets\creditos.txt'), 'r', encoding='utf8')
        msg.setText(arquivo.read())
        # mudar o formato do texto para aceitar HTML inline
        msg.setTextFormat(1)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(QtGui.QIcon(resource_path('src/GUI/assets/icone.ico')))
        msg.setWindowTitle("Créditos do projeto")
        msg.exec_()

    def show_popup_mem_dados(self):
        self.ui_dados.show()
        self.ui_dados.setFocus(True)
        self.ui_dados.raise_()

    def show_popup_mem_programa(self):
        self.ui_programa.show()
        self.ui_programa.setFocus(True)
        self.ui_programa.raise_()

    def abre_consulta(self):      
        msg = QMessageBox()
        arquivo = io.open(resource_path(r'src\GUI\assets\consulta_alt.txt'), 'r', encoding='utf8')
        msg.setText(arquivo.read())
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(QtGui.QIcon(resource_path('src/GUI/assets/icone.ico')))
        msg.setWindowTitle("Consulta de comnados")
        msg.exec_()

    # endregion

    # region Altera a UI de um popup

    def limpa_memoria_de_dados(self):
        self.processador.memoria_de_dados.limpa_memoria()
        self.ui_dados.preenche_tabela(self.processador.pega_memoria_de_dados())

    def salva_memoria_de_dados(self, caminho: str, tipo: str):
        nome = caminho.rsplit("/", 1)[1].split(".")[0]
        caminho = caminho.rsplit("/", 1)[0]

        if "cdm" in tipo:
            self.processador.memoria_de_dados_para_cdm(caminho, nome)

        # elif "txt" in tipo:
        #     self.processador.memoria_de_dados_para_txt(caminho, nome)

        # TODO implement error
            
    def limpa_memoria_de_programa(self):
        self.processador.memoria_de_programa.limpa_memoria()
        self.ui_programa.preenche_tabela(
            self.processador.pega_memoria_de_programa())
    
    def salva_memoria_de_programa(self, caminho_completo: str, tipo: str):
        nome = caminho_completo.rsplit("/", 1)[1].split(".")[0]
        caminho = caminho_completo.rsplit("/", 1)[0]

        if "cdm" in tipo:
            self.processador.memoria_de_programa_para_cdm(caminho, nome)

        # elif "txt" in tipo:
        #     self.processador.memoria_de_programa_para_txt(caminho, nome)

        # TODO implement error
    
    def carrega_memoria_de_dados(self, linhas: List[str], tipo: str):
        if "cdm" in tipo:
            self.processador.altera_memoria_de_dados_com_cdm(linhas)

        else: 
            return
        
        self.ui_dados.preenche_tabela(self.processador.pega_memoria_de_dados())
        self.set_selecionado_mem_programa(0, 0)

    def carrega_memoria_de_programa(self, linhas: List[str], tipo: str):
        if "cdm" in tipo:
            self.processador.altera_memoria_de_programa_com_cdm(linhas)

        elif "txt" in tipo:
            self.processador.altera_memoria_de_programa_com_txt(linhas)

        else: 
            return
        
        self.ui_programa.preenche_tabela(self.processador.pega_memoria_de_programa())
        self.set_selecionado_mem_programa(0, 0)


    def set_selecionado_mem_programa(self, linha, coluna):
        for i in range(self.ui_programa.tableWidget.rowCount()):
            for j in range(self.ui_programa.tableWidget.columnCount()):

                item = self.ui_programa.tableWidget.item(i, j)

                if i % 2 == 1:
                    color = QtGui.QColor(255, 255, 255)
                else:
                    color = QtGui.QColor(0, 71, 133)
                    color.setAlphaF(0.2)

                item.setBackground(color)

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

                if i % 2 == 1:
                    color = QtGui.QColor(255, 255, 255)
                else:
                    color = QtGui.QColor(0, 71, 133)
                    color.setAlphaF(0.1)

                item.setBackground(color)

        item = self.ui_dados.tableWidget.item(linha, coluna)
        highlight = QtGui.QColor(0, 71, 133)
        highlight.setAlphaF(0.8)

    def set_secret_feature(self):

        # darkmode
        if self.secret_feature_bool:
            self.setStyleSheet("QWidget{background: rgb(38, 45, 55);color: rgb(213, 213, 213);}QPushButton{border-radius: 20%;background-color:" 
                               "rgb(0, 69, 136);color: rgb(213, 213, 213);}QPushButton:hover{background-color: rgb(0, 59, 126);}"
                               "QPushButton:pressed{background-color: rgb(0, 49, 116);}QLCDNumber{background-color: rgb(30, 99, 165);"
                               "border-radius: 20%;color: rgb(213, 213, 213);}")
        
        #lightmode
        else:
            self.setStyleSheet("QWidget{background: rgb(213,213,213);color: rgb(0, 69, 135);}QPushButton{border-radius: 20%;background-color:" 
                               "rgb(0, 69, 136);color: white;}QPushButton:hover{background-color: rgb(0, 59, 126);}"
                               "QPushButton:pressed{background-color: rgb(0, 49, 116);}QLCDNumber{background-color: rgb(30, 99, 165);"
                               "border-radius: 20%;color: white;}")

        self.secret_feature_bool = not self.secret_feature_bool

    # endregion

    # endregion
