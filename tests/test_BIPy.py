from src.BIPy import BIPy
from src.entidades.celula import Celula
from src.memoria.memoria_mock import MemoriaMock


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
        
    def test_LDI(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.LDI(valor="123")
        assert processador.acc == "0123"

    def test_STO(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        assert processador.memoria_de_dados.ler_celula("0x000") == "0000"
        
        processador.LDI(valor="123")
        processador.STO(valor="123")
        assert processador.memoria_de_dados.ler_celula("0x123") == "0123"
        
    def test_LD(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.LDI(valor="123")
        processador.STO(valor="AAA")
        processador.LD(valor="BBB")
        assert processador.acc == "0000"
        
        processador.LD(valor="AAA")
        assert processador.acc == "0123"
        
    def test_ADD_1(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.LDI(valor="123")
        processador.STO(valor="123")
        processador.LDI(valor="456")
        processador.ADD(valor="123")
        assert processador.acc == "0579"
        
    def test_ADD_2(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.LDI(valor="000")
        processador.STO(valor="123")
        processador.LDI(valor="456")
        processador.ADD(valor="123")
        assert processador.acc == "0456"
                
    def test_ADD_3(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.LDI(valor="FFF")
        processador.STO(valor="123")
        processador.LDI(valor="001")
        processador.ADD(valor="123")
        assert processador.acc == "1000"
        
    def test_ADDI_1(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.LDI(valor="123")
        processador.ADDI(valor="123")
        assert processador.acc == "0246"
                
    def test_ADDI_2(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.LDI(valor="000")
        processador.ADDI(valor="123")
        assert processador.acc == "0123"

    def test_ADDI_3(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.LDI(valor="FFF")
        processador.ADDI(valor="002")
        assert processador.acc == "1001"
    
    def test_SUB_1(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.LDI(valor="00F")
        processador.STO(valor="123")
        processador.LDI(valor="014")
        processador.SUB(valor="123")
        assert processador.acc == "0005"
        
    def test_SUB_2(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.LDI(valor="FAF")
        processador.STO(valor="123")
        processador.LDI(valor="FA0")
        processador.SUB(valor="123")
        assert processador.acc == "FFF1"
        
    def test_SUB_3(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.LDI(valor="000")
        processador.STO(valor="123")
        processador.LDI(valor="014")
        processador.SUB(valor="123")
        assert processador.acc == "0014"
        
    def test_SUBI_1(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.LDI(valor="014")
        processador.SUBI(valor="00F")
        assert processador.acc == "0005"
        
    def test_SUBI_2(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.LDI(valor="FA0")
        processador.SUBI(valor="FAF")
        assert processador.acc == "FFF1"
        
    def test_SUBI_3(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.LDI(valor="123")
        processador.SUBI(valor="000")
        assert processador.acc == "0123"
        
    def test_JUMP_1(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.memoria_de_programa.altera_celula("0x123", "0123")
        processador.JUMP(valor="123")
        assert processador.instrucao == Celula(endereco="0x123", valor="0123")
    
    def test_JUMP_2(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.memoria_de_programa.altera_celula("0x000", "ACDC")
        processador.JUMP(valor="000")
        assert processador.instrucao == Celula(endereco="0x000", valor="ACDC")
        
    def test_NOP(self):
        memoria_mock = MemoriaMock()
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.NOP(valor="ACD")
        assert processador.instrucao == Celula(endereco="0x000", valor=memoria_mock.ler_celula("0x000"))
        assert processador.acc == "0000"
        assert processador.pc == "0000"
        assert processador.comparacao.value == "SEM_COMPARACAO"
    
    def test_CMP_maior(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.LDI(valor="123")
        processador.STO(valor="123")
        processador.LDI(valor="456")
        processador.CMP(valor="123")
        assert processador.comparacao.value == "MAIOR"
        
    def test_CMP_menor(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.LDI(valor="F00")
        processador.STO(valor="123")
        processador.LDI(valor="456")
        processador.CMP(valor="123")
        assert processador.comparacao.value == "MENOR"
        
    def test_CMP_igual(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.LDI(valor="000")
        processador.CMP(valor="123")
        assert processador.comparacao.value == "IGUAL"
        
    def test_JNE_certo(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.LDI(valor="123")
        processador.STO(valor="123")
        processador.LDI(valor="456")
        processador.CMP(valor="123")
        processador.memoria_de_programa.altera_celula("0x456", "0456")
        processador.JNE(valor="456")
        assert processador.instrucao == Celula(endereco="0x456", valor="0456")
    
    def test_JNE_errado(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.LD(valor="123")
        processador.CMP(valor="123")
        processador.memoria_de_programa.altera_celula("0x456", "0456")
        processador.JNE(valor="456")
        assert processador.instrucao == Celula(endereco="0x000", valor="0000")
        
    def test_JL_certo(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.LDI(valor="123")
        processador.STO(valor="123")
        processador.LDI(valor="001")
        processador.CMP(valor="123")
        processador.memoria_de_programa.altera_celula("0x456", "0456")
        processador.JL(valor="456")
        assert processador.instrucao == Celula(endereco="0x456", valor="0456")
        
    def test_JL_errado(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.LD(valor="000")
        processador.CMP(valor="123")
        processador.memoria_de_programa.altera_celula("0x456", "0456")
        processador.JL(valor="456")
        assert processador.instrucao == Celula(endereco="0x000", valor="0000")
    
    def test_JG_certo(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.LDI(valor="123")
        processador.STO(valor="123")
        processador.LDI(valor="12F")
        processador.CMP(valor="123")
        processador.memoria_de_programa.altera_celula("0x456", "0456")
        processador.JG(valor="456")
        assert processador.instrucao == Celula(endereco="0x456", valor="0456")
        
    def test_JG_errado(self):
        processador = BIPy(memoria_de_programa=MemoriaMock(), memoria_de_dados=MemoriaMock())
        processador.LD(valor="000")
        processador.CMP(valor="123")
        processador.memoria_de_programa.altera_celula("0x456", "0456")
        processador.JG(valor="456")
        assert processador.instrucao == Celula(endereco="0x000", valor="0000")
        
    def test_executa_comando_HLT(self):
        memoria_de_programa = MemoriaMock()
        memoria_de_programa.altera_celula("0x000", "0ACB")
        
        processador = BIPy(memoria_de_programa=memoria_de_programa, memoria_de_dados=MemoriaMock())
        processador.LDI(valor="AAA")
        processador.executa_comando()
        
        assert processador.instrucao == Celula(endereco="0x000", valor="0ACB")
        assert processador.acc == "0AAA"
        assert processador.pc == "0000"
        assert processador.comparacao.value == "SEM_COMPARACAO"
        
    def test_executa_comando_STO(self):
        memoria_de_programa = MemoriaMock()
        memoria_de_programa.altera_celula("0x000", "1ACB")
        memoria_de_programa.altera_celula("0x001", "ACDC")
        
        processador = BIPy(memoria_de_programa=memoria_de_programa, memoria_de_dados=MemoriaMock())
        processador.LDI(valor="AAA")
        processador.executa_comando()
        
        assert processador.instrucao == Celula(endereco="0x001", valor="ACDC")
        assert processador.acc == "0AAA"
        assert processador.pc == "0001"
        assert processador.comparacao.value == "SEM_COMPARACAO"
        assert processador.memoria_de_dados.ler_celula(endereco="0xACB") == "0AAA"
        
    def test_executa_comando_LD(self):
        memoria_de_programa = MemoriaMock()
        memoria_de_programa.altera_celula("0x000", "2ACB")
        memoria_de_programa.altera_celula("0x001", "ACDC")
        
        memoria_de_dados = MemoriaMock()
        memoria_de_dados.altera_celula("0xACB", "0AAA")
        
        processador = BIPy(memoria_de_programa=memoria_de_programa, memoria_de_dados=memoria_de_dados)
        processador.executa_comando()
        
        assert processador.instrucao == Celula(endereco="0x001", valor="ACDC")
        assert processador.acc == "0AAA"
        assert processador.acc == memoria_de_dados.ler_celula(endereco="0xACB")
        assert processador.pc == "0001"
        assert processador.comparacao.value == "SEM_COMPARACAO"
        
    def test_executa_comando_LDI(self):
        memoria_de_programa = MemoriaMock()
        memoria_de_programa.altera_celula("0x000", "3ACB")
        memoria_de_programa.altera_celula("0x001", "ACDC")
        
        processador = BIPy(memoria_de_programa=memoria_de_programa, memoria_de_dados=MemoriaMock())
        processador.executa_comando()
        
        assert processador.instrucao == Celula(endereco="0x001", valor="ACDC")
        assert processador.acc == "0ACB"
        assert processador.pc == "0001"
        assert processador.comparacao.value == "SEM_COMPARACAO" 
        
    def test_executa_comando_ADD(self):
        memoria_de_programa = MemoriaMock()
        memoria_de_programa.altera_celula("0x000", "4ACB")
        memoria_de_programa.altera_celula("0x001", "ACDC")
        
        memoria_de_dados = MemoriaMock()
        memoria_de_dados.altera_celula("0xACB", "0AAA")
        
        processador = BIPy(memoria_de_programa=memoria_de_programa, memoria_de_dados=memoria_de_dados)
        processador.LDI(valor="AAA")
        processador.executa_comando()
        
        assert processador.instrucao == Celula(endereco="0x001", valor="ACDC")
        assert processador.acc == "1554"
        assert processador.pc == "0001"
        assert processador.comparacao.value == "SEM_COMPARACAO"
        
    def test_executa_comando_ADDI(self):
        memoria_de_programa = MemoriaMock()
        memoria_de_programa.altera_celula("0x000", "5ACB")
        memoria_de_programa.altera_celula("0x001", "ACDC")
        
        processador = BIPy(memoria_de_programa=memoria_de_programa, memoria_de_dados=MemoriaMock())
        processador.LDI(valor="AAA")
        processador.executa_comando()
        
        assert processador.instrucao == Celula(endereco="0x001", valor="ACDC")
        assert processador.acc == "1575"
        assert processador.pc == "0001"
        assert processador.comparacao.value == "SEM_COMPARACAO"
        
    def test_executa_comando_SUB(self):
        memoria_de_programa = MemoriaMock()
        memoria_de_programa.altera_celula("0x000", "6ACB")
        memoria_de_programa.altera_celula("0x001", "ACDC")
        
        memoria_de_dados = MemoriaMock()
        memoria_de_dados.altera_celula("0xACB", "0AAA")
        
        processador = BIPy(memoria_de_programa=memoria_de_programa, memoria_de_dados=memoria_de_dados)
        processador.LDI(valor="ACB")
        processador.executa_comando()
        
        assert processador.instrucao == Celula(endereco="0x001", valor="ACDC")
        assert processador.acc == "0021"
        assert processador.pc == "0001"
        assert processador.comparacao.value == "SEM_COMPARACAO"
        
    def test_executa_comando_SUBI(self):
        memoria_de_programa = MemoriaMock()
        memoria_de_programa.altera_celula("0x000", "714D")
        memoria_de_programa.altera_celula("0x001", "ACDC")
        
        memoria_de_dados = MemoriaMock()
        
        processador = BIPy(memoria_de_programa=memoria_de_programa, memoria_de_dados=memoria_de_dados)
        processador.LDI(valor="AFB")
        processador.executa_comando()
        
        assert processador.instrucao == Celula(endereco="0x001", valor="ACDC")
        assert processador.acc == "09AE"
        assert processador.pc == "0001"
        assert processador.comparacao.value == "SEM_COMPARACAO"
        
    def test_executa_comando_JUMP(self):
        memoria_de_programa = MemoriaMock()
        memoria_de_programa.altera_celula("0x000", "8ACB")
        memoria_de_programa.altera_celula("0xACB", "FFFF")
        
        processador = BIPy(memoria_de_programa=memoria_de_programa, memoria_de_dados=MemoriaMock())
        processador.executa_comando()
        
        assert processador.instrucao == Celula(endereco="0xACB", valor="FFFF")
        assert processador.pc == "0001"
        assert processador.comparacao.value == "SEM_COMPARACAO"
        
    def test_executa_comando_NOP(self):
        memoria_de_programa = MemoriaMock()
        memoria_de_programa.altera_celula("0x000", "9ACB")
        memoria_de_programa.altera_celula("0x001", "ACDC")
        
        processador = BIPy(memoria_de_programa=memoria_de_programa, memoria_de_dados=MemoriaMock())
        processador.executa_comando()
        
        assert processador.instrucao == Celula(endereco="0x001", valor="ACDC")
        assert processador.pc == "0001"
        assert processador.comparacao.value == "SEM_COMPARACAO"
        
    def test_executa_comando_CMP(self):
        memoria_de_programa = MemoriaMock()
        memoria_de_programa.altera_celula("0x000", "AACB")
        memoria_de_programa.altera_celula("0x001", "ACDC")
        
        memoria_de_dados = MemoriaMock()
        memoria_de_dados.altera_celula("0xACB", "0AAA")
        
        processador = BIPy(memoria_de_programa=memoria_de_programa, memoria_de_dados=memoria_de_dados)
        processador.LDI(valor="AA1")
        processador.executa_comando()
        
        assert processador.instrucao == Celula(endereco="0x001", valor="ACDC")
        assert processador.acc == "0AA1"
        assert processador.pc == "0001"
        assert processador.comparacao.value == "MENOR"
        
    def test_executa_comando_JNE(self):
        memoria_de_programa = MemoriaMock()
        memoria_de_programa.altera_celula("0x000", "AACB")
        memoria_de_programa.altera_celula("0x001", "BFFF")
        memoria_de_programa.altera_celula("0xFFF", "FFFF")
        
        memoria_de_dados = MemoriaMock()
        memoria_de_dados.altera_celula("0xACB", "0AAA")

        processador = BIPy(memoria_de_programa=memoria_de_programa, memoria_de_dados=memoria_de_dados)
        processador.LDI(valor="AA1")
        processador.executa_comando()
        processador.executa_comando()
        
        assert processador.instrucao == Celula(endereco="0xFFF", valor="FFFF")
        assert processador.acc == "0AA1"
        assert processador.pc == "0002"
        assert processador.comparacao.value == "MENOR"
        
    def test_executa_comando_JNE_sem_JUMP(self):
        memoria_de_programa = MemoriaMock()
        memoria_de_programa.altera_celula("0x000", "AACB")
        memoria_de_programa.altera_celula("0x001", "BFFF")
        memoria_de_programa.altera_celula("0x002", "0002")
        memoria_de_programa.altera_celula("0xFFF", "FFFF")
        
        memoria_de_dados = MemoriaMock()
        memoria_de_dados.altera_celula("0xACB", "0AAA")

        processador = BIPy(memoria_de_programa=memoria_de_programa, memoria_de_dados=memoria_de_dados)
        processador.LDI(valor="AAA")
        processador.executa_comando()
        processador.executa_comando()
        
        assert processador.instrucao == Celula(endereco="0x002", valor="0002")
        assert processador.acc == "0AAA"
        assert processador.pc == "0002"
        assert processador.comparacao.value == "IGUAL"
        
    def test_executa_comando_JL(self):
        memoria_de_programa = MemoriaMock()
        memoria_de_programa.altera_celula("0x000", "AACB")
        memoria_de_programa.altera_celula("0x001", "CFFF")
        memoria_de_programa.altera_celula("0xFFF", "FFFF")
        
        memoria_de_dados = MemoriaMock()
        memoria_de_dados.altera_celula("0xACB", "0AAA")

        processador = BIPy(memoria_de_programa=memoria_de_programa, memoria_de_dados=memoria_de_dados)
        processador.LDI(valor="AA1")
        processador.executa_comando()
        processador.executa_comando()
        
        assert processador.instrucao == Celula(endereco="0xFFF", valor="FFFF")
        assert processador.acc == "0AA1"
        assert processador.pc == "0002"
        assert processador.comparacao.value == "MENOR"
        
    def test_executa_comando_JL_sem_JUMP(self):
        memoria_de_programa = MemoriaMock()
        memoria_de_programa.altera_celula("0x000", "AACB")
        memoria_de_programa.altera_celula("0x001", "CFFF")
        memoria_de_programa.altera_celula("0x002", "0002")
        memoria_de_programa.altera_celula("0xFFF", "FFFF")
        
        memoria_de_dados = MemoriaMock()
        memoria_de_dados.altera_celula("0xACB", "0AAA")

        processador = BIPy(memoria_de_programa=memoria_de_programa, memoria_de_dados=memoria_de_dados)
        processador.LDI(valor="AAA")
        processador.executa_comando()
        processador.executa_comando()
        
        assert processador.instrucao == Celula(endereco="0x002", valor="0002")
        assert processador.acc == "0AAA"
        assert processador.pc == "0002"
        assert processador.comparacao.value == "IGUAL"
        
    def test_executa_comando_JG(self):
        memoria_de_programa = MemoriaMock()
        memoria_de_programa.altera_celula("0x000", "AACB")
        memoria_de_programa.altera_celula("0x001", "DFFF")
        memoria_de_programa.altera_celula("0xFFF", "FFFF")
        
        memoria_de_dados = MemoriaMock()
        memoria_de_dados.altera_celula("0xACB", "0AAA")

        processador = BIPy(memoria_de_programa=memoria_de_programa, memoria_de_dados=memoria_de_dados)
        processador.LDI(valor="F00")
        processador.executa_comando()
        processador.executa_comando()
        
        assert processador.instrucao == Celula(endereco="0xFFF", valor="FFFF")
        assert processador.acc == "0F00"
        assert processador.pc == "0002"
        assert processador.comparacao.value == "MAIOR"
        
    def test_executa_comando_JG_sem_JUMP(self):
        memoria_de_programa = MemoriaMock()
        memoria_de_programa.altera_celula("0x000", "AACB")
        memoria_de_programa.altera_celula("0x001", "DFFF")
        memoria_de_programa.altera_celula("0x002", "0002")
        memoria_de_programa.altera_celula("0xFFF", "FFFF")
        
        memoria_de_dados = MemoriaMock()
        memoria_de_dados.altera_celula("0xACB", "0F00")

        processador = BIPy(memoria_de_programa=memoria_de_programa, memoria_de_dados=memoria_de_dados)
        processador.LDI(valor="AAA")
        processador.executa_comando()
        processador.executa_comando()
        
        assert processador.instrucao == Celula(endereco="0x002", valor="0002")
        assert processador.acc == "0AAA"
        assert processador.pc == "0002"
        assert processador.comparacao.value == "MENOR"