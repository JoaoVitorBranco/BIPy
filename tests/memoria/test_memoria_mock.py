from src.entidades.dominio import Dominio
from src.memoria.repo.memoria_mock import MemoriaMock


class Test_MemoriaMock:
    def test_memoria_mock(self):
        memoria = MemoriaMock()
        assert len(memoria.memoria) == 16**3
        assert memoria.memoria["0x000"] == "0000"
        assert memoria.memoria["0xFFF"] == "0000"
        assert memoria.memoria["0xA2D"] == "0000"
        assert memoria.memoria["0x1C3"] == "0000"
        
    def test_memoria_ler_e_altera_celula(self):
        memoria = MemoriaMock()
        assert memoria.ler_celula("0x000") == "0000" 
        
        memoria.altera_celula("0x000", "ABCD")
        assert memoria.ler_celula("0x000") == "ABCD"
        
    def test_memoria_ler_todas_as_celulas(self):
        memoria = MemoriaMock()
        assert memoria.memoria == memoria.ler_todas_as_celulas()
        
    def test_memoria_altera_todas_as_celulas(self):
        memoria = MemoriaMock()
        nova_memoria = {
            "0x" + Dominio.HEXADECIMAL[i] + Dominio.HEXADECIMAL[j] + Dominio.HEXADECIMAL[k]: "ACDC"
            for i in range(0, 16)
            for j in range(0, 16)
            for k in range(0, 16)
        }
        memoria.altera_todas_as_celulas(nova_memoria)
        
        assert len(memoria.memoria) == 16**3
        assert memoria.memoria["0x000"] == "ACDC"
        assert memoria.memoria["0xFFF"] == "ACDC"
        assert memoria.memoria["0xA2D"] == "ACDC"
        assert memoria.memoria["0x1C3"] == "ACDC"
        
    def test_limpa_memoria(self):
        memoria = MemoriaMock()
        nova_memoria = {
            "0x" + Dominio.HEXADECIMAL[i] + Dominio.HEXADECIMAL[j] + Dominio.HEXADECIMAL[k]: "ACDC"
            for i in range(0, 16)
            for j in range(0, 16)
            for k in range(0, 16)
        }
        memoria.altera_todas_as_celulas(nova_memoria)
        memoria.limpa_memoria()
        assert len(memoria.memoria) == 16**3
        assert memoria.memoria["0x000"] == "0000"
        assert memoria.memoria["0xFFF"] == "0000"
        assert memoria.memoria["0xA2D"] == "0000"
        assert memoria.memoria["0x1C3"] == "0000"
        
        
