import os
os.makedirs('data',exist_ok=True)
os.makedirs('sites',exist_ok=True)
os.makedirs('temp',exist_ok=True)
import pygame_textinput
from PIL import Image
import pygame
import time
import json
import webpage, website
import asyncio
import subprocess
import psutil
import threading
import random
import urllib.parse
import shutil
import sys
import webbrowser

BASE = getattr(sys, '_MEIPASS', os.path.abspath('.'))

assets = ['bgimg.png','cancel.gif','cancel.png','del.gif','delete.gif','delete.png','eye.png','fs.jpeg','github.png','gmail.png','hanging_spider.png','i-cursor.png','idea.gif','internet.gif','leftji.png','main_logo_webber.png','man.gif','meditation.gif','mouse.png','mouse2.png','pause.png','play.png','rocket_icon.png','sad.gif','slack.png','some_catie.gif','spider_logo_main.png','spider.png','ss.png','success.gif','tick.png','w_button_ji_animated.png','w_button_ji.png','fonts/FiraSans-Bold.ttf','fonts/HappyMonkey-Regular.ttf','fonts/LuckiestGuy-Regular.ttf','fonts/VarelaRound-Regular.ttf']

pygame.init()
fontp = pygame.font.Font(None,24)
img = pygame.image.load(os.path.join(BASE,"assets/bgimg.png"))
screen = pygame.display.set_mode((1000, 667))
clock = pygame.time.Clock()
screen.blit(img,(0,0))
bh = fontp.render("Loading Assets ...", True, (255, 255, 255))
screen.blit(bh, (10,10))
pygame.display.set_caption("Webber")
pygame.display.update()

# for ice in assets:
#     if not os.path.exists(f'assets/{ice}'):
#         screen.blit(img,(0,0))
#         bh = fontp.render("Missing Assets !! Please re-install to resolve this issue !!", True, (255, 255, 255))
#         screen.blit(bh, (10,10))
#         pygame.display.update()
#         time.sleep(10)
#         sys.exit()


re_write = True
if os.path.exists('data/details.json'):
    re_write = False
    with open('data/details.json','r') as k:
        try:
            a = json.load(k)['Websites']
        except:
            re_write = True
else:
    with open('data/details.json','w') as ll:
        json.dump({"Websites": []},ll)


total_lists = {}
cached_done_once = True

apman = fontp.render("Loading Assets ...",True,(255,255,255))
screen.blit(apman, (20,20))

font = pygame.font.Font(os.path.join(BASE,"assets/fonts/VarelaRound-Regular.ttf"), 24)
font2 = pygame.font.Font(os.path.join(BASE,"assets/fonts/LuckiestGuy-Regular.ttf"), 30)
font3 = pygame.font.Font(os.path.join(BASE,"assets/fonts/FiraSans-Bold.ttf"), 30)
font4 = pygame.font.Font(os.path.join(BASE,"assets/fonts/FiraSans-Bold.ttf"), 40)
font5 = pygame.font.Font(os.path.join(BASE,"assets/fonts/FiraSans-Bold.ttf"), 24)
font6 = pygame.font.Font(os.path.join(BASE,"assets/fonts/FiraSans-Bold.ttf"), 18)
font7 = pygame.font.Font(os.path.join(BASE,"assets/fonts/LuckiestGuy-Regular.ttf"), 50)
font8 = pygame.font.Font(os.path.join(BASE,"assets/fonts/FiraSans-Bold.ttf"), 10)

some_thread = {}
some_thread_result = {}
display_err = False
display_err_msg = ""

# Create TextInput-object
manager = pygame_textinput.TextInputManager(validator=lambda input: len(input) <= 35)
textinput = pygame_textinput.TextInputVisualizer(manager=manager, font_object=font)

textinput.font_color = (255, 255, 255)

main_logoji = pygame.image.load(os.path.join(BASE,"assets/main_logo_webber.png"))

logo = pygame.image.load(os.path.join(BASE,"assets/spider_logo_main.png"))
logo3 = pygame.transform.scale(logo, (96, 96))
logo2 = pygame.transform.scale(logo, (64,64))
pygame.display.set_icon(logo)
pygame.display.set_caption("Webber")

aleft = pygame.image.load(os.path.join(BASE,"assets/leftji.png"))
aleft = pygame.transform.scale(aleft, (30,30))
aright = aleft.copy()
aright = pygame.transform.rotate(aright, 180)

github = pygame.image.load(os.path.join(BASE,'assets/github.png'))
slack = pygame.image.load(os.path.join(BASE,'assets/slack.png'))
simg = pygame.image.load(os.path.join(BASE,"assets/fs.jpeg"))
simg.set_alpha(40)
screenshot = pygame.image.load(os.path.join(BASE,"assets/ss.png"))
# img.set_alpha(10)
btn_img = pygame.image.load(os.path.join(BASE,"assets/w_button_ji.png"))
btn_img_clicked = pygame.image.load(os.path.join(BASE,"assets/w_button_ji_animated.png"))
spider_img = pygame.image.load(os.path.join(BASE,"assets/spider.png"))
spider_hanging_img = pygame.image.load(os.path.join(BASE,"assets/hanging_spider.png"))
rocket = pygame.image.load(os.path.join(BASE,"assets/rocket_icon.png"))
delete = pygame.image.load(os.path.join(BASE,"assets/delete.png"))
pause = pygame.image.load(os.path.join(BASE,"assets/pause.png"))
play = pygame.image.load(os.path.join(BASE,"assets/play.png"))
cancel = pygame.image.load(os.path.join(BASE,"assets/cancel.png"))
tick = pygame.image.load(os.path.join(BASE,"assets/tick.png"))
eye = pygame.image.load(os.path.join(BASE,'assets/eye.png'))
gmail = pygame.image.load(os.path.join(BASE,'assets/gmail.png'))

github = pygame.transform.scale(github, (45,45))
slack = pygame.transform.scale(slack, (108, 44.25))
gmail = pygame.transform.scale(gmail, (30,30))
btn_img = pygame.transform.scale(btn_img, (314, 74))
btn_img_clicked = pygame.transform.scale(btn_img_clicked, (314, 74))
spider_img = pygame.transform.scale(spider_img, (254, 186))
#spider_hanging_img = pygame.transform.scale(spider_hanging_img, (313, 267))
# rocket = pygame.transform.scale(rocket, (39, 39))
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
eye = pygame.transform.scale(eye, (35, 35))

rect = img.get_rect()
rect2 = btn_img.get_rect()
rect3 = btn_img.get_rect()
# print(rect)
rect2.x = 465
rect2.y = 340+119
rect3.x = 465
rect3.y = 340+119
screen.fill((225, 225, 225))

# pygame.key.set_repeat(200, 25)
pressed = False
STARTED = pygame.USEREVENT
LOGS_LOADING = pygame.USEREVENT

hover_downloads = False
DOWNLOADS_HOVER = pygame.USEREVENT
pressed_downloads = False
pressed_credits = False
DOWNLOADS_PRESSED = pygame.USEREVENT
CREDITS_PRESSED = pygame.USEREVENT
CANCEL_PRESSED = pygame.USEREVENT
LOADER = pygame.USEREVENT
DELETE_IT = pygame.USEREVENT
DOWNLOAD_THE_DAMN_WEBSITE = pygame.USEREVENT

storage_location = "sites/"

surf = pygame.image.load(os.path.join(BASE,"assets/mouse.png"))
surf = pygame.transform.scale(surf, (50,50))
nw_mouse = pygame.cursors.Cursor((5, 5), surf)


surf2 = pygame.image.load(os.path.join(BASE,"assets/mouse2.png"))
surf2 = pygame.transform.scale(surf2, (50,50))
nw_mouse2 = pygame.cursors.Cursor((5, 5), surf2)
pygame.mouse.set_cursor(nw_mouse2)

surf3 = pygame.image.load(os.path.join(BASE,"assets/i-cursor.png"))
surf3 = pygame.transform.scale(surf3, (40,40))
nw_mouse3 = pygame.cursors.Cursor((5, 5), surf3)
pygame.mouse.set_cursor(nw_mouse3)

gg_rect = pygame.Rect(220, 253+119, 560, 80)

quitting_not_started = True

rect4 = rect2.copy()
rect4.x += 23
rect4.y += 28

rect5 = rect2.copy()
rect5.x += 300
rect5.y += 0
rect5.w = 254
rect5.h = 186

rect6 = rect2.copy()
rect6.x = -60
rect6.y = -75
rect6.w = 313
rect6.h = 267
page_num = 1

rectangle1 = pygame.Rect(780, 20, 200, 50)
rectangle2 = pygame.Rect(815, 30, 200, 50)
rectangle3 = pygame.Rect(30, 600, 160, 50)
rectangle4 = pygame.Rect(65, 610, 160, 50)

rectji = pygame.Rect(10, 10, 200, 50)
rectji2 = pygame.Rect(15, 15, 50, 40)
rectji3 = pygame.Rect(30, 21, 40, 40)

gif = Image.open(os.path.join(BASE,"assets/meditation.gif"))
frames = []
try:
    while True:
        frame = gif.copy().convert("RGBA")
        mode = frame.mode
        size = frame.size
        data = frame.tobytes()
        surf = pygame.image.fromstring(data, size, mode)
        frames.append(surf)
        gif.seek(gif.tell() + 1)
except EOFError:
    pass  # All frames loaded

gif2 = Image.open(os.path.join(BASE,"assets/some_catie.gif"))
frames2 = []
try:
    while True:
        frame2 = gif2.copy().convert("RGBA")
        mode2 = frame2.mode
        size2 = frame2.size
        data2 = frame2.tobytes()
        surf2 = pygame.image.fromstring(data2, size2, mode2)
        frames2.append(surf2)
        gif2.seek(gif2.tell() + 1)
except EOFError:
    pass  # All frames loaded


gif3 = Image.open(os.path.join(BASE,"assets/success.gif"))
frames3 = []
try:
    while True:
        frame3 = gif3.copy().convert("RGBA")
        mode3 = frame3.mode
        size3 = frame3.size
        data3 = frame3.tobytes()
        surf3 = pygame.image.fromstring(data3, size3, mode3)
        frames3.append(surf3)
        gif3.seek(gif3.tell() + 1)
except EOFError:
    pass  # All frames loaded

gif4 = Image.open(os.path.join(BASE,"assets/cancel.gif"))
frames4 = []
try:
    while True:
        frame4 = gif4.copy().convert("RGBA")
        mode4 = frame4.mode
        size4 = frame4.size
        data4 = frame4.tobytes()
        surf4 = pygame.image.fromstring(data4, size4, mode4)
        frames4.append(surf4)
        gif4.seek(gif4.tell() + 1)
except EOFError:
    pass  # All frames loaded

gif5 = Image.open(os.path.join(BASE,"assets/del.gif"))
frames5 = []
try:
    while True:
        frame5 = gif5.copy().convert("RGBA")
        mode5 = frame5.mode
        size5 = frame5.size
        data5 = frame5.tobytes()
        surf5 = pygame.image.fromstring(data5, size5, mode5)
        frames5.append(surf5)
        gif5.seek(gif5.tell() + 1)
except EOFError:
    pass  # All frames loaded

gif6 = Image.open(os.path.join(BASE,"assets/sad.gif"))
frames6 = []
try:
    while True:
        frame6 = gif6.copy().convert("RGBA")
        mode6 = frame6.mode
        size6 = frame6.size
        data6 = frame6.tobytes()
        surf6 = pygame.image.fromstring(data6, size6, mode6)
        frames6.append(surf6)
        gif6.seek(gif6.tell() + 1)
except EOFError:
    pass  # All frames loaded


