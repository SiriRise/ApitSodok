from tkinter import *
import os
from tkinter.messagebox import showwarning
import string
import tkinter as tk
import random


show_setting = "*"
font_style = ("Arial", 16, "bold")
font_style_text = ("Arial", 16)


def program_start(username):
    # создаём окно
    root.title('Апит Содок')  # заголовок окна
    root.resizable(False, False)
    doska = Canvas(width=800, height=800, bg='#FFFFF3')

    doska.pack()

    i1 = PhotoImage(file="res\\2b.gif")
    i2 = PhotoImage(file="res\\2h.gif")
    peshki = [0, i1, i2]

    # начинаем новую игру
    def novaya_igra():
        global pole, current_player, comp, player
        pole = [[2] * 8, [0] * 8, [2] * 8, [0] * 8, [0] * 8, [1] * 8, [0] * 8, [1] * 8]

        vivod(0, 0)
        player = 1
        comp = 2
        current_player = 0
        MsgBox = tk.messagebox.askquestion("Выбор первого хода", f"{username} вы хотите ходить первым?")
        if MsgBox == "yes":
            current_player = player
        else:
            current_player = comp
            root.after(500, hod_bota)


    def vivod(x_poz_1, y_poz_1):
        global pole, kr_ramka, zel_ramka
        cell_size = 100
        doska.delete('all')

        # Рисуем доску
        for x in range(8):
            for y in range(8):
                doska.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill="#FFFFF3")

        kr_ramka = doska.create_rectangle(-5, -5, -5, -5, outline="red", width=4)

        zel_ramka = doska.create_rectangle(-5, -5, -5, -5, outline="green", width=4)

        # Рисуем стоячие пешки
        for x in range(8):
            for y in range(8):
                z = pole[y][x]
                if z and (x_poz_1, y_poz_1) != (x, y):
                    doska.create_image(x * cell_size, y * cell_size, anchor=NW, image=peshki[z])

        # Рисуем активную пешку
        z = pole[y_poz_1][x_poz_1]
        if z:
            doska.create_image(x_poz_1 * cell_size, y_poz_1 * cell_size, anchor=NW, image=peshki[z], tag='ani')
            doska.update()  # Обновление

    # выбор клетки для хода 1
    def pozici_1(event):

        x, y = (event.x) // 100, (event.y) // 100  # вычисляем координаты клетки
        if 0 <= x < 8 and 0 <= y < 8:
            doska.coords(zel_ramka, x * 100 + 3, y * 100 + 3, x * 100 + 98, y * 100 + 98)


    def pozici_2(event):
        global poz1_x, poz1_y, poz2_x, poz2_y
        try:
            x, y = (event.x) // 100, (event.y) // 100
            if pole[y][x] == player:
                doska.coords(kr_ramka, x * 100 + 3, y * 100 + 3, x * 100 + 98, y * 100 + 98)
                poz1_x, poz1_y = x, y
            elif pole[poz1_y][poz1_x] == player:
                poz2_x, poz2_y = x, y
                if check_move_available(poz1_x, poz1_y, poz2_x, poz2_y):
                    hod_igroka()

                    doska.coords(kr_ramka, -5, -5, -5, -5)
        except tk.TclError:
            pass
        except NameError:
            pass


    def hod_igroka():  # Ход игрока
        global poz1_x, poz1_y, poz2_x, poz2_y, player , current_player

        if pole[poz1_y][poz1_x] == player and check_move_available(poz1_x, poz1_y, poz2_x, poz2_y):
            # делаем ход
            pole[poz2_y][poz2_x], pole[poz1_y][poz1_x] = pole[poz1_y][poz1_x], pole[poz2_y][poz2_x]
            srubit_fishku(poz2_x, poz2_y)
            vivod(0, 0)

            # передаем ход другому игроку
            if igra_okonchena():
                return True
            else:
                current_player = comp
                root.after(500, hod_bota)


    def check_available_moves(x, y, dx, dy):
        moves = []
        new_x, new_y = x + dx, y + dy
        while 0 <= new_x < 8 and 0 <= new_y < 8:
            if pole[new_y][new_x] == 0:
                moves.append((x, y, new_x, new_y))
                new_x += dx
                new_y += dy
            else:
                break
        return moves


    def hod_bota():
        global pole, current_player

        available_moves = []  # Список доступных ходов для каждой пешки
        for y, row in enumerate(pole):
            for x, cell in enumerate(row):
                if cell == comp:  # Если находим пешку противника, проверяем возможные ходы
                    available_moves.extend(check_available_moves(x, y, -1, 0))  # Проверяем ходы влево
                    available_moves.extend(check_available_moves(x, y, 1, 0))  # Проверяем ходы вправо
                    available_moves.extend(check_available_moves(x, y, 0, -1))  # Проверяем ходы вверх
                    available_moves.extend(check_available_moves(x, y, 0, 1))  # Проверяем ходы вниз

        if available_moves:  # Если есть доступные ходы
            move = random.choice(available_moves)  # Выбираем случайный ход
            x_start, y_start, x_end, y_end = move
            # Совершаем ход
            pole[y_end][x_end], pole[y_start][x_start] = pole[y_start][x_start], 0
            srubit_fishku(x_end, y_end)
            vivod(0, 0)
            if igra_okonchena():
                return True
            else:
                current_player = player
        else:
            MsgBox = tk.messagebox.askquestion("Игра окончена", f"{username} вы победили!!\n" "У противника нет доступных ходов\n" "Хотите сыграть еще раз?")
            if MsgBox == "yes":
                vivod(0, 0)
                novaya_igra()
            else:
                root.destroy()
        return True


    def check_move_available(x1, y1, x2, y2):  # Проверка ходов
        global pole
        # проверить, нет ли препятствий (финальная клетка пустая)
        if pole[y2][x2] != 0:
            showwarning("Ошибка хода", "Клетка занята")
            return False

        # шаг должен быть впереди или назад, влево или вправо
        if x1 != x2 and x1 != -1 and y1 != y2:
            showwarning("Ошибка хода", "Так ходить нельзя")
            return False  # был сделан ни горизонтальный, ни вертикальный ход

        if x1 == x2:  # проверка хода по вертикали
            step = 1 if y1 < y2 else -1
            for y in range(y1 + step, y2, step):
                if pole[y][x1] != 0:
                    showwarning("Ошибка хода", "На пути есть препятствие")
                    return False  # если есть препятствие, то ход невозможен
        else:  # проверка хода по горизонтали
            step = 1 if x1 < x2 else -1
            for x in range(x1 + step, x2, step):
                if pole[y1][x] != 0:
                    showwarning("Ошибка хода", "На пути есть препятствие")
                    return False  # если есть препятствие, то ход невозможен
        return True


    def srubit_fishku(x, y):  # Функция "срубания" фигур
        global pole

        for y in range(8):
            for x in range(8):
                if pole[y][x] == current_player and pole[y][x] != 0:
                    if 0 < y < len(pole) - 1 and pole[y - 1][x] != current_player and pole[y - 1][x] != 0 and \
                            pole[y + 1][x] != current_player and pole[y + 1][x] != 0:
                        pole[y - 1][x] = pole[y + 1][x] = 0
                    elif 0 < x < len(pole[0]) - 1 and pole[y][x - 1] != current_player and pole[y][x - 1] != 0 and \
                            pole[y][x + 1] != current_player and pole[y][x + 1] != 0:
                        pole[y][x - 1] = pole[y][x + 1] = 0
                elif pole[y][x] != current_player and pole[y][x] != 0:
                    if 0 < y < len(pole) - 1 and pole[y - 1][x] == current_player and pole[y - 1][x] != 0 and \
                            pole[y + 1][x] == current_player and pole[y + 1][x] != 0:
                        pole[y][x] = 0
                    elif 0 < x < len(pole[0]) - 1 and pole[y][x - 1] == current_player and pole[y][x - 1] != 0 and \
                            pole[y][x + 1] == current_player and pole[y][x + 1] != 0:
                        pole[y][x] = 0


    def igra_okonchena():
        # Проверка, есть ли на поле фигурки для каждого игрока
        player_remaining = any(player in row for row in pole)
        comp_remaining = any(comp in row for row in pole)

        # Если одному из игроков нечем ходить, игра окончена
        if not comp_remaining:
            MsgBox = tk.messagebox.askquestion("Игра окончена", f"{username} вы победили!!\n""Хотите сыграть еще раз?")
            if MsgBox == "yes":
                vivod(0, 0)
                novaya_igra()
            else:
                root.destroy()
            return True
        elif not player_remaining:
            MsgBox = tk.messagebox.askquestion("Игра окончена", f"{username} вы проиграли!!\n""Хотите сыграть еще раз?")
            if MsgBox == "yes":
                vivod(0, 0)
                novaya_igra()
            else:
                root.destroy()
            return True


    novaya_igra()
    vivod(0, 0)  # рисуем игровое поле
    doska.bind("<Motion>", pozici_1)  # движение мышки по полю
    doska.bind("<Button-1>", pozici_2)  # нажатие левой кнопки


