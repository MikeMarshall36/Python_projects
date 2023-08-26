def my_func(data_set: dict, start: int):
    res = [start]
    for item in data_set.get(start):
        if item not in res:
            res.append(item)
            try:
                for sub_item in data_set.get(item):
                    if sub_item not in res:
                        res.append(sub_item)
            except TypeError:
                break
    count = 0
    while count < len(res):
        for i in range(len(res)):
            result = res[i]
            count += 1
            yield result


data = {
    1: [2, 3],
    2: [4]
}

data2 = {
    1: [2, 3],
    2: [3, 4],
    4: [1]
}

for i in my_func(data, 1):
    print(i)