gif7 = Image.open(os.path.join(BASE,"assets/internet.gif"))
frames7 = []
try:
    while True:
        frame7 = gif7.copy().convert("RGBA")
        mode7 = frame7.mode
        size7 = frame7.size
        data7 = frame7.tobytes()
        surf7 = pygame.image.fromstring(data7, size7, mode7)
        frames7.append(surf7)
        gif7.seek(gif7.tell() + 1)
except EOFError:
    pass  # All frames loaded


gif8 = Image.open(os.path.join(BASE,"assets/man.gif"))
frames8 = []
try:
    while True:
        frame8 = gif8.copy().convert("RGBA")
        mode8 = frame8.mode
        size8 = frame8.size
        data8 = frame8.tobytes()
        surf8 = pygame.image.fromstring(data8, size8, mode8)
        frames8.append(surf8)
        gif8.seek(gif8.tell() + 1)
except EOFError:
    pass  # All frames loaded

gif9 = Image.open(os.path.join(BASE,"assets/idea.gif"))
frames9 = []
try:
    while True:
        frame9 = gif9.copy().convert("RGBA")
        mode9 = frame9.mode
        size9 = frame9.size
        data9 = frame9.tobytes()
        surf9 = pygame.image.fromstring(data9, size9, mode9)
        frames9.append(surf9)
        gif9.seek(gif9.tell() + 1)
except EOFError:
    pass  # All frames loaded




something_done = True
something_other_done = True
change_page = False
do = True
launch_text = True
launch_press_allow = True

processes_running = []

# rect, launch text, rocket img, rotation, launched?, animation_complete?, (i[0]+700, i[1]+18,39, 39)
alist = []
alist2 = []
alist_of_running = []
    # print('ALIST:\n\n')
    # print(alist)

frame_num = 0
frame_num2 = 0
frame_num3 = 0
frame_num4 = 0
frame_num5 = 0
frame_num6 = 0
frame_num7 = 0
frame_num8 = 0
frame_num9 = 0

base_pos = [50,100,900,200]

set_cursor_back3 = True
canceled = False

download_resources_enabled = True
download_cors_resources_enabled = True
same_origin_crawl_limit = 2
refetch_enabled = False

cors_enabled = False
resources_for_cors = False
Max_cors = 0

max_threads = 50

op = 0
t = 0
loader = ['Loading','Loading .','Loading ..','Loading ...']
text_load = 'Loading'
webviews_opened = {}

rects = {
    'd_resource_rect' : pygame.Rect(650, 195, 30, 30),
    'd_c_resource_rect' : pygame.Rect(650, 250, 30, 30),
    'cors_rect' : pygame.Rect(650, 410, 30, 30),
    'cors_resources' : pygame.Rect(435, 472, 25, 25),
    'left_max_cors' : pygame.Rect(565, 474, 30, 30),
    'right_max_cors' : pygame.Rect(630, 473, 30, 30),
    'left_socl': pygame.Rect(620, 300, 30, 30),
    'right_socl': pygame.Rect(685, 299, 30, 30),
    'left_mt': pygame.Rect(616, 350, 30, 30),
    'right_mt': pygame.Rect(689, 349, 30, 30),
    'go_on': pygame.Rect(723, 526, 60, 40)
}


rect_play_pause = pygame.Rect(530+125, 523, 50, 50)
cancel_color = (255, 255, 255)
rect_cancel = pygame.Rect(600+125, 523, 180, 50)
circle_rect = pygame.draw.circle(screen, (30, 28, 34), (795, 83), 28)
circle_rectl = pygame.draw.circle(screen, (30, 28, 34), (795+125+35, 83-35), 28)


with open(os.path.join(BASE,"data/file_types.json"),'r') as file_tp:
        a = json.load(file_tp)
os.environ['file_types'] = str(a['file_types_to_mime'])
    

loading_allow = False
checking = None

at_last = True
allow_options = True



websites_currently_in_process = 0



change_the_page = False

website_being_downloaded = None #rename to current website
completed_checking = False

loop = asyncio.new_event_loop()
currently_settings = {}
current_logs = []
websites = {} # currently_settings, current_logs, renderers


cached_log_renderers = []
some_other_thread = {}
completed = []
last_page = 1
clicked = []
downloads = font.render("Downloads", True, (0,0,0))
credits = font.render("Credits", True, (0,0,0))
some_text = font2.render("CRAWL & DOWNLOAD", True, (255, 191, 0))

success_paji = []
fail_paji = []

def recalculate():
    global websites_currently_in_process, alist, alist2
    roc = [753, 122, 39,39]
    man = [50,100,900,200]
    bb = 0
    for j in alist:
        # print(alist)
        # print(alist2)
        temp2 = alist2[bb][0][1]
        temp3 = alist[bb][0][1]
        temp4 = temp3 - temp2
        j[0][1] = man[1] + 250*(websites_currently_in_process) + temp4
        j[2][4][1] = roc[1] + 250*(websites_currently_in_process) + temp4
        bb += 1
    if alist == [] and websites_currently_in_process==0 and page_num==2:
        ggcam = font4.render("Nothing to show here !", True, (255, 255, 255))
        screen.blit(ggcam, (300, 300))

no_internet = False

def read_logs(hash):
    # print('atleast it started ! ')
    global websites_currently_in_process, website_being_downloaded, no_internet
    
    log = websites[hash][4].stdout.read1().decode('utf-8')
    log2 = log.split("$@")
    while ('0' not in log2 and '1' not in log2) and not websites[hash][5] and not websites[hash][7]:
        for i in log2:
            # print(i)
            if i.strip()!="":
                websites[hash][9] = True
                websites[hash][1].append(i)
                # print(i)
                ap = i.split("|")
                if ap[0].startswith("Download Success"):
                    some_thread_result[hash][1][ap[1]] = (None, False, True)

                t = i[:55]
                if len(t)!=len(i):
                    t+="..."
                if i.startswith("Downloading Webpage"):
                    obj = font.render(t,True, (255,255,255))
                elif i.startswith("Download Success") or i.startswith("Resource Download Success"):
                    obj = font.render(t,True, (0,255,0))
                elif i.startswith("Download Failed") or i.startswith("Resource Download Failed"):
                    obj = font.render(t, True, (255,0,0))
                elif i=="No Internet Connection !!":
                    obj = font.render(t, True, (255,0,0))
                    no_internet = True
                else:
                    obj = font.render(t, True,(255,255,255))
                if len(websites[hash][2])==0:
                    websites[hash][2].append([obj,[120, 450]])
                else:
                    websites[hash][2].append([obj, [120, websites[hash][2][-1][1][1]+30]])
                for i in websites[hash][2]:
                    i[1][1] -= 30
                
                
        log = websites[hash][4].stdout.read1().decode('utf-8')
        log2 = log.split("$@")
        if no_internet:
            log2.append("0")
        time.sleep(1)
    else:
        # print('got the issue ??')
        if not websites[hash][5] and not websites[hash][7]:
            # print('nope')
            for i in log2:
                # print(i)
                if i.strip()=="1":
                    # print('success')
                    websites[hash][3] = 1
                    websites[hash][0]['completed'] = True
                    completed.append(hash)
                    with open('data/details.json','r') as asta:
                        goen = json.load(asta)
                    websing = goen['Websites']
                    should_i_do_it = True
                    indexji = 0
                    for pk in websing:
                        if pk['hash']==hash:
                            websing[indexji] = websites[hash][0]
                            should_i_do_it = False
                            # print(f'reset bro with {websites[hash][0]}')
                            break
                        indexji += 1
                    if should_i_do_it:
                        websing.append(websites[hash][0])
                    goen['Websites'] = websing
                    with open('data/details.json','w') as pasta:
                        # print(f"written with {goen}")
                        json.dump(goen, pasta)
                       
                    obj1 = font.render("="*40, True, (255, 255, 255)) 
                    obj = font.render(f"SUCCESSFULLY DOWNLOADED - {hash}",True, (255,255,255))
                    obj2 = font.render("="*40, True, (255, 255, 255)) 
                    if len(websites[hash][2])==0:
                        websites[hash][2].append([obj1,[120, 450]])
                    else:
                        websites[hash][2].append([obj1, [120, websites[hash][2][-1][1][1]+30]])
                    websites[hash][2].append([obj, [120, websites[hash][2][-1][1][1]+30]])
                    websites[hash][2].append([obj2, [120, websites[hash][2][-1][1][1]+30]])
                    for i in websites[hash][2]:
                        i[1][1] -= 90
                    websites[hash][9] = True


                    website_being_downloaded = None
                    websites_currently_in_process -= 1
                    success_paji.append(hash)
                    
                    if os.path.isfile(f'temp/{hash}.json'):
                        try:
                            os.remove(f'temp/{hash}.json')
                        except:
                            pass
                    update_list()
                    if page_num == 2:
                        page_two()
                    elif page_num == 3:
                        page_three()
                    break
                elif i.strip()=="0":
                    websites[hash][3] = 0
                    completed.append(hash)
                    puppy = websites[hash][0]
                    if os.path.isdir(storage_location + str(hash)):
                        try:
                            shutil.rmtree(storage_location + str(hash))
                        except:
                            pass
                    with open('data/details.json','r') as mumbai:
                        ggboi = json.load(mumbai)
                    websitedata = ggboi['Websites']
                    for i in websitedata.copy():
                        if i['hash']==puppy['hash']:
                            websitedata.remove(i)
                    pp = {'Websites':websitedata}
                    with open('data/details.json','w') as goa:
                        json.dump(pp, goa)
                    # del websites[hash]
                    
                    obj1 = font.render("="*40, True, (255, 255, 255)) 
                    obj = font.render(f"FAILED DOWNLOADING - {hash}",True, (255,255,255))
                    obj2 = font.render("="*40, True, (255, 255, 255)) 
                    if len(websites[hash][2])==0:
                        websites[hash][2].append([obj1,[120, 450]])
                    else:
                        websites[hash][2].append([obj1, [120, websites[hash][2][-1][1][1]+30]])
                    websites[hash][2].append([obj, [120, websites[hash][2][-1][1][1]+30]])
                    websites[hash][2].append([obj2, [120, websites[hash][2][-1][1][1]+30]])
                    for i in websites[hash][2]:
                        i[1][1] -= 90
                    websites[hash][9] = True
                    
                    website_being_downloaded = None
                    websites_currently_in_process -= 1
                    fail_paji.append(hash)
                    
                    if os.path.isfile(f'temp/{hash}.json'):
                        try:
                            os.remove(f'temp/{hash}.json')
                        except:
                            pass
                    
                    update_list()
                    if page_num == 2:
                        page_two()
                    elif page_num == 3:
                        page_three()
                    break
                elif i.strip()!="":
                    websites[hash][9] = True
                    websites[hash][1].append(i)
                    # print(i)  
                    ap1 = i.split("|")
                    if ap1[0].startswith("Download Success"):
                        some_thread_result[hash][1][ap1[1]] = (None, False, True)
                    t = i[:55]
                    if len(t)!=len(i):
                        t+="..."
                    if i.startswith("Downloading Webpage"):
                        obj = font.render(t,True, (255,255,255))
                    elif i.startswith("Download Success") or i.startswith("Resource Download Success"):
                        obj = font.render(t,True, (0,255,0))
                    elif i.startswith("Download Failed") or i.startswith("Resource Download Failed"):
                        obj = font.render(t, True, (255,0,0))
                    elif i=="No Internet Connection !!":
                        obj = font.render(t, True, (255,0,0))
                        no_internet = True
                    else:
                        obj = font.render(t, True,(255,255,255))
                    if len(websites[hash][2])==0:
                        websites[hash][2].append([obj,[120, 450]])
                    else:
                        websites[hash][2].append([obj, [120, websites[hash][2][-1][1][1]+30]])
                    for i in websites[hash][2]:
                        i[1][1] -= 30
    # print('byeee')

