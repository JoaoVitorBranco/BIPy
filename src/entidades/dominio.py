from typing import List


class Dominio:
    HEXADECIMAL: List[str] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    
    @staticmethod
    def valida_4bit(valor: str) -> bool:
        if len(valor) != 4:
            return False
        for i in valor:
            if i not in Dominio.HEXADECIMAL:
                return False
        return True
    
    @staticmethod
    def valida_bit(valor: str) -> bool:
        if len(valor) != 1:
            return False
        if valor not in Dominio.HEXADECIMAL:
            return False
        return True
    
    @staticmethod
    def soma(v1: str, v2: str) -> str:
        valor = hex(int(v1, 16) + int(v2, 16))[2:].upper()
        if(len(valor) == 5):
            return valor[1:]
        return valor.zfill(4)
    
    @staticmethod
    def subtracao(v1: str, v2: str) -> str:
        v1_int = int(v1, 16)
        v2_int = int(v2, 16)
        
        if(v1_int > v2_int): 
            return hex(v1_int - v2_int)[2:].upper().zfill(4)
        elif(v1_int < v2_int): 
            return hex(int("10000", 16) - (v2_int - v1_int))[2:].upper().zfill(4)
        else: return "0000"