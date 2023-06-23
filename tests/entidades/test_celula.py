import pytest
from entidades.celula import Celula
from src.shared.erros.erro_de_entidade import ErroDeEntidade


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
            
    def test_celula_pega_comando_e_valor(self):
        celula = Celula(endereco="0xABC", valor="ACDC")
        assert celula.pega_comando() == "A"
        assert celula.pega_valor() == "CDC"
        
        celula_2 = Celula()
        assert celula_2.pega_comando() == "0"
        assert celula_2.pega_valor() == "000"
        
    def test_celula_proximo_endereco(self):
        celula = Celula()
        celula.proximo_endereco()
        assert celula.endereco == "0x001"
        
        celula = Celula(endereco="0x00F")
        celula.proximo_endereco()
        assert celula.endereco == "0x010"
        
        celula = Celula(endereco="0x0FF")
        celula.proximo_endereco()
        assert celula.endereco == "0x100"
        
        celula = Celula(endereco="0x09F")
        celula.proximo_endereco()
        assert celula.endereco == "0x0A0"
        
        celula = Celula(endereco="0x0A9")
        celula.proximo_endereco()
        assert celula.endereco == "0x0AA"
        
        celula = Celula(endereco="0xFFE")
        celula.proximo_endereco()
        assert celula.endereco == "0xFFF"
        
        celula = Celula(endereco="0x00A")
        celula.proximo_endereco()
        assert celula.endereco == "0x00B"
        
        celula.proximo_endereco()
        assert celula.endereco == "0x00C"
        
        celula.proximo_endereco()
        assert celula.endereco == "0x00D"
        
        celula.proximo_endereco()
        assert celula.endereco == "0x00E"
        
        celula.proximo_endereco()
        assert celula.endereco == "0x00F"
        
    def test_celula_altera_valor(self):
        celula = Celula(valor="0000")
        celula.altera_valor("0001")
        assert celula.valor == "0001"
        
    def test_celula_altera_endereco(self):
        celula = Celula()
        celula.altera_endereco("0xABC")
        assert celula.endereco == "0xABC"
