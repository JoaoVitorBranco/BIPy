from abc import ABC, abstractmethod


class MemoriaInterface(ABC):
    
    @abstractmethod
    def ler_celula(endereco: str) -> str:
        pass
    
    @abstractmethod
    def altera_celula(endereco: str, valor: str):
        pass
    
    @abstractmethod
    def ler_todas_as_celulas() -> dict:
        pass
    
    @abstractmethod
    def altera_todas_as_celulas(dicionario: dict):
        pass
    
    @abstractmethod
    def limpa_memoria():
        pass
    
    @abstractmethod
    def salvar_em_arquivo():
        pass
    
    