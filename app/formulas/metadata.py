from abc import ABC, abstractmethod
from collections import defaultdict
from copy import deepcopy
from typing import Iterable

import numpy as np
from numpy import cos, sin
from pydantic import BaseModel
import sympy as sp
from functools import wraps
from sympy.abc import *
from sympy.abc import S


class Literal(BaseModel):
    """
    Base model for literals, functions and constants.
    """
    literal: str
    name: str
    si: dict
    is_constant: bool = False
    is_function: bool = False
    ed: str | None = None
    value: float | None = None

    def __init__(self, **data):
        super().__init__(**data)
        self.si = defaultdict(lambda *x, **y: 1, **self.si)
        for opt, numeric in self.si.items():
            if numeric == 1:
                self.ed = opt
        if self.ed is None:
            raise ValueError("There is no main measure option~!")

    def __hash__(self):
        return hash(self.formula)


class Constant(Literal):
    """Constant model (si = ed)"""
    is_constant: bool = True
    value: float


class Function(Literal):
    """Function model (si is of argument one) model"""
    is_function: bool = True
    py_name: str


class BaseFormula(ABC):
    __slots__ = ("formula", "literals", "args", "pattern")
    _template: str

    def __init__(
        self,
        formula: str,
        name: str,
        **kwargs
    ):
        global storage
        if name in storage:
            raise AssertionError("Name is already in the storage!")
        storage[name] = self
        self.formula = formula
        self.pattern: sp.Eq = sp.simplify(self._template.replace("?", ", ".join(formula.split("="))))
        self.args: tuple[str] = tuple(kwargs.keys())
        self.literals: dict[str, Literal] = dict(kwargs)

    def __len__(self) -> int:
        return len(self.args)

    def __repr__(self) -> str:
        return str(self.formula)

    @abstractmethod
    def get_constants(self) -> Iterable[Literal]:
        pass

    @abstractmethod
    def get_formulas(self) -> Iterable[Literal]:
        pass

    def as_dict(self) -> dict:
        return {
            "formula": self.formula,
            "args": self.args,
            "literals": {k: v.dict() for k, v in self.literals.items()}
        }


class Formula(BaseFormula):
    __slots__ = ()
    _template = "Eq(?)"
    
    def get_constants(self) -> Iterable[Literal]:
        return filter(
            lambda x: x.is_constant, 
            self.literals.values()
            )

    def get_formulas(self) -> Iterable[Literal]:
        return filter(
            lambda x: x.is_function, 
            self.literals.values()
            )

    def match(self, **nums):
        expr = self.pattern.subs(nums)
        print(expr, nums, self.pattern)
        print(sp.solve(expr))
        return sp.solve(expr)


# define storage
storage: dict[str, Formula] = {}    


# ======================================= LITERALS ================================== #

Impulse = Literal(si={"kg*m/s": 1, "g*m/s": 0.001}, name = "Impulse", literal="p")
Speed = Literal(si={"m/s": 1, "km/s": 1000}, name = "Speed", literal="V")
Mass = Literal(si={"kg": 1, "g": 0.001}, name = "Mass", literal="m")
Way = Literal(si={"m": 1, "km": 1000, "sm": 0.01}, name='Way', literal="S")
Height = Literal(si={"m": 1, "km": 1000, "sm": 0.01}, name='Height', literal="h")
Density = Literal(si={"kg/m^3": 1}, literal="p", name="Density")
Pressure = Literal(si={"Pa": 1, "kPa": 1000, "mPa": 0.001}, name="Pressure", literal='ro')
Force = Literal(si={"N": 1, "kN": 1000, "mN": 0.001}, name="Force", literal='F')
Acceleration = Literal(si={"m/s^2": 1, "km/s^2": 1000}, name="Acceleration", literal="a")
Coordinate = Literal(si={"_": 1}, name="Coordinate", literal="")


def coordinate(literal: str) -> Literal:
    return Literal(si={"_": 1}, name="Coordinate", literal=literal)


def literal_rename(literal: Literal, literal_symbol: str) -> Literal:
    new_literal = deepcopy(literal)
    new_literal.literal = literal_symbol
    return new_literal


# ======================================= CONSTANTS ================================== #

G = Constant(si={"m/s^2": 1}, name="Free fall acceleration", literal='g', value=9.813)
PI = Constant(si={"_": 1}, name="Pi", literal="pi", value=np.pi)
K = Constant(si={"_": 1}, name="Dielectric constant", literal='k', value=9*10**(-9))


# ======================================= FUNCTIONS ================================== #

cos_ = Function(si={"radians": 1, "degrees": 0.017453293}, name="Cosinus", literal="cos", py_name='cos')

# ======================================= FORMULAS ================================== #

impulse = Formula(name='impulse', formula="p = m * V", p=Impulse, m=Mass, V=Speed)
pressure_liquid = Formula(name='pressure_liquid', formula="p = r * g * h", p=Pressure, r=Density, h=Height, g=G)
newton2 = Formula(name="newton2", formula="F = m * a", F=Force, m=Mass, a=Acceleration)
peremeshenie = Formula(name='peremeshenie', formula="s = x - x_0",
                       s=Way, x=coordinate("x"), x_0=coordinate("x_0"))
moving_proection = Formula(name="moving_proection", formula="s_x = s * cos(a)",
                           s_x=literal_rename(Way, "S_x"), s=Way, a=cos_)


def get_formula(slug: str):
    return storage.get(slug)
