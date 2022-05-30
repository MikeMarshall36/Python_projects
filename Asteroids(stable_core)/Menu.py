import os
from tkinter import *
root = Tk()
root.title('Запуск симуляции астероидов')
root.geometry('300x250')
root.resizable(False, False)


def launch_game():
    print('Запускаемся')
    os.system('python main.py')


def exit_game():
    exit()


def run():
    btn = Button(
        root,
        activebackground='maroon',
        bg='red', justify='left',
        text='Начать',
        command=launch_game
    )
    btn.pack()
    exit = Button(
        root,
        activebackground='blue',
        bg='steelblue',
        justify='right',
        text='Выйти',
        command=exit_game
    )
    exit.pack()

text = Text(
    width=25,
    height=5,
    font='Arial 14',
    bg='black',
    fg='green'
)
text.pack()
text.insert(1.0, "Asteroids")


run()
root.mainloop()
