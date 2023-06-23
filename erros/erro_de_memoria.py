from erros.base_error import BaseError


class ErroDeMemoria(BaseError):
    def __init__(self, memoria: str, mensagem: str):
        if(memoria == None):
            super().__init__(mensagem)
        else:
            super().__init__(f'Erro na memória {memoria}: {mensagem}')