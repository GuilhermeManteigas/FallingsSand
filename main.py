import threading
import os
from msvcrt import getch
from time import sleep
import ctypes
import random
import time
import sys
import subprocess

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)
kernel32.SetConsoleTitleW("Falling Sand")
os.system('mode con: cols=30 lines=20')

clear = lambda: os.system('cls')

COLOR_BLACK = "\033[1;30;40m"
COLOR_RED = "\033[1;31;40m"
COLOR_GREEN = "\033[1;32;40m"
COLOR_YELLOW = "\033[1;33;40m"
COLOR_BLUE = "\033[1;34;40m"
COLOR_PURPLE = "\033[1;35;40m"
COLOR_CYAN = "\033[1;36;40m"
COLOR_WHITE = "\033[1;37;40m"

PLAYER_ROW = 11
game_on = True
game_time = 0
sand_dodged = 0
sand_list = []
player_position = 14

map = [
    [COLOR_PURPLE + "+", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-",
     "-", "-", "-", "-", "-", "+" + COLOR_PURPLE],
    ["|" + COLOR_YELLOW, " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ",  COLOR_PURPLE + "|"],
    ["|" + COLOR_YELLOW, " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", COLOR_PURPLE + "|"],
    ["|" + COLOR_YELLOW, " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", COLOR_PURPLE + "|"],
    ["|" + COLOR_YELLOW, " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", COLOR_PURPLE + "|"],
    ["|" + COLOR_YELLOW, " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", COLOR_PURPLE + "|"],
    ["|" + COLOR_YELLOW, " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", COLOR_PURPLE + "|"],
    ["|" + COLOR_YELLOW, " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", COLOR_PURPLE + "|"],
    ["|" + COLOR_YELLOW, " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", COLOR_PURPLE + "|"],
    ["|" + COLOR_YELLOW, " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", COLOR_PURPLE + "|"],
    ["|" + COLOR_YELLOW, " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", COLOR_PURPLE + "|"],
    ["|" + COLOR_YELLOW, " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", COLOR_PURPLE + "|"],
    [COLOR_PURPLE + "+", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-",
     "-", "-", "-", "-", "-", "+"]]


def timer():
    while game_on:
        time.sleep(0.1)
        global game_time
        game_time += 100
        threading.Thread(target=print_map).start()


def get_time(time):
    ms = (time % 1000) // 10
    s = (time//1000) % 60
    m = ((time//1000)//60) % 60
    return [m, s, ms]


def print_map():
        temp = ""
        for i in map:
            for j in i:
                temp += j
            temp += "\n"
        temp += "|     " + COLOR_YELLOW + "Time       " + COLOR_YELLOW + "Points" + COLOR_PURPLE + "     |\n"
        temp += "|   " + COLOR_CYAN + "{:>02}:{:>02}:{:>02}      " + COLOR_GREEN + "{:>04}      " + COLOR_PURPLE + "|\n"
        temp += "+---------------------------+"
        clear()
        m, s, ms = get_time(game_time)
        print(temp.format(m, s, ms, sand_dodged))


def create_sand():
    while game_on:
        time.sleep(0.5 * (((2200 - sand_dodged)//200)/10))
        rand = random.randint(1, 27)
        if map[1][rand] == " ":
            map[1][rand] = "-"
            sand_list.append([1, rand])


def update_sand():
    while game_on:
        time.sleep(0.3)
        for index, i in enumerate(sand_list):
            vertical = i[0]
            horizontal = i[1]
            if vertical <= 11:
                map[vertical][horizontal] = " "
                map[vertical + 1][horizontal] = "-"
                sand_list[index] = [vertical + 1, horizontal]
            else:
                sand_list.remove([vertical, horizontal])
                global sand_dodged
                sand_dodged += 1
        threading.Thread(target=check_impact).start()


def check_impact():
    for i in sand_list:
        if i[1] == player_position:
            if i[0] == 11:
                global game_on
                game_on = False
                time.sleep(0.1)
                if sand_dodged < 2000:
                    print(COLOR_PURPLE + "|" + COLOR_RED + "     You Lost The Game     " + COLOR_PURPLE + "|")
                else:
                    print(COLOR_PURPLE + "|" + COLOR_GREEN + "     You Won The Game!     " + COLOR_PURPLE + "|")
                print(COLOR_PURPLE + "+---------------------------+")
                threading.Thread(target=show_credits).start()


def show_credits():
    credit_list = ["|                           |",
                   "|                           |",
                   "|                           |",
                   "|       Game Creator:       |",
                   "|    Guilherme Manteigas    |",
                   "|                           |",
                   "|                           |",
                   "|                           |",
                   "|                           |",
                   "|           Thank           |",
                   "|            You            |",
                   "|                           |",
                   "|            For            |",
                   "|          Playing          |",
                   "|            :D             |",
                   "|                           |",
                   "|                           |",
                   "+---------------------------+"]

    for i in credit_list:
        time.sleep(0.2)
        print(i)
    time.sleep(1)
    threading.Thread(target=play_again).start()


def play_again():
    play_again_list = [" ",
                   "+---------------------------+\n"+
                   "|                           |\n"+
                   "|                           |\n"+
                   "|                           |\n"+
                   "|       Game Creator:       |\n"+
                   "|    Guilherme Manteigas    |\n"+
                   "|                           |\n"+
                   "|                           |\n"+
                   "|                           |\n"+
                   "|                           |\n"+
                   "|           Thank           |\n"+
                   "|            You            |\n"+
                   "|                           |\n"+
                   "|            For            |\n"+
                   "|          Playing          |\n"+
                   "|            :D             |\n"+
                   "|                           |\n"+
                   "|                           |\n"+
                   "+---------------------------+",
                   " "," ",
                   "+---------------------------+\n" +
                   "|                           |\n" +
                   "|                           |\n" +
                   "|                           |\n" +
                   "|       Game Creator:       |\n" +
                   "|    Guilherme Manteigas    |\n" +
                   "|                           |\n" +
                   "|                           |\n" +
                   "|                           |\n" +
                   "|                           |\n" +
                   "|           Thank           |\n" +
                   "|            You            |\n" +
                   "|                           |\n" +
                   "|            For            |\n" +
                   "|          Playing          |\n" +
                   "|            :D             |\n" +
                   "|                           |\n" +
                   "|                           |\n" +
                   "+---------------------------+",
                   " ", " ",
                   "\\"," ",
                   " ", " ",
                   "\\\\", " ",
                   "\\\\Do", " ",
                   "\\\\Do You", " ",
                   "\\\\Do You Want", " ",
                   "\\\\Do You Want To", " ",
                   "\\\\Do You Want To Play", " ",
                   "\\\\Do You Want To Play Again", " ",
                   "\\\\Do You Want To Play Again?", " ",
                   "\\\\Do You Want To Play Again?\n(yes/no)"]
    for i in play_again_list:
        time.sleep(0.1)
        clear()
        print(i)

    answer = input("(yes/no)\n")
    if answer == "yes" or answer == "Yes" or answer == "y" or answer == "Y" or answer == "es":
        os.system('py "main.py"')
    else:
        os.system('exit')


def start_game():
    global map
    global player_position
    map[PLAYER_ROW][player_position] = COLOR_RED + "O" + COLOR_YELLOW

    clock = threading.Thread(target=timer)
    clock.start()

    sand_creator = threading.Thread(target=create_sand)
    sand_creator.start()

    sand_updater = threading.Thread(target=update_sand)
    sand_updater.start()

    while game_on:
        key = getch()
        if key == b'K':
            if player_position > 1:
                map[PLAYER_ROW][player_position] = " "
                player_position -= 1
                map[PLAYER_ROW][player_position] = COLOR_RED + "O" + COLOR_YELLOW
        elif key == b'M':
            if player_position < 27:
                map[PLAYER_ROW][player_position] = " "
                player_position += 1
                map[PLAYER_ROW][player_position] = COLOR_RED + "O" + COLOR_YELLOW


start_game()
