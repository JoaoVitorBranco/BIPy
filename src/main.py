import sys
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow

from src.BIPy import BIPy
from src.GUI.MainPage import Ui_MainPage
from src.memoria.memoria_mock import MemoriaMock

memoria_de_programa = MemoriaMock()
memoria_de_programa.altera_celula("0x000", "3004")
memoria_de_programa.altera_celula("0x001", "5004")
memoria_de_programa.altera_celula("0x002", "5004")
memoria_de_programa.altera_celula("0x003", "5004")
memoria_de_programa.altera_celula("0x004", "1000")

memoria_de_dados = MemoriaMock()

processador = BIPy(memoria_de_dados=memoria_de_dados,
                   memoria_de_programa=memoria_de_programa)


app = QtWidgets.QApplication(sys.argv)
UIWindow = Ui_MainPage(processador=processador)
app.exec_()
