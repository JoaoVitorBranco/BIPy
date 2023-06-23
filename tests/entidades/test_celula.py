import pytest
from entidades.celula import Celula
from erros.erro_de_entidade import ErroDeEntidade


class Test_Celula:
    def test_celula_1(self):
        celula = Celula(endereco="0xABC", valor="ACDC")
        assert celula.endereco == "0xABC"
        assert celula.valor == "ACDC"
        
    def test_celula_2(self): 
        celula = Celula()
        assert celula.endereco == "0x000"
        assert celula.valor == "0000"
        
    def test_celula_valor_errado(self):
        with pytest.raises(ErroDeEntidade):
            celula = Celula(endereco="0xABC", valor="ACD")
        