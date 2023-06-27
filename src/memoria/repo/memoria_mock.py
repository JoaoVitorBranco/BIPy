from typing import Dict
from src.entidades.dominio import Dominio
from src.enums.tipo_de_memoria_enum import TipoDeMemoriaEnum
from src.memoria.repo.memoria_interface import MemoriaInterface


class MemoriaMock(MemoriaInterface):
    diretorio: str = "src/memoria/armazenamento"
    arquivo: str
    memoria: Dict[str, str] # endereco: valor
        
    def __init__(self, arquivo: TipoDeMemoriaEnum = None):
        memoria = {
            "0x" + Dominio.HEXADECIMAL[i] + Dominio.HEXADECIMAL[j] + Dominio.HEXADECIMAL[k]: "0000"
            for i in range(0, 16)
            for j in range(0, 16)
            for k in range(0, 16)
        }
        self.memoria = memoria 
        self.arquivo = "memoria.json"
        
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
