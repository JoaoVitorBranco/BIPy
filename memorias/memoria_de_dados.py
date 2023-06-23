from memorias.memoria import Memoria


class MemoriaDeDados(Memoria):
    __valores: dict = {}
    
    def __init__(self, valores: dict = None):
        super().__init__(valores=valores)
        
    


    