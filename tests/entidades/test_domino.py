from entidades.dominio import Dominio


class Test_Dominio:
    def test_valida_4bit(self):
        assert Dominio.valida_4bit("A0F0")
        assert Dominio.valida_4bit("0000")
        assert Dominio.valida_4bit("123E")
        assert Dominio.valida_4bit("FFFF")
        assert Dominio.valida_4bit("ACDC")
        
    def test_valida_4bit_tamanho(self):
        assert not Dominio.valida_4bit("000")
        
    def test_valida_4bit_hexadecimal(self):
        assert not Dominio.valida_4bit("0x0A")
        assert not Dominio.valida_4bit("00-A")
        assert not Dominio.valida_4bit("00GA")
        assert not Dominio.valida_4bit("ç000")
        assert not Dominio.valida_4bit("000a")
        