class Error(Exception):
    def __init__(self, message=None):
        if message is None:
            self.message = self.__doc__
        else:
            self.message = message
        super().__init__(self.message)


class NotAuthenticatedException(Error):
    pass


class DeletingModeException(Error):
    """Для работы в режиме удаления установите delete_mode = True"""

    def __call__(self, *args, **kwargs):
        print(self.__doc__)


class AddLineException(Error):
    """Количество аргументов не соответствует количеству столбцов."""

    def __call__(self, *args, **kwargs):
        print(self.__doc__)


class AddColumnException(Error):
    """Количество аргументов не соответствует количеству строк."""

    def __call__(self, *args, **kwargs):
        print(self.__doc__)


class ColumnDoesNotExists(Error):
    """Колонна с данным именем не существует."""


class InvalidDataFormat(Error):
    """Неверный формат данных list[dict['name': str, 'birthday': str]]"""


class FileExtensionError(Error):
    """Разрешение данного файла запрещено"""


class EmptyDataError(Error):
    """Отсутствуют данные в таблице"""




