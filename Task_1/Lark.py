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

# Ниже представлена грамматика для парсера.
"""
Проблема возникла именно с грамматикой, так как ESCAPED_STRING и WORD работают не совсем так, как ожидал
Суть в том, что при попытке использовать самописные правила с регулярными выражениями, Lark их как будто игнорирует
Пробовал по разному, но в итоге уже потратил несколько дней и каких-либо изменений не увидел.
Сейчас грамматика переварит практически все, в том числе и не правильные варианты
В сети смотрел примеры использования, но их очень мало 
"""
query_grammar = r"""
    ?start: query

    ?query: key_word
    | key_phrase
    | operator // Данные, которые мы встретим в запросе
    key_word : ESCAPED_STRING | WORD // Описание ключевого слова (может быть в кавычках, а может и без)
    key_phrase : key_word + // Описание ключевой фразы (Всегда обрамляется кавычками) 
    operator :  and | not | or // Операторы
    and : /"and"/
    not : /"not"/
    or : /"or"/
    
// Импорты из стандарты шаблонов библиотеки 
   %import common.ESCAPED_STRING // Строка с кавычками
   %import common.WORD // Просто слово

   %ignore " " // Игнорировать пробел
"""


# Функция для предобработки запроса
def _preprocessor_(text: str) -> str:
    text = text.lower()  # Переносим запрос в нижний регистр
    text = text.replace('"', '\"').replace('(', '').replace(')', '')
    # Убираем скобки и заменяем кавычки на то, что может увидеть Lark
    text = text.split(' ')  # Режем строку по пробелам
    preprocessed_query = []  # Создаем список для обработанного запроса
    for word in text:
        if word not in operator_list:
            preprocessed_query.append(word)  # Записываем все значения, что не входят в операторы
    processed_text = str(' '.join(preprocessed_query))  # Создаем строку из списка запроса без операторов
    return processed_text


def get_keywords(query: str) -> list:  # Функция для поиска ключевых слов
    result_list = []  # Список с результатами
    processed_query = _preprocessor_(query)  # Вызываем обработчик запроса
    query_parser = Lark(query_grammar)  # Создаем парсер с использованием нашей грамматики
    tree = query_parser.parse(processed_query)  # Создаем дерево результатов
    tree = tree.pretty().replace('key_phrase', '').replace('key_word\t', '').split('\n')  # Переводим дерево в список
    for i in range(len(tree)):
        if tree[i] != '' and tree[i] != ' ':  # Ищем слова и фразы
            result_list.append(tree[i].strip())  # Записываем в список
    result_list = Series(result_list)  # Конвертируем список в серию, чтобы вытащить уникальные значения
    result_list.unique()  # В общем вытаскиваем уникальные значения
    return list(result_list)


def check_query(query: str) -> bool:  # Проверяем грамматику (ага-да-да))
    processed_query = _preprocessor_(query)  # Обрабатываем запрос
    query_parser = Lark(query_grammar)  # Создаем парсер с грамматикой
    try:
        query_parser.parse(processed_query)  # Если парсер смог разобрать запрос в соответствии с грамматикой, то все ок
    except UnexpectedInput:  # Если нет, то грамматика не соблюдена, а значит запрос не верный
        return False
    return True


# print(_preprocessor_(query_input))
print(get_keywords(query_input))
print(check_query(query_input))
