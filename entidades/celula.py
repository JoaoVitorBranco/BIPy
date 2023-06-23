from typing import List


class Celula:
    endereco_col: str
    endereco_val: str
    valor: str
    hexadecimal: List[str] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'E', 'F']
    
    def __init__(self, endereco: str = "0000", valor: str = None):
        pass