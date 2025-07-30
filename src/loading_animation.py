"""

    Outdated File !
    Contains animation for console based website downloading !

    
"""










import time
import sys
import os
from threading import Event


def load_animation(display_text, event):
    animation = "|/-\\"
    i = 0
    anicount = 0
    k=0
    p=0
    ls_len = len(display_text[p])
    while event.is_set():
        if k%50==0:
            p+=1
            ls_len = len(display_text[p%len(display_text)])
            i = 0
        time.sleep(0.075)
        load_str_list = list(display_text[p%len(display_text)])

        x = ord(load_str_list[i])
        y = 0

        if x!=32 and x!=46:
            if x>90:
                y = x-32
            else:
                y = x+32
            load_str_list[i] = chr(y)

        res = ''
        for j in range(ls_len):
            res += load_str_list[j]

        sys.stdout.write("\r"+res+animation[anicount])
        sys.stdout.flush()

        display_text[p%len(display_text)] = res

        anicount = (anicount + 1)%4
        i = (i + 1) % ls_len
        k+=1
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


if __name__ == "__main__":
    a = Event()
    a.set()
    load_animation(["Loading animation ","Scraping Earth"], a)