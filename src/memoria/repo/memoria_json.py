from typing import Dict
from src.entidades.dominio import Dominio
from src.enums.tipo_de_memoria_enum import TipoDeMemoriaEnum
from src.memoria.repo.memoria_interface import MemoriaInterface
import json

class MemoriaJSON(MemoriaInterface):
    diretorio: str = "src/memoria/armazenamento"
    arquivo: str
    memoria: Dict[str, str] # endereco: valor
    
    def __init__(self, arquivo: TipoDeMemoriaEnum):
        self.arquivo = arquivo.value
        with open(f"{self.diretorio}/{self.arquivo}.json") as f:
            memoria = json.load(f)
            f.close()
        
        self.memoria = memoria
        
    def ler_celula(self, endereco: str) -> str:
        pass
    
    def altera_celula(self, endereco: str, valor: str):
        pass
    def ler_todas_as_celulas(self) -> dict:
        pass
    
    def altera_todas_as_celulas(self, nova_memoria: dict):
        pass
    
    def limpa_memoria(self):
        pass
    
    def salvar_em_arquivo(self):
        pass    
