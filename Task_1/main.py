from pandas import Series
# Импортируем из модуля Pandas тип данных Series, чтобы выводить уникальные данные (pd.Series.unique())
import re  # Импортируем модуль регулярных выражений

logical_operations = ['and', 'or', 'not']  # Список логических операций


"""
Примеры запросов:
"data base" and malware ("detect*" or fix) - результат True
malware and ("detect*" or "data base") - результат True
malware and ("detect*" or not "data base") - результат True

malware and or ("detect*" or "data base") - результат False
malware and ("detect* or "data base") - результат False
malware and ("detect*" or data base) - результат False
"""


def get_keywords(query: str) -> list:
    exp = r'([^"]*)'  # Создаем шаблон регулярного выражения для поиска текста внутри кавычек
    result = []  # Список хранящий в себе результат выполнения функции
    for operator in logical_operations:  # Проходимся по списку логических операций
        query = query.replace(f' {operator} ', '')  # Убираем логические операторы
    query = query.replace('(', '')  # Избавляемся от скобок
    query = query.replace(')', '')
    query = re.findall(exp, query)  # Ищем все совпадения с шаблоном

    for i in range(len(query)):  # Проходимся по запросу, чтобы отсеять пустые значения и пробелы
        if query[i] != '' and query[i] != ' ':
            result.append(query[i])  # Записываем результат в лист
    result = list(Series(result).unique())
    return result


def check_query(query: str) -> bool:
    rules_checked_arr = [brackets_check(query), key_phrases_check(query), keywords_comma_check(query)]
    # Создаем список который хранит результаты отдельных проверок
    if False in rules_checked_arr:  # Проверяем, что все проверки пройдены на True (все правила соблюдены)
        return False
    else:
        return True

#####################################_Без дополнительных функций было не обойтись_######################################

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
    return (not br_stack)


def key_phrases_check(text: str) -> bool:
    result_list = []
    text = text.replace('(', '|')  # Избавляемся от скобок
    text = text.replace(')', '|')

    for operator in logical_operations:  # Заменяем все возможные логические операторы на |
        text = text.replace(f' {operator} ', '|')
    pre_processed_text = text.split('|')  # Разделяем получившуюся строку по знаку |
    if '' in pre_processed_text:
        pre_processed_text.remove('')
    print(pre_processed_text)
    for i in range(len(pre_processed_text)):  # В получившемся массиве ищем элементы содержащие пробелы
        pre_processed_text[i] = pre_processed_text[i].strip()
        if ' ' in pre_processed_text[i] and (pre_processed_text[i][0] == '"' and pre_processed_text[i][-1] == '"'):
            # Проверяем, что это точно фраза (2+ слова, разделенные пробелом)
            result_list.append(True)
        elif ' ' in pre_processed_text[i] and (pre_processed_text[i][0] != '"' or pre_processed_text[i][-1] == '"' or pre_processed_text[i][0] == '"' or pre_processed_text[i][-1] != '"'):
            # Проверяем противоположное условие (Фраза, в которой есть только открытие или закрытие скобки)
            result_list.append(False)

    if False in result_list:
        return False
    else:
        return True


def keywords_comma_check(text: str) -> bool:
    result_list = []
    text = text.replace(' (', '|')  # Избавляемся от скобок
    text = text.replace(')', '|')

    for operator in logical_operations:  # Заменяем все возможные логические операторы на |
        text = text.replace(f' {operator} ', '|')

    pre_processed_text = text.split('|')  # Разделяем получившуюся строку по знаку |
    if '' in pre_processed_text:
        pre_processed_text.remove('')
    for i in range(len(pre_processed_text)):  # В получившемся массиве ищем элементы содержащие пробелы
        if ' ' not in pre_processed_text[i] and (pre_processed_text[i][0] == '"' and pre_processed_text[i][-1] == '"') and pre_processed_text[i] not in logical_operations:
            # Проверяем что это именно слово, значит без пробелов. И что оно имеет две парные кавычки
            result_list.append(True)
        elif ' ' not in pre_processed_text[i] and (pre_processed_text[i][0] == '"' and pre_processed_text[i][-1] != '"' or pre_processed_text[i][0] != '"' and pre_processed_text[i][-1] == '"') or pre_processed_text[i] in logical_operations:
            result_list.append(False)  # Проверяем что это слово, но оно имеет одну кавычку (любую, но одну)
    if False in result_list:
        return False
    else:
        return True


if __name__ == "__main__":  # Можно использовать как пакет, и при этом не испытывать проблем с лишними вызовами
    query = str(input('Введите запрос: ')).lower().strip()  # Не обязательный ввод текста для удобства
    print(get_keywords(query))  # Вывод для просмотра ключевых слов
    print(check_query(query))  # Вывод для проверки корректности запроса

