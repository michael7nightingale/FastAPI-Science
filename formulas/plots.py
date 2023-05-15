import os
import matplotlib.pyplot as plt
import numpy as np
from numpy import cos, sin, tan, pi, e, power, sqrt
from abc import ABC, abstractmethod
import re


class BasePlot(ABC):
    mathematical_names: set
    pattern: str
    __step: float

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def download_image(self):
        pass


class Plot:
    mathematical_names = {'cos', 'sin', 'tan', 'e', 'pi', 'sqrt'}
    pattern = r'\s|\*|\d|-|/|\+|\(|\)'
    __step = 0.1

    def __init__(self, functions: list,
                 xlim: tuple,
                 ylim: tuple = None):
        self.__functions = functions
        self.__xlim = int(xlim[0]), int(xlim[1])
        if ylim is not None:
            self.__ylim = int(ylim[0]), int(ylim[1])
        else:
            self.__ylim = None
        self.__figure = plt.figure(figsize=(7, 7))
        # try:
        plt.xlim(self.__xlim)
        plt.ylim(self.__ylim)
        plt.grid()
        self.set_plot()
        # except:
        #     raise ValueError("Невалидные данные")

    def set_plot(self):
        """Построение графика всех функций"""
        for number, function in enumerate(self.__functions, 1):
            self.set_graphic(function, number)

    def set_graphic(self, function: str, number: int):
        """Построение графика отдельной функции"""
        # setattr(self,
        #         f'__ax{number}',
        #         self.__figure.add_subplot()
        #         )
        plt.plot(*self.__define(function))
        # ax_ = getattr(self,
        #               f'__ax{number}')
        # ax_.plot(*self.__define(function))
        # ax_.set_xlim(*self.__xlim)
        # if self.__ylim:
        #     ax_.set_ylim(*self.__ylim)
        # ax_.grid()

    def __define(self, function: str):
        """:return x and y coords to define axis. len(x) == len(y)"""
        function_argument = None
        for i in filter(
                self.__check_literals,
                re.split(self.pattern, function)
        ):
            if i.isalpha():
                if function_argument is None:
                    function_argument = i
                elif function_argument == i:
                    pass
                else:
                    raise ValueError("В функции определено несколько аргументов!")
        definers = np.arange(self.__xlim[0], self.__xlim[1], self.__step)
        function = re.sub(r"(\S+\.?\S*)\s*\*\*\s*(-?\S+\.?\S*)", r"power(\1, \2)",  function)
        # print(function)
        # ocs_to_replace = re.findall(r"\s*\S+\s*\*\*\s*[-+]?\d*[.,]?\d*", function)
        # ocs_to_power = re.findall(r"\s*(\S+)\s*\*\*\s*([-+]?\d*[.,]?\d*)", function)
        # print(ocs_to_power, ocs_to_replace)
        # for element, replacement in zip(ocs_to_replace, ocs_to_power):
        #     function = function.replace(element, 'power({}, {})'.format(*replacement))
        definitions = np.array(
            [eval(function.replace(function_argument, str(definer))) for definer in definers],
            dtype=float,
        )
        return definers, definitions

    def __check_literals(self, literal: str) -> bool:
        return bool(literal) and literal not in self.mathematical_names

    @staticmethod
    def show():
        plt.show()

    @staticmethod
    def save_plot(path: str):
        print('1231234124')
        print(path)
        plt.savefig(path)
        print('saved')

