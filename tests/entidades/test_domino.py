from src.entidades.dominio import Dominio


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
        
    def test_soma(self):
        assert Dominio.soma("A0F0", "0000") == "A0F0"
        assert Dominio.soma("0001", "000F") == "0010"
        assert Dominio.soma("0001", "00FF") == "0100"
        assert Dominio.soma("0FFF", "0001") == "1000"
        assert Dominio.soma("FFFF", "0001") == "0000"
        assert Dominio.soma("FFFF", "0009") == "0008"
        assert Dominio.soma("09FF", "0001") == "0A00"
        assert Dominio.soma("000A", "0002") == "000C"
        assert Dominio.soma("0002", "000D") == "000F"
        
    def test_subtracao(self):
        assert Dominio.subtracao("A0F0", "0000") == "A0F0"
        assert Dominio.subtracao("A0F0", "0001") == "A0EF"
        assert Dominio.subtracao("0001", "000F") == "FFF2"
        assert Dominio.subtracao("0001", "00FF") == "FF02"
        assert Dominio.subtracao("0FFF", "0001") == "0FFE"
        assert Dominio.subtracao("FFFF", "0001") == "FFFE"
