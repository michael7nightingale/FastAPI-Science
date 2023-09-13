import sympy as sp


def equation_system(equations) -> dict:
    try:
        result = sp.solve(
            [sp.sympify("Eq(" + equation_.replace("=", ",") + ")") for equation_ in equations],
            dict=True
        )[0]
    except Exception:
        return {'Результат': "Ошибка в написании уравнения!"}
    else:
        return {str(k): str(v) for k, v in result.items()}
