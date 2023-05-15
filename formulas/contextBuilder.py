import numpy as np
import logging
from numpy import pi, e

from app.package import database
from app.package import schema
from app.formulas import jsonGetParams
from app.formulas import counter


# логирование
logger = logging.getLogger(__name__)

HistoryDb = database.HistoryDb(database.session())
MathemParameters = jsonGetParams.Parameters('mathem')
PhysicsParameters = jsonGetParams.Parameters('phy')


async def build_template(request_schema: schema.RequestSchema | None, user_id, formula_name, science_name):
    # получение параметров
    find_mark = 'x'
    _history = 'Вы не зарегистрированы'
    result = ''
    message = ""
    if science_name == 'physics':
        params, constants, functions, args = PhysicsParameters.get_params(name=formula_name)
    elif science_name == 'mathem':
        params, constants, functions, args = MathemParameters.get_params(name=formula_name)
    logger.debug(f"Getting formula params by name: {formula_name}")
    try:
        # переменные, которые могут поменяться если будет POST метод
        if request_schema.method == "POST":
            # параметры для шаблона
            find_mark = request_schema.find_mark
            # параметры для вычисления
            nums_comma = request_schema.nums_comma
            pattern = params[find_mark]['pattern']
            nums = np.array([], dtype='float16')
            si = np.array([], dtype='float16')
            for arg in args.replace(find_mark, ''):
                nums = np.append(nums, eval(request_schema.data[arg]))
                si = np.append(si, float(params[arg]["INFO"]['si'].get(request_schema.data.get(f"{arg}si"), 1)))
            logger.debug("Setting calculation data SUCCESS")
            # считать результат
            result = counter.counter(num_vector=nums * si,
                                         pattern=pattern,
                                         nums_comma=nums_comma,
                                         constants=constants,
                                         functions=functions,
                                         pattern_args=args.replace(find_mark, ''))
            logger.debug(f"Calculating SUCCESS with result: {result}")
        # заносить результат в историю
        if request_schema.method == "POST":
            if user_id is not None:
                historySchema = schema.HistorySchema(result=result,
                                                     formula=params[find_mark]['formula'],
                                                     user_id=user_id,
                                                     formula_url=request_schema.url,
                                                     date_time=database.nowTime())
                _history = await HistoryDb.form_history(historySchema)
    except (SyntaxError, NameError):
        message = "Невалидные данные."
    except TypeError:
        message = "Ожидаются рациональные числа."
    except ZeroDivisionError:
        message = "На ноль делить нет смысла."
    logger.debug("Forming history SUCCESS")
    logger.debug("Building context SUCCESS")
    tab_div, tab_content_div = await build_html(params=params,
                                              constants=constants,
                                              args=args,
                                              url=request_schema.url,
                                              result=str(result),
                                              find_mark=find_mark)
    # контекст шаблона
    return {
        "tab_div": tab_div,
        "tab_content_div": tab_content_div,
        "history": _history,
        "message": message,
    }


async def build_html(params: dict,
               constants: dict,
               args: str,
               url: str,
               find_mark: str,
               result: str = ""):
    tab_div = ""
    tab_content_divs = ""
    # формирование шаблона в питончике удобнее
    for find_ in args:
        # форматирование тега табов
        # если это обычный литерал
        # [find_]['literal']
        if find_ not in constants:
            if find_ == find_mark:
                tab_div += f"""<button class="tablinks active" onclick="openCity(event, 'tab_{find_}')">Найти {params[find_]['literal']}</button>"""
            else:
                tab_div += f"""<button class="tablinks" onclick="openCity(event, 'tab_{find_}')">Найти {params[find_]['literal']}</button>"""
        # формирование форм для каждого таб контента
        style = "style=\"display: none;\"" if find_ != find_mark else ""
        find_tab_content = (f"<div id=\"tab_{find_}\" class=\"tabcontent white_text\" {style}>\n"
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
        for formula_argument in args.replace(find_, ''):
            formula_argument_literal = params[formula_argument]["literal"]
            options_tab = ""
            for ed in params[formula_argument]['INFO']['si']:
                options_tab += f"<option value=\"{ed}\">{ed}</option>\n"
            if formula_argument not in constants:
                find_tab_content += ("<div class=\"form\">\n"
                                     f"<input type=\"text\" placeholder=\"{formula_argument_literal} = \"  name=\"{formula_argument}\" class=\"form-control\" >\n"
                                     f"<label for=\"{formula_argument}si\">Ед.измерения:</label>\n"
                                     f"<select name=\"{formula_argument}si\" id=\"{formula_argument}si\">\n"
                                     f"{options_tab}"
                                     "</select>\n"
                                     "</div>")
            else:
                formula_argument_value = params[formula_argument]["INFO"]["value"]
                find_tab_content += ("<div class=\"form\">\n"
                                     f"<input type=\"text\" placeholder=\"{formula_argument_literal}= {formula_argument_value}\" value=\"{formula_argument_value}\" name=\"{formula_argument}\" class=\"form-control\" >\n"
                                     f"<select name=\"{formula_argument}si\" id=\"{formula_argument}si\">\n"
                                     f"{options_tab}"
                                     "</select></div>\n")

        # закрываем тег таб контента для данного искомого аргумента
        if find_ == find_mark:
            find_tab_content += (f"<input type=\"text\" hidden=\"hidden\" name=\"find_mark\" value=\"{find_}\">\n"
                                 "<input type=\"submit\">\n"
                                 f"<h4 class=\"text\" style='color: green'>{params[find_]['literal']} = {result}</h4>\n"
                                 "</form></div>")
        else:
            find_tab_content += (f"<input type=\"text\" hidden=\"hidden\" name=\"find_mark\" value=\"{find_}\">\n"
                                 "<input type=\"submit\">\n"
                                 f"<h4 class=\"text\">{params[find_]['literal']} = ...</h4>\n"
                                 "</form></div>")
        tab_content_divs += find_tab_content
    return tab_div, tab_content_divs
