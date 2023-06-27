from typing import Dict
from src.entidades.dominio import Dominio
from src.enums.tipo_de_memoria_enum import TipoDeMemoriaEnum
from src.memoria.repo.memoria_interface import MemoriaInterface
from src.shared.erros.erro_de_memoria import ErroDeMemoria


class MemoriaMock(MemoriaInterface):
    caminho_do_arquivo: str
    nome_do_arquivo: str
    memoria: Dict[str, str] # endereco: valor
        
    def __init__(self, arquivo: TipoDeMemoriaEnum = None):
        self.nome_do_arquivo = "memoria"
        memoria = {
            "0x" + Dominio.HEXADECIMAL[i] + Dominio.HEXADECIMAL[j] + Dominio.HEXADECIMAL[k]: "0000"
            for i in range(0, 16)
            for j in range(0, 16)
            for k in range(0, 16)
        }
        self.memoria = memoria 
        self.arquivo = f"src/memoria/armazenamento/{self.nome_do_arquivo}.json"
        
    def ler_celula(self, endereco: str) -> str:
        if(self.memoria.get(endereco) == None):
            raise ErroDeMemoria("MemoriaJSON", f"Endereço {endereco} não encontrado")
        valor = self.memoria.get(endereco)
        return valor
    
    def altera_celula(self, endereco: str, valor: str) -> None:
        self.memoria[endereco] = valor
    
    def ler_todas_as_celulas(self) -> dict:
        return self.memoria
    
    def altera_todas_as_celulas(self, nova_memoria: dict) -> None:
        self.memoria = nova_memoria
    
    def limpa_memoria(self):
        self.memoria = {
            "0x" + Dominio.HEXADECIMAL[i] + Dominio.HEXADECIMAL[j] + Dominio.HEXADECIMAL[k]: "0000"
            for i in range(0, 16)
            for j in range(0, 16)
            for k in range(0, 16)
        }
    
    def salvar_em_arquivo(self) -> None:
        pass    
