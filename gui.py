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

executor = ThreadPoolExecutor(max_workers=2)

total_lists = {}
pygame.init()

font = pygame.font.Font("assets/VarelaRound-Regular.ttf", 24)
font2 = pygame.font.Font("assets/LuckiestGuy-Regular.ttf", 30)
font3 = pygame.font.Font("assets/FiraSans-Bold.ttf", 30)
font4 = pygame.font.Font("assets/FiraSans-Bold.ttf", 40)
font5 = pygame.font.Font("assets/FiraSans-Bold.ttf", 24)
font6 = pygame.font.Font("assets/FiraSans-Bold.ttf", 18)

some_thread = {}
some_thread_result = {}
display_err = False
display_err_msg = ""

# Create TextInput-object
manager = pygame_textinput.TextInputManager(validator=lambda input: len(input) <= 35)
textinput = pygame_textinput.TextInputVisualizer(manager=manager, font_object=font)

textinput.font_color = (255, 255, 255)

screen = pygame.display.set_mode((1000, 667))
clock = pygame.time.Clock()


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

hover_downloads = False
DOWNLOADS_HOVER = pygame.USEREVENT
pressed_downloads = False
pressed_credits = False
DOWNLOADS_PRESSED = pygame.USEREVENT
CREDITS_PRESSED = pygame.USEREVENT
CANCEL_PRESSED = pygame.USEREVENT
LOADER = pygame.USEREVENT
STARTED_EVENT = pygame.USEREVENT
DELETE_IT = pygame.USEREVENT

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

gg_rect = pygame.Rect(220, 253+119, 560, 80)

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
rect6.y = -60
rect6.w = 313
rect6.h = 267
page_num = 1

rectangle1 = pygame.Rect(780, 20, 200, 50)
rectangle2 = pygame.Rect(815, 30, 200, 50)
rectangle3 = pygame.Rect(30, 600, 160, 50)
rectangle4 = pygame.Rect(65, 610, 160, 50)

rectji = pygame.Rect(10, 10, 200, 50)
rectji2 = pygame.Rect(15, 15, 50, 40)
rectji3 = pygame.Rect(30, 25, 40, 40)

gif = Image.open("assets/meditation.gif")
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

gif2 = Image.open("assets/some_catie.gif")
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


gif3 = Image.open("assets/success.gif")
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

gif4 = Image.open("assets/cancel.gif")
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

gif5 = Image.open("assets/delete.gif")
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



something_done = True
something_other_done = True
change_page = False
do = True
launch_text = True
launch_press_allow = True

processes_running = []

# rect, launch text, rocket img, rotation, launched?, animation_complete?, (i[0]+700, i[1]+18,39, 39)
alist = []
alist_of_running = []

def update_list():
    global alist
    with open('data/details.json' ,'r') as file:
        data = json.load(file)
    websites_temp = data['Websites']
    # print('Websites Temp:\n\n')
    # print(websites_temp)
    alist = []
    for i in range(len(websites_temp)):
        if i==0:
            alist.append([[50,100,900,200], True, [rocket.copy(), 0, False, False, [753, 122, 39,39]], True, [], True, [], websites_temp[i], True])
        else:
            b = alist[i-1]
            alist.append([[b[0][0],b[0][1]+250,b[0][2],b[0][3]], True, [rocket.copy(),0,False,False,[753,b[2][4][1]+250,39,39]],True,[],True,[], websites_temp[i], True])
    # print('ALIST:\n\n')
    # print(alist)

frame_num = 0
frame_num2 = 0
frame_num3 = 0
frame_num4 = 0
frame_num5 = 0

base_pos = [50,100,900,200]

set_cursor_back3 = True
canceled = False

download_resources_enabled = True
download_cors_resources_enabled = False
same_origin_crawl_limit = 0
refetch_enabled = False

cors_enabled = False
resources_for_cors = False
Max_cors = 0

op = 0
t = 0
loader = ['Loading','Loading .','Loading ..','Loading ...']
text_load = 'Loading'
webviews_opened = {}

rects = {
    'd_resource_rect' : pygame.Rect(650, 195, 30, 30),
    'd_c_resource_rect' : pygame.Rect(650, 250, 30, 30),
    'refetch_rect' : pygame.Rect(650, 350, 30, 30),
    'cors_rect' : pygame.Rect(650, 410, 30, 30),
    'cors_resources' : pygame.Rect(435, 472, 25, 25),
    'left_max_cors' : pygame.Rect(565, 474, 30, 30),
    'right_max_cors' : pygame.Rect(630, 473, 30, 30),
    'left_socl': pygame.Rect(620, 300, 30, 30),
    'right_socl': pygame.Rect(685, 299, 30, 30),
    'go_on': pygame.Rect(723, 526, 60, 40)
}

update_list()


rect_play_pause = pygame.Rect(530+125, 100-35, 50, 50)
cancel_color = (255, 255, 255)
rect_cancel = pygame.Rect(600+125, 100-35, 180, 50)
circle_rect = pygame.draw.circle(screen, (30, 28, 34), (795, 83), 28)



with open("data/file_types.json",'r') as file_tp:
        a = json.load(file_tp)
