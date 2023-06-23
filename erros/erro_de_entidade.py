from erros.base_error import BaseError


class ErroDeEntidade(BaseError):
    def __init__(self, entidade: str, mensagem: str):
        super().__init__(f'Erro na entidade {entidade}: {mensagem}')