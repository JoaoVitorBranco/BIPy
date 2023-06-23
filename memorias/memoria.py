from typing import Dict

from erros.erro_de_memoria import ErroDeMemoria

class Memoria:
    __hexadecimal = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    MEMORIA_ZERADA: Dict[str,str]
    __valores: Dict[str,str]
    __nome_da_memoria: str

    def __init__(self, nome_da_memoria: str = "Memoria"):
        self.MEMORIA_ZERADA = {}
        for i in self.__hexadecimal:
            for j in self.__hexadecimal:
                for k in self.__hexadecimal:
                    self.MEMORIA_ZERADA[i+j+k] = "0000"
        self.__valores = self.MEMORIA_ZERADA

        if(type(nome_da_memoria) != str):
            raise ErroDeMemoria(mensagem="O nome da memória deve ser uma string")
        self.__nome_da_memoria = nome_da_memoria
            
    def le_nome(self) -> str:
        """
        Função que retorna o nome da memória.
        """
        return self.__nome_da_memoria
    
    def le_valores(self) -> Dict[str,str]:
        """
        Função que retorna os valores da memória.
        """
        return self.__valores

        
    def le_valor(self, chave: str) -> str:
        """
        Função que retorna o valor da chave passada como parâmetro, levantando um erro caso o valor não possa ser encontrado.
        """
        valor = self.__valores.get(chave)
        if valor == None:
            raise ErroDeMemoria(memoria=self.__nome_da_memoria, mensagem=f"Não foi possível encontrar o valor da chave {chave}")
        return self.__valores.get(keyname=chave)
    
    def mudar_valor(self, chave: str, valor: int) -> int:
        """
        Função que muda o valor da chave passada como parâmetro, retornando -1 se o valor não for encontrado e 1 se for encontrado.
        """
        if(self.__valores.get(chave) is not None):
            self.__valores[chave] = valor
            return 1
        else:
            return -1
        
    def sobrepor_memoria(self, valores: Dict[str,str]):
        """
        Função que sobrepõe os valores da memória com os valores passados como parâmetro, retornando 1 se a operação foi bem sucedida e -1 se não foi.
        """
        
        self.__valores = valores
    
    
    