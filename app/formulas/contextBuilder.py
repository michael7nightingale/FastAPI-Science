import numpy as np

from app.db.repositories import HistoryRepository
from app.formulas.metadata import storage
from app.models.schemas import RequestSchema


async def build_template(request: RequestSchema, formula_slug: str, history_repo: HistoryRepository | None = None):
    # получение параметров
    formula_obj = storage[formula_slug]
    params = formula_obj.literals
    args = formula_obj.args
    find_mark = args[0]
    _history = 'Вы не зарегистрированы'
    result = ''
    message = ""

    try:
        # переменные, которые могут поменяться если будет POST метод
        if request.method == "POST":
            # параметры для шаблона
            find_mark = request.find_mark
            # параметры для вычисления
            nums_comma = int(request.nums_comma)
            nums = np.array([], dtype='float16')
            si = np.array([], dtype='float16')
            find_args = tuple(filter(lambda x: x != find_mark, formula_obj.args))

            for arg in find_args:
                nums = np.append(nums, eval(request.data[arg]))
                si = np.append(si, float(params[arg].si[request.data[f"{arg}si"]]))

            # считать результат
            result = formula_obj.match(
                **dict(zip(find_args, nums * si))
            )[0]
            result = round(result, nums_comma)
            if request.user_id is not None:
                await history_repo.create(
                    user_id=request.user_id,
                    result=str(result),
                    formula_id=request.formula_id,
                    formula_url=request.url,
                )

    except (SyntaxError, NameError):
        message = "Невалидные данные."
    except TypeError:
        message = "Ожидаются рациональные числа."
    except ZeroDivisionError:
        message = "На ноль делить нет смысла."
    except ArithmeticError:
        message = "Вычислительно невозможное выражение"

    tab_div, tab_content_div = await build_html(
        params=params,
        args=formula_obj.args,
        url=request.url,
        result=str(result),
        find_mark=find_mark
    )

    # контекст шаблона
    return {
        "tab_div": tab_div,
        "tab_content_div": tab_content_div,
        "history": _history,
        "message": message,
    }


async def build_html(
        params: dict,
        args: tuple,
        url: str,
        find_mark: str,
        result: str = ""
    ):
    tab_div = ""
    tab_content_divs = ""
    # формирование шаблона в питончике удобнее
    for find_ in args:
        # форматирование тега табов
        # если это обычный литерал
        if not params[find_].is_constant:
            if find_ == find_mark:
                tab_div += f"""<button class="tablinks active" onclick="openTab(event, 'tab_{find_}')">Найти {params[find_].literal}</button>"""
            else:
                tab_div += f"""<button class="tablinks" onclick="openTab(event, 'tab_{find_}')">Найти {params[find_].literal}</button>"""
        # формирование форм для каждого таб контента
        style = "display: none; min-height: 400px" if find_ != find_mark else "min-height: 400px"
        find_tab_content = (f"<div id=\"tab_{find_}\" class=\"tabcontent white_text\" style=\"{style}\">\n"
                            f"<form method=\"post\" action=\"{url}\">\n"
                            "<label for=\"nums_comma\">Цифр после запятой: </label>\n"
                            "<select title=\"nums_comma\" name=\"nums_comma\" id=\"nums_comma\" >\n"
                            "<option value=\"10\">10</option>\n"
                            "<option value=\"0\">0</option>\n"
                            "<option value=\"1\">1</option>\n"
                            "<option value=\"2\">2</option>\n"
                            "<option value=\"3\">3</option>\n"
                            "<option value=\"4\">4</option>\n"
                            "<option value=\"5\">5</option>\n"
                            "<option value=\"6\">6</option>\n"
                            "<option value=\"7\">7</option>\n"
                            "<option value=\"8\">8</option>\n"
                            "<option value=\"9\">9</option>\n"
                            "</select>")
        for formula_argument in filter(lambda x: x != find_, args):
            formula_argument_literal = params[formula_argument].literal
            options_tab = ""
            for ed in params[formula_argument].si:
                options_tab += f"<option value=\"{ed}\">{ed}</option>\n"
            if params[formula_argument].is_constant:
                formula_argument_value = params[formula_argument].value
                find_tab_content += ("<div class=\"form\" style={min-height: 400px}>\n"
                                     f"<input type=\"text\" placeholder=\"{formula_argument_literal}= {formula_argument_value}\" value=\"{formula_argument_value}\" name=\"{formula_argument}\" class=\"form-control\" >\n"
                                     f"<select name=\"{formula_argument}si\" id=\"{formula_argument}si\">\n"
                                     f"{options_tab}"
                                     "</select></div>\n")
            else:
                find_tab_content += ("<div class=\"form\"  style={min-height: 400px}>\n"
                                     f"<input type=\"text\" placeholder=\"{formula_argument_literal} = \"  name=\"{formula_argument}\" class=\"form-control\" >\n"
                                     f"<label for=\"{formula_argument}si\">Ед.измерения:</label>\n"
                                     f"<select name=\"{formula_argument}si\" id=\"{formula_argument}si\">\n"
                                     f"{options_tab}"
                                     "</select>\n"
                                     "</div>")
                
        # закрываем тег таб контента для данного искомого аргумента
        if find_ == find_mark:
            find_tab_content += (f"<input type=\"text\" hidden=\"hidden\" name=\"find_mark\" value=\"{find_}\">\n"
                                "<button class=\"btn btn-primary\" type=\"submit\">Считать</button>\n"
                                 f"<h4 class=\"text\" style='color: darkseagreen'>{params[find_].literal} = {result}</h4>\n"
                                 "</form></div>")
        else:
            find_tab_content += (f"<input type=\"text\" hidden=\"hidden\" name=\"find_mark\" value=\"{find_}\">\n"
                                 "<button class=\"btn btn-primary\" type=\"submit\">Считать</button>\n"
                                 f"<h3 class=\"text\">{params[find_].literal} = ...</h4>\n"
                                 "</form></div>")
        tab_content_divs += find_tab_content
    return tab_div, tab_content_divs


async def count_result(request: RequestSchema, formula_slug: str, history_repo: HistoryRepository | None = None):
    formula_obj = storage[formula_slug]
    params = formula_obj.literals
    args = formula_obj.args
    find_mark = args[0]
    _history = 'Вы не зарегистрированы'
    result = ''
    message = ""

    try:
        # переменные, которые могут поменяться если будет POST метод
        if request.method == "POST":
            # параметры для шаблона
            find_mark = request.find_mark
            # параметры для вычисления
            nums_comma = int(request.nums_comma)
            nums = np.array([], dtype='float16')
            si = np.array([], dtype='float16')
            find_args = tuple(filter(lambda x: x != find_mark, formula_obj.args))

            for arg in find_args:
                nums = np.append(nums, eval(request.data[arg]))
                si = np.append(si, float(params[arg].si[request.data[f"{arg}si"]]))

            # считать результат
            result = formula_obj.match(
                **dict(zip(find_args, nums * si))
            )[0]
            result = round(result, nums_comma)
            if request.user_id is not None:
                await history_repo.create(
                    user_id=request.user_id,
                    result=str(result),
                    formula_id=request.formula_id,
                    formula_url=request.url,
                )

    except (SyntaxError, NameError):
        message = "Невалидные данные."
    except TypeError:
        message = "Ожидаются рациональные числа."
    except ZeroDivisionError:
        message = "На ноль делить нет смысла."
    except ArithmeticError:
        message = "Вычислительно невозможное выражение"

    return result if result else message