info_rects = []
delete_rects = []
launch_rects = []
                
                
def update_list(main=False):
    global websites_currently_in_process, alist2, alist
    # print('updated')
    global alist
    with open('data/details.json' ,'r') as file:
        data = json.load(file)
    websites_temp = data['Websites']
    # print('Websites Temp:\n\n')
    # print(websites_temp)
    alist = []
    j = 0
    if main:
        for i in range(len(websites_temp)):
            if not websites_temp[i]['completed']:
                current = websites_temp[i]
                websites[current['hash']] = [current, [], [], 0, None, True, False, False, None, False]
                websites_currently_in_process += 1
    numji = 0  
    for i in range(len(websites_temp)):
        # print('num: ',numji)
        if websites_temp[i]['completed']:
            # print("added: ",numji)
            if j==0:
                alist.append([[50,100+(250*websites_currently_in_process),900,200], True, [rocket.copy(), 0, False, False, [753, 122+(250*websites_currently_in_process), 39,39]], True, [], True, [], websites_temp[i], True])
            else:
                # print(i)
                b = alist[j-1]
                alist.append([[b[0][0],b[0][1]+250,b[0][2],b[0][3]], True, [rocket.copy(),0,False,False,[753,b[2][4][1]+250,39,39]],True,[],True,[], websites_temp[i], True])
        j+=1
        numji += 1
    alist2 = alist.copy()
    # print(alist)
    if alist == [] and websites_currently_in_process==0 and page_num==2:
        ggcam = font4.render("Nothing to show here !", True, (255, 255, 255))
        screen.blit(ggcam, (300, 300))


update_list(True)


def run_process_man(url, download_res, download_cors_res, cors, cors_download_res, cors_download_cors_res, max_cors, same_origin_deviation, location, maintain_logs, show_failed_files, refetch, hash, max_threads, resources, webpages):
    script_path = os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), 'website.py')
    process_ji = subprocess.Popen(['python', script_path, url, download_res, download_cors_res, cors, cors_download_res, cors_download_cors_res, max_cors, same_origin_deviation, location, maintain_logs, show_failed_files, refetch, hash, max_threads, resources, webpages],stdout=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
    websites[eval(hash)][4] = process_ji
    websites[eval(hash)][8] = threading.Thread(target=read_logs,args=(eval(hash),),daemon=True)
    websites[eval(hash)][8].start()
    process_ji.wait()


def main_window():
    screen.fill((255, 255, 255))
    screen.blit(img, rect)
    
    screen.blit(main_logoji, (200, 0))
    
    pygame.draw.rect(screen, (30, 28, 34), [200, 233+119, 600, 200], border_radius=20)
    pygame.draw.rect(screen, (0, 0, 0), [200, 233+119, 600, 200], 8, border_radius=20)
    pygame.draw.rect(screen, (44, 42, 49), [220, 253+119, 560, 80], border_radius=20)
    pygame.draw.rect(screen, (0, 0, 0), [220, 253+119, 560, 80], 8, border_radius=20)
    
    
    pygame.draw.rect(screen, (0, 0, 0), [780, 49, 200, 25], border_radius=12)
    pygame.draw.rect(screen, (232, 232, 232), rectangle1 , border_radius=12)
    pygame.draw.rect(screen, (30, 28, 34), rectangle1, 3, border_radius=12)
    screen.blit(downloads, rectangle2)
    
    pygame.draw.rect(screen, (0, 0, 0), [30, 605, 160, 50], border_radius=12)
    pygame.draw.rect(screen, (232, 232, 232), rectangle3 , border_radius=12)
    pygame.draw.rect(screen, (30, 28, 34), rectangle3, 3, border_radius=12)
    screen.blit(credits, rectangle4)

    # pygame.draw.rect(screen, (0, 0, 0), [455, 340, 320, 80], 8, border_radius=20)
    if not pressed:
        screen.blit(btn_img, rect2)
    else:
        screen.blit(btn_img_clicked, rect3)
    screen.blit(some_text, rect4)
    screen.blit(spider_img, rect5)
    screen.blit(spider_hanging_img, rect6)

def download_button_update():
    screen.blit(img, (760, 0, 240, 100), (760, 0, 240, 100))
    pygame.draw.rect(screen, (0, 0, 0), [780, 49, 200, 25], border_radius=12)
    pygame.draw.rect(screen, (232, 232, 232), rectangle1 , border_radius=12)
    pygame.draw.rect(screen, (30, 28, 34), rectangle1, 3, border_radius=12)
    screen.blit(downloads, rectangle2)

def credits_button_update():
    screen.blit(img, (0, 600, 200, 67), (0, 600, 200, 67))
    pygame.draw.rect(screen, (0, 0, 0), [30, 605, 160, 50], border_radius=12)
    pygame.draw.rect(screen, (232, 232, 232), rectangle3 , border_radius=12)
    pygame.draw.rect(screen, (30, 28, 34), rectangle3, 3, border_radius=12)
    screen.blit(credits, rectangle4)
    
def crawlanddownload():
    if not pressed:
        screen.blit(btn_img, rect2)
    else:
        screen.blit(btn_img_clicked, rect3)
    screen.blit(some_text, rect4)
    


def page_two():
    screen.fill((255, 255, 255))
    screen.blit(img, rect)
    maggi = 0
    for jackychan in websites:
        if jackychan not in completed:
            temporary_location = [base_pos[0],base_pos[1]+(250*maggi),base_pos[2],base_pos[3]]
            pygame.draw.rect(screen, (26, 26, 26), temporary_location, border_radius=12) #Black box
            
            pygame.draw.rect(screen, (0, 0, 0), temporary_location, 8, border_radius=12) #Black box border
            screen.blit(logo3, (temporary_location[0]+840,temporary_location[1]+140,96,96)) # Spider logo on right
            
            a = font3.render(websites[jackychan][0]['url'],True,(255, 255, 255)) #NAME
            screen.blit(a, (temporary_location[0]+33, temporary_location[1]+26,temporary_location[2],temporary_location[3]))
            pygame.draw.line(screen, (0,0,0), (temporary_location[0]+30, temporary_location[1]+70), (temporary_location[0]+temporary_location[2]-30, temporary_location[1]+70),6) #LINE SEPARATION
            b = font.render("#"+str(websites[jackychan][0]['hash']),True,(255, 255, 255)) #URL
            screen.blit(b, (temporary_location[0]+33, temporary_location[1]+85,temporary_location[2],temporary_location[3]))
            pygame.draw.rect(screen, (255, 215, 0), (temporary_location[0]+30,temporary_location[1]+135, 180, 50), border_radius=12)
            pygame.draw.rect(screen, (0,0,0), (temporary_location[0]+30,temporary_location[1]+135, 180, 50),4, border_radius=12)
            c = font3.render("!   INFO", True, (0,0,0))
            screen.blit(c, (temporary_location[0]+75,temporary_location[1]+142, 200, 50))
            
            
            pygame.draw.rect(screen, (0, 0, 255), (temporary_location[0]+220,temporary_location[1]+135, 50, 50), border_radius=12)
            pygame.draw.rect(screen, (0,0,0), (temporary_location[0]+220,temporary_location[1]+135, 50, 50),4, border_radius=12)
            screen.blit(eye, [temporary_location[0]+220+7, temporary_location[1]+135+8])
            
            pygame.draw.rect(screen, (255, 215, 0), (temporary_location[0]+620, temporary_location[1]+14, 50, 50), border_radius=12)
            pygame.draw.rect(screen, (0,0,0), (temporary_location[0]+620, temporary_location[1]+14, 50, 50),4, border_radius=12)
            if websites[jackychan][5]:
                screen.blit(play, (temporary_location[0]+628, temporary_location[1]+14+7))
            else:
                screen.blit(pause, (temporary_location[0]+628, temporary_location[1]+14+7))
            
            pygame.draw.rect(screen, (210, 4, 45), (temporary_location[0]+685,temporary_location[1]+14, 180, 50), border_radius=12)
            pygame.draw.rect(screen, (0,0,0), (temporary_location[0]+685,temporary_location[1]+14, 180, 50),4, border_radius=12)
            b = font3.render("Cancel",True,cancel_color) #NAME
            screen.blit(b, (temporary_location[0]+685+38,temporary_location[1]+14+7, 180, 50))
            maggi += 1
            
    # print("\n\n\n\n\n")
    # print(alist)
    for j in alist:
        i = j[0]
        # print(i)
        rocketloc = j[2][4]
        #BUTTONS
        # temprect_launch.add(pygame.Rect(i[0]+685,i[1]+14, 180, 45))
        if j[8]:
            pygame.draw.rect(screen, (211, 214, 219), (i[0]+685,i[1]+14, 180, 50), border_radius=12)
            pygame.draw.rect(screen, (0,0,0), (i[0]+685,i[1]+14, 180, 50),4, border_radius=12)
            if j[1]:
                c = font3.render("Launch", True, (0,0,0))
                screen.blit(c, (i[0]+750,i[1]+21, 200, 50))
            screen.blit(j[2][0], rocketloc)
        else:
            pygame.draw.rect(screen, (210, 4, 45), (i[0]+685,i[1]+14, 180, 50), border_radius=12)
            pygame.draw.rect(screen, (0,0,0), (i[0]+685,i[1]+14, 180, 50),4, border_radius=12)
            if not j[1]:
                cj = font3.render("Stop", True, (0,0,0))
                screen.blit(cj, (i[0]+770,i[1]+21,200,50))
                pygame.draw.rect(screen, (0,0,0), (i[0]+720,i[1]+25,30,30),4,border_radius=7)
        
        
        # Main box
        pygame.draw.rect(screen, (26, 26, 26), (i[0], i[1], 685, i[3]), border_radius=12) #Black box
        pygame.draw.rect(screen, (26, 26, 26), (i[0]+685, i[1]+64, i[2]-685, i[3]-64), border_radius=12) #Black box
        pygame.draw.rect(screen, (26, 26, 26), (i[0]+685, i[1], i[2]-685, 14), border_radius=12) #Black box
        pygame.draw.rect(screen, (26, 26, 26), (i[0]+685+180, i[1]+14, i[2]-685-180, 50), border_radius=12) #Black box
        
        
        
        pygame.draw.rect(screen, (0, 0, 0), i, 8, border_radius=12) #Black box border
        screen.blit(logo3, (i[0]+840,i[1]+140,96,96)) # Spider logo on right
        
        # DATA
        a = font3.render(str(j[7]['hash']),True,(255, 255, 255)) #NAME
        screen.blit(a, (i[0]+33, i[1]+26,i[2],i[3]))
        
        pygame.draw.line(screen, (0,0,0), (i[0]+30, i[1]+70), (i[0]+i[2]-30, i[1]+70),6) #LINE SEPARATION
        
        b = font.render(j[7]['url'],True,(255, 255, 255)) #URL
        screen.blit(b, (i[0]+33, i[1]+85,i[2],i[3]))
        
        pygame.draw.rect(screen, (255, 215, 0), (i[0]+30,i[1]+135, 180, 50), border_radius=12)
        pygame.draw.rect(screen, (0,0,0), (i[0]+30,i[1]+135, 180, 50),4, border_radius=12)
        if j[3]:
            c = font3.render("!   INFO", True, (0,0,0))
            screen.blit(c, (i[0]+75,i[1]+142, 200, 50))
        # screen.blit(exclamation, (i[0]+60,i[1]+143, 200, 50))
        
        if j[8]:
            pygame.draw.rect(screen, (255, 47, 47), (i[0]+230,i[1]+135, 180, 50), border_radius=12)
            pygame.draw.rect(screen, (0,0,0), (i[0]+230,i[1]+135, 180, 50),4, border_radius=12)
            if j[5]:
                c = font3.render("DELETE", True, (0,0,0))
                screen.blit(c, (i[0]+290,i[1]+142, 200, 50))
            screen.blit(delete, (i[0]+250,i[1]+141, 200, 50))
            
    pygame.draw.rect(screen, (232, 232, 232), rectji , border_radius=12)
    back = font.render("Go Back", True, (0,0,0))
    if do:
        screen.blit(back, (85, 20, 200, 50))
    pygame.draw.rect(screen, (157,0,255), rectji2 , border_radius=12)
    screen.blit(aleft, rectji3)




def page_four():
    global download_resources_enabled, download_cors_resources_enabled, allow_options, same_origin_crawl_limit, refetch_enabled, cors_enabled, Max_cors, resources_for_cors, max_threads
    screen.fill((255, 255, 255))
    screen.blit(img, rect)
    pygame.draw.rect(screen, (47, 21, 68), [200, 83, 600, 500], border_radius=20)
    screen.blit(simg, (200, 83), (100, 60, 600, 73))
    pygame.draw.rect(screen, (0, 0, 0), [200, 83, 600, 500], 8, border_radius=20)
    
    
    circle_rect = pygame.draw.circle(screen, (30, 28, 34), (795, 83), 28)
    pygame.draw.circle(screen, (0, 0, 0), (795, 83), 28, 5)
    screen.blit(cancel, (780, 68))
    
    # screen.blit(settings, (368, 80))
    settings_text = font4.render("SETTINGS", True, (255, 255, 255))
    screen.blit(settings_text, (410, 101))
    
    
    pygame.draw.line(screen, (0,0,0), (220, 155), (780, 155),6)
    pygame.draw.line(screen, (171, 84, 139), (220, 158), (780, 158),3)
    
    
    pygame.draw.rect(screen, (47, 21, 68), [250, 173, 500, 350], border_radius=20)
    pygame.draw.rect(screen, (48, 25, 52), [250, 395, 498, 58])
    pygame.draw.rect(screen, (0, 0, 0), [250, 173, 500, 350], 8, border_radius=20)
    
    resources = font5.render("Download Resources", True, (255,255,255))
    screen.blit(resources, (270, 200))
    if allow_options:
        pygame.draw.rect(screen, (0, 0, 0), rects['d_resource_rect'], 4)
    elif not download_resources_enabled:
        screen.blit(cancel, (650, 195))
    if download_resources_enabled:
        screen.blit(tick, (650, 186))
    resources = font5.render("Download CORS Resources", True, (255,255,255))
    screen.blit(resources, (270, 250))
    if allow_options:
        pygame.draw.rect(screen, (0, 0, 0), rects['d_c_resource_rect'], 4)
    elif not download_cors_resources_enabled:
        screen.blit(cancel, (650, 250))
    if download_cors_resources_enabled:
        screen.blit(tick, (650, 241))
    resources = font5.render("Same Origin Crawl Limit", True, (255,255,255))
    screen.blit(resources, (270, 300))
    if allow_options:
        screen.blit(left, rects['left_socl'])
    num = font5.render(str(same_origin_crawl_limit), True , (255, 255, 255))
    screen.blit(num, (657, 297))
    if allow_options:
        screen.blit(right, rects['right_socl'])
    # pygame.draw.rect(screen, (0, 0, 0), [650, 295, 30, 30], 4)
    resources = font5.render("Max Threads", True, (255,255,255))
    screen.blit(resources, (270, 347))
    special_info = font8.render("Change based on your PC's capabilities - Risky dude !", True, (255,255,255))
    screen.blit(special_info, (270,380))
    if allow_options:
        screen.blit(left, rects['left_mt'])
    num = font5.render(str(max_threads), True , (255, 255, 255))
    if len(str(max_threads))==3:
        screen.blit(num, (647, 347))
    elif len(str(max_threads))==2:
        screen.blit(num, (651, 347))
    else:
        screen.blit(num, (655, 347))
    if allow_options:
        screen.blit(right, rects['right_mt'])
    # if allow_options:
    #     pygame.draw.rect(screen, (0, 0, 0), rects['refetch_rect'], 4)
    # elif not refetch_enabled:
    #     screen.blit(cancel, (650, 350))
    # if refetch_enabled:
    #     screen.blit(tick, (650, 341))
    
    
    pygame.draw.line(screen, (0,0,0), (250, 395), (748, 395),4)
    resources = font5.render("Cross-Origin Sites", True, (255,255,255))
    screen.blit(resources, (270, 410))
    if allow_options:
        pygame.draw.rect(screen, (0, 0, 0), rects['cors_rect'], 4)
    elif not cors_enabled:
        screen.blit(cancel, (650, 410))
    if cors_enabled:
        screen.blit(tick, (650, 401))
    pygame.draw.line(screen, (0,0,0),(250, 453), (748, 453), 4)
    
    
    resources = font6.render("Resources", True, (255, 255, 255))
    aboi = pygame.Surface((25, 25))
    aboi.fill((47, 21, 68))
    resources2 = font6.render("Max Cors", True, (255, 255, 255))
    if allow_options:
        pygame.draw.rect(aboi, (0, 0, 0), [0, 0, 25, 25], 4)
        
    num = font5.render(str(Max_cors), True , (192, 192, 192))
        
    if cors_enabled:
        if allow_options:
            screen.blit(left, rects['left_max_cors'])
            screen.blit(right, rects['right_max_cors'])
    else:
        if allow_options:
            num.set_alpha(50)
            aboi.set_alpha(130)
            resources.set_alpha(50)
            resources2.set_alpha(50)
        if allow_options:
            screen.blit(left2, (565, 474, 30, 30))
            screen.blit(right2, (630, 473, 30, 30))
        
    screen.blit(num, (602, 471))
    screen.blit(resources, (335, 474))
    screen.blit(resources2, (485, 474))
    screen.blit(aboi, (435, 472))
    
    if not allow_options and not resources_for_cors:
        screen.blit(cancel, (435, 472))
    
    if allow_options:
        pygame.draw.rect(screen, (48, 25, 52), rects['go_on'], border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), rects['go_on'], 6, border_radius=10)
        screen.blit(aright, (rects['go_on'].x + 12, rects['go_on'].y + 6))
    
    if resources_for_cors and cors_enabled:
        screen.blit(tick2, (435, 463))

