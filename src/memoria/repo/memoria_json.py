from typing import Dict
from src.entidades.dominio import Dominio
from src.enums.tipo_de_memoria_enum import TipoDeMemoriaEnum
from src.memoria.repo.memoria_interface import MemoriaInterface
import json

from src.shared.erros.erro_de_memoria import ErroDeMemoria

class MemoriaJSON(MemoriaInterface):
    _diretorio: str = "src/memoria/armazenamento"
    caminho_do_arquivo: str
    nome_do_arquivo: str
    memoria: Dict[str, str] # endereco: valor
    
    def __init__(self, arquivo: TipoDeMemoriaEnum = None):
        if(type(arquivo) == None):
            raise ErroDeMemoria("MemoriaJSON", "Deve ser inserido um tipo de memória")
        if(type(arquivo) != TipoDeMemoriaEnum):
            raise ErroDeMemoria("MemoriaJSON", "Tipo de 'arquivo' está inválido")
        
        self.nome_do_arquivo = arquivo.value
        self.caminho_do_arquivo = f"{self._diretorio}/{self.nome_do_arquivo}.json"
        with open(self.caminho_do_arquivo) as f:
            memoria = json.load(f)
            f.close()
        self.memoria = memoria
        
    def ler_celula(self, endereco: str) -> str:
        if(self.memoria.get(endereco) == None):
            raise ErroDeMemoria("MemoriaJSON", f"Endereço {endereco} não encontrado")
        valor = self.memoria.get(endereco)
        return valor
    
    def altera_celula(self, endereco: str, valor: str) -> None:
        self.memoria[endereco] = valor
        # with open(self.caminho_do_arquivo, 'w') as f:
        #     json.dump(self.memoria, f, indent=4)
    
    def salvar(self):
        with open(self.caminho_do_arquivo, 'w') as f:
            json.dump(self.memoria, f, indent=4)

    def ler_todas_as_celulas(self) -> dict:
        return self.memoria
    
    def altera_todas_as_celulas(self, nova_memoria: dict) -> None:
        self.memoria = nova_memoria
        # with open(self.caminho_do_arquivo, 'w') as f:
        #     json.dump(self.memoria, f, indent=4)
    
    def limpa_memoria(self) -> None:
        self.memoria = {
            "0x" + Dominio.HEXADECIMAL[i] + Dominio.HEXADECIMAL[j] + Dominio.HEXADECIMAL[k]: "0000"
            for i in range(0, 16)
            for j in range(0, 16)
            for k in range(0, 16)
        }
        with open(self.caminho_do_arquivo, 'w') as f:
            json.dump(self.memoria, f, indent=4)
    
    def salvar_em_arquivo(self) -> None:
        arquivo = open(f'src/cdm/{self.nome_do_arquivo}.cdm', 'w')
        for idx, value in enumerate(self.memoria.values()):
            arquivo.write(f'{hex(idx).upper()[2:]} : {value}\n')
        arquivo.close()