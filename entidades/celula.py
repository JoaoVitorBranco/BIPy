from typing import List
from entidades.dominio import Dominio

from entidades.endereco import Endereco
from erros.erro_de_entidade import ErroDeEntidade


class Celula:
    endereco: Endereco
    valor: str
    
    def __init__(self, endereco: str = "0x000", valor: str = "0000"):
        self.endereco = endereco
        
        if(not Dominio.valida_4bit(valor)):
            raise ErroDeEntidade(entidade="Celula", mensagem=f"valor {valor} deve ter tamanho 4 e ser hexadecimal")
        self.valor = valor
        
    def pega_comando(self) -> str:
        return self.valor[0]
    
    def pega_valor(self) -> str:
        return self.valor[1:]
    
    def proximo_endereco(self):
        endereco_int = int(self.endereco[2:], 16)
        endereco_int += 1
        novo_endereco = hex(endereco_int)[2:].upper()
        if(len(novo_endereco) == 4):
            raise ErroDeEntidade(entidade="Celula", mensagem=f"endereço {novo_endereco} não pode ser maior que 0xFFF")
        self.endereco = "0x"+novo_endereco.zfill(3)
        
    def altera_valor(self, valor: str):
        self.valor = valor
            
    def altera_endereco(self, endereco: str):
        self.endereco = endereco
        
    def __eq__(self, other) -> bool:
        return self.valor == other.valor and self.endereco == other.endereco