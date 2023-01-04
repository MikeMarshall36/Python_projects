from pandas import Series
# Импортируем из модуля Pandas тип данных Series, чтобы выводить уникальные данные (pd.Series.unique())
import re  # Импортируем модуль регулярных выражений

"""

Примеры запросов в поисковик:

query = "data base" and malware ("detect*" or fix)
wrong_query = malware and ("detect*" or data base)
possible_right_query = malware and spyware not software
absolutely_wrong_query = malware and ("detect*" or and "data base)
possible_wrong_query = malware and ("detect*" or "not" "relational data base" and "data base control")
"""
logical_operations = ('and', 'or', 'not')  # Массив логических операторов


def get_keywords(query: str) -> list:
    query = query.replace('(', '').replace(')', '')  # Избавляемся от скобок в строке
    data = re.findall(r'(".+?"|[^ ]+)', query)
    # Применяем регулярное выражение для поиска слов и фраз, заключенных в кавычки
    result = []  # Список для записи итогового списка
    for i in range(len(data)):  # Проходимся по списку в поиске операторов
        if data[i] not in logical_operations:  # Записываем список слов, избавляясь от операторов
            result.append(data[i])
    return result


def check_query(query: str) -> bool:
    result = [
        key_phrase_check(query),  # Собираем список результатов проверок
        brackets_check(query),
        operator_check(query)
    ]
    if len(result) > 0 and False not in result:
        # Проверяем, чтобы все проверки были пройдены. Если хоть одна не пройдена, то запрос составлен неверно
        return True
    else:
        return False


# Функция для разбития запроса на элементы (Пишем раз, чтобы много раз использовать)
def parse_query(text: str) -> list:
    processed_text = []  # Сюда будем записывать результат обработки
    text = text.replace('(', ' ( ').replace(')', ' ) ')  # К скобкам добавляем пробелы, при парсе они будут отделены
    preprocessed_text = text.split(' ')
    # Пилим получившуюся строку по пробелам и создаем список с получившимися значениями
    for word in preprocessed_text:  # Убираем пустые значения
        if word != '':
            processed_text.append(word)
    return processed_text


# Функция для проверки, обернуты ли ключевые фразы в кавычки
def key_phrase_check(text: str) -> bool:
    delimiters = ['(', ')']  # Задаем разделители, а именно скобки
    opened = False  # создаем флаг, означающий, что кавычки открыты
    delimiters.extend(logical_operations)  # Добавляем к разделителям логические операции
    result = []  # Здесь будет записываться результат проверки в зависимости от итераций по if'ам
    processed_text = parse_query(text)  # Парсим запрос (Функция описана выше)
    if '"' in text and len(processed_text) > 1:  # Проверяем наличие кавычек в тексте
        for i in range(len(processed_text)):
            if processed_text[i][0] == '"' and processed_text[i][-1] != '"':
                # Проверяем, чтобы элемент списка начинался с кавычки
                opened = True  # Меняем флаг. Кавычки открыты
                for j in range(i, len(processed_text)):  # Ищем слово с закрывающей кавычкой (ТОЛЬКО с закрывающей)
                    if processed_text[j][0] != '"' and processed_text[j][-1] == '"' and opened:
                        # Проверяем, чтобы условие проходило
                        result.append(True)
                        opened = False  # Кавычки закрыты
                        break
            elif processed_text[i][0] != '"' and processed_text[i][-1] != '"' and processed_text[i] not in delimiters \
                    and processed_text[i + 1] not in delimiters \
                    and processed_text[i + 1][0] != '"' and processed_text[i + 1][-1] != '"' and not opened:
                result.append(False)
                """ Выше мы проверяем, чтобы кавычки отсутствовали либо с одной стороны, либо с другой.
                То есть, чтобы либо открывались, либо закрывались.
                При этом чтобы соседние слова не были с кавычками или разделителями (то есть скобками или операторами)
                Тогда записываем, что проверка не пройдена
                 """
        if len(result) > 0 and False not in result:  # Проверяем, что все прошло нормально и нет False'ов
            return True
        else:
            return False
    elif '"' not in text and len(processed_text) > 1:  # Если мы не встретили кавычек и при этом у нас несколько слов
        text = text.split()
        for i in range(1, len(text), 2):  # Проверяем, чтобы операторы стояли через раз и проходим циклом с шагов в 2
            if text[i - 1] not in logical_operations and text[i] in logical_operations:
                # Проверяем, что текущее значение не было оператором, а значение далее - является
                result.append(True)
        if len(result) > 0 and False not in result:  # Убеждаемся, что все проверки пройдены удачно
            return True
        else:
            return False
    elif len(processed_text) <= 1 and processed_text[0] not in logical_operations:
        # Это на случай, если слово всего одно
        return True


