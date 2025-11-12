from ..Estado import Estado


class ConfirmadoPorPersonal(Estado):
    """Estado ConfirmadoPorPersonal: evento confirmado manualmente por personal."""

    def __init__(self, ambito=None):
        super().__init__("ConfirmadoPorPersonal", ambito)
    # Esta clase define sólo la identidad del estado; la transición a
    # 'Cerrado' se omite porque no hay llamadas estáticas a `cerrar` en el
    # repositorio. Si en el futuro la transición se usa, reimplementar aquí.
