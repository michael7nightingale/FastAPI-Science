import os
from abc import ABC, abstractmethod
from typing import Sequence
import pandas as pd
import csv

from package import exceptions



class BaseTableManager(ABC):
    """Базовый интерфейс для работы с табличными данными."""
    def __init__(self, filepath: str, delete_mode: bool = False, default=""):
        if self.validate_filename(filepath):
            self.filepath = filepath
        self._delete_mode = delete_mode
        self.default = default
        self._data = None
        self.columns = None
        # logger.info(f"__TABLES__ Создан менеджер таблиц для файла по пути {self.filepath}")

    @abstractmethod
    def init_data(self, column_names: Sequence):
        pass


    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data) -> None:
        if not self._data:
            self._data = new_data

    @abstractmethod
    def open_data(self) -> None:
        """Открыть и установить данные по указанному пути"""
        pass

    @abstractmethod
    def get_column_data(self, column_name: str) -> tuple:
        pass

    @abstractmethod
    def add_column(self, column_name: str,
                   column_data: Sequence = tuple(),
                   nullable: bool = False) -> None:
        """Добавить колонку в таблицу."""
        pass

    @abstractmethod
    def add_line(self, args: Sequence = tuple(),
                 nullable: bool = False) -> None:
        """Добавить строку в таблицу"""
        pass

    @abstractmethod
    def delete_column(self, column_name: str) -> None:
        pass

    @abstractmethod
    def get_list_of_dicts_data(self) -> list[dict]:
        pass

    @abstractmethod
    def save_data(self, filepath=None) -> None:
        """Сохранение файла."""
        pass

    @staticmethod
    def validate_filename(filename: str):
        """Проверка расширения файла"""
        try:
            match filename.rsplit('/', 1)[-1].split('.'):
                case [file_, extension]:
                    # if extension in TABLES['ALLOWED_EXTENSIONS']:
                    if extension == 'csv':
                        return True
                    else:
                        raise exceptions.FileExtensionError
                case _:
                    raise exceptions.FileExtensionError
        except:
            raise exceptions.FileExtensionError

    def __iter__(self):
        """Вдруг понадобится итерирование."""
        return iter(self.get_list_of_dicts_data())

    def __len__(self):
        return len(self._data)

    def __getitem__(self, item):
        if isinstance(item, int) or isinstance(item, slice):
            return self._data[item]
        else:
            raise TypeError


class CsvTableManager(BaseTableManager):
    """Расширение для работы с табличными данными c помощью библиотеки csv."""
    _data: list[dict]
    columns: list

    def init_data(self, column_names: Sequence):
        self.columns = column_names
        self._data = []

    def open_data(self):
        with open(self.filepath, encoding='utf-8') as csv_file:
            self._data = list(csv.DictReader(csv_file))
        self.columns = list(self._data[0].keys())
        # logger.info(f"__TABLES__ Открыт файл для менеджера файла {self.filepath}")

    def add_line(self, line_data: Sequence = tuple(),
                 nullable: bool = False) -> None:
        if nullable:
            nulls_to_add: int = len(self.columns) - len(line_data) if (len(self.columns) - len(line_data) >= 0) else 0
            self._data.append(
                dict(
                    zip(self.columns,
                        (tuple(line_data) + tuple((self.default for i in range(nulls_to_add))))[:len(self.columns)]
                        )
                    )
                             )
        else:
            if len(line_data) != len(self.columns):
                # logger.error("__TABLES__" + exceptions.AddLineException.__doc__)
                raise exceptions.AddLineException()
            else:
                self._data.append(dict(zip(self.columns, line_data)))

    def add_column(self, column_name: str,
                   column_data: Sequence = tuple(),
                   nullable: bool = False) -> None:
        if nullable:
            nulls_to_add = len(self._data) - len(column_data) if (len(self._data) - len(column_data)) >= 0 else 0
            column_data = tuple(column_data) + tuple((self.default for _ in range(nulls_to_add)))
        else:
            if len(column_data) != len(self.data):
                # logger.error("__TABLES__" + exceptions.AddColumnException.__doc__)
                raise exceptions.AddColumnException()
        print(column_name)
        # добавляем новую колонку в данные

        self.columns.append(column_name)
        print(self.columns)
        for line_number in range(len(self._data)):
            self._data[line_number][column_name] = column_data[line_number]
        # logger.info(f"__TABLES__ В данные объекта успешно добавлена колонка {column_name}")

    def get_column_data(self, column_name: str) -> tuple:
        if column_name not in self.columns:
            # logger.error("__TABLES__" + exceptions.ColumnDoesNotExists.__doc__)
            raise exceptions.ColumnDoesNotExists
        return tuple((i[column_name] for i in self._data))

    def get_list_of_dicts_data(self) -> list[dict]:
        return self._data

    def delete_column(self, column_name: str) -> None:
        # если выключен режим удаления
        if not self._delete_mode:
            # logger.error("__TABLES__" + exceptions.DeletingModeException.__doc__)
            raise exceptions.DeletingModeException
        # если колонны с таки именем не существует
        if column_name not in self.columns:
            # logger.error("__TABLES__" + exceptions.ColumnDoesNotExists.__doc__)
            raise exceptions.ColumnDoesNotExists
        # если такая колонна есть
        for line in self._data:
            del line[column_name]
        self.columns.remove(column_name)

    def save_data(self, filepath=None) -> None:
        if self.data:
            if filepath is None:
                filepath = self.filepath
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(
                    f, fieldnames=list(self._data[0].keys()), dialect='excel')
                writer.writeheader()
                for d in self._data:
                    writer.writerow(d)
        else:
            raise exceptions.EmptyDataError
        # logger.info(f'__TABLES__ SUCCESS - файл с таблицей сохранен по пути {filepath}')


