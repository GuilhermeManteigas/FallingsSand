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

game_on = []
game_time = 0

map = [
    ["+", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-",
     "-", "-", "-", "-", "-", "+"],
    ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", "|"],
    ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", "|"],
    ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", "|"],
    ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", "|"],
    ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", "|"],
    ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", "|"],
    ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", "|"],
    ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", "|"],
    ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", "|"],
    ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", "|"],
    ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
     " ", " ", " ", " ", " ", "|"],
    ["+", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-",
     "-", "-", "-", "-", "-", "+"]]

PLAYER_ROW = 11


def timer():
    while len(game_on) < 1:
        time.sleep(0.1)
        global game_time
        game_time += 100


def gettime(time):
    ms = time % 1000
    s = (time//1000)%60
    m = ((time//1000)//60)%60
    #while s > 60:
     #   s -= 60
      #  m += 1
    return [m, s, ms]


def print_map():
    while len(game_on) < 1:
        temp = ""
        for i in map:
            for j in i:
                temp += j
            temp += "\n"
        temp += "|     Time - {:>02}:{:>02}:{:>02}           |\n"
        temp += "|----------------------------|\n"
        clear()
        m, s, ms = gettime(game_time)
        print(temp.format(m, s, ms))


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
            if vertical < 11:
                # print("here")
                map[vertical][horizontal] = " "
                map[vertical + 1][horizontal] = "-"
                sand_list[index] = [vertical + 1, horizontal]
            else:
                map[vertical][horizontal] = " "
                sand_list.remove([vertical, horizontal])


def check_impact():
    while len(game_on) < 1:
        for i in sand_list:
            if i[0] == 11:
                if i[1] == player_position:
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

checkImpactUpdater = threading.Thread(target=check_impact)
checkImpactUpdater.start()

player_position = 14
map[PLAYER_ROW][player_position] = "O"

while len(game_on) < 1:
    key = getch()
    if key == b'K':
        if player_position > 1:
            map[PLAYER_ROW][player_position] = " "
            player_position -= 1
            map[PLAYER_ROW][player_position] = "O"
            # create_sand()
            # update_sand()
    elif key == b'M':
        if player_position < 27:
            map[PLAYER_ROW][player_position] = " "
            player_position += 1
            map[PLAYER_ROW][player_position] = "O"
            # create_sand()
            # update_sand()
