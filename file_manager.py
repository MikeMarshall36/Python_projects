import os
import random
import shutil
req_main = ''
req = ''
sec_req = ''

opeSys = os.name

with open('manual.txt', 'r', encoding='utf-8') as file:
    print(*file)

def separating_reqest(request):
    global req_main
    global req
    global sec_req
    req_array = []
    request = request.lstrip()
    req_array = request.split(' ')
    if len(req_array) == 2:
        req_main = req_array[0]
        req = req_array[1]
        print(req_array)
        print(req_main, req)
    elif len(req_array) == 1:
        req_main = req_array[0]
        print(req_main)
    elif len(req_array) == 3:
        req_main = req_array[0]
        req = req_array[1]
        sec_req = req_array[2]
        print(req_array)
        print(req_main, req, sec_req)

def cur_dir():
    full_path = os.getcwd()
    cur_path = full_path.split('\\')
    pwd = cur_path[len(cur_path)-1]
    print(pwd, '\n')

def dir_rem(dir_name):
    os.rmdir(dir_name)
    print(f'Директория {dir_name} удалена', '\n')

def mkdir_py(dir_name):
    if not os.path.isdir(dir_name):
        os.umask(0)
        os.mkdir(dir_name,0o777)
        print(f'Директория с именем {dir_name} создана', '\n')
    else:
        print('Директория с таким именем уже существует')

def F_list(dir_name):
    List = os.listdir()
    for i in range(len(List)):
        print(List[i])
    print('\n')

def touch(file_name):
    global opeSys
    if opeSys == 'posix':
        os.system(open(file_name + '.txt'))

    elif opeSys != 'posix':
        if not os.path.isfile(file_name):
            text_file = open(file_name + '.txt', 'w+')
            text_file.write('')
            file_name += '.txt'
            os.startfile(file_name)
    print('Текстовый файл создан!')

def open_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        print(*file)

def rename(old_Fname, new_Fanme):
    old_Fname += '.txt'
    new_Fanme += '.txt'
    os.rename(old_Fname, new_Fanme)
    print(f'Теперь файл {old_Fname} называется {new_Fanme}!')

def rm(file_name):
    os.remove(file_name)
    print(f'Файл с именем {file_name} - удалён')

def moveto(file_name, dir_name):
    os.replace(file_name, f'{dir_name}/{file_name}')
    print(f'Файл {file_name} был перемещён в директорию {dir_name} !')

def chdir(dir_name):
    if dir_name != 'back':
        os.chdir(dir_name)
        print(f'Рабочая директория изменена на {dir_name}.')
    else:
        os.chdir('..')
        print('Возврат к предыдущей директории')

def copy_file(file_name, second_file):
    shutil.copyfile(file_name, second_file)
    print(f'Файл {file_name} скопирован')

def copy_folder(file_name, dir_name):
    if not os.path.isdir(dir_name):
        shutil.copy(file_name, dir_name)
        print(f'Файл {file_name} был скопирован в директорию {dir_name}')

def edit_file(file_name):
    global opeSys
    if opeSys == 'posix':
        os.system(open(file_name + '.txt'))
    elif opeSys != 'posix':
        file_name += '.txt'
        os.startfile(file_name)
    print(f'Файл {file_name} был изменён')
user_input = str(os.getcwd()) + ': '

def man():
    open_file('manual.txt')

requ = input('Введите запрос: ')
requ.lower()
while len(requ) != '    ':
    exit_check = requ.lower()
    if exit_check == 'exit':
        a = int(random.random() * 100)
        if a % 5 == 0:
            print('\nSee you next time!')
        else:
            print('\nShutting down...')
            exit()
    else:
        try:
            separating_reqest(requ)
            if req_main == 'mkdir':
                mkdir_py(req)
            if req_main == 'remdir':
                dir_rem(req)
            if req_main == 'pwd':
                cur_dir()
            if req_main == 'ls':
                F_list(req)

            if req_main == 'touch':
                touch(req)

            if req_main == 'rm':
                rm(req)

            if req_main == 'moveto':
                moveto(req, sec_req)

            if req_main == 'rename':
                rename(req, sec_req)

            if req_main == 'open':
                open_file(req)

            if req_main == 'chdir':
                chdir(req)

            if req_main == 'edit':
                edit_file(req)

            if req_main == 'copyFile':
                copy_file(req, sec_req)

            if req_main == 'copyto':
                copy_folder(req, sec_req)
                
            if req_main == 'copyto':
                copy_folder(req, sec_req)
             
            if req_main == 'man':
                man()

            user_input = str(os.getcwd()) + ': '


        except:
            continue

        finally:

            requ = input(user_input)

print('Запрос: ', req_main)

if req != '':

    print('Параметр запроса: ', req)
