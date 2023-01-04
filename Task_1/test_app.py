import pytest
from main import check_query

""" Тесты для проверки правил составления запроса """


@pytest.fixture
def test_query_checker():
    return check_query


# Данные для проверки
query_data = [  # ('текст запроса типа str', ожидаемый результат в виде True или False)
    ('"data base" and malware ("detect*" or fix)', True),
    ('malware and ("detect*" or "data base")', True),
    ('malware and ("detect*" or data base)', False),
    ('malware and not ("detect*" or "data base")', True),
    ('malware and spyware not software', True),
    ('malware and ("detect*" or and "data base)', False),
    ('malware and ("detect*" or "not" "relational data base" and "data base control")', True),
    ('malware and ("detect*" not or "relational data base" and "data base control")', False),
    ('software', False)
]


@pytest.mark.parametrize('text, expected_result', query_data)
# Параметризованный тест для проверки правильности составления запроса
def test_check_query(text, expected_result, test_query_checker):
    print(text)
    assert test_query_checker(text) == expected_result
