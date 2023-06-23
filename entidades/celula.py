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