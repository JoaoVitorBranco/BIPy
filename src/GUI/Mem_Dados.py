from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox

from src.GUI.MemInterface import Mem_Interface


class Mem_Dados(Mem_Interface):
    altera_memoria_de_dados: callable
    limpa_memoria: callable
    def __init__(self, memoria_de_dados: dict, altera_memoria_de_dados, limpa_memoria):
        super().__init__(UI_string='MemoriaDados', memoria=memoria_de_dados)

        self.altera_memoria_de_dados = altera_memoria_de_dados
        self.limpa_memoria = limpa_memoria
        self.tipos_de_arquivo = "Arquivo CedarLogic (*.cdm);; Arquivo de Texto (*.txt)"

        for i in range(self.num_colunas):
            delegate = StyledItemDelegate(self.tableWidget)
            self.tableWidget.setItemDelegateForColumn(i, delegate)

        # region Designando funções aos botões

        self.actionZero.triggered.connect(self.zerar_memoria)
        self.actionSalvar.triggered.connect(self.salvar_arquivo)
        self.actionCarregar.triggered.connect(self.carregar_arquivo)

        # endregion

    # region Funções de controle

    def on_changed(self, item):
        linha = item.row()
        coluna = item.column()
        valor = item.text()
        celula = f'0x{linha:02X}{coluna:X}'

        self.altera_memoria_de_dados(celula, valor)

    def zerar_memoria(self):
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon(self.resource_path('src/GUI/assets/icone.ico')))
            msg.setWindowTitle("Zerar memória")
            msg.setIcon(QMessageBox.Question)
            msg.addButton('Sim', QMessageBox.YesRole)
            msg.addButton('Não', QMessageBox.NoRole)        
            msg.setText('Certeza que quer zerar a memória? ')
            msg.exec_()
            resposta = msg.buttonRole(msg.clickedButton())

            if resposta == QMessageBox.YesRole:
                self.limpa_memoria()
                qm = QMessageBox()
                qm.setWindowTitle("Zerar memória")
                qm.setText("Memória zerada")
                qm.setWindowIcon(QtGui.QIcon(self.resource_path('src/GUI/assets/icone.ico')))
                qm.setIcon(QMessageBox.Information)
                qm.exec_()

    def salvar_arquivo(self):
        nome , _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Salvar arquivo', '', self.tipos_de_arquivo)
        try:
            arquivo = open(nome, 'w')
            texto = 'fodase'
            arquivo.write(texto)
            arquivo.close()
        except(FileNotFoundError):
            print("Arquivo não encontrado")

    def carregar_arquivo(self):
        nome , _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Abrir Arquivo', '', self.tipos_de_arquivo)
        try:
            arquivo = open(nome, 'r')
        
            with arquivo:
                texto = arquivo.read()
            print(texto)
        except(FileNotFoundError):
            print("Arquivo não encontrado")

    #endregion

class StyledItemDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QtWidgets.QLineEdit):
            regex = f"^[0-9A-Fa-f]{'{4}'}$"
            regex = r"{}".format(regex)
            validator = QtGui.QRegExpValidator(
                QtCore.QRegExp(regex, cs=QtCore.Qt.CaseInsensitive), editor,
            )
            editor.setValidator(validator)

        complete = QtWidgets.QCompleter(editor)
        editor.setCompleter(complete)

        return editor
