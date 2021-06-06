import time
from tkinter import *


class TwoBodyView(object):

    empty_list = []

    with open("results.txt") as f:
        for line in f:
            x = line.split(",")
            empty_list.append(x)

    body_one_x = []
    body_one_y = []
    body_two_x = []
    body_two_y = []

    for i in range(10000):
        for j in range(1):
            body_one_x.append(empty_list[i][0])
            body_one_y.append(empty_list[i][1])
            body_two_x.append(empty_list[i][2])
            body_two_y.append(empty_list[i][3])

    tk = Tk()

    H = 500
    W = 600

    canvas = Canvas(tk, width=W, height=H)
    tk.title("Graphics")
    canvas.pack()

    body_one = canvas.create_oval(185, 185, 200, 200, fill="red")
    body_two = canvas.create_oval(285, 285, 300, 300, fill="blue")


    for i in range(1, len(body_two_x)):

        canvas.move(body_one, (float(body_one_x[i]) - float(body_one_x[i - 1]))*50, (float(body_one_y[i]) - float(body_one_y[i - 1]))*50)
        canvas.move(body_two, (float(body_two_x[i]) - float(body_two_x[i - 1]))*50, (float(body_two_y[i]) - float(body_two_y[i - 1]))*50)

        canvas.create_line(canvas.coords(body_one), fill="red")
        canvas.create_line(canvas.coords(body_two), fill="blue")

        tk.update()
        time.sleep(0.00001)


view = TwoBodyView()