cached_name_for_website = None
cached_name_for_website2 = None
def page_three():
    global website_being_downloaded, cached_name_for_website, cached_name_for_website2, circle_rectl, screen, cancel, websites
    screen.fill((255, 255, 255))
    screen.blit(img, rect)
    pygame.draw.rect(screen, (234, 111, 0), [75, -22, 850, 685], border_radius=20)
    pygame.draw.rect(screen, (44, 42, 49), [220-125, -22, 560+250, 280+70+25+150], border_radius=20)
    pygame.draw.rect(screen, (0, 0, 0), [220-125, -22, 560+250, 280+70+25+150], 4, border_radius=20)
    pygame.draw.rect(screen, (0, 0, 0), [75, -22, 850, 685], 8, border_radius=20)
    if website_being_downloaded:
        a = font3.render(str(websites[website_being_downloaded][0]['url']),True,(255, 255, 255)) #NAME
        screen.blit(a, [100, 533])
        cached_name_for_website = str(websites[website_being_downloaded][0]['url'])
        
        a = font3.render('#'+str(websites[website_being_downloaded][0]['hash']),True,(255, 255, 255)) #NAME
        screen.blit(a, [100, 573])
        cached_name_for_website2 = str(websites[website_being_downloaded][0]['hash'])
    else:
        a = font3.render(cached_name_for_website,True,(255, 255, 255)) #NAME
        screen.blit(a, [100, 533])
        a = font3.render('#'+str(cached_name_for_website2),True,(255, 255, 255)) #NAME
        screen.blit(a, [100, 573])
    circle_rectl = pygame.draw.circle(screen, (30, 28, 34), (795+125+35, 83-35), 28)
    pygame.draw.circle(screen, (0, 0, 0), (795+125+35, 83-35), 28, 5)
    screen.blit(cancel, (780+125+35, 33))
    
    if website_being_downloaded:
        pygame.draw.rect(screen, (255, 215, 0), rect_play_pause, border_radius=12)
        pygame.draw.rect(screen, (0,0,0), rect_play_pause,4, border_radius=12)
        if websites[website_being_downloaded][5]:
            screen.blit(play, [537+125, 530])
        else:
            screen.blit(pause, [537+125, 530])
        pygame.draw.rect(screen, (210, 4, 45), rect_cancel, border_radius=12)
        pygame.draw.rect(screen, (0,0,0), rect_cancel,4, border_radius=12)
        b = font3.render("Cancel",True,cancel_color) #NAME
        screen.blit(b, [638+125, 530, 180, 50])
        
def page_six():
    screen.fill((255, 255, 255))
    screen.blit(img, rect)
    pygame.draw.rect(screen, (31, 42, 54), (100, 100, 800, 270),border_radius=20)
    pygame.draw.rect(screen, (0,0,0), (100, 100, 800, 270),5,border_radius=20)
    
    bbj = font7.render("Yogya Chugh", True, (255, 255, 255))
    screen.blit(bbj, (450, 150))
    screen.blit(gmail,(450,210))
    ddj = font6.render("yogya.developer@gmail.com",True, (255,255,255))
    screen.blit(ddj, (500,213))
    
    pygame.draw.rect(screen, (0,0,0),(450, 260, 150,50),border_radius=20)
    pygame.draw.rect(screen, (0,0,0),(450, 260, 150,50),4,border_radius=20)
    pygame.draw.rect(screen, (44, 42, 49), (471, 260, 45, 45),border_radius=10)
    screen.blit(github, (471,260))
    agi = font6.render("Github",True,(255,255,255))
    screen.blit(agi, (515,273))
    
    
    pygame.draw.rect(screen, (255,250,250),(610, 260, 150,50),border_radius=20)
    pygame.draw.rect(screen, (0,0,0),(610, 260, 150,50),4,border_radius=20)
    screen.blit(slack, (630, 262))
    
    hey = font3.render('Resource Attributions', True, (255,255,255))
    screen.blit(hey, (120,400))
    pygame.draw.line(screen, (255,255,255),(120,440),(420,440),4)
    hey2 = font6.render('Due to a lot of resources being used, credits/attributions can be found by clicking on the button below !', True, (255,255,255))
    screen.blit(hey2, (120,460))
    
    pygame.draw.rect(screen, (255, 215, 0), (120, 500, 180, 50), border_radius=12)
    pygame.draw.rect(screen, (0,0,0), (120, 500, 180, 50),4, border_radius=12)
    c = font3.render("Credits", True, (0,0,0))
    screen.blit(c, (160,509))

def update_the_play_pause():
    pygame.draw.rect(screen, (255, 215, 0), rect_play_pause, border_radius=12)
    pygame.draw.rect(screen, (0,0,0), rect_play_pause,4, border_radius=12)
    if websites[website_being_downloaded][5]:
        screen.blit(play, [537+125, 533])
    else:
        screen.blit(pause, [537+125, 533])

def remove_the_buttons():
    pygame.draw.rect(screen, (234, 111, 0), rect_play_pause, border_radius=12)
    pygame.draw.rect(screen, (234, 111, 0), rect_cancel, border_radius=12)


