from tkinter import *
import socket
import threading
import os

def Scan():
    file_name = 'scan_res.txt'

    if file_name in os.listdir():
        os.remove('scan_res.txt')

    res_lable.config(text=f'Открытые порты: -\nЗакрытые порты: -', bg='gray')
    status_lable.config(text='Текущий статус: running')

    open_array = []
    close_array = []

    if len(IP_insert.get()) == 0:
        root.bell()
        ip = '127.0.0.1'
    else:
        ip = IP_insert.get()
    for port in range(1, 64001):
        scan_ports(ip, port, close_array, open_array)
    res_lable.config(text=f'Открытые порты: {len(open_array)}\nЗакрытые порты: {len(close_array)}')
    status_lable.config(text='Текущий статус: done')
    status_lable.bell()

def scan_ports(ip, port_name, closed_thread, open_thread):
    sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockt.settimeout(0.01)

    try:

        connect = sockt.connect((ip, port_name))
        f = open('scan_res.txt', 'a')
        f.write(f'{ip}:{port_name} - is open\n')
        f.close()
        open_thread.append(port_name)
        sockt.close()

    except:

        closed_thread.append(port_name)
        f = open('scan_res.txt', 'a')
        f.write(f'{ip}:{port_name} - closed\n')
        f.close()
        sockt.close()

def start():
    thread = threading.Thread(target=Scan)
    thread.start()


root = Tk()
root.title('Сканнер портов сервера')
root.geometry('280x200')
root.resizable(False, False)

GUI_frame = Frame(root, bg='gray')

ip_lable = Label(GUI_frame, text='IP адрес или доменное имя:', bg='gray')

IP_insert = Entry(GUI_frame, width=35)
IP_insert.config(bg='black', fg='green', insertbackground='green')

btn = Button(GUI_frame, activebackground='maroon', bg='red', justify='left', text='Начать', command=start)
status_lable = Label(GUI_frame, text='Текущий статус: stand by', bg='gray')
res_lable = Label(GUI_frame, text=f'Открытые порты: -\nЗакрытые порты: -', bg='gray')

ip_lable.pack()
IP_insert.pack()
btn.pack()
status_lable.pack()
res_lable.pack()
GUI_frame.pack()


root.mainloop()
