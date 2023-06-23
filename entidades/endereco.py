from entidades.dominio import Dominio
from src.shared.erros.erro_de_entidade import ErroDeEntidade


class Endereco:
    linha: str # 0x00
    coluna: str # 0
    
    def __init__(self, linha: str = "0x00", coluna: str = "0"):
        if(type(linha) != str): 
            raise ErroDeEntidade(entidade="Endereco", mensagem="linha deve ser uma string")
        if(len(linha) != 4): 
            raise ErroDeEntidade(entidade="Endereco", mensagem="linha deve ter 4 caracteres")
        if(linha[0] != '0'):
            raise ErroDeEntidade(entidade="Endereco", mensagem=f"caractere {linha[0]} da linha deveria ser 0")
        if(linha[1] != 'x'):
            raise ErroDeEntidade(entidade="Endereco", mensagem=f"caractere {linha[1]} da linha deveria ser x")
        if(not Dominio.valida_bit(linha[2])):
            raise ErroDeEntidade(entidade="Endereco", mensagem=f"caractere {linha[2]} da linha deveria ser hexadecimal")
        if(not Dominio.valida_bit(linha[3])):
            raise ErroDeEntidade(entidade="Endereco", mensagem=f"caractere {linha[3]} da linha deveria ser hexadecimal")
        self.linha = linha
        
        if (not Dominio.valida_bit(coluna)): 
            raise ErroDeEntidade(entidade="Endereco", mensagem=f"coluna deveria ser hexadecimal")
        self.coluna = coluna
        
    def valor(self):
        return self.linha + self.coluna
    
    def __eq__(self, other) -> bool:
        return self.valor() == other.valor()
