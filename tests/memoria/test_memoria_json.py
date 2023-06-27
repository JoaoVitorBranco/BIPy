from src.entidades.dominio import Dominio
from src.enums.tipo_de_memoria_enum import TipoDeMemoriaEnum
from src.memoria.repo.memoria_json import MemoriaJSON


class Test_MemoriaMock:
    def test_memoria_mock(self):
        memoria = MemoriaJSON(arquivo=TipoDeMemoriaEnum.MEMORIA_DE_DADOS)
        assert True        
        
