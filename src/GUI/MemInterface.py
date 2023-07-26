import os
import sys
from PyQt5 import QtCore, QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QShortcut
from PyQt5.QtGui import QFont, QKeySequence

class Mem_Interface(QMainWindow):
    memoria: dict

    def __init__(self, titulo, memoria: dict):
        super().__init__()
        self.memoria = memoria

        uic.loadUi(f'src/GUI/assets/Memoria.ui', self)
        self.setWindowIcon(QtGui.QIcon(self.resource_path('src/GUI/assets/icone.ico')))
        self.setWindowTitle(titulo)


        # region Formata a tabela

        self.num_linhas = self.tableWidget.rowCount()
        self.num_colunas = self.tableWidget.columnCount()
        self.tableWidget.setHorizontalHeaderLabels([hex(i)[-1].upper() for i in range(self.num_colunas)])
        self.tableWidget.setVerticalHeaderLabels(['0x' + hex(i).split('x')[1].upper().zfill(2) + 'X' for i in range(self.num_linhas)])
        self.preenche_tabela(memoria)
        self.tableWidget.resizeColumnsToContents()
        self.ajusta_janela()

        self.secret_feature = QShortcut(QKeySequence('Esc'), self)
        self.secret_feature.activated.connect(self.close)
        self.tableWidget.itemChanged.connect(self.on_changed)
        self.tableWidget.itemActivated.connect(self.user_change)
        self.actionZero.triggered.connect(self.zerar_memoria)
        self.actionSalvar.triggered.connect(self.salvar_arquivo)
        self.actionCarregar.triggered.connect(self.carregar_arquivo)

        #endregion

    # region Funções de formatação da UI

    def preenche_tabela(self, memoria):
        self.memoria = memoria
        for i in range(self.num_linhas):
            linha = '0x' + hex(i).split('x')[1].upper().zfill(2)
            for j in range(self.num_colunas):
                coluna = hex(j)[-1].upper()
                item = QtWidgets.QTableWidgetItem()
                font = QFont()
                font.setCapitalization(QFont.AllUppercase)
                item.setFont(font)
                item.setText(self.memoria.get(linha).get(coluna))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(i, j, item)

    def ajusta_janela(self):
        self.resize(self.tamanho_da_tabela(self.tableWidget), self.size().height())

    def user_change(self, item):
        coluna = item.column()
        self.tableWidget.resizeColumnToContents(coluna)
        self.resize(self.tamanho_da_tabela(self.tableWidget), self.size().height())

    # endregion


    # region Função de controle

    def resource_path(self,relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def tamanho_da_tabela(self, tabela: QTableWidget):
        tamanho = 0
        for i in range(16):
            tamanho += tabela.columnWidth(i)
        return tamanho+65
    
    # endregion

    def on_changed(self, item):
        pass

    def zerar_memoria(self):
        pass

    def salvar_arquivo(self):
        pass

    def carregar_arquivo(self):
        pass

