from abc import ABC, abstractmethod


class MemoriaInterface(ABC):
    diretorio: str
    
    @abstractmethod
    def ler_celula(self, endereco: str) -> str:
        pass
    
    @abstractmethod
    def altera_celula(self, endereco: str, valor: str):
        pass
    
    @abstractmethod
    def ler_todas_as_celulas(self) -> dict:
        pass
    
    @abstractmethod
    def altera_todas_as_celulas(self, dicionario: dict):
        pass
    
    @abstractmethod
    def limpa_memoria(self):
        pass
    
    @abstractmethod
    def salvar_em_arquivo(self):
        pass    
    
    