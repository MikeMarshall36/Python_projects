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

# Набор правил для грамматики парсера
grammar = r"""
    ?start: query
    
    query: (key_word | key_word_q | key_phrase | operator)* // Элементы, которые можно встретить в запросе
    
    key_word : WORD  // регулярное выражение для поиска слов без кавычек
    key_word_q : /"[^"]\S*"/ // регулярное выражение для поиска слов с кавычками
    key_phrase : /"[^"]*"/  // регулярное выражение для поиска фраз (2+ слова) в кавчках 
    operator : and | or | not  // Операрторы and, or, not 
    and : "and"
    or : "or"
    not : "not"
    
    %import common.WORD  // импортируем регулярное выражения из набора предустановок
    
    %ignore " " // Игнорируем пробелы
"""


def _preprocess(text: str) -> str:  # функция для предобработки запроса
    text = text.replace('(', '').replace(')', '')  # Избавляемся от скобок
    return text


def check_query(query: str) -> bool:  # Функция для проверки грамматики запорса
    preprocessed_query = _preprocess(query)  # Предобрабатываем запрос (удаляем скобки)
    query_parser = Lark(grammar, parser="earley", ambiguity="explicit")  # создаем парсер с нужной грамматикой
    try:
        query_parser.parse(preprocessed_query)  # Если парсер может обработать запрос, то грамматика соблюдена
    except UnexpectedInput:
        return False
    return True


def get_keywords(query: str) -> list | str:  # функция для получения ключевых слов
    if check_query(query):  # проверка грамматики
        result_list = []  # список с ключевыми словами
        processed_query = _preprocess(query)  # Выполняем предобработку запроса
        query_parser = Lark(grammar, parser="earley", ambiguity="explicit")  # заводим парсер
        tree = query_parser.parse(processed_query)  # Собственно парсим запос
        result_tree = tree.pretty().split('query')[-1]  # записываем дерево, но только последний набор
        #print(result_tree)  # Вывод дерева
        for word in result_tree.split('\n'):  # поиск ключевых слов и фраз
            if word.strip().startswith('key'):  # Ищем элементы списка начинающиеся с key
                result_list.append(word.strip().split('\t')[-1])  # берем только значения
        result_list = Series(result_list)  # записываем результат в серию
        result_list = result_list.unique()  # записываем уникальные значения
        return list(result_list)
    else:
        return "Incorrect query"


if __name__ == "__main__":
    query_input = str(input('Введите текст запроса: '))
    print(check_query(query_input))
    print(get_keywords(query_input))
