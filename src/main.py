import sys
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow

from src.BIPy import BIPy
from src.GUI.MainPage import Ui_MainPage
from src.enums.tipo_de_memoria_enum import TipoDeMemoriaEnum
from src.memoria.repo.memoria_json import MemoriaJSON
from src.memoria.repo.memoria_mock import MemoriaMock

memoria_de_programa = MemoriaJSON(arquivo=TipoDeMemoriaEnum.MEMORIA_DE_PROGRAMA)

memoria_de_dados = MemoriaJSON(arquivo=TipoDeMemoriaEnum.MEMORIA_DE_DADOS)

processador = BIPy(memoria_de_dados=memoria_de_dados,
                   memoria_de_programa=memoria_de_programa)

app = QtWidgets.QApplication(sys.argv)
UIWindow = Ui_MainPage(processador=processador)
app.exec_()