def check_if_website_correct():
    valid = None
    global display_err, display_err_msg, pressed, loading_allow, page_num
    # print('Reached')
    try:
        valid = webpage.download_resource_safe(textinput.value)
    except Exception as e:
        try:
            if not textinput.value.startswith("http"):
                valid = webpage.download_resource_safe("https://" + textinput.value)
        except Exception as p:
            try:
                valid2 = webpage.download_resource_safe("https://www.example.com")
                display_err = True
                display_err_msg = "Invalid URL !"
                # print('invalid url')
            except Exception as g:
                # print('no internet')
                display_err = True
                display_err_msg = "No Internet Connection !"
                
    pressed = False
    # print('Completed')
    loading_allow = False
    completed_checking = True
    if valid!=None:
        page_num = 4
        page_four()


def tip():
    screen.fill((255, 255, 255))
    screenshot.set_alpha(180)
    screen.blit(screenshot, rect)
    pygame.draw.rect(screen, (47, 21, 68), [200, 183, 600, 300], border_radius=20)
    screen.blit(simg, (200, 183), (100, 60, 600, 73))
    pygame.draw.rect(screen, (0, 0, 0), [200, 183, 600, 300], 8, border_radius=20)
    
    pygame.draw.line(screen, (0,0,0), (220, 255), (780, 255),6)
    pygame.draw.line(screen, (171, 84, 139), (220, 258), (780, 258),3)

    bro = font2.render("Tip Of The Day",True,(255,255,255))
    screen.blit(bro, (240, 215))

    advice = font6.render('Download as many websites as you want but remember !',True,(255,255,255))
    advice2 = font6.render('Some websites have dependencies which would require',True,(255,255,255))
    advice3 = font6.render('you to set Same Origin Crawl Limit to atleast 3 in',True,(255,255,255))
    advice4 = font6.render('the settings as well as Turn on CORS',True,(255,255,255))
    advice5 = font6.render('resources download.',True,(255,255,255))
    advice6 = font6.render('NOTE:',True,(255,255,255))
    advice7 = font6.render('Default Settings are perfect for',True,(255,255,255))
    advice8 = font6.render('"summer.hackclub.com"',True,(255,255,255))
    screen.blit(advice, (240, 270))
    screen.blit(advice2, (240, 295))
    screen.blit(advice3, (240, 320))
    screen.blit(advice4, (240, 345))
    screen.blit(advice5, (240, 370))
    screen.blit(advice6, (240, 395))
    screen.blit(advice7, (240, 420))
    screen.blit(advice8, (240, 445))
    pygame.draw.line(screen, (0,0,0),(240,416),(284,416),4)

if not os.path.exists('webber.log'):
    with open('webber.log','w') as f:
        f.write('Initialized Application !')
    page_num=7
    tip()
else:
    page_num=1
    main_window()


