

class EinarException(Exception):
    "base exception for Einar."


class EinarError(EinarException):
    def __init__(self, mensage):
        super().__init__(mensage)
        self.mensage = mensage
