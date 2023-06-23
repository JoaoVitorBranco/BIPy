from entidades.dominio import Dominio
from memoria.memoria_interface import MemoriaInterface


class MemoriaMock(MemoriaInterface):
    def __init__(self):
        memoria = {}
        for i in range(0, 16):
            for j in range(0, 16):
                for k in range(0, 16):
                    memoria["0x"+Dominio.HEXADECIMAL[i]+Dominio.HEXADECIMAL[j]+Dominio.HEXADECIMAL[k]] = "0000"
        self.memoria = memoria 
        
    def ler_celula(endereco: str) -> str:
        pass
    
    def altera_celula(endereco: str, valor: str):
        pass
    
    def ler_todas_as_celulas() -> dict:
        pass
    
    def altera_todas_as_celulas(dicionario: dict):
        pass
    
    def limpa_memoria():
        pass
    
    def salvar_em_arquivo():
        pass    
    