class PandasTableManager(BaseTableManager):
    """Расширение для работы с табличными данными c помощью библиотеки pandas
    (`pd` - синоним)."""
    _data = pd.DataFrame
    columns = pd.Index

    def init_data(self, column_names: Sequence):
        self.columns = list(column_names)
        self._data = pd.DataFrame(columns=self.columns)

    def open_data(self) -> None:
        self._data: pd.DataFrame = pd.read_csv(self.filepath)
        self.columns: list = list(self._data.columns)
        # logger.info(f"__TABLES__ Открыт файл для менеджера файла {self.filepath}")

    def get_column_data(self, column_name: str) -> tuple:
        if column_name not in self.columns:
            # logger.error("__TABLES__" + exceptions.ColumnDoesNotExists.__doc__)
            raise exceptions.ColumnDoesNotExists
        return tuple(self._data[column_name])

    def add_line(self, line_data: Sequence = tuple(),
                 nullable: bool = False) -> None:
        if nullable:
            nulls_to_add: int = len(self.columns) - len(line_data) if (len(self.columns) - len(line_data) >= 0) else 0
            self._data.loc[len(self._data)] = \
                (list(line_data) + [self.default for _ in range(nulls_to_add)])[:len(self.columns)]
        else:
            if len(line_data) != len(self.columns):
                # logger.error("__TABLES__" + exceptions.AddLineException.__doc__)
                raise exceptions.AddLineException()
            else:
                self._data.loc[len(self._data)] = line_data
        # logger.info(f"В данные объекта успешно добавлена строчка")

    def add_column(self, column_name: str,
                   column_data: Sequence = tuple(),
                   nullable: bool = False) -> None:
        if nullable:
            nulls_to_add: int = len(self._data.values) - len(column_data) if (len(self._data.values) - len(column_data)) >= 0 else 0
            self._data[column_name] = (list(column_data) + ["" for _ in range(nulls_to_add)])[:len(self._data.values)]
        else:
            if len(column_data) != len(self.data):
                # logger.error("__TABLES__" + exceptions.AddColumnException.__doc__)
                raise exceptions.AddColumnException()
            else:
                self._data[column_name] = column_data
        self.columns.append(column_name)
        # logger.info(f"__TABLES__ В данные объекта успешно добавлена колонка {column_name}")

    def delete_column(self, column_name: str) -> None:
        # если выключен режим удаления
        if not self._delete_mode:
            # logger.error("__TABLES__" + exceptions.DeletingModeException.__doc__)
            raise exceptions.DeletingModeException
        # если колонны с таки именем не существует
        if column_name not in self.columns:
            # logger.error("__TABLES__" + exceptions.ColumnDoesNotExists.__doc__)
            raise exceptions.ColumnDoesNotExists
        # если такая колонна есть
        del self._data[column_name]
        self.columns.remove(column_name)
        # logger.info(f"__TABLES__ Из данных объекта успешно удалена колонка {column_name}")

    def get_list_of_dicts_data(self) -> list[dict]:
        return [
            dict(zip(
                self.columns, line
            )) for line in self._data.values
        ]

    def save_data(self, filepath=None) -> None:
        if filepath is None:
            filepath = self.filepath
        self._data.to_csv(filepath)
        # logger.info(f'__TABLES__ SUCCESS - файл с таблицей сохранен по пути {filepath}')


if __name__ == '__main__':
    # table = PandasTableManager('d:test.csv', True, 0)
    # table.open_data()
    # print(table.add_column('mama', nullable=True))
    # print(table.columns)
    # print(table.get_list_of_dicts_data())
    pass


