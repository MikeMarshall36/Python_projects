"""
Первое задание.

Нужно было вывести данные в соответствии со вложенностью их в
"""


def my_func(data_set: dict):  # Первая функция
    keys = data_set.keys()
    for key in keys:
        print(f'{key}')
        try:
            my_func(data_set.get(key))
        except AttributeError:
            print(f'\t{data_set.get(key)}\n')


data_set_1 = {
    'first': 'first_value',
    'second': 'second_value'
}

data_set_2 = {
    '1': {
        'child': '1/child/value'
    },
    '2': {
        'child': '2/child/value'
    }
}

my_func(data_set_1)
my_func(data_set_2)

# Табуляция у меня не вышла...
