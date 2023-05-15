import copy
import os
import json
# from methodtools import lru_cache
from frozendict import frozendict
from functools import lru_cache


class Parameters:
    __slots__ = ("DATA", "FORMULAS", "CONSTANTS", "FORMULAS_NAMES", "LITERALS", "FUNCTIONS", "science_name")
    BASE_DIR: str = os.getcwd() + '/app/'
    params_path: str = '/formulas/'

    def __init__(self, science_name):
        self.science_name = science_name
        self.DATA = {}
        self.FORMULAS = {}
        self.LITERALS = {}
        self.FORMULAS_NAMES = {}
        self.FUNCTIONS = {}
        self.CONSTANTS ={}
        print(3)
        self.load_data()

    def get_params(self, name: str):
        # параметры в общем виде
        if name in self.FORMULAS_NAMES:
            params_common = self.FORMULAS[name]
        else:
            raise ValueError("В файле конфигурация формул не содержится формулы с данным именем обращения")
        # подставляем данные из литералов
        params = copy.deepcopy(params_common)
        args = "".join((i for i in params.keys() if len(i) == 1))
        for arg in args:
            if params_common[arg]['INFO'] == "number":
                params[arg]['INFO'] = {"si": {}}
            elif params_common[arg]['INFO'] in self.CONSTANTS:
                params[arg]['INFO'] = self.CONSTANTS[params_common[arg]['INFO']]
            elif params_common[arg]['INFO'] in self.FUNCTIONS:
                params[arg]['INFO'] = self.FUNCTIONS[params_common[arg]['INFO']]
            else:
                params[arg]['INFO'] = self.LITERALS[params_common[arg]['INFO']]
        return params, self.get_constants(params_common, args), self.get_functions(params_common, args), args

    # @lru_cache(maxsize=64)
    def get_constants(self, params_common: frozendict, args: str):
        constants = dict()
        if 'constants' in params_common:
            for i in params_common:
                if i in args:
                    if params_common[i]["INFO"] in self.CONSTANTS:
                        constants[i] = self.CONSTANTS[params_common[i]['INFO']]['value']
        return constants

    # @lru_cache(maxsize=64)
    def get_functions(self, params_common: frozendict, args: str):
        functions = dict()
        for i in params_common:
            if i in args:
                if params_common[i]["INFO"] in self.FUNCTIONS:
                    functions[i] = self.FUNCTIONS[params_common[i]['INFO']]['name']
        return functions


    def load_data(self) -> None:
        try:
            with open(str(self.BASE_DIR) + self.params_path + self.science_name + '_params.json') as file:
                self.DATA = json.load(file)
        except Exception as e:
            assert False, "Missed parameters json file!!! Error on data side~!"
        self.CONSTANTS = self.DATA['constants']
        self.FORMULAS = self.DATA['formulas']
        self.LITERALS = self.DATA.get('literals', {})
        self.FUNCTIONS = self.DATA['functions']
        self.FORMULAS_NAMES = tuple(self.FORMULAS.keys())


# class PhysicsParameters(Parameters):
#     params_path = '/formulas/phy_params.json'
#
#
# class MathemParameters(Parameters):
#     params_path = '/formulas/mathem_params.json'
