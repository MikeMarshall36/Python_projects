import pytest
from main import get_keywords, check_query


@pytest.fixture
def test_query_checker():
    return check_query


query_data = [  # Данные для проверки

    ('"data base" and malware ("detect*" or fix)', True),
    ('malware and ("detect*" or "data base")', True),
    ('malware and fix or ("detect*" or "data base")', True),

    ('malware and spyware and not ("detect*" or "data base")', False),
    ('malware and ("detect* or "data base")', False),
    ('malware and ("detect*" or data base)', False),
]


@pytest.mark.parametrize('text, expected_result', query_data)
# Параметризованный тест для проверки правильности составления запроса
def test_check_query(text, expected_result, test_query_checker):
    print(text)
    assert test_query_checker(text) == expected_result
