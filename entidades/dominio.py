from typing import List


class Dominio:
    HEXADECIMAL: List[str] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    
    @staticmethod
    def valida_4bit(valor: str):
        if len(valor) != 4:
            return False
        for i in valor:
            if i not in Dominio.HEXADECIMAL:
                return False
        return True
    
    @staticmethod
    def valida_bit(valor: str):
        if len(valor) != 1:
            return False
        if valor not in Dominio.HEXADECIMAL:
            return False
        return True