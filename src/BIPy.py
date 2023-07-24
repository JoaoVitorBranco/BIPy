from typing import Dict, List

from src.entidades.celula import Celula
from src.enums.comparacao_enum import ComparacaoEnum
from src.entidades.dominio import Dominio
from src.memoria.repo.memoria_interface import MemoriaInterface
from src.shared.erros.erro_de_processador import ErroDeProcessador


class BIPy:
    acc: str
    pc: str
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
    dict_assemblador_inv : Dict[str, str]
    
    def __init__(self, memoria_de_programa: MemoriaInterface, memoria_de_dados: MemoriaInterface):
        self.memoria_de_programa = memoria_de_programa
        self.memoria_de_dados = memoria_de_dados
        self.dict_assemblador_inv = {v: k for k, v in self.dict_assemblador.items()}
        self.reset()
    
    def reset(self):
        self.acc = "0000"
        self.pc = "0000"
        self.instrucao = Celula(endereco="0x000", valor=self.memoria_de_programa.ler_celula("0x000")) 
        self.comparacao = ComparacaoEnum.SEM_COMPARACAO
        
    def altera_memoria_de_dados(self, nova_memoria: dict) -> None:
        nova_memoria_de_dados = dict()
        for linha, dict_linha in nova_memoria.items():
            for coluna, valor in dict_linha.items():
                if(len(valor) != 4):
                    raise ErroDeProcessador(metodo="altera_memoria_de_programa", mensagem=f"Valor deve ser 4 digitos")
                nova_memoria_de_dados[f"{linha}{coluna}"] = valor

        self.memoria_de_dados.altera_todas_as_celulas(nova_memoria_de_dados)
        
    def altera_memoria_de_programa(self, nova_memoria: dict):
        nova_memoria_de_programa = dict()
        for linha, dict_linha in nova_memoria.items():
            for coluna, valor in dict_linha.items():
                comando_e_valor = valor.split()
                comando_em_hex = self.dict_assemblador.get(comando_e_valor[0])
                if(comando_em_hex == None):
                    raise ErroDeProcessador(metodo="altera_memoria_de_programa", mensagem=f"Comando {comando_e_valor[0]} não existe")
                    
                valor_formatado = f'{comando_em_hex}{comando_e_valor[1]}'
                nova_memoria_de_programa[f"{linha}{coluna}"] = valor_formatado

        self.memoria_de_programa.altera_todas_as_celulas(nova_memoria_de_programa)
        
    def altera_memoria_de_dados_com_cdm(self, cdm: List[str]) -> None:
        indexes = [
            "0x" + Dominio.HEXADECIMAL[i] + Dominio.HEXADECIMAL[j] + Dominio.HEXADECIMAL[k]
            for i in range(0, 16)
            for j in range(0, 16)
            for k in range(0, 16)
        ]
        i = 0
        nova_memoria_de_dados = dict()
        for val in cdm:
            valor_a_inserir = val.split(" ")[2].replace('\n', '')
            while len(valor_a_inserir) < 4:
                valor_a_inserir = "0" + valor_a_inserir
            nova_memoria_de_programa[indexes[i]] = valor_a_inserir
            i += 1
        while(i != len(indexes)):
            nova_memoria_de_dados[indexes[i]] = "0000"
            i += 1
        self.memoria_de_dados.altera_todas_as_celulas(nova_memoria_de_dados)
        self.memoria_de_dados.salvar_em_json()

    def altera_memoria_de_programa_com_cdm(self, cdm: List[str]) -> None:
        indexes = [
            "0x" + Dominio.HEXADECIMAL[i] + Dominio.HEXADECIMAL[j] + Dominio.HEXADECIMAL[k]
            for i in range(0, 16)
            for j in range(0, 16)
            for k in range(0, 16)
        ]
        i = 0
        nova_memoria_de_programa = dict()
        for val in cdm:
            valor_a_inserir = val.split(" ")[2].replace('\n', '')
            while len(valor_a_inserir) < 4:
                valor_a_inserir = "0" + valor_a_inserir
            nova_memoria_de_programa[indexes[i]] = valor_a_inserir
            i += 1
        while(i != len(indexes)):
            nova_memoria_de_programa[indexes[i]] = "0000"
            i += 1
        self.memoria_de_programa.altera_todas_as_celulas(nova_memoria_de_programa)
        self.memoria_de_programa.salvar_em_json()

    def limpa_memorias(self) -> None:
        self.limpa_memoria_de_dados()
        self.limpa_memoria_de_programa()    
        self.reset()
    
    def valor_em_endereco(self, valor) -> str:
        return f"0x{valor}"
    
    def limpa_memoria_de_dados(self) -> None:
        self.memoria_de_dados.limpa_memoria()
        
    def limpa_memoria_de_programa(self) -> None:
        self.memoria_de_programa.limpa_memoria()
        
    
    def pega_memoria_de_dados(self) -> dict:
        memoria_de_dados = dict()
        for i in Dominio.HEXADECIMAL:
            for j in Dominio.HEXADECIMAL:
                linha = dict()
                for k in Dominio.HEXADECIMAL:
                    linha[k] = self.memoria_de_dados.ler_celula(endereco=f"0x{i}{j}{k}")
                memoria_de_dados[f"0x{i}{j}"] = linha
        return memoria_de_dados

    def pega_memoria_de_programa(self) -> dict:
        memoria_de_programa_traduzida = dict()
        for i in Dominio.HEXADECIMAL:
            for j in Dominio.HEXADECIMAL:
                linha = dict()
                for k in Dominio.HEXADECIMAL:
                    valor = self.memoria_de_programa.ler_celula(endereco=f"0x{i}{j}{k}")
                    comando = self.dict_assemblador_inv.get(valor[0])
                    if (comando == None):
                        raise ErroDeProcessador(metodo="pega_memoria_de_programa", mensagem=f"Comando {valor} não existe")
                    linha[k] = comando + ' ' + valor[1:]
                memoria_de_programa_traduzida[f"0x{i}{j}"] = linha
        return memoria_de_programa_traduzida

    def memoria_de_dados_para_cdm(self, caminho:str, nome_do_arquivo:str=None) -> None:
        self.memoria_de_dados.salvar_em_cdm(caminho=caminho, nome=nome_do_arquivo)

    def memoria_de_programa_para_cdm(self, caminho:str, nome_do_arquivo:str=None) -> None:
        self.memoria_de_programa.salvar_em_cdm(caminho=caminho, nome=nome_do_arquivo)
        
    def salva_memorias(self):
        self.memoria_de_programa.salvar_em_json()
        self.memoria_de_dados.salvar_em_json()
    
    def executa_comando(self) -> None:
        comando = self.instrucao.pega_comando()
        valor = self.instrucao.pega_valor()
        
        if(comando not in self.dict_assemblador_inv.keys()):
            raise ErroDeProcessador(metodo="executa_comando", mensagem=f"comando {comando} não existe")
        elif(comando == "0"):
            self.HLT(valor=valor)
        else:
            self.instrucao.proximo_endereco()
            self.instrucao.altera_valor(valor=self.memoria_de_programa.ler_celula(self.instrucao.endereco))
            self.pc = Dominio.soma(v1=self.pc, v2="0001")
            if(comando == "1"):
                self.STO(valor=valor)
            elif(comando == "2"):
                self.LD(valor=valor)
            elif(comando == "3"):
                self.LDI(valor=valor)
            elif(comando == "4"):
                self.ADD(valor=valor)
            elif(comando == "5"):
                self.ADDI(valor=valor)
            elif(comando == "6"):
                self.SUB(valor=valor)
            elif(comando == "7"):
                self.SUBI(valor=valor)
            elif(comando == "8"):
                self.JUMP(valor=valor)
            elif(comando == "9"):
                self.NOP(valor=valor)
            elif(comando == "A"):
                self.CMP(valor=valor)
            elif(comando == "B"):
                self.JNE(valor=valor)
            elif(comando == "C"):
                self.JL(valor=valor)
            elif(comando == "D"):
                self.JG(valor=valor)
         
       
    def HLT(self, valor: str):
        pass
    
    def STO(self, valor: str):
        self.memoria_de_dados.altera_celula(endereco=self.valor_em_endereco(valor), valor=self.acc)
    
    def LD(self, valor: str):
        self.acc = self.memoria_de_dados.ler_celula(endereco=self.valor_em_endereco(valor))
    
    def LDI(self, valor:str):
        self.acc = "0" + valor
    
    def ADD(self, valor:str):
        self.acc = Dominio.soma(v1=self.acc, v2=self.memoria_de_dados.ler_celula(endereco=self.valor_em_endereco(valor)))
    
    def ADDI(self, valor: str):
        self.acc = Dominio.soma(v1=self.acc, v2="0" + valor)
    
    def SUB(self, valor: str):
        self.acc = Dominio.subtracao(v1=self.acc, v2=self.memoria_de_dados.ler_celula(endereco=self.valor_em_endereco(valor)))
    
    def SUBI(self, valor: str):
        self.acc = Dominio.subtracao(v1=self.acc, v2="0" + valor)
    
    def JUMP(self, valor: str):
        self.instrucao.altera_endereco(endereco=self.valor_em_endereco(valor))
        self.instrucao.altera_valor(valor=self.memoria_de_programa.ler_celula(self.instrucao.endereco))
    
    def NOP(self, valor: str):
        pass
    
    def CMP(self, valor: str):
        valor_a_comparar = self.memoria_de_dados.ler_celula(endereco=self.valor_em_endereco(valor))
        acc_int = int(self.acc, 16)
        comparacao_int = int(valor_a_comparar, 16)
        
        if(acc_int > comparacao_int):
            self.comparacao = ComparacaoEnum.MAIOR
        elif(acc_int < comparacao_int):
            self.comparacao = ComparacaoEnum.MENOR
        else:
            self.comparacao = ComparacaoEnum.IGUAL
    
    def JNE(self, valor: str):
        if(self.comparacao.value != "IGUAL"):
            self.instrucao.altera_endereco(endereco=self.valor_em_endereco(valor))
            self.instrucao.altera_valor(valor=self.memoria_de_programa.ler_celula(self.instrucao.endereco))
    
    def JL(self, valor: str):
        if(self.comparacao.value == "MENOR"):
            self.instrucao.altera_endereco(endereco=self.valor_em_endereco(valor))
            self.instrucao.altera_valor(valor=self.memoria_de_programa.ler_celula(self.instrucao.endereco))
    
    def JG(self, valor: str):
        if(self.comparacao.value == "MAIOR"):
            self.instrucao.altera_endereco(endereco=self.valor_em_endereco(valor))
            self.instrucao.altera_valor(valor=self.memoria_de_programa.ler_celula(self.instrucao.endereco))
    
    

