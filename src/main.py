import sys
from PyQt5 import QtCore, QtWidgets, QtGui

from src.BIPy import BIPy
from src.GUI.MainPage import Ui_MainPage
from src.GUI.box.WarningMessageBox import WarningMessageBox
from src.enums.tipo_de_memoria_enum import TipoDeMemoriaEnum
from src.memoria.repo.memoria_json import MemoriaJSON

memoria_de_programa = MemoriaJSON(arquivo=TipoDeMemoriaEnum.MEMORIA_DE_PROGRAMA)

memoria_de_dados = MemoriaJSON(arquivo=TipoDeMemoriaEnum.MEMORIA_DE_DADOS)

app = QtWidgets.QApplication(sys.argv)

try:
    BIPy.valida_memorias(memoria_de_dados, memoria_de_programa)
except Exception as e:
    WarningMessageBox("Erro de memória", str(e))

processador = BIPy(memoria_de_dados=memoria_de_dados,
                   memoria_de_programa=memoria_de_programa)
  
UIWindow = Ui_MainPage(processador=processador)
app.exec_()