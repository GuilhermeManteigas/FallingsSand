import threading
import os
from msvcrt import getch
from time import sleep

clear = lambda: os.system('cls')

map = [["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|"],
       ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|"],
       ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|"],
       ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|"],
       ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|"],
       ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|"],
       ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|"],
       ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|"],
       ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|"]]


def print_map():
    while True:
        #sleep(0.05)

        temp = ""
        for i in map:
            for j in i:
                temp += j
                #print(j, end="")
            temp += "\n"
        clear()
        print(temp)


x = threading.Thread(target=print_map)
x.start()

while True:
    key = getch()
    if key == b'K':
        map[1][1] = "O"
