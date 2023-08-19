import sympy as sp


def equation_system(equations) -> list[dict]:
    try:
        print(equations)
        return sp.solve(
            [sp.sympify("Eq(" + equation_.replace("=", ",") + ")") for equation_ in equations],
            dict=True
        )
    except Exception as e:
        print(str(e))
        return [{'Результат': "Ошибка в написании уравнения!"}]
