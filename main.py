from tkinter import *
from tkinter import colorchooser
from random import *
import time
import threading

size = 1001
root = Tk()
canvas = Canvas(root, width=size, height=size, bg='black')
canvas.pack()
count = 0
def moving_particle():
    ball = canvas.create_oval(530, 980, 550, 1000, fill='white',outline='white')
    x0 = uniform(-0.7, 0.7)
    y0 = randint(-4, -1)
    live_time = randrange(34, 54)
    for i in range(live_time + 2):
        if i == live_time//2:
            canvas.itemconfig(ball, fill='light gray', outline='light gray')
        if i == live_time - 7:
            canvas.itemconfig(ball, fill='gray', outline='gray')
        canvas.move(ball, x0, y0)
        time.sleep(0.003)
        root.update()
    canvas.delete(ball)
    moving_particle()

for i in range(35):
    thred = threading.Thread(target=moving_particle)
    thred.start()


root.mainloop()