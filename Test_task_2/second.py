"""
Задание второе

Нужно вывести достижимые вершины для заданной точки
"""

data = {
    1: [2, 3],
    2: [4]
}  # Наборы данных для проверки

data2 = {
    1: [2, 3],
    2: [3, 4],
    4: [1]
}


def _func(data_set: dict, start: int, res=None):  # Функция для вывода достижимых вершин
    if res is None:
        res = []
    res.append(start)
    keys = tuple(data_set.keys())  # Создаем кортеж ключей
    for item in data_set.get(start):  # Получаем значения по ключу
        if item not in res:  # Проверяем наличие элемента в результирующем списке
            if item in keys:  # Проверяем, является ли это значение ключом в словаре
                _func(data_set, item, res)  # Вызываем функцию с тем же словарем, но ключ используем новый
            else:
                res.append(item)  # Добавляем значение в список
    return res


def my_code(data_set: dict, start: int):  # Функция преобразования результата в генератор
    yield from _func(data_set, start)  # Собственно возврат генератора


for i in my_code(data2, 1):  # Вызов функции
    print(i)
