from lark import Lark, UnexpectedInput
from pandas import Series

"""
Примеры запросов в поисковик:
1) "data base" and malware ("detect*" or fix)
2) malware and ("detect*" or data base)
3) malware and spyware not software
4) malware and ("detect*" or and "data base)
5) malware and ("detect*" or "not" "relational data base" and "data base control")
"""

operator_list = ['and', 'or', 'not']  # Лист с операторами
query_input = str(input("Enter query: "))  # Ввод запроса

query_grammar = r"""
    ?start: (query)

    query: (key_word
    | key_phrase
    | operator
    | key_word_q)*

    key_word_q : /"[^"]\S*"/
    key_word : WORD
    key_phrase : /"[^"]*"/
    operator : and | not | or
    and : "and"
    not : "not"
    or : "or"

   %import common.ESCAPED_STRING
   %import common.WORD

   %ignore " "
"""


# Функция для предварительной обработки запроса
def _preprocessor_(text: str) -> str:
    text = text.lower()  # Переносим запрос в нижний регистр
    text = text.replace('"', '\"').replace('(', '').replace(')', '')
    # Убираем скобки и заменяем кавычки на то, что может увидеть Lark
    preprocessed_query = text.split(' ')  # Режем строку по пробелам
    processed_text = str(' '.join(preprocessed_query))  # Создаем строку из списка запроса без операторов
    return processed_text

def get_keywords(query: str) -> list:  # Функция для поиска ключевых слов
    result_list = []  # Список с результатами
    query_parser = Lark(query_grammar, parser="earley", ambiguity="explicit")
    # Вызываем парсер, чтобы получить данные
    try:
        processed_query = _preprocessor_(query)  # Вызываем обработчик запроса
        tree = query_parser.parse(processed_query)
        result_tree = tree.pretty().split('query')[-1]
        # print(result_tree) # Вывод итогового варианта обработанного запроса (раскомментируйте, чтобы увидеть дерево)
        for word in result_tree.split('\n'):  # Избавляемся от переноса каретки
            if word.strip().startswith('key'):  # Ищем строки начинающиеся на key
                result_list.append(word.strip().split('\t')[-1])  # Берем значения для ключевых элементов
        result_list = Series(result_list)  # Конвертируем список в серию, чтобы вытащить уникальные значения
        result_list = result_list.unique()  # В общем вытаскиваем уникальные значения
    except UnexpectedInput:
        return query.split(' ')  # В случае если запрос не прошел проверку правил - выводим список с исходным запросом
    return list(result_list)


def check_query(query: str) -> bool:  # Проверяем грамматику (ага-да-да))
    processed_query = _preprocessor_(query)  # Обрабатываем запрос
    query_parser = Lark(query_grammar)  # Создаем парсер с грамматикой
    try:
        query_parser.parse(processed_query)  # Если парсер смог разобрать запрос в соответствии с грамматикой, то все ок
    except UnexpectedInput:  # Если нет, то грамматика не соблюдена, а значит запрос не верный
        return False
    return True


print(get_keywords(query_input))  # Вывод ключевых слов
print(check_query(query_input))  # Вывод результата проверки
