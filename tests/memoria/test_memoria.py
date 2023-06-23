import pytest
from erros.erro_de_memoria import ErroDeMemoria
from memorias.memoria import Memoria



class Test_Memoria:
    def test_memoria(self):
        memoria = Memoria(nome_da_memoria="Memoria de teste")
        assert memoria.le_nome() == "Memoria de teste"
        
        valores_na_memoria = memoria.le_valores()
        assert valores_na_memoria == memoria.MEMORIA_ZERADA
        assert len(valores_na_memoria) == 16*16*16
        assert valores_na_memoria["FFF"] == "0000"
        assert valores_na_memoria["F2A"] == "0000"
        assert valores_na_memoria["000"] == "0000"
        
    def test_memoria_2(self):
        memoria = Memoria()
        assert memoria.le_nome() == "Memoria"
        
    def le_valor(self):
        memoria = Memoria()
        valor = memoria.le_valor("FFF")
        assert valor == "0000"
        
    def le_valor_2(self):
        memoria = Memoria()
        with pytest.raises(ErroDeMemoria):
            pass
    
        
    
        
        