def password_encryption(password):
    key = 3
    encryption_password = ""
    for i in password:
        encryption_password_temp = chr(ord(i) + key)
        encryption_password += encryption_password_temp
        key = -key + 1
    return encryption_password


def registration():
    username = entry_username.get()
    password_raw = entry_password.get()
    password = password_encryption(password_raw)

    if not username or not password:
        showwarning("Регистрация", "Пожалуйста, заполните все поля")
        return
    if len(username) <= 2:
        showwarning("Регистрация", "Имя пользователя должно быть длиннее 2 символов")
        return
    if len(password) < 8 or not any(char in password for char in string.punctuation):
        showwarning("Регистрация", "Пароль должен быть длиннее 7 символов и содержать хотя бы один специальный символ")
        return

    print(username, password)
    with open("user_data.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            stored_username, _ = line.strip().split('•')
            if username == stored_username:
                showwarning("Регистрация", "Пользователь с таким именем уже существует")
                return

    with open("user_data.txt", "a") as file:
        file.write(f'{username}•{password}\n')
    showwarning("Регистрация", "Регистрация прошла успешно!")
    program_start(username)


def login():
    username = entry_username.get()
    password_raw = entry_password.get()
    password = password_encryption(password_raw)

    if not username or not password:
        showwarning("Авторизация", "Пожалуйста, заполните все поля")
        return

    with open("user_data.txt", "r") as file:
        lines = file.readlines()
        user_found = False
        incorrect_password = False

        for line in lines:
            stored_username, stored_password = line.strip().split('•')
            if username == stored_username:
                if password == stored_password:
                    user_found = True
                    showwarning("Авторизация", f"Добро пожаловать {username}!")
                    program_start(username)
                    break
                else:
                    incorrect_password = True
                    break
        if not user_found or incorrect_password:
            showwarning("Вход", "Неверный логин или пароль")
        return


if not os.path.exists("user_data.txt"):
    with open("user_data.txt", "w"):
        pass


def show_password():
    global show_setting
    if show_setting == "*":
        show_setting = ""
        button_text = "Скрыть пароль"
    else:
        show_setting = "*"
        button_text = "Показать пароль"
    try:
        button_show_password.config(text=button_text)
        entry_password.config(show=show_setting)
    except (NameError):
        pass


root = Tk()
root.resizable(False, False)
root.title("Регистрация и вход")
width = 800
height = 800

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)

root.geometry("%dx%d+%d+%d" % (width, height, x, y))

label_username = Label(root, text="Логин", font=font_style)
label_username.place(x=254, y=70)

entry_username = Entry(root, font=font_style_text)
entry_username.place(x=254, y=100, width=292, height=45)

label_password = Label(root, text="Пароль", font=font_style)
label_password.place(x=254, y=170)

entry_password = Entry(root, show=show_setting, font=font_style_text)
entry_password.place(x=254, y=200, width=292, height=45)

button_reg = Button(root, text="Регистрация", command=registration, font=font_style)
button_reg.place(x=254, y=270, width=292, height=45)

button_log = Button(root, text="Авторизация", command=login, font=font_style)
button_log.place(x=254, y=320, width=292, height=45)

button_show_password = Button(root, text="Показать пароль", command=show_password, font=font_style_text)
button_show_password.place(x=546, y=200, width = 170, height=45)

mainloop()