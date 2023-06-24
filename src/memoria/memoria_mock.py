from src.entidades.dominio import Dominio
from src.memoria.memoria_interface import MemoriaInterface


class MemoriaMock(MemoriaInterface):
    
    def __init__(self, diretorio: str = "memoria/"):
        memoria = {
            "0x" + Dominio.HEXADECIMAL[i] + Dominio.HEXADECIMAL[j] + Dominio.HEXADECIMAL[k]: "0000"
            for i in range(0, 16)
            for j in range(0, 16)
            for k in range(0, 16)
        }
        self.memoria = memoria 
        
    def ler_celula(self, endereco: str) -> str:
        valor = self.memoria[endereco]
        return valor
    
    def altera_celula(self, endereco: str, valor: str):
        self.memoria[endereco] = valor
    
    def ler_todas_as_celulas(self) -> dict:
        return self.memoria
    
    def altera_todas_as_celulas(self, nova_memoria: dict):
        self.memoria = nova_memoria
    
    def limpa_memoria(self):
        self.memoria = {
            "0x" + Dominio.HEXADECIMAL[i] + Dominio.HEXADECIMAL[j] + Dominio.HEXADECIMAL[k]: "0000"
            for i in range(0, 16)
            for j in range(0, 16)
            for k in range(0, 16)
        }
    
    def salvar_em_arquivo(self):
        pass    