def brackets_check(text: str) -> bool:
    bracket_types = "()"
    # Тип скобок который мы будем искать (можно через запятую добавить ещё несколько. Будет работать)
    opening_b = bracket_types[::2]
    # Используем срез для получения списка открывающих скобок
    closing_b = bracket_types[1:2]
    # Используем срез для получения списка закрывающих скобок
    br_stack = []
    # Массив позволяющий отслеживать сходство скобок с помощью их условного тип (1 тип, 2 тип и т.д.)
    for character in text:
        # Проходимся по всем символам текста
        if character in opening_b:
            # Проверяем, является ли символ открывающей скобкой
            br_stack.append(opening_b.index(character))
            # Добавляем индекс в список
        elif character in closing_b:
            # Проверяем является ли скобка закрывающей
            if br_stack and br_stack[-1] == closing_b.index(character):
                # Если есть пара отк. + закр., то удаляем из списка найденную пару
                br_stack.pop()
            else:
                return False
    return not br_stack


"""
Функция ниже нужна для проверки операторов, так как два оператора не должны находится рядом.
Хотя вот тут возникла дилемма, так как с одной стороны можно написать and not, и это будет означать,
что мы берем значения, которые не входят во второе выражение.
А с другой стороны это два стоящих рядом оператора...
При необходимости нужно просто убрать "and processed_text[operator_pos + 1] != 'not'" в каждой проверке

В общем, нужно было бы это обсудить, но сейчас не хочу никого тревожить, так что пока реализовал первый вариант
"""


def operator_check(text: str) -> bool:
    result = []  # Список для записи результатов проверок
    processed_text = parse_query(text)  # Обработанный текст (результат парсинга в виде списка)
    if 'and' in processed_text:  # Поиск оператора and (проверяем его наличие)
        operator_pos = processed_text.index('and')  # Записываем индекс оператора
        if (processed_text[operator_pos + 1] in logical_operations and processed_text[operator_pos + 1] != 'not') \
                or processed_text[operator_pos - 1] in logical_operations:
            # Проверяем соседние значения, чтобы они небыли в списке операторов, а идущие за оператором не были not
            result.append(False)  # Если условие выполняется - это ошибка и запрос не верный
        else:
            result.append(True)
    if 'or' in processed_text:  # Поиск оператора or (проверяем его наличие)
        operator_pos = processed_text.index('or')  # Записываем индекс оператора
        if (processed_text[operator_pos + 1] in logical_operations and processed_text[operator_pos + 1] != 'not') \
                or processed_text[operator_pos - 1] in logical_operations:
            # Проверяем соседние значения, чтобы они небыли в списке операторов, а идущие за оператором не были not
            result.append(False)
        else:
            result.append(True)
    if 'not' in processed_text:  # Поиск оператора or (проверяем его наличие)
        operator_pos = processed_text.index('not')  # Записываем индекс
        if processed_text[operator_pos + 1] in logical_operations:  # Проверяем, чтобы после not не было оператора
            result.append(False)
        else:
            result.append(True)

    if len(result) > 0 and False not in result:  # Проверяем, что все проверки пройдены без False'ов
        return True
    else:
        return False


if __name__ == "__main__":  # Создаем точку входа, чтобы иметь возможность импортировать файл без лишних выводов
    query = str(input('\033[35mВведите запрос: \033[0m'))
    # \033[Xm используется для изменения цвета текста, но чтобы цвет не применялся везде, обнуляю его после ввода
    print(get_keywords(query))  # Вывод ключевых слов
    print(check_query(query))  # Вывод проверки запроса
