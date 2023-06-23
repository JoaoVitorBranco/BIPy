from memoria.memoria_mock import MemoriaMock


class Test_MemoriaMock:
    def test_memoria_mock(self):
        memoria = MemoriaMock()
        assert len(memoria.memoria) == 16**3
        assert memoria.memoria["0x000"] == "0000"
        assert memoria.memoria["0xFFF"] == "0000"
        assert memoria.memoria["0xA2D"] == "0000"
        assert memoria.memoria["0x1C3"] == "0000"
        