def file_reader(file_name, split_type):
    with open(file_name) as file:
        content = list(filter(None, file.read().split(split_type)))
        return content

def file_writer(file_name, data=''):
    with open(file_name, 'a+') as file:
        file.write(data+'\n')

def file_wipe(file_name):
    with open(file_name, 'w') as file:
        file.write('')

users = file_reader('users.txt', ', ')
