class WrongLocationException(Exception):

    def __init__(self, message="Указанное местоположение не найдено."):
        self.message = message
        super().__init__(self.message)