while True:
    # print("CPU:", psutil.cpu_percent())
    # print("Threads:", threading.active_count())
    events = pygame.event.get()
    pos = pygame.mouse.get_pos()
    
    if page_num == 1:
        last_page = 1
        textinput.update(events)
        
        pygame.draw.rect(screen, (44, 42, 49), [220+8, 253+119+8, 560-16, 80-16], border_radius=20)
        
        screen.blit(textinput.surface, (250,400))
        
        # Check for URL Correct !
        if completed_checking:
            if isinstance(checking, website.StoppableThread):
                checking.join()
                checking = None
                completed_checking = False
        
        # Error Message if present !
        if display_err and display_err_msg:
            pygame.draw.rect(screen, (30, 28, 34), [390, 455, 70, 70])
            ay = font6.render(display_err_msg, True, (255,0,0))
            screen.blit(ay, (230, 493))
         
         # Cute cat loading animation   
        if loading_allow:
            pygame.draw.rect(screen, (30, 28, 34), [390, 455, 70, 70])
            screen.blit(frames2[frame_num2], (390, 455))
            frame_num2 = (frame_num2 + 1) % len(frames2)
        
        
        # Hovers
        if rect2.collidepoint(pos):
            pygame.mouse.set_cursor(nw_mouse2)
        elif gg_rect.collidepoint(pos):
            pygame.mouse.set_cursor(nw_mouse3)
        elif rectangle1.collidepoint(pos):
            pygame.mouse.set_cursor(nw_mouse2)
            if something_done:
                something_done = False
                rectangle1.y -= 3
                rectangle2.y -= 3
                download_button_update()
        elif rectangle3.collidepoint(pos):
            pygame.mouse.set_cursor(nw_mouse2)
            if something_other_done:
                something_other_done = False
                rectangle3.y -= 3
                rectangle4.y -= 3
                credits_button_update()
        else:
            if not something_done:
                something_done = True
                rectangle1.y += 3
                rectangle2.y += 3
                download_button_update()
            if not something_other_done:
                something_other_done = True
                rectangle3.y += 3
                rectangle4.y += 3
                credits_button_update()
            pygame.mouse.set_cursor(nw_mouse)
            
        # Click for downloads page !
        if change_page:
            change_page = False
            # rectangle1.y -= 5
            # rectangle2.y -= 5
            pygame.mouse.set_cursor(nw_mouse)
            pygame.display.update()
            time.sleep(0.25)
            update_list()
            base_pos = [50,100,900,200]
            page_num = 2
            page_two()
        
        
        # Clicks
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:    
                if rect2.collidepoint(event.pos) and not pressed:
                    pressed = True
                    rect4.y += 1
                    counterman = 0
                    crawlanddownload()
                    for pasta in websites:
                        if not websites[pasta][5] and not websites[pasta][7]:
                            counterman += 1
                    # print("Websites Running: ",counterman)
                    if counterman>=1:
                        display_err = True
                        display_err_msg = "Max 1 at a time !"
                        loading_allow = False
                    else:
                        loading_allow = True
                        display_err = False
                        display_err_msg = ""
                        pygame.time.set_timer(STARTED, 10, loops=1)
                if rectangle1.collidepoint(event.pos):
                    pressed_downloads = True
                    rectangle1.y += 5
                    rectangle2.y += 5
                    download_button_update()
                    pygame.time.set_timer(DOWNLOADS_PRESSED, 200, loops=1)
                if rectangle3.collidepoint(event.pos):
                    pressed_credits = True
                    rectangle3.y += 5
                    rectangle4.y += 5
                    credits_button_update()
                    pygame.time.set_timer(CREDITS_PRESSED, 200, loops=1)
                    
            if event.type == STARTED and pressed:
                display_err = False
                rect4.y -= 1
                valid = None
                pressed = False
                crawlanddownload()
                counterman = 0
                for pasta in websites:
                    if not websites[pasta][5] and not websites[pasta][7]:
                        counterman += 1
                if counterman<1:
                    allow_options = True
                    download_resources_enabled = True
                    download_cors_resources_enabled = True
                    same_origin_crawl_limit = 2
                    refetch_enabled = False

                    cors_enabled = False
                    resources_for_cors = False
                    Max_cors = 0
                    max_threads = 50
                    checking = website.StoppableThread(target=check_if_website_correct)
                    checking.start()
                pygame.mouse.set_cursor(nw_mouse)
            if event.type == DOWNLOADS_PRESSED and pressed_downloads:
                rectangle1.y -= 5
                rectangle2.y -= 5
                pressed_downloads = False
                change_page = True
                download_button_update()
            if event.type == CREDITS_PRESSED and pressed_credits:
                rectangle3.y -=5
                rectangle4.y -=5
                pressed_credits = False
                credits_button_update()
                page_num = 6
                page_six()
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pressed = True
                rect4.y += 1
                loading_allow = True
                display_err = False
                display_err_msg = ""
                # print("Websites Running: ",counterman)
                if websites_currently_in_process>=1:
                    display_err = True
                    display_err_msg = "Max 1 at a time !"
                    loading_allow = False
                else:
                    loading_allow = True
                    display_err = False
                    display_err_msg = ""
                    pygame.time.set_timer(STARTED, 10, loops=1)
        
            

    elif page_num == 2:
        last_page = 2
        set_cursor_back = True
        set_cursor_back2 = True
        paji_maggi = 0
        
        for jackychan in websites:
            if jackychan not in completed:
                temporary_location = [base_pos[0],base_pos[1]+(250*paji_maggi),base_pos[2],base_pos[3]]
                if (pos[0]>temporary_location[0]+30 and pos[0]<temporary_location[0]+30+180 and pos[1]>temporary_location[1]+135 and pos[1]<temporary_location[1]+185) or (pos[0]>temporary_location[0]+685 and pos[0]<temporary_location[0]+685+180 and pos[1]>temporary_location[1]+14 and pos[1]<temporary_location[1]+14+50) or (pos[0]>temporary_location[0]+220 and pos[0]<temporary_location[0]+220+50 and pos[1]>temporary_location[1]+135 and pos[1]<temporary_location[1]+135+50) or (pos[0]>temporary_location[0]+620 and pos[0]<temporary_location[0]+620+50 and pos[1]>temporary_location[1]+14 and pos[1]<temporary_location[1]+14+50):
                    set_cursor_back = False
                    pygame.mouse.set_cursor(nw_mouse2)
                paji_maggi += 1

        for j in alist:
            i = j[0]
            rocketloc = j[2][4]
            # Check for launch
            change = False
            if pos[0]>i[0]+685 and pos[0]<i[0]+865 and pos[1]>i[1]+14 and pos[1]<i[1]+64:
                set_cursor_back = False
                if j[8]:
                    if launch_press_allow:
                        change = True
                    else:
                        change = False
                        if not j[2][2]:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)
                else:
                    pygame.mouse.set_cursor(nw_mouse2)
            else:
                change = False

            # Check for Delete & Info
            if ((pos[0]>i[0]+230 and pos[0]<i[0]+410 and pos[1]>i[1]+135 and pos[1]<i[1]+185) and j[8]) or (pos[0]>i[0]+30 and pos[0]<i[0]+210 and pos[1]>i[1]+135 and pos[1]<i[1]+185):
                set_cursor_back = False
                pygame.mouse.set_cursor(nw_mouse2)
            if j[8]:
                if change:
                    if j[2][1]==0:
                        pygame.mouse.set_cursor(nw_mouse2)
                        j[2][1] = 360
                    elif j[2][1]!=270:
                        j[2][1] -= 15
                    j[1] = False
                    if j[2][1]!=0:
                        j[2][0] = pygame.transform.rotate(rocket, j[2][1])
                    pygame.draw.rect(screen, (211, 214, 219), (i[0]+685,i[1]+14, 180, 50), border_radius=12)
                    pygame.draw.rect(screen, (0,0,0), (i[0]+685,i[1]+14, 180, 50),4, border_radius=12)
                    if j[1]:
                        c = font3.render("Launch", True, (0,0,0))
                        screen.blit(c, (i[0]+750,i[1]+21, 200, 50))
                    screen.blit(j[2][0], rocketloc)
                else:
                    if j[2][1]!=0 and not j[2][2]:
                        if j[2][1]!=360:
                            j[2][1]+= 15
                        else:
                            j[2][1]=0
                            set_cursor_back = True
                        j[1] = True
                        j[2][0] = pygame.transform.rotate(rocket, j[2][1])
                        pygame.draw.rect(screen, (211, 214, 219), (i[0]+685,i[1]+14, 180, 50), border_radius=12)
                        pygame.draw.rect(screen, (0,0,0), (i[0]+685,i[1]+14, 180, 50),4, border_radius=12)
                        if j[1]:
                            c = font3.render("Launch", True, (0,0,0))
                            screen.blit(c, (i[0]+750,i[1]+21, 200, 50))
                        screen.blit(j[2][0], rocketloc)
            if j[2][2] and not j[2][3]:
                j[2][1] = 270
                j[2][0] = pygame.transform.rotate(rocket, j[2][1])
                rocketloc[0] += 20
                if rocketloc[0]>i[0]+180+665:
                    j[2][3] = True
                    pygame.draw.rect(screen, (210, 4, 45), (i[0]+685,i[1]+14, 180, 50), border_radius=12)
                    pygame.draw.rect(screen, (0,0,0), (i[0]+685,i[1]+14, 180, 50),4, border_radius=12)
                    if not j[1]:
                        cj = font3.render("Stop", True, (0,0,0))
                        screen.blit(cj, (i[0]+770,i[1]+21,200,50))
                        pygame.draw.rect(screen, (0,0,0), (i[0]+720,i[1]+25,30,30),4,border_radius=7)
                else:
                    pygame.draw.rect(screen, (211, 214, 219), (i[0]+685,i[1]+14, 180, 50), border_radius=12)
                    pygame.draw.rect(screen, (0,0,0), (i[0]+685,i[1]+14, 180, 50),4, border_radius=12)
                    if j[1]:
                        c = font3.render("Launch", True, (0,0,0))
                        screen.blit(c, (i[0]+750,i[1]+21, 200, 50))
                    screen.blit(j[2][0], rocketloc)
                    pygame.draw.rect(screen, (26, 26, 26), (i[0]+685+180, i[1]+14, i[2]-685-180-20, 50), border_radius=12)
        
        draw_back_button = False

        if rectji.collidepoint(pos):
            pygame.mouse.set_cursor(nw_mouse2)
            set_cursor_back2 = False
            do = False
            if rectji2.w<=180:
                rectji2.w += 10
                draw_back_button = True
            if rectji3.x<=80:
                rectji3.x += 10
                draw_back_button = True
        else:
            set_cursor_back2 = True
            do = True
            if rectji2.w>=50:
                rectji2.w -= 10
                draw_back_button = True
            if rectji3.x>=30:
                rectji3.x -= 10
                draw_back_button = True
        
        if draw_back_button:
            pygame.draw.rect(screen, (232, 232, 232), rectji , border_radius=12)
            back = font.render("Go Back", True, (0,0,0))
            if do:
                screen.blit(back, (85, 20, 200, 50))
            pygame.draw.rect(screen, (157,0,255), rectji2 , border_radius=12)
            screen.blit(aleft, rectji3)  
        
                
        if set_cursor_back and set_cursor_back2:
            pygame.mouse.set_cursor(nw_mouse)
            
        if alist == [] and websites_currently_in_process==0 and page_num==2:
            ggcam = font4.render("Nothing to show here !", True, (255, 255, 255))
            screen.blit(ggcam, (300, 300))
            
            
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                nope = False
                for giraffe in events:
                    if giraffe.type == pygame.MOUSEWHEEL:
                        nope = True
                        break
                if nope:
                    continue
                if rectji.collidepoint(event.pos):
                    time.sleep(0.25)
                    page_num = 1
                    main_window()
                    break
                if page_num == 2:
                    # print(alist)
                    for j in alist:
                        i = j[0]
                        if event.pos[0]>i[0]+685 and event.pos[0]<i[0]+865 and event.pos[1]>i[1]+14 and event.pos[1]<i[1]+64:
                            if j[8]:
                                j[8] = False
                                j[2][2] = True
                                dothat = True
                                for d in total_lists:
                                    if d==j[-2]['hash'] and total_lists[d]!=None:
                                        dothat = False
                                        break
                                if dothat:
                                    script_path = os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), 'webview_launch.py')
                                    process = subprocess.Popen(['python', script_path,"../" + j[-2]['file_location'],f'Webber - {j[-2]['hash']}'],creationflags=subprocess.CREATE_NO_WINDOW)
                                    total_lists[j[-2]['hash']] = ([j[-2]['file_location'],process])
                                    clicked.append(j[-2]['hash'])
                                    pygame.draw.rect(screen, (211, 214, 219), (i[0]+685,i[1]+14, 180, 50), border_radius=12)
                                    pygame.draw.rect(screen, (0,0,0), (i[0]+685,i[1]+14, 180, 50),4, border_radius=12)
                                    if j[1]:
                                        c = font3.render("Launch", True, (0,0,0))
                                        screen.blit(c, (i[0]+750,i[1]+21, 200, 50))
                                    screen.blit(j[2][0], j[2][4])
                                else:
                                    pass
                                    # print('totail')
                                    # print(total_lists)
                                page_two()
                            else:
                                apboi = total_lists.get(j[-2]['hash'])
                                if apboi:
                                    try:
                                        psutil.Process(apboi[1].pid).terminate()
                                    except:
                                        pass
                                    j[0][0] = 50
                                    j[0][2] = 900
                                    j[0][3] = 200
                                    j[1] = True
                                    j[2][0] = rocket.copy()
                                    j[2][1] = 0
                                    j[2][2] = False
                                    j[2][3] = False
                                    j[2][4][0] = 753
                                    j[2][4][2] = 39
                                    j[2][4][3] = 39
                                    j[3] = True
                                    j[4] = []
                                    j[5] = True
                                    j[6] = []
                                    j[8] = True
                                    del total_lists[j[-2]['hash']]
                                    # print("deleted !")
                                    # print(total_lists)
                                    clicked.remove(j[-2]['hash'])
                                    apboi = None
                                    page_two()
                            break
                        if (event.pos[0]>i[0]+30 and event.pos[0]<i[0]+210 and event.pos[1]>i[1]+135 and event.pos[1]<i[1]+185):
                            # print('info clickedd')
                            allow_options = False
                            download_resources_enabled = j[-2]['download_res']
                            download_cors_resources_enabled = j[-2]['download_cors_res']
                            cors_enabled = j[-2]['cors']
                            Max_cors = j[-2]['max_cors']
                            max_threads = j[-2]['max_threads']
                            resources_for_cors = j[-2]['cors_download_res']
                            same_origin_crawl_limit = j[-2]['same_origin_deviation']
                            page_num = 4
                            page_four()
                            break
                        
                        if (j[8] and event.pos[0]>i[0]+230 and event.pos[0]<i[0]+410 and event.pos[1]>i[1]+135 and event.pos[1]<i[1]+185):
                            puppy = j[7]
                            if os.path.isdir(storage_location+str(puppy['hash'])):
                                try:
                                    shutil.rmtree(storage_location+str(puppy['hash']))
                                except Exception as e:
                                    # print(e)
                                    # print("location: ", storage_location+str(puppy['hash']))
                                    pass
                            with open('data/details.json','r') as mumbai:
                                ggboi = json.load(mumbai)
                            websitedata = ggboi['Websites']
                            for i in websitedata.copy():
                                if i['hash']==puppy['hash']:
                                    websitedata.remove(i)
                            pp = {'Websites':websitedata}
                            with open('data/details.json','w') as goa:
                                json.dump(pp, goa)
                            update_list()
                            page_two()
                            page_num = 5
                            change_the_page = True
                            completed.append(j[7]['hash'])
                            pygame.time.set_timer(DELETE_IT,2000, loops=1)
                    dosa_num = 0
                    for dosa in websites:
                        if dosa not in completed:
                            dosa_location = [base_pos[0],base_pos[1]+(250*dosa_num),base_pos[2],base_pos[3]]
                            play_pause_loc = [dosa_location[0]+620, dosa_location[1]+14, 50, 50]
                            info_loc = [dosa_location[0]+30,dosa_location[1]+135, 180, 50]
                            if (event.pos[0]>info_loc[0] and event.pos[0]<info_loc[0]+180 and event.pos[1]>info_loc[1] and event.pos[1]<info_loc[1]+50):
                                allow_options = False
                                download_resources_enabled = websites[dosa][0]['download_res']
                                download_cors_resources_enabled = websites[dosa][0]['download_cors_res']
                                cors_enabled = websites[dosa][0]['cors']
                                Max_cors = websites[dosa][0]['max_cors']
                                max_threads = websites[dosa][0]['max_threads']
                                resources_for_cors = websites[dosa][0]['cors_download_res']
                                same_origin_crawl_limit = websites[dosa][0]['same_origin_deviation']
                                page_num = 4
                                page_four()
                                break
                            
                            if event.pos[0]>play_pause_loc[0] and event.pos[0] <play_pause_loc[0]+play_pause_loc[2] and event.pos[1]>play_pause_loc[1] and event.pos[1]<play_pause_loc[1]+play_pause_loc[3]:
                                if websites[dosa][5] and not websites[dosa][3]==0:
                                    pass
                                else:
                                    websites[dosa][5] = not websites[dosa][5]
                                    if not websites[dosa][5]:
                                        resultp = some_thread_result.get(dosa)
                                        bbgip = websites[dosa][0]
                                        if resultp:
                                            bhai = threading.Thread(target=run_process_man, args=(str(bbgip['url']), str(bbgip['download_res']), str(bbgip['download_cors_res']), str(bbgip['cors']), str(bbgip['cors_download_res']), str(bbgip['cors_download_cors_res']), str(bbgip['max_cors']), str(bbgip['same_origin_deviation']), str(bbgip['location']), str(bbgip['maintain_logs']), str(bbgip['show_failed_files']), str(bbgip['refetch']), str(bbgip['hash']), str(bbgip['max_threads']), str(resultp[0]), str(resultp[1])))
                                        else:
                                            bhai = threading.Thread(target=run_process_man, args=(str(bbgip['url']), str(bbgip['download_res']), str(bbgip['download_cors_res']), str(bbgip['cors']), str(bbgip['cors_download_res']), str(bbgip['cors_download_cors_res']), str(bbgip['max_cors']), str(bbgip['same_origin_deviation']), str(bbgip['location']), str(bbgip['maintain_logs']), str(bbgip['show_failed_files']), str(bbgip['refetch']), str(bbgip['hash']), str(bbgip['max_threads']), '{}','{}'))
                                        bhai.start()
                                        websites[dosa][3] = None
                                        websites[dosa][6] = False
                                        websites[dosa][7] = False
                                        some_thread_result[websites[dosa][0]['hash']] = [{},{}]
                                    else:
                                        websites[dosa][3] = 0
                                        if websites[dosa][4] and not websites[dosa][4].poll():
                                            try:
                                                psutil.Process(websites[dosa][4].pid).terminate()
                                            except:
                                                pass
                                        obj1 = font.render("="*40, True, (255, 255, 255)) 
                                        obj = font.render("Paused Scraping ...",True, (255,255,255))
                                        obj2 = font.render("="*40, True, (255, 255, 255)) 
                                        if len(websites[dosa][2])==0:
                                            websites[dosa][2].append([obj1,[120, 450]])
                                        else:
                                            websites[dosa][2].append([obj1, [120, websites[dosa][2][-1][1][1]+30]])
                                        websites[dosa][2].append([obj, [120, websites[dosa][2][-1][1][1]+30]])
                                        websites[dosa][2].append([obj2, [120, websites[dosa][2][-1][1][1]+30]])
                                        for i in websites[dosa][2]:
                                            i[1][1] -= 90
                                        websites[dosa][9] = True
                                    page_two()
                                    break
                            cancel_loc = [dosa_location[0]+685,dosa_location[1]+14, 180, 50]
                            if event.pos[0]>cancel_loc[0] and event.pos[0]<cancel_loc[0]+cancel_loc[2] and event.pos[1]>cancel_loc[1] and event.pos[1]<cancel_loc[1]+cancel_loc[3]:
                                if not websites[dosa][6] and not websites[dosa][7]:
                                    websites[dosa][7] = True
                                    websites[dosa][5] = False
                                    websites[dosa][3] = 0
                                    cancel_color = (0,0,0)
                                    pygame.time.set_timer(CANCEL_PRESSED, 100, loops=1)
                                    if websites[dosa][4] and not websites[dosa][4].poll():
                                        try:
                                            psutil.Process(websites[dosa][4].pid).terminate()
                                        except:
                                            pass
                                    # del websites[dosa]
                                    if os.path.isdir(storage_location+str(dosa)):
                                        try:
                                            shutil.rmtree(storage_location+str(dosa))
                                        except Exception as e:
                                            pass
                                    website_being_downloaded = None
                                    websites_currently_in_process -= 1
                                    with open('data/details.json','r') as jinga:
                                        some_daata = json.load(jinga)
                                    bhai = some_daata['Websites']
                                    new_data = []
                                    for boy in bhai:
                                        if boy['hash'] == dosa:
                                            pass
                                        else:
                                            new_data.append(boy)
                                    with open('data/details.json','w') as ginga:
                                        json.dump({'Websites': new_data},ginga)
                                        
                                    if os.path.isfile(f'temp/{dosa}.json'):
                                        try:
                                            os.remove(f'temp/{dosa}.json')
                                        except:
                                            pass
                                    obj1 = font.render("="*40, True, (255, 255, 255)) 
                                    obj = font.render("Cancelled Scraping ...",True, (255,255,255))
                                    obj2 = font.render("="*40, True, (255, 255, 255)) 
                                    if len(websites[dosa][2])==0:
                                        websites[dosa][2].append([obj1,[120, 450]])
                                    else:
                                        websites[dosa][2].append([obj1, [120, websites[dosa][2][-1][1][1]+30]])
                                    websites[dosa][2].append([obj, [120, websites[dosa][2][-1][1][1]+30]])
                                    websites[dosa][2].append([obj2, [120, websites[dosa][2][-1][1][1]+30]])
                                    for i in websites[dosa][2]:
                                        i[1][1] -= 90
                                    websites[dosa][9] = True
                                    completed.append(dosa)
                                    recalculate()
                                    page_two()
                                    break
                            if event.pos[0]>dosa_location[0]+220 and event.pos[0]<dosa_location[0]+220+50 and event.pos[1]>dosa_location[1]+135 and event.pos[1]<dosa_location[1]+135+50:
                                website_being_downloaded = dosa
                                page_num = 3
                                cached_done_once = True
                                cached_log_renderers = []
                                page_three()
                                websites[dosa][9] = True
                                break
            if event.type == pygame.MOUSEWHEEL:
                if (len(alist)+websites_currently_in_process)!=0:
                    if len(alist)==0:
                        if event.y<0 and base_pos[1]+(250*(websites_currently_in_process-1))>400:
                            base_pos[1] -= 50
                        elif event.y>=0 and base_pos[1]<100:
                            base_pos[1] += 50
                    else:
                        if event.y<0 and alist[-1][0][1]>400:
                            for i in range(len(alist)):
                                alist[i][0][1] -= 50
                                alist[i][2][4][1] -= 50
                            if websites_currently_in_process!=0:
                                base_pos[1] -= 50
                        elif event.y>=0 and (alist[0][0][1] - (250*websites_currently_in_process))<100:
                            for i in range(len(alist)):
                                alist[i][0][1] += 50
                                alist[i][2][4][1] += 50
                            if websites_currently_in_process!=0:
                                base_pos[1] += 50
                    page_two()
            
    elif page_num == 3:
        if website_being_downloaded and websites[website_being_downloaded][9]:
            websites[website_being_downloaded][9] = False
            pygame.draw.rect(screen, (44, 42, 49), [220-125+4, -22, 560+250-8, 280+70+25+150-4], border_radius=20)
            for i in websites[website_being_downloaded][2]:
                screen.blit(i[0],i[1])
                cached_log_renderers.append(i)
        elif not website_being_downloaded and cached_done_once:
            cached_done_once = False
            for i in cached_log_renderers:
                screen.blit(i[0],i[1])
                
        if website_being_downloaded and not websites[website_being_downloaded][7]:
            if websites[website_being_downloaded][3] is None or websites[website_being_downloaded][5]:
                if (pos[0]>rect_play_pause[0] and pos[0]<(rect_play_pause[0]+rect_play_pause[2]) and pos[1]>rect_play_pause[1] and pos[1]<(rect_play_pause[1]+rect_play_pause[3])) and not websites[website_being_downloaded][7]:
                    set_cursor_back3 = False
                    if websites[website_being_downloaded][6]:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)
                    else:
                        pygame.mouse.set_cursor(nw_mouse2)
                elif (pos[0]>rect_cancel[0] and pos[0]<(rect_cancel[0]+rect_cancel[2]) and pos[1]>rect_cancel[1] and pos[1]<(rect_cancel[1]+rect_cancel[3])) or (circle_rectl.collidepoint(pos)) and not websites[website_being_downloaded][7]:
                    set_cursor_back3 = False
                    if websites[website_being_downloaded][7]:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)
                    else:
                        pygame.mouse.set_cursor(nw_mouse2)
                else:
                    set_cursor_back3 = True
            else:
                if circle_rectl.collidepoint(pos):
                    set_cursor_back3 = False
                    pygame.mouse.set_cursor(nw_mouse2)
                else:
                    set_cursor_back3 = True
        # success, cancel & sad
        if website_being_downloaded:
            screen.blit(frames[frame_num], (420, 503))
            pygame.display.update()
            frame_num = (frame_num + 1) % len(frames)
        elif cached_name_for_website2 and eval(cached_name_for_website2) in success_paji:
            pygame.draw.rect(screen, (234, 111, 0), (420, 503, 180, 150))
            screen.blit(frames3[frame_num3], (420, 503))
            pygame.display.update()
            frame_num3 = (frame_num3 + 1) % len(frames3)
        elif cached_name_for_website2 and eval(cached_name_for_website2) in fail_paji:
            if no_internet:
                pygame.draw.rect(screen, (44, 42, 49), [220-125, -22, 560+250, 280+70+25+150], border_radius=20)
                pygame.draw.rect(screen, (0, 0, 0), [220-125, -22, 560+250, 280+70+25+150], 4, border_radius=20)
                pygame.draw.rect(screen, (234, 111, 0), (420, 503, 180, 150))
                screen.blit(frames7[frame_num7], (420, 387))
                pygame.display.update()
                frame_num7 = (frame_num7 + 1) % len(frames7)
            else:
                pygame.draw.rect(screen, (234, 111, 0), (420, 503, 180, 150))
                screen.blit(frames6[frame_num6], (420, 503))
                pygame.display.update()
                frame_num6 = (frame_num6 + 1) % len(frames6)
        else:
            pygame.draw.rect(screen, (234, 111, 0), (420, 503, 180, 150))
            screen.blit(frames4[frame_num4], (360, 56))
            pygame.display.update()
            frame_num4 = (frame_num4 + 1) % len(frames4)

        if set_cursor_back3:
            pygame.mouse.set_cursor(nw_mouse)
            
            
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                nope = False
                for giraffe in events:
                    if giraffe.type == pygame.MOUSEWHEEL:
                        nope = True
                        break
                if nope:
                    continue
                if rect_play_pause.collidepoint(event.pos) and website_being_downloaded and not websites[website_being_downloaded][7]:
                    if websites[website_being_downloaded][5] and not websites[website_being_downloaded][3]==0:
                        pass
                    else:
                        websites[website_being_downloaded][5] = not websites[website_being_downloaded][5]
                        if not websites[website_being_downloaded][5]:
                            result = some_thread_result.get(website_being_downloaded)
                            bbgi = websites[website_being_downloaded][0]
                            if result:
                                bh = threading.Thread(target=run_process_man,args=(str(bbgi['url']), str(bbgi['download_res']), str(bbgi['download_cors_res']), str(bbgi['cors']), str(bbgi['cors_download_res']), str(bbgi['cors_download_cors_res']), str(bbgi['max_cors']), str(bbgi['same_origin_deviation']), str(bbgi['location']), str(bbgi['maintain_logs']), str(bbgi['show_failed_files']), str(bbgi['refetch']), str(bbgi['hash']), str(bbgi['max_threads']), str(result[0]), str(result[1])))
                            else:
                                bh = threading.Thread(target=run_process_man,args=(str(bbgi['url']), str(bbgi['download_res']), str(bbgi['download_cors_res']), str(bbgi['cors']), str(bbgi['cors_download_res']), str(bbgi['cors_download_cors_res']), str(bbgi['max_cors']), str(bbgi['same_origin_deviation']), str(bbgi['location']), str(bbgi['maintain_logs']), str(bbgi['show_failed_files']), str(bbgi['refetch']), str(bbgi['hash']), str(bbgi['max_threads']), '{}', '{}'))
                            bh.start()
                            websites[website_being_downloaded][3] = None
                            websites[website_being_downloaded][6] = False
                            websites[website_being_downloaded][7] = False
                            some_thread_result[bbgi['hash']] = [{},{}]
                        else:
                            websites[website_being_downloaded][3] = 0
                            if websites[website_being_downloaded][4] and not websites[website_being_downloaded][4].poll():
                                try:
                                    psutil.Process(websites[website_being_downloaded][4].pid).terminate()
                                except:
                                    pass
                            obj1 = font.render("="*40, True, (255, 255, 255)) 
                            obj = font.render("Paused Scraping ...",True, (255,255,255))
                            obj2 = font.render("="*40, True, (255, 255, 255)) 
                            if len(websites[website_being_downloaded][2])==0:
                                websites[website_being_downloaded][2].append([obj1,[120, 450]])
                            else:
                                websites[website_being_downloaded][2].append([obj1, [120, websites[website_being_downloaded][2][-1][1][1]+30]])
                            websites[website_being_downloaded][2].append([obj, [120, websites[website_being_downloaded][2][-1][1][1]+30]])
                            websites[website_being_downloaded][2].append([obj2, [120, websites[website_being_downloaded][2][-1][1][1]+30]])
                            for i in websites[website_being_downloaded][2]:
                                i[1][1] -= 90
                            websites[website_being_downloaded][9] = True
                        update_the_play_pause()

                if rect_cancel.collidepoint(event.pos) and website_being_downloaded and not websites[website_being_downloaded][7]:
                    if not websites[website_being_downloaded][7]:
                        websites[website_being_downloaded][7] = True
                        websites[website_being_downloaded][5] = False
                        websites[website_being_downloaded][3] = 0
                        cancel_color = (0,0,0)
                        pygame.time.set_timer(CANCEL_PRESSED, 100, loops=1)
                        if websites[website_being_downloaded][4] and not websites[website_being_downloaded][4].poll():
                            try:
                                psutil.Process(websites[website_being_downloaded][4].pid).terminate()
                            except:
                                pass
                        if os.path.isdir(storage_location+str(website_being_downloaded)):
                            try:
                                shutil.rmtree(storage_location+str(website_being_downloaded))
                            except Exception as e:
                                pass
                        # del websites[website_being_downloaded]
                        websites_currently_in_process -= 1
                        with open('data/details.json','r') as jinga:
                            some_daata = json.load(jinga)
                        bhai = some_daata['Websites']
                        new_data = []
                        for boy in bhai:
                            if boy['hash'] == website_being_downloaded:
                                pass
                            else:
                                new_data.append(boy)
                        with open('data/details.json','w') as ginga:
                            json.dump({'Websites': new_data},ginga)
                            
                        if os.path.isfile(f'temp/{website_being_downloaded}.json'):
                            try:
                                os.remove(f'temp/{website_being_downloaded}.json')
                            except:
                                pass
                        obj1 = font.render("="*40, True, (255, 255, 255)) 
                        obj = font.render("Cancelled Scraping ...",True, (255,255,255))
                        obj2 = font.render("="*40, True, (255, 255, 255)) 
                        if len(websites[website_being_downloaded][2])==0:
                            websites[website_being_downloaded][2].append([obj1,[120, 450]])
                        else:
                            websites[website_being_downloaded][2].append([obj1, [120, websites[website_being_downloaded][2][-1][1][1]+30]])
                        websites[website_being_downloaded][2].append([obj, [120, websites[website_being_downloaded][2][-1][1][1]+30]])
                        websites[website_being_downloaded][2].append([obj2, [120, websites[website_being_downloaded][2][-1][1][1]+30]])
                        for i in websites[website_being_downloaded][2]:
                            i[1][1] -= 90
                        websites[website_being_downloaded][9] = True
                        completed.append(website_being_downloaded)
                        website_being_downloaded = None
                        recalculate()
                        remove_the_buttons()

                if circle_rectl.collidepoint(event.pos):
                    website_being_downloaded = None
                    page_num = last_page
                    if page_num == 1:
                        main_window()
                    else:
                        page_two()
                
                if event.type == CANCEL_PRESSED:
                    cancel_color = (255, 255, 255)
            
    elif page_num == 4:
        
        if circle_rect.collidepoint(pos):
            set_cursor_back4 = False
            pygame.mouse.set_cursor(nw_mouse2)
        else:
            set_cursor_back4 = True
            
        for ji in rects:
            if rects[ji].collidepoint(pos) and allow_options:
                set_cursor_back4 = False
                pygame.mouse.set_cursor(nw_mouse2)
            
        if set_cursor_back4:
            pygame.mouse.set_cursor(nw_mouse)
            
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                nope = False
                for giraffe in events:
                    if giraffe.type == pygame.MOUSEWHEEL:
                        nope = True
                        break
                if nope:
                    continue
                if circle_rect.collidepoint(event.pos):
                    page_num = last_page
                    if page_num==1:
                        main_window()
                    else:
                        page_two()
                if allow_options:    
                    for pp in rects:
                        if rects[pp].collidepoint(event.pos):
                            if pp == "d_resource_rect":
                                download_resources_enabled = not download_resources_enabled
                            elif pp == "d_c_resource_rect":
                                download_cors_resources_enabled = not download_cors_resources_enabled
                            elif pp == "cors_rect":
                                cors_enabled = not cors_enabled
                            elif pp == "cors_resources":
                                resources_for_cors = not resources_for_cors
                            elif pp == "left_max_cors":
                                if Max_cors>0:
                                    Max_cors -=1
                            elif pp == "right_max_cors":
                                if Max_cors<9:
                                    Max_cors += 1
                            elif pp == "left_socl":
                                if same_origin_crawl_limit>0:
                                    same_origin_crawl_limit -=1
                            elif pp == "right_socl":
                                if same_origin_crawl_limit<9:
                                    same_origin_crawl_limit +=1
                            elif pp == "left_mt":
                                if max_threads>0:
                                    max_threads -= 1
                            elif pp == "right_mt":
                                if max_threads<999:
                                    max_threads += 1
                            elif pp == "go_on":
                                loading_for_website_download = True
                                pygame.time.set_timer(DOWNLOAD_THE_DAMN_WEBSITE,1000, loops=1)
                            page_four()
            if event.type == DOWNLOAD_THE_DAMN_WEBSITE:
                websites_currently_in_process += 1
                recalculate()
                hashy = random.randint(500000,2000000)
                script_path = os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), 'website.py')
                process_man = subprocess.Popen(['python', script_path,textinput.value,str(download_resources_enabled),str(download_cors_resources_enabled),str(cors_enabled),str(resources_for_cors),'False',str(Max_cors),str(same_origin_crawl_limit),storage_location+str(hashy),'True','True',str(refetch_enabled),str(max_threads),str(hashy),'{}','{}'],stdout=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
                website_being_downloaded = hashy
                urlji = urllib.parse.quote(textinput.value.replace("\\","/"), safe=":/()=-$#';\\`~!@%,.^&+={}[]")
                atempo = urllib.parse.urlparse(urlji)
                if str(atempo.scheme).strip() == "":
                    urlji = "https://" + urlji
                boi_url = urllib.parse.urlparse(urlji)
                websites[website_being_downloaded] = [{
                    'Name': 'Website 1',
                    'url': textinput.value,
                    "download_res": download_resources_enabled,
                    "download_cors_res": download_cors_resources_enabled,
                    "cors": cors_enabled,
                    "cors_download_res": download_cors_resources_enabled,
                    "cors_download_cors_res": False,
                    "max_cors": Max_cors,
                    "max_threads": max_threads,
                    "same_origin_deviation": same_origin_crawl_limit,
                    "location": storage_location+str(hashy),
                    "maintain_logs": True,
                    "show_failed_files": True,
                    "refetch": refetch_enabled,
                    "logs": [],
                    "hash": hashy,
                    "completed": False,
                    'file_location': os.path.join(os.path.join(storage_location+str(hashy), str(boi_url.hostname)),'index.html')
                }, [], [], None, process_man, False, False, False, threading.Thread(target=read_logs,args=(hashy,), daemon=True), False]
                some_thread_result[hashy] = [{},{}]
                websites[website_being_downloaded][8].start()
                page_num = 3
                cached_done_once = True
                cached_log_renderers = []
                page_three()
                obj1 = font.render("="*40, True, (255, 255, 255)) 
                obj = font.render(f"Scraping Website {textinput.value}",True, (255,255,255))
                obj2 = font.render("="*40, True, (255, 255, 255)) 
                if len(websites[website_being_downloaded][2])==0:
                    websites[website_being_downloaded][2].append([obj1,[120, 450]])
                else:
                    websites[website_being_downloaded][2].append([obj1, [120, websites[website_being_downloaded][2][-1][1][1]+30]])
                websites[website_being_downloaded][2].append([obj, [120, websites[website_being_downloaded][2][-1][1][1]+30]])
                websites[website_being_downloaded][2].append([obj2, [120, websites[website_being_downloaded][2][-1][1][1]+30]])
                for i in websites[website_being_downloaded][2]:
                    i[1][1] -= 90
                websites[website_being_downloaded][9] = True
                loading_for_website_download = False
                # print(f"For {hashy}: {websites[website_being_downloaded][0]}")
                # print(f"Download called for {textinput.value}")
 

    elif page_num ==  5:
        screen.fill((255, 255, 255))
        screen.blit(img, rect)
        screen.blit(frames5[frame_num5], (260, 146))
        pygame.display.update()
        frame_num5 = (frame_num5 + 1) % len(frames5)
        
    elif page_num == 6:
        
        pygame.draw.rect(screen, (232, 232, 232), rectji , border_radius=12)
        back = font.render("Go Back", True, (0,0,0))
        if do:
            screen.blit(back, (85, 20, 200, 50))
        pygame.draw.rect(screen, (157,0,255), rectji2 , border_radius=12)
        screen.blit(aleft, rectji3)
        
        screen.blit(frames8[frame_num8], (50, 80))
        pygame.display.update()
        frame_num8 = (frame_num8 + 1) % len(frames8)
        
        set_cursor_back9 = True
        draw_back_button = True
        if rectji.collidepoint(pos):
            pygame.mouse.set_cursor(nw_mouse2)
            set_cursor_back9 = False
            do = False
            if rectji2.w<=180:
                rectji2.w += 10
                draw_back_button = True
            if rectji3.x<=80:
                rectji3.x += 10
                draw_back_button = True
        else:
            set_cursor_back9 = True
            do = True
            if rectji2.w>=50:
                rectji2.w -= 10
                draw_back_button = True
            if rectji3.x>=30:
                rectji3.x -= 10
                draw_back_button = True
        
        if (pos[0]>450 and pos[0]<450+150 and pos[1]>260 and pos[1]<260+50) or (pos[0]>610 and pos[0]<610+150 and pos[1]>260 and pos[1]<260+50) or (pos[0]>120 and pos[0]<120+180 and pos[1]>500 and pos[1]<500+50):
            set_cursor_back9 = False
            pygame.mouse.set_cursor(nw_mouse2)
                
                
        
        if draw_back_button:
            pygame.draw.rect(screen, (232, 232, 232), rectji , border_radius=12)
            back = font.render("Go Back", True, (0,0,0))
            if do:
                screen.blit(back, (85, 20, 200, 50))
            pygame.draw.rect(screen, (157,0,255), rectji2 , border_radius=12)
            screen.blit(aleft, rectji3)          
                
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rectji.collidepoint(event.pos):
                    time.sleep(0.25)
                    page_num = 1
                    main_window()
                    break
                if (event.pos[0]>450 and event.pos[0]<450+150 and event.pos[1]>260 and event.pos[1]<260+50):
                    webbrowser.open('https://github.com/YogyaChugh')
                if (event.pos[0]>610 and event.pos[0]<610+150 and event.pos[1]>260 and event.pos[1]<260+50):
                    webbrowser.open('https://hackclub.slack.com/team/U09218J0E94')
                if (event.pos[0]>120 and event.pos[0]<120+180 and event.pos[1]>500 and event.pos[1]<500+50):
                    webbrowser.open('https://webber-credits.onrender.com/')
        
        if set_cursor_back9:
            pygame.mouse.set_cursor(nw_mouse)

    elif page_num == 7:
        pygame.draw.rect(screen, (47, 21, 68), [630, 320, 150, 150], border_radius=20)
        screen.blit(frames9[frame_num9], (630, 320))
        pygame.display.update()
        frame_num9 = (frame_num9 + 1) % len(frames9)
        
        recr = pygame.draw.circle(screen, (30, 28, 34), (795, 183), 28)
        pygame.draw.circle(screen, (0, 0, 0), (795, 183), 28, 5)
        screen.blit(cancel, (780, 168))
        
        if recr.collidepoint(pos):
            pygame.mouse.set_cursor(nw_mouse2)
        else:
            pygame.mouse.set_cursor(nw_mouse)
            
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if recr.collidepoint(event.pos):
                    page_num = 1
                    screen.set_alpha(255)
                    main_window()


    for event in events:
        if event.type == pygame.QUIT:
            if quitting_not_started:
                quitting_not_started = False
                screen.blit(img,(0,0))
                bh = font.render("Exiting safely ...", True, (255, 255, 255))
                screen.blit(bh, (10,10))
                pygame.display.update()
                for jjman in websites.copy():
                    if jjman not in completed:
                        try:
                            with open(f"temp/{jjman}.json",'w') as pick:
                                json.dump({jjman: some_thread_result[jjman]}, pick)
                            if websites[jjman][4] and not websites[jjman][4].poll():
                                try:
                                    psutil.Process(websites[jjman][4].pid).terminate()
                                except:
                                    pass
                            with open('data/details.json','r') as asta:
                                goenj = json.load(asta)
                            websing = goenj['Websites']
                            websing.append(websites[jjman][0])
                            goenj['Websites'] = websing
                            with open('data/details.json','w') as pasta:
                                json.dump(goenj, pasta)
                            del websites[jjman]
                        except:
                            pass
                time.sleep(0.3)
                sys.exit()
        if event.type == DELETE_IT:
            if change_the_page:
                page_num = last_page
                change_the_page = False
                page_two()
            
    for pizza in total_lists.copy():
        bhai = total_lists[pizza][1].poll()
        if bhai is not None:
            for pja in alist:
                if pja[7]['hash']==pizza:
                    pja[0][0] = 50
                    pja[0][2] = 900
                    pja[0][3] = 200
                    pja[1] = True
                    pja[2][0] = rocket.copy()
                    pja[2][1] = 0
                    pja[2][2] = False
                    pja[2][3] = False
                    pja[2][4][0] = 753
                    pja[2][4][2] = 39
                    pja[2][4][3] = 39
                    pja[3] = True
                    pja[4] = []
                    pja[5] = True
                    pja[6] = []
                    pja[8] = True
                    del total_lists[pja[-2]['hash']]
                    clicked.remove(pja[-2]['hash'])
                    if page_num==2:
                        page_two()
                    break
            
    pygame.display.update()
    clock.tick(60)