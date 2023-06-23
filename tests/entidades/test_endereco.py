import pytest
from entidades.endereco import Endereco
from src.shared.erros.erro_de_entidade import ErroDeEntidade


class Test_Dominio:
    def test_construtor_1(self):
        endereco = Endereco()
        assert endereco.linha == "0x00"
        assert endereco.coluna == "0"
        
    def test_construtor_2(self):
        endereco = Endereco("0xAB", "F")
        assert endereco.linha == "0xAB"
        assert endereco.coluna == "F"
        
    def test_construtor_linha_deve_ser_string(self):
        with pytest.raises(ErroDeEntidade):
            endereco = Endereco(0, "F")
            
    def test_construtor_linha_deve_ter_tamanho_4(self):
        with pytest.raises(ErroDeEntidade):
            endereco = Endereco("0xFFFFF", "F")
            
    def test_construtor_linha_primeiro_caractere(self):
        with pytest.raises(ErroDeEntidade):
            endereco = Endereco("FxFF", "F")
    
    def test_construtor_linha_segundo_caractere(self):
        with pytest.raises(ErroDeEntidade):
            endereco = Endereco("00FA", "F")
            
    def test_construtor_linha_terceiro_caractere(self):
        with pytest.raises(ErroDeEntidade):
            endereco = Endereco("0xGA", "F")
            
    def test_construtor_linha_quarto_caractere(self):
        with pytest.raises(ErroDeEntidade):
            endereco = Endereco("0xFG", "F")
            
    def test_construtor_coluna(self):
        with pytest.raises(ErroDeEntidade):
            endereco = Endereco("0xFF", "G")
            
    def test_valor_1(self):
        endereco = Endereco("0xAB", "F")
        assert endereco.valor() == "0xABF"
        
    def test_valor_2(self):
        endereco = Endereco()
        assert endereco.valor() == "0x000"   
