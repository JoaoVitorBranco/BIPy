from erros.base_error import BaseError


class ErroDeProcessador(BaseError):
    def __init__(self, metodo: str, mensagem: str):
        super().__init__(f'Erro no método {metodo}: {mensagem}')