os.environ['file_types'] = str(a['file_types_to_mime'])
    

loading_allow = False
checking = None

at_last = True
allow_options = True
change_the_page = False

website_being_downloaded = None #rename to current website
completed_checking = False

def check_if_website_correct():
    valid = None
    global display_err, display_err_msg, pressed, loading_allow, page_num
    print('Reached')
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
                print('invalid url')
            except Exception as g:
                print('no internet')
                display_err = True
                display_err_msg = "No Internet Connection !"
                
    pressed = False
    print('Completed')
    loading_allow = False
    completed_checking = True
    if valid!=None:
        page_num = 4

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

while True:
    print("CPU:", psutil.cpu_percent())
    print("Threads:", threading.active_count())
    events = pygame.event.get()
    screen.fill((255, 255, 255))
    screen.blit(img, rect)
    pos = pygame.mouse.get_pos()
    if page_num == 1:
        last_page = 1
        textinput.update(events)
        
        screen.blit(main_logoji, (200, 0))
        
        
        pygame.draw.rect(screen, (30, 28, 34), [200, 233+119, 600, 200], border_radius=20)
        pygame.draw.rect(screen, (0, 0, 0), [200, 233+119, 600, 200], 8, border_radius=20)
        pygame.draw.rect(screen, (44, 42, 49), [220, 253+119, 560, 80], border_radius=20)
        pygame.draw.rect(screen, (0, 0, 0), [220, 253+119, 560, 80], 8, border_radius=20)
        
        
        pygame.draw.rect(screen, (0, 0, 0), [780, 49, 200, 25], border_radius=12)
        pygame.draw.rect(screen, (232, 232, 232), rectangle1 , border_radius=12)
        pygame.draw.rect(screen, (30, 28, 34), rectangle1, 3, border_radius=12)
        screen.blit(downloads, rectangle2)
        
        pygame.draw.rect(screen, (0, 0, 0), [30, 600, 160, 50], border_radius=12)
        pygame.draw.rect(screen, (232, 232, 232), rectangle3 , border_radius=12)
        pygame.draw.rect(screen, (30, 28, 34), rectangle3, 3, border_radius=12)
        screen.blit(credits, rectangle4)
        
        
        # pygame.draw.rect(screen, (0, 0, 0), [455, 340, 320, 80], 8, border_radius=20)
        screen.blit(textinput.surface, (250,400))
        if not pressed:
            screen.blit(btn_img, rect2)
        else:
            screen.blit(btn_img_clicked, rect3)
        screen.blit(some_text, rect4)
        screen.blit(spider_img, rect5)
        screen.blit(spider_hanging_img, rect6)
        
        if completed_checking:
            if isinstance(checking, website.StoppableThread):
                checking.join()
                checking = None
        
        if display_err and display_err_msg:
            ay = font6.render(display_err_msg, True, (255,0,0))
            screen.blit(ay, (230, 493))
            
        if loading_allow:
            screen.blit(frames2[frame_num2], (390, 455))
            pygame.display.update()
            frame_num2 = (frame_num2 + 1) % len(frames2)
        
        if not page_num==4:
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
            elif rectangle3.collidepoint(pos):
                pygame.mouse.set_cursor(nw_mouse2)
                if something_other_done:
                    something_other_done = False
                    rectangle3.y -= 3
                    rectangle4.y -= 3
            else:
                if not something_done:
                    something_done = True
                    rectangle1.y += 3
                    rectangle2.y += 3
                if not something_other_done:
                    something_other_done = True
                    rectangle3.y += 3
                    rectangle4.y += 3
                pygame.mouse.set_cursor(nw_mouse)
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
    elif page_num == 2:
        last_page = 2
        set_cursor_back = True
        set_cursor_back2 = True
        #another list alist_of_running
        maggi = 0
        for jackychan in websites:
            # a = [{
            #     'Name': 'Website 1',
            #     'url': textinput.value,
            #     "download_res": download_resources_enabled,
            #     "download_cors_res": download_cors_resources_enabled,
            #     "cors": cors_enabled,
            #     "cors_download_res": download_cors_resources_enabled,
            #     "cors_download_cors_res": False,
            #     "max_cors": Max_cors,
            #     "same_origin_deviation": same_origin_crawl_limit,
            #     "location": ".",
            #     "maintain_logs": True,
            #     "show_failed_files": True,
            #     "refetch": refetch_enabled,
            #     "logs": [],
            #     "hash": temp_website.hash,
            #     "completed": False,
            #     'file_location': os.path.join(temp_website.index_file_location,'index.html')
            # },[],[],temp_website, None, False, False, False]
            if jackychan not in completed and not websites[jackychan][7]:
                temporary_location = [base_pos[0],base_pos[1]+(250*maggi),base_pos[2],base_pos[3]]
                pygame.draw.rect(screen, (26, 26, 26), temporary_location, border_radius=12) #Black box
                
                pygame.draw.rect(screen, (0, 0, 0), temporary_location, 8, border_radius=12) #Black box border
                screen.blit(logo3, (temporary_location[0]+840,temporary_location[1]+140,96,96)) # Spider logo on right
                
                a = font3.render(websites[jackychan][0]['Name'],True,(255, 255, 255)) #NAME
                screen.blit(a, (temporary_location[0]+33, temporary_location[1]+26,temporary_location[2],temporary_location[3]))

                pygame.draw.line(screen, (0,0,0), (temporary_location[0]+30, temporary_location[1]+70), (temporary_location[0]+temporary_location[2]-30, temporary_location[1]+70),6) #LINE SEPARATION

                b = font.render(websites[jackychan][0]['url'],True,(255, 255, 255)) #URL
                screen.blit(b, (temporary_location[0]+33, temporary_location[1]+85,temporary_location[2],temporary_location[3]))

                pygame.draw.rect(screen, (255, 215, 0), (temporary_location[0]+30,temporary_location[1]+135, 180, 50), border_radius=12)
                pygame.draw.rect(screen, (0,0,0), (temporary_location[0]+30,temporary_location[1]+135, 180, 50),4, border_radius=12)
                c = font3.render("!   INFO", True, (0,0,0))
                screen.blit(c, (temporary_location[0]+75,temporary_location[1]+142, 200, 50))
                
                
                pygame.draw.rect(screen, (0, 0, 255), (temporary_location[0]+220,temporary_location[1]+135, 50, 50), border_radius=12)
                pygame.draw.rect(screen, (0,0,0), (temporary_location[0]+220,temporary_location[1]+135, 50, 50),4, border_radius=12)
                screen.blit(eye, [temporary_location[0]+220+7, temporary_location[1]+135+8])
                
                # Imp buttons
                # pygame.draw.rect(screen, (255, 215, 0), (temporary_location[0]+610,temporary_location[1]+14, 50, 50), border_radius=12)
                # pygame.draw.rect(screen, (0,0,0), (temporary_location[0]+610,temporary_location[1]+14, 50, 50),4, border_radius=12)
                # if websites[jackychan][5]:
                #     screen.blit(play, [temporary_location[0]+610+7, temporary_location[1]+14+8])
                # else:
                #     screen.blit(pause, [temporary_location[0]+610+7, temporary_location[1]+14+8])
                pygame.draw.rect(screen, (210, 4, 45), (temporary_location[0]+685,temporary_location[1]+14, 180, 50), border_radius=12)
                pygame.draw.rect(screen, (0,0,0), (temporary_location[0]+685,temporary_location[1]+14, 180, 50),4, border_radius=12)
                b = font3.render("Cancel",True,cancel_color) #NAME
                screen.blit(b, (temporary_location[0]+685+38,temporary_location[1]+14+7, 180, 50))
                
                # Mouse change for info, play-pause and cancel
                if (pos[0]>temporary_location[0]+30 and pos[0]<temporary_location[0]+30+180 and pos[1]>temporary_location[1]+135 and pos[1]<temporary_location[1]+185) or (pos[0]>temporary_location[0]+685 and pos[0]<temporary_location[0]+685+180 and pos[1]>temporary_location[1]+14 and pos[1]<temporary_location[1]+14+50) or (pos[0]>temporary_location[0]+220 and pos[0]<temporary_location[0]+220+50 and pos[1]>temporary_location[1]+135 and pos[1]<temporary_location[1]+135+50):
                    set_cursor_back = False
                    pygame.mouse.set_cursor(nw_mouse2)
                
                maggi += 1
        for j in alist:
            i = j[0].copy()
            i[1] += 250*(maggi)
            rocketloc = j[2][4].copy()
            rocketloc[1] += 250*(maggi)
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
            a = font3.render(j[7]['Name'],True,(255, 255, 255)) #NAME
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
            
            
            if not page_num==4:
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
                    else:
                        if j[2][1]!=0 and not j[2][2]:
                            if j[2][1]!=360:
                                j[2][1]+= 15
                            else:
                                j[2][1]=0
                                set_cursor_back = True
                            j[1] = True
                            j[2][0] = pygame.transform.rotate(rocket, j[2][1])

                    if j[2][2] and not j[2][3]:
                        j[2][1] = 270
                        j[2][0] = pygame.transform.rotate(rocket, j[2][1])
                        rocketloc[0] += 20
                        if rocketloc[0]>i[0]+180+665:
                            j[2][3] = True
                    
        if alist == [] and websites == {}:
            ggcam = font4.render("Nothing to show here !", True, (255, 255, 255))
            screen.blit(ggcam, (300, 300))
        
        
        pygame.draw.rect(screen, (232, 232, 232), rectji , border_radius=12)
        back = font.render("Go Back", True, (0,0,0))
        if do:
            screen.blit(back, (85, 20, 200, 50))
        pygame.draw.rect(screen, (157,0,255), rectji2 , border_radius=12)
        screen.blit(aleft, rectji3)
        
        if not page_num==4:
            if rectji.collidepoint(pos):
                pygame.mouse.set_cursor(nw_mouse2)
                set_cursor_back2 = False
                do = False
                if rectji2.w<=180:
                    rectji2.w += 10
                if rectji3.x<=80:
                    rectji3.x += 10
            else:
                set_cursor_back2 = True
                do = True
                if rectji2.w>=50:
                    rectji2.w -= 10
                if rectji3.x>=30:
                    rectji3.x -= 10
                
        if set_cursor_back and set_cursor_back2:
            pygame.mouse.set_cursor(nw_mouse)
    elif page_num==3:
        pygame.draw.rect(screen, (234, 111, 0), [75, 48, 850, 570], border_radius=20)
        pygame.draw.rect(screen, (44, 42, 49), [220-125, 285-60, 560+250, 280+70+25], border_radius=20)
        if website_being_downloaded:
            for i in websites[website_being_downloaded][2]:
                if not i[1][1]<0 and not i[1][1]>667:
                    screen.blit(i[0],i[1])
        else:
            tj = 0
            for i in cached_log_renderers:
                tj += 1
                if not i[1][1]<0 and not i[1][1]>667:
                    screen.blit(i[0],i[1])
        pygame.draw.rect(screen, (0, 0, 0), [220-125, 285-60, 560+250, 280+70+25], 4, border_radius=20)
        pygame.draw.rect(screen,  (234, 111, 0), [75+25, 48, 850-25, 178])
        # pygame.draw.rect(screen,  (234, 111, 0), [75, 48+225, 20, 570-225])
        # pygame.draw.rect(screen,  (234, 111, 0), [75+830, 48+225, 20, 570-225])
        pygame.draw.rect(screen,  (234, 111, 0), [75+25, 225+375, 850-25-20, 18])
        # screen.blit(simg, (75, 83), (0,0,850,100))
        pygame.draw.rect(screen, (0, 0, 0), [75, 48, 850, 570], 8, border_radius=20)
        screen.blit(img, (75, 0), (75, 0, 850, 48))
        screen.blit(img, (75, 570+48), (75, 570+48, 850, 667-(570+48)))
        
        if website_being_downloaded:
            a = font3.render(websites[website_being_downloaded][0]['Name'],True,(255, 255, 255)) #NAME
            screen.blit(a, [100, 110-35])
        circle_rect = pygame.draw.circle(screen, (30, 28, 34), (795+125, 83-35), 28)
        pygame.draw.circle(screen, (0, 0, 0), (795+125, 83-35), 28, 5)
        screen.blit(cancel, (780+125, 68-35))
        
        if website_being_downloaded:
            # print('lalalalala')
            # print(website_being_downloaded.logs)
            currji = websites[website_being_downloaded][1]
            currji_lala = websites[website_being_downloaded][2]
            if currji_lala==[] and currji!=[]:
                for i in currji:
                    t = i[:60]
                    if len(t)!=len(i):
                        t+="..."
                    if i.startswith("Downloading Webpage"):
                        obj = font.render(t,True, (255,255,255))
                    elif i.startswith("Download Success") or i.startswith("Resource Download Success"):
                        obj = font.render(t,True, (0,255,0))
                    elif i.startswith("Download Failed") or i.startswith("Resource Download Failed"):
                        obj = font.render(t, True, (255,0,0))
                    else:
                        obj = font.render(t, True,(255,255,255))
                    if len(currji_lala)==0:
                        currji_lala.append([obj,[120, 550]])
                    else:
                        currji_lala.append([obj, [120, currji_lala[-1][1][1]+30]])
                if at_last:
                    for i in currji_lala:
                        i[1][1] -= (len(currji)*30)
                websites[website_being_downloaded][2] = currji_lala
                cached_log_renderers = currji_lala
            if websites[website_being_downloaded][3].logs!=currji:
                websites[website_being_downloaded][1] = websites[website_being_downloaded][3].logs
                curr = websites[website_being_downloaded][2]
                curr2 = websites[website_being_downloaded][1]
                g = True if curr==[] else False
                p = len(websites[website_being_downloaded][2]) - 1
                gt = 0
                for i in websites[website_being_downloaded][3].logs:
                    p+=1
                    gt+=1
                    t = i[:60]
                    if len(t)!=len(i):
                        t+="..."
                    if i.startswith("Downloading Webpage"):
                        obj = font.render(t,True, (255,255,255))
                    elif i.startswith("Download Success") or i.startswith("Resource Download Success"):
                        obj = font.render(t,True, (0,255,0))
                    elif i.startswith("Download Failed") or i.startswith("Resource Download Failed"):
                        obj = font.render(t, True, (255,0,0))
                    else:
                        obj = font.render(t, True,(255,255,255))
                    if p==0:
                        curr.append([obj,[120, 550]])
                    else:
                        curr.append([obj, [120, curr[p-1][1][1]+30]])
                if at_last:
                    for i in curr:
                        i[1][1] -= (gt*30)
                websites[website_being_downloaded][2] = curr
                cached_log_renderers = curr
                websites[website_being_downloaded][3].logs = []
                
        if website_being_downloaded and not websites[website_being_downloaded][7]:
            if not websites[website_being_downloaded][3].done and ((not websites[website_being_downloaded][3].failed) or (websites[website_being_downloaded][5] and not websites[website_being_downloaded][7])):
                pygame.draw.rect(screen, (255, 215, 0), rect_play_pause, border_radius=12)
                pygame.draw.rect(screen, (0,0,0), rect_play_pause,4, border_radius=12)
                if websites[website_being_downloaded][5]:
                    screen.blit(play, [537+125, 108-35])
                else:
                    screen.blit(pause, [537+125, 108-35])
                pygame.draw.rect(screen, (210, 4, 45), rect_cancel, border_radius=12)
                pygame.draw.rect(screen, (0,0,0), rect_cancel,4, border_radius=12)
                b = font3.render("Cancel",True,cancel_color) #NAME
                screen.blit(b, [638+125, 107-35, 180, 50])
                screen.blit(frames[frame_num], (420, 56))
                pygame.display.update()
                frame_num = (frame_num + 1) % len(frames)
                if not page_num==4:
                    if (pos[0]>rect_play_pause[0] and pos[0]<(rect_play_pause[0]+rect_play_pause[2]) and pos[1]>rect_play_pause[1] and pos[1]<(rect_play_pause[1]+rect_play_pause[3])):
                        set_cursor_back3 = False
                        if websites[website_being_downloaded][6]:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)
                        else:
                            pygame.mouse.set_cursor(nw_mouse2)
                    elif (pos[0]>rect_cancel[0] and pos[0]<(rect_cancel[0]+rect_cancel[2]) and pos[1]>rect_cancel[1] and pos[1]<(rect_cancel[1]+rect_cancel[3])) or (circle_rect.collidepoint(pos)):
                        set_cursor_back3 = False
                        if websites[website_being_downloaded][7]:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)
                        else:
                            pygame.mouse.set_cursor(nw_mouse2)
                    else:
                        set_cursor_back3 = True
            else:
                if not websites[website_being_downloaded][7] and not websites[website_being_downloaded][6] and not websites[website_being_downloaded][5]:
                    screen.blit(frames3[frame_num3], (420, 100))
                    pygame.display.update()
                    frame_num3 = (frame_num3 + 1) % len(frames3)
                else:
                    print('dilkfsegsgfsegs')
                    print("paused: ",websites[website_being_downloaded][5])
                    print("failed: ",websites[website_being_downloaded][3].failed)
                    print('done: ',websites[website_being_downloaded][3].done)
                if (pos[0]>rect_cancel[0] and pos[0]<(rect_cancel[0]+rect_cancel[2]) and pos[1]>rect_cancel[1] and pos[1]<(rect_cancel[1]+rect_cancel[3])) or (circle_rect.collidepoint(pos)):
                    set_cursor_back3 = False
                    pygame.mouse.set_cursor(nw_mouse2)
                else:
                    set_cursor_back3 = True
            
        else:
            screen.blit(frames4[frame_num4], (360, 56))
            pygame.display.update()
            frame_num4 = (frame_num4 + 1) % len(frames4)

        if set_cursor_back3:
            pygame.mouse.set_cursor(nw_mouse)

            
    elif page_num == 4:
        pygame.draw.rect(screen, (47, 21, 68), [200, 83, 600, 500], border_radius=20)
        screen.blit(simg, (200, 83), (0, 0, 600, 73))
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
        if download_resources_enabled:
            screen.blit(tick, (650, 186))
        resources = font5.render("Download CORS Resources", True, (255,255,255))
        screen.blit(resources, (270, 250))
        if allow_options:
            pygame.draw.rect(screen, (0, 0, 0), rects['d_c_resource_rect'], 4)
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
        resources = font5.render("Refetch", True, (255,255,255))
        screen.blit(resources, (270, 350))
        if allow_options:
            pygame.draw.rect(screen, (0, 0, 0), rects['refetch_rect'], 4)
        if refetch_enabled:
            screen.blit(tick, (650, 341))
        
        
        pygame.draw.line(screen, (0,0,0), (250, 395), (748, 395),4)
        resources = font5.render("Cross-Origin Sites", True, (255,255,255))
        screen.blit(resources, (270, 410))
        if allow_options:
            pygame.draw.rect(screen, (0, 0, 0), rects['cors_rect'], 4)
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
        
        if allow_options:
            pygame.draw.rect(screen, (48, 25, 52), rects['go_on'], border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), rects['go_on'], 6, border_radius=10)
            screen.blit(aright, (rects['go_on'].x + 12, rects['go_on'].y + 9))
        
        if resources_for_cors and cors_enabled:
            screen.blit(tick2, (435, 463))
        
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


    elif page_num ==  5:
        screen.blit(frames5[frame_num5], (420, 256))
        pygame.display.update()
        frame_num5 = (frame_num5 + 1) % len(frames5)


    for event in events:
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            nope = False
            for giraffe in events:
                if giraffe.type == pygame.MOUSEWHEEL:
                    nope = True
                    break
            if nope:
                continue
            if not page_num==4:
                if rect2.collidepoint(event.pos) and page_num == 1 and not pressed:
                    pressed = True
                    rect4.y += 1
                    counterman = 0
                    for pasta in websites:
                        if not websites[pasta][5] and not websites[pasta][7]:
                            counterman += 1
                    print("Websites Running: ",counterman)
                    if counterman>=1:
                        display_err = True
                        display_err_msg = "Max 1 at a time !"
                    else:
                        loading_allow = True
                        display_err = False
                        display_err_msg = ""
                        pygame.time.set_timer(STARTED, 1000)
                if rectangle1.collidepoint(event.pos) and page_num == 1:
                    pressed_downloads = True
                    rectangle1.y += 5
                    rectangle2.y += 5
                    pygame.time.set_timer(DOWNLOADS_PRESSED, 200)
                if rectangle3.collidepoint(event.pos) and page_num == 1:
                    pressed_credits = True
                    rectangle3.y += 5
                    rectangle4.y += 5
                    pygame.time.set_timer(CREDITS_PRESSED, 200)
                if rectji.collidepoint(event.pos) and page_num == 2:
                    time.sleep(0.25)
                    page_num = 1

                if page_num == 2:
                    doit = True
                    for pppp in events:
                        if pppp.type== pygame.MOUSEWHEEL:
                            doit = False
                            break
                    if doit:
                        maggiji = 0
                        for people in websites:
                            if people not in completed:
                                maggiji += 1
                        # print(alist)
                        for j in alist:
                            i = j[0].copy()
                            i[1] += (250*(maggiji))
                            if event.pos[0]>i[0]+685 and event.pos[0]<i[0]+865 and event.pos[1]>i[1]+14 and event.pos[1]<i[1]+64:
                                if j[8]:
                                    j[8] = False
                                    j[2][2] = True
                                    # with open(f'web_{j[-2]['file_location']}.pkl', 'w') as fp:
                                    #     pass
                                    dothat = True
                                    for d in total_lists:
                                        if d==j[-2]['hash'] and total_lists[d]!=None:
                                            dothat = False
                                            break
                                    if dothat:
                                        print('created')
                                        process = subprocess.Popen(['python','webview_launch.py',j[-2]['file_location']])
                                        total_lists[j[-2]['hash']] = ([j[-2]['file_location'],process])
                                        clicked.append(j[-2]['hash'])
                                    # pygame.time.set_timer(STARTED_EVENT,5000)
                                else:
                                    apboi = total_lists.get(j[-2]['hash'])
                                    # os.kill(apboi[2].pid, signal.SIGTERM)
                                    if apboi:
                                        print('came')
                                        # print(apboi)
                                        psutil.Process(apboi[1].pid).terminate()
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
                                        print("deleted !")
                                        # print(total_lists)
                                        clicked.remove(j[-2]['hash'])
                                        apboi = None
                                break
                            if (event.pos[0]>i[0]+30 and event.pos[0]<i[0]+210 and event.pos[1]>i[1]+135 and event.pos[1]<i[1]+185):
                                allow_options = False
                                download_resources_enabled = j[-2]['download_res']
                                download_cors_resources_enabled = j[-2]['download_cors_res']
                                cors_enabled = j[-2]['cors']
                                Max_cors = j[-2]['max_cors']
                                resources_for_cors = j[-2]['cors_download_res']
                                same_origin_crawl_limit = j[-2]['same_origin_deviation']
                                page_num = 4
                                break
                            
                            if (j[8] and event.pos[0]>i[0]+230 and event.pos[0]<i[0]+410 and event.pos[1]>i[1]+135 and event.pos[1]<i[1]+185):
                                puppy = j[7]
                                if os.path.isdir(puppy['file_location']):
                                    try:
                                        shutil.rmtree(puppy['file_location'])
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
                                update_list()
                                page_num = 5
                                change_the_page = True
                                pygame.time.set_timer(DELETE_IT,3000)

                if page_num == 3 and rect_play_pause.collidepoint(event.pos):
                    if websites[website_being_downloaded][5] and not websites[website_being_downloaded][3].canceled:
                        pass
                    else:
                        websites[website_being_downloaded][5] = not websites[website_being_downloaded][5]
                        websites[website_being_downloaded][6] = True
                        websites[website_being_downloaded][3].failed = True
                        if not websites[website_being_downloaded][5]:
                            result = some_thread_result.get(website_being_downloaded)
                            temp_website = website.Website(websites[website_being_downloaded][0])
                            temp_website.hash = website_being_downloaded
                            if result:
                                temp_website.webpages_scraped = result[0]
                                temp_website.resources_downloaded = result[1]
                            websites[website_being_downloaded][4] = website.StoppableThread(target=temp_website.download)
                            websites[website_being_downloaded][4].start()
                        else:
                            t = website.StoppableThread(target=websites[website_being_downloaded][3].cancel)
                            t.start()
                            some_thread[website_being_downloaded] = t

                if page_num == 3 and rect_cancel.collidepoint(event.pos):
                    if not websites[website_being_downloaded][6] and not websites[website_being_downloaded][7]:
                        websites[website_being_downloaded][7] = True
                        websites[website_being_downloaded][5] = False
                        websites[website_being_downloaded][3].failed = True
                        cancel_color = (0,0,0)
                        pygame.time.set_timer(CANCEL_PRESSED, 100)
                        t = website.StoppableThread(target=websites[website_being_downloaded][3].cancel,args=([True]))
                        t.start()
                        some_thread[website_being_downloaded] = t

                if page_num == 3 and circle_rect.collidepoint(event.pos):
                    website_being_downloaded = None
                    page_num = last_page
                    
                    
                if page_num == 2:
                    dosa_num = 0
                    for dosa in websites:
                        if dosa not in completed:
                            dosa_location = [base_pos[0],base_pos[1]+(250*dosa_num),base_pos[2],base_pos[3]]
                            play_pause_loc = [dosa_location[0]+610+7, dosa_location[1]+14+8, 50, 50]
                            info_loc = [dosa_location[0]+30,dosa_location[1]+135, 180, 50]
                            if (event.pos[0]>info_loc[0] and event.pos[0]<info_loc[0]+180 and event.pos[1]>info_loc[1] and event.pos[1]<info_loc[1]+50):
                                allow_options = False
                                download_resources_enabled = websites[dosa][0]['download_res']
                                download_cors_resources_enabled = websites[dosa][0]['download_cors_res']
                                cors_enabled = websites[dosa][0]['cors']
                                Max_cors = websites[dosa][0]['max_cors']
                                resources_for_cors = websites[dosa][0]['cors_download_res']
                                same_origin_crawl_limit = websites[dosa][0]['same_origin_deviation']
                                page_num = 4
                                break
                            
                            # if event.pos[0]>play_pause_loc[0] and event.pos[0] <play_pause_loc[0]+play_pause_loc[2] and event.pos[1]>play_pause_loc[1] and event.pos[1]<play_pause_loc[1]+play_pause_loc[3]:
                            #     if websites[dosa][5] and not websites[dosa][3].canceled:
                            #         pass
                            #     else:
                            #         websites[dosa][5] = not websites[dosa][5]
                            #         websites[dosa][6] = True
                            #         websites[dosa][3].failed = True
                            #         if not websites[dosa][5]:
                            #             result = some_thread_result.get(dosa)
                            #             temp_website = website.Website(websites[dosa][0])
                            #             temp_website.hash = dosa
                            #             if result:
                            #                 temp_website.webpages_scraped = result[0]
                            #                 temp_website.resources_downloaded = result[1]
                            #             websites[dosa][4] = website.StoppableThread(target=temp_website.download)
                            #             websites[dosa][4].start()
                            #         else:
                            #             t = website.StoppableThread(target=websites[dosa][3].cancel)
                            #             t.start()
                            #             some_thread[dosa] = t
                            #         break
                            cancel_loc = [dosa_location[0]+685,dosa_location[1]+14, 180, 50]
                            if event.pos[0]>cancel_loc[0] and event.pos[0]<cancel_loc[0]+cancel_loc[2] and event.pos[1]>cancel_loc[1] and event.pos[1]<cancel_loc[1]+cancel_loc[3]:
                                if not websites[dosa][6] and not websites[dosa][7]:
                                    websites[dosa][7] = True
                                    websites[dosa][5] = False
                                    websites[dosa][3].failed = True
                                    cancel_color = (0,0,0)
                                    pygame.time.set_timer(CANCEL_PRESSED, 100)
                                    t = website.StoppableThread(target=websites[dosa][3].cancel,args=([True]))
                                    t.start()
                                    some_thread[dosa] = t  
                                    break
                            if event.pos[0]>dosa_location[0]+220 and event.pos[0]<dosa_location[0]+220+50 and event.pos[1]>dosa_location[1]+135 and event.pos[1]<dosa_location[1]+135+50:
                                website_being_downloaded = dosa
                                page_num = 3
                                break

            else:
                if circle_rect.collidepoint(event.pos):
                    page_num = last_page
                if allow_options:    
                    for pp in rects:
                        if rects[pp].collidepoint(event.pos):
                            if pp == "d_resource_rect":
                                download_resources_enabled = not download_resources_enabled
                            elif pp == "d_c_resource_rect":
                                download_cors_resources_enabled = not download_cors_resources_enabled
                            elif pp == "refetch_rect":
                                refetch_enabled = not refetch_enabled
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
                            elif pp == "go_on":
                                temp_website = website.Website({
                                    'Name': 'Website 1',
                                    'url': textinput.value,
                                    "download_res": download_resources_enabled,
                                    "download_cors_res": download_cors_resources_enabled,
                                    "cors": cors_enabled,
                                    "cors_download_res": download_cors_resources_enabled,
                                    "cors_download_cors_res": False,
                                    "max_cors": Max_cors,
                                    "same_origin_deviation": same_origin_crawl_limit,
                                    "location": ".",
                                    "maintain_logs": True,
                                    "show_failed_files": True,
                                    "refetch": refetch_enabled,
                                    "logs": [],
                                })
                                website_being_downloaded = temp_website.hash
                                websites[website_being_downloaded] = [{
                                    'Name': 'Website 1',
                                    'url': textinput.value,
                                    "download_res": download_resources_enabled,
                                    "download_cors_res": download_cors_resources_enabled,
                                    "cors": cors_enabled,
                                    "cors_download_res": download_cors_resources_enabled,
                                    "cors_download_cors_res": False,
                                    "max_cors": Max_cors,
                                    "same_origin_deviation": same_origin_crawl_limit,
                                    "location": ".",
                                    "maintain_logs": True,
                                    "show_failed_files": True,
                                    "refetch": refetch_enabled,
                                    "logs": [],
                                    "hash": temp_website.hash,
                                    "completed": False,
                                    'file_location': os.path.join(temp_website.index_file_location,'index.html')
                                },[],[],temp_website, None, False, False, False]
                                page_num = 3
                                websites[website_being_downloaded][4] = website.StoppableThread(target=temp_website.download)
                                websites[website_being_downloaded][4].start()
                                print(f"Download called for {textinput.value}")
                
        if event.type == CANCEL_PRESSED and not page_num == 4:
            cancel_color = (255, 255, 255)     
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and page_num == 1:
            pressed = True
            rect4.y += 1
            loading_allow = True
            display_err = False
            display_err_msg = ""
            counterman = 0
            for pasta in websites:
                if not websites[pasta][5] and not websites[pasta][7]:
                    counterman += 1
            print("Websites Running: ",counterman)
            if counterman>=1:
                display_err = True
                display_err_msg = "Max 1 at a time !"
            else:
                loading_allow = True
                display_err = False
                display_err_msg = ""
                pygame.time.set_timer(STARTED, 1000)
                
        if event.type == pygame.MOUSEWHEEL and page_num == 2:
            if len(alist)!=0:
                if event.y<0 and alist[-1][0][1]>400:
                    for i in range(len(alist)):
                        alist[i][0][1] -= 50
                        alist[i][2][4][1] -= 50
                    base_pos[1] -= 50
                elif event.y>=0 and alist[0][0][1]<100:
                    for i in range(len(alist)):
                        alist[i][0][1] += 50
                        alist[i][2][4][1] += 50
                    base_pos[1] += 50
                    
        position = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEWHEEL and page_num == 3 and (position[0]>95 and position[0]<95+810 and position[1]>225 and position[1]<225+375):
            tempsingh = websites[website_being_downloaded][2]
            if event.y<0 and tempsingh[-1][1][1]!=550:
                for i in tempsingh:
                    i[1][1] -= 30
            if event.y>=0 and tempsingh[0][1][1]!=250:
                for i in tempsingh:
                    i[1][1] += 30
                
        if event.type == STARTED and pressed and not page_num==4:
            display_err = False
            rect4.y -= 1
            valid = None
            pressed = False
            counterman = 0
            for pasta in websites:
                if not websites[pasta][5] and not websites[pasta][7]:
                    counterman += 1
            if counterman<1:
                allow_options = True
                download_resources_enabled = True
                download_cors_resources_enabled = False
                same_origin_crawl_limit = 0
                refetch_enabled = False
                
                cors_enabled = False
                resources_for_cors = False
                Max_cors = 0
                checking = website.StoppableThread(target=check_if_website_correct)
                checking.start()
            pygame.mouse.set_cursor(nw_mouse)
        if event.type == DOWNLOADS_PRESSED and pressed_downloads and page_num == 1 and not page_num==4:
            rectangle1.y -= 5
            rectangle2.y -= 5
            pressed_downloads = False
            change_page = True
        if event.type == CREDITS_PRESSED and pressed_credits and page_num == 1 and not page_num ==4:
            rectangle3.y -=5
            rectangle4.y -=5
            pressed_credits = False
            
            
        if event.type == DELETE_IT:
            if change_the_page:
                page_num = last_page
                change_the_page = False
            
        if event.type == STARTED_EVENT:
            pass
            # if total_lists!=[]:
            #     a = total_lists[0]
            #     with open(f'web_{a[0]}.pkl','rb') as ff:
            #         obj = dill.load(ff)
            #     print(obj)
            #     if obj[0] == a[0]:
            #         webviews_opened[a[1]] = obj[1]
            #     total_lists = total_lists[1:]
            
    for i in websites.copy():
        if i in completed:
            continue
        if websites[i][3].canceled:
            some_thread[i].join()
            sabji = some_thread[i].get_result()
            if websites[i][7]:
                t = website.StoppableThread(target=websites[i][3].delete)
                t.start()
                some_other_thread[i] = t
            else:
                some_thread_result[i] = sabji
                websites[i][6] = False
        if websites[i][3].deleted:
            some_other_thread[i].join()
        if websites[i][3].completed and websites[i][4] and not websites[i][3].deleted and not websites[i][5] and not websites[i][7]:
            websites[i][4].join()
            websites[i][0]['completed'] = True
            with open('data/details.json','r') as file:
                tempdata = json.load(file)
            a = tempdata['Websites']
            a.append(websites[i][0])
            tempdata['Websites'] = a
            # print(tempdata)
            with open('data/details.json','w') as file:
                json.dump(tempdata, file)
            websites[i][3].done = True
            if i==website_being_downloaded:
                if not websites[i][7] and websites[i][3].failed:
                    cached_log_renderers.append((font.render("DOWNLOAD FAILED !!", True, (255, 0,255)),[120,cached_log_renderers[-1][1][1]+30]))
                elif not websites[i][7] and not websites[i][5]:
                    cached_log_renderers.append((font.render("DOWNLOAD SUCCESSFULL !!", True, (0,255,255)),[120,cached_log_renderers[-1][1][1]+30]))
                if at_last:
                    for r in cached_log_renderers:
                        r[1][1] -= 30
            completed.append(i)
            print(i)
            update_list()
            # del websites[i]
            
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
                    break
            
    pygame.display.update()
    clock.tick(60)