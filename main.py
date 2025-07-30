import pygame_textinput
from PIL import Image
import pygame
import time
import json
import webpage, website
import os
import asyncio
import subprocess
import os
import psutil
from concurrent.futures import ThreadPoolExecutor
import threading
import random
import urllib.parse
import shutil
import sys
import math

# Init Pygame
pygame.init()
screen = pygame.display.set_mode((1000, 667))
clock = pygame.time.Clock()


# Load fonts !
font = pygame.font.Font("assets/VarelaRound-Regular.ttf", 24)
font2 = pygame.font.Font("assets/LuckiestGuy-Regular.ttf", 30)
font3 = pygame.font.Font("assets/FiraSans-Bold.ttf", 30)
font4 = pygame.font.Font("assets/FiraSans-Bold.ttf", 40)
font5 = pygame.font.Font("assets/FiraSans-Bold.ttf", 24)
font6 = pygame.font.Font("assets/FiraSans-Bold.ttf", 18)

# Text Input Setup for Landing Page !
manager = pygame_textinput.TextInputManager(validator=lambda input: len(input) <= 35)
textinput = pygame_textinput.TextInputVisualizer(manager=manager, font_object=font)
textinput.font_color = (255, 255, 255)


# Image Loading & Transformations/Scaling !
main_logoji = pygame.image.load("assets/main_logo_webber.png")

logo = pygame.image.load("assets/spider_logo_main.png")
logo3 = pygame.transform.scale(logo, (96, 96))
logo2 = pygame.transform.scale(logo, (64,64))
pygame.display.set_icon(logo)
pygame.display.set_caption("Webber")

aleft = pygame.image.load("assets/arrow_left.svg")
aright = aleft.copy()
aright = pygame.transform.rotate(aright, 180)

img = pygame.image.load("assets/bgimg.png")
simg = pygame.image.load("assets/settings_bg.jpeg")
simg.set_alpha(40)
# img.set_alpha(10)
btn_img = pygame.image.load("assets/w_button_ji.png")
btn_img_clicked = pygame.image.load("assets/w_button_ji_animated.png")
spider_img = pygame.image.load("assets/spider.png")
spider_hanging_img = pygame.image.load("assets/fff.png")
rocket = pygame.image.load("assets/rocket_icon.png")
exclamation = pygame.image.load("assets/exclamation.png")
delete = pygame.image.load("assets/delete.png")
pause = pygame.image.load("assets/pause.png")
play = pygame.image.load("assets/play.png")
cancel = pygame.image.load("assets/cancel.png")
settings = pygame.image.load("assets/spidieee.png")
tick = pygame.image.load("assets/tick.png")
eye = pygame.image.load('assets/eye.png')

btn_img = pygame.transform.scale(btn_img, (314, 74))
btn_img_clicked = pygame.transform.scale(btn_img_clicked, (314, 74))
spider_img = pygame.transform.scale(spider_img, (254, 186))
#spider_hanging_img = pygame.transform.scale(spider_hanging_img, (313, 267))
# rocket = pygame.transform.scale(rocket, (39, 39))
exclamation = pygame.transform.scale(exclamation, (32, 35))
delete = pygame.transform.scale(delete, (35, 35))
pause = pygame.transform.scale(pause, (35, 35))

right = pygame.transform.scale(play, (25, 25))
left = pygame.transform.rotate(right, 180)
left2 = left.copy()
left2.set_alpha(130)
right2 = right.copy()
right2.set_alpha(130)
play = pygame.transform.scale(play, (35, 35))
cancel = pygame.transform.scale(cancel, (30, 30))
tick = pygame.transform.scale(tick, (40, 40))
tick2 = tick.copy()
tick2 = pygame.transform.scale(tick2, (35, 35))
settings = pygame.transform.scale(settings, (80, 80))
eye = pygame.transform.scale(eye, (35, 35))


# Custom Mouse Images
surf = pygame.image.load("assets/mouse.png")
surf = pygame.transform.scale(surf, (50,50))
nw_mouse = pygame.cursors.Cursor((5, 5), surf)


surf2 = pygame.image.load("assets/mouse2.png")
surf2 = pygame.transform.scale(surf2, (50,50))
nw_mouse2 = pygame.cursors.Cursor((5, 5), surf2)
pygame.mouse.set_cursor(nw_mouse2)

surf3 = pygame.image.load("assets/i-cursor-solid.svg")
surf3 = pygame.transform.scale(surf3, (20,40))
nw_mouse3 = pygame.cursors.Cursor((5, 5), surf3)
pygame.mouse.set_cursor(nw_mouse3)



