from typing import Dict, List

from entidades.celula import Celula
from enum.comparacao_enum import ComparacaoEnum
from erros.erro_de_processador import ErroDeProcessador
from memoria.memoria_interface import MemoriaInterface


class BIPy:
    acc: str
    pc: int
    memoria_de_programa: MemoriaInterface
    memoria_de_dados: MemoriaInterface
    instrucao: Celula
    comparacao: ComparacaoEnum
    dict_assemblador : Dict[str, str] = {
        "HLT": "0",
        "STO": "1",
        "LD": "2",
        "LDI": "3",
        "ADD": "4",
        "ADDI": "5",
        "SUB": "6",
        "SUBI": "7",
        "JUMP": "8",
        "NOP": "9",
        "CMP": "A",
        "JNE": "B",
        "JL": "C",
        "JG": "D"
    }
    
    def __init__(self, memoria_de_programa: MemoriaInterface, memoria_de_dados: MemoriaInterface):
        self.memoria_de_programa = memoria_de_programa
        self.memoria_de_dados = memoria_de_dados
        self.reset()
        
    def reset(self):
        self.acc = "0000"
        self.pc = 0
        self.instrucao = Celula(endereco="0x000", valor=self.memoria_de_programa.ler_celula("0x000")) 
        self.comparacao = ComparacaoEnum.SEM_COMPARACAO
    
    def executa_comando(self):
        dict_assemblador_inv = {v: k for k, v in self.dict_assemblador.items()}
        comando = Celula.pega_comando()
        valor = Celula.pega_valor()
        
        if(comando not in dict_assemblador_inv.keys()):
            raise ErroDeProcessador(metodo="executa_comando", mensagem=f"comando {comando} não existe")
        elif(comando == "0"):
            self.HLT()
        else:
            if(comando == "1"):
                self.STO()
            elif(comando == "2"):
                self.LD()
            elif(comando == "3"):
                self.LDI()
            elif(comando == "4"):
                self.ADD()
            elif(comando == "5"):
                self.ADDI()
            elif(comando == "6"):
                self.SUB()
            elif(comando == "7"):
                self.SUBI()
            elif(comando == "8"):
                self.JUMP()
            elif(comando == "9"):
                self.NOP()
            elif(comando == "A"):
                self.CMP()
            elif(comando == "B"):
                self.JNE()
            elif(comando == "C"):
                self.JL()
            elif(comando == "D"):
                self.JG()
            # aumenta em 1 o endereço da instrução
            
    def HLT(self):
        pass
    
    def STO(self):
        pass
    
    def LD(self):
        pass
    
    def LDI(self):
        pass
    
    def ADD(self):
        pass
    
    def ADDI(self):
        pass
    
    def SUB(self):
        pass
    
    def SUBI(self):
        pass
    
    def JUMP(self):
        pass
    
    def NOP(self):
        pass
    
    def CMP(self):
        pass
    
    def JNE(self):
        pass
    
    def JL(self):
        pass
    
    def JG(self):
        pass
    
    

    