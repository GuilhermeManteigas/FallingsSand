import threading
import os
from msvcrt import getch
from time import sleep
import ctypes
import random
import time

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)

clear = lambda: os.system('cls')

COLOR_BLACK = "\033[1;30;40m"
COLOR_RED = "\033[1;31;40m"
COLOR_GREEN = "\033[1;32;40m"
COLOR_YELLOW = "\033[1;33;40m"
COLOR_BLUE = "\033[1;34;40m"
COLOR_PURPLE = "\033[1;35;40m"
COLOR_CYAN = "\033[1;36;40m"
COLOR_WHITE = "\033[1;37;40m"

game_on = []
game_time = 0
sand_dodged = 0

map = [
    [COLOR_PURPLE + "+", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-",
     "-", "-", "-", "-", "-", "+" + COLOR_PURPLE],
    ["|", COLOR_YELLOW + " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ",  COLOR_PURPLE + "|"],
    ["|", COLOR_YELLOW + " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", COLOR_PURPLE + "|"],
    ["|", COLOR_YELLOW + " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", COLOR_PURPLE + "|"],
    ["|", COLOR_YELLOW + " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", COLOR_PURPLE + "|"],
    ["|", COLOR_YELLOW + " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", COLOR_PURPLE + "|"],
    ["|", COLOR_YELLOW + " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", COLOR_PURPLE + "|"],
    ["|", COLOR_YELLOW + " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", COLOR_PURPLE + "|"],
    ["|", COLOR_YELLOW + " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", COLOR_PURPLE + "|"],
    ["|", COLOR_YELLOW + " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", COLOR_PURPLE + "|"],
    ["|", COLOR_YELLOW + " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", COLOR_PURPLE + "|"],
    ["|", COLOR_YELLOW + " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", COLOR_PURPLE + "|"],
    [COLOR_PURPLE + "+", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-",
     "-", "-", "-", "-", "-", "+"]]

PLAYER_ROW = 11


def timer():
    while len(game_on) < 1:
        time.sleep(0.1)
        global game_time
        game_time += 100


def get_time(time):
    ms = (time % 1000) // 10
    s = (time//1000) % 60
    m = ((time//1000)//60) % 60
    return [m, s, ms]


def print_map():
    while len(game_on) < 1:
        temp = ""
        for i in map:
            for j in i:
                temp += j
            temp += "\n"
        temp += "|     " + COLOR_CYAN + "Time       " + COLOR_GREEN + "Points" + COLOR_PURPLE + "     |\n"
        temp += "|   " + COLOR_CYAN + "{:>02}:{:>02}:{:>02}      " + COLOR_GREEN + "{:>04}      " + COLOR_PURPLE + "|\n"
        temp += "|---------------------------|\n"
        clear()
        m, s, ms = get_time(game_time)
        print(temp.format(m, s, ms, sand_dodged))


sand_list = []


def create_sand():
    while len(game_on) < 1:
        time.sleep(0.5)
        rand = random.randint(1, 27)
        if map[1][rand] == " ":
            map[1][rand] = "-"
            sand_list.append([1, rand])


def update_sand():
    while len(game_on) < 1:
        time.sleep(0.5)
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
                game_on.append("lost")
                print_map()
                print("Players lost game")


clock = threading.Thread(target=timer)
clock.start()

mapUpdater = threading.Thread(target=print_map)
mapUpdater.start()

sandCreator = threading.Thread(target=create_sand)
sandCreator.start()

sandUpdater = threading.Thread(target=update_sand)
sandUpdater.start()

player_position = 14
map[PLAYER_ROW][player_position] = COLOR_RED + "O" + COLOR_BLACK

while len(game_on) < 1:
    key = getch()
    if key == b'K':
        if player_position > 1:
            map[PLAYER_ROW][player_position] = " "
            player_position -= 1
            #if map[PLAYER_ROW][player_position] == "-":
            #sand_list.remove([PLAYER_ROW, player_position])
            map[PLAYER_ROW][player_position] = COLOR_RED + "O" + COLOR_BLACK
    elif key == b'M':
        if player_position < 27:
            map[PLAYER_ROW][player_position] = " "
            player_position += 1
            #if map[PLAYER_ROW][player_position] == "-":
            #sand_list.remove([PLAYER_ROW, player_position])
            map[PLAYER_ROW][player_position] = COLOR_RED + "O" + COLOR_BLACK
