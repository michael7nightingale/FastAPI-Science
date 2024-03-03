from abc import ABC, abstractmethod
from collections import defaultdict
from copy import deepcopy
from typing import Iterable

import numpy as np    # noqa: F401
from numpy import cos, sin  # noqa: F401
from pydantic import BaseModel
import sympy as sp
from sympy.abc import *  # noqa: F401, F403
from sympy.abc import S  # noqa: F401


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

    @classmethod
    def from_dict(cls, data: dict) -> "Literal":
        fields = "si", "literal", "ed", "name"
        nullable_fields = "value", "is_constant", "is_function"
        assert all(fields in data for fields in fields)
        return cls(
            **{field: data[field] for field in fields},
            **{nullable_field: data.get(nullable_field) for nullable_field in nullable_fields}
        )


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
        literals: dict[str, Literal]
    ):
        global storage
        self.formula = formula
        self.pattern: sp.Eq = sp.simplify(self._template.replace("?", ", ".join(formula.split("="))))
        self.args: tuple[str, ...] = tuple(literals.keys())
        self.literals: dict[str, Literal] = literals

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
            "literals": {k: v.model_dump() for k, v in self.literals.items()}
        }

    @classmethod
    def from_dict(cls, data: dict) -> "BaseFormula":
        fields = "formula", "literals"
        assert all(field in data for field in fields)
        literals = {
            literal_key: Literal.from_dict(literal_data) for literal_key, literal_data in data['literals'].items()
        }
        return cls(
            formula=data['formula'],
            literals=literals
        )


class Formula(BaseFormula):
    __slots__ = ()
    _template = "Eq(?)"

    def get_constants(self) -> Iterable[Literal]:
        return filter(
            lambda literal: literal.is_constant,
            self.literals.values()
        )

    def get_formulas(self) -> Iterable[Literal]:
        return filter(
            lambda literal: literal.is_function,
            self.literals.values()
        )

    def match(self, **nums):
        expr = self.pattern.subs(nums)
        return sp.solve(expr)


def literal_rename(literal: Literal, literal_symbol: str) -> Literal:
    new_literal = deepcopy(literal)
    new_literal.literal = literal_symbol
    return new_literal


def get_formula(slug: str):
    return storage.get(slug)
