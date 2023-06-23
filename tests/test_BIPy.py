import pytest
from BIPy import BIPy
from entidades.celula import Celula
from memoria.memoria_mock import MemoriaMock


class Test_BIPy:
    def test_constructor(self):
        memoria_mock = MemoriaMock()
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        assert processador.acc == "0000"
        assert processador.comparacao.value == "SEM_COMPARACAO"
        assert processador.pc == "0000"
        assert processador.instrucao == Celula(endereco="0x000", valor=memoria_mock.ler_celula("0x000"))
        assert processador.memoria_de_programa.memoria == memoria_mock.memoria
        assert processador.memoria_de_dados.memoria == memoria_mock.memoria
        
    def test_valor_em_endereco(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        assert processador.valor_em_endereco("000") == "0x000"
        assert processador.valor_em_endereco("00F") == "0x00F"
        assert processador.valor_em_endereco("0F0") == "0x0F0"
        assert processador.valor_em_endereco("F00") == "0xF00"
        
    def test_HLT(self):
        memoria_mock = MemoriaMock()
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.HLT(valor="000")
        assert processador.instrucao == Celula(endereco="0x000", valor=memoria_mock.ler_celula("0x000"))
        assert processador.acc == "0000"
        assert processador.pc == "0000"
        assert processador.comparacao.value == "SEM_COMPARACAO"
        
    # def test_LDI(self):
    #     memoria_mock = MemoriaMock()
    #     memoria_mock.altera_celula("0x001", "0456")
    #     processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
    #     processador.LDI(valor="123")
    #     assert processador.instrucao.endereco == "0x001"
    #     assert processador.instrucao.valor == "0456"
    #     assert processador.acc == "0123"
    #     assert processador.pc == "0001"
    #     assert processador.comparacao.value == "SEM_COMPARACAO"