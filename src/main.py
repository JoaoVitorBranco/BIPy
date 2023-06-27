import sys
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow

from src.BIPy import BIPy
from src.GUI.MainPage import Ui_MainPage
from src.memoria.memoria_mock import MemoriaMock

memoria_de_programa = MemoriaMock()

memoria_de_dados = MemoriaMock()

processador = BIPy(memoria_de_dados=memoria_de_dados,
                   memoria_de_programa=memoria_de_programa)

processador.memoria_de_programa.altera_celula('0x000', '5001')
processador.memoria_de_programa.altera_celula('0x001', '5002')
processador.memoria_de_programa.altera_celula('0x002', '5003')
processador.memoria_de_programa.altera_celula('0x003', '5004')
processador.memoria_de_programa.altera_celula('0x004', '5005')
processador.memoria_de_programa.altera_celula('0x005', '5006')
processador.memoria_de_programa.altera_celula('0x006', '5007')


app = QtWidgets.QApplication(sys.argv)
UIWindow = Ui_MainPage(processador=processador)
app.exec_()
