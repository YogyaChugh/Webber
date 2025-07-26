import pygame_textinput
from PIL import Image
import pygame
import time
import json
import webpage, website
import os
import webview
import asyncio

pygame.init()

font = pygame.font.Font("assets/VarelaRound-Regular.ttf", 24)
font2 = pygame.font.Font("assets/LuckiestGuy-Regular.ttf", 30)
font3 = pygame.font.Font("assets/FiraSans-Bold.ttf", 30)
font4 = pygame.font.Font("assets/FiraSans-Bold.ttf", 40)
font5 = pygame.font.Font("assets/FiraSans-Bold.ttf", 24)
font6 = pygame.font.Font("assets/FiraSans-Bold.ttf", 18)


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

rect = img.get_rect()
rect2 = btn_img.get_rect()
rect3 = btn_img.get_rect()
# print(rect)
rect2.x = 465
rect2.y = 340+119
rect3.x = 465
rect3.y = 340+119
screen.fill((225, 225, 225))

pygame.key.set_repeat(200, 25)
pressed = False
STARTED = pygame.USEREVENT

hover_downloads = False
DOWNLOADS_HOVER = pygame.USEREVENT
pressed_downloads = False
DOWNLOADS_PRESSED = pygame.USEREVENT
CANCEL_PRESSED = pygame.USEREVENT
LOADER = pygame.USEREVENT

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

gg_rect = pygame.Rect(220, 253, 560, 80)

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

something_done = True
change_page = False
do = True
launch_text = True
launch_press_allow = True

# rect, launch text, rocket img, rotation, launched?, animation_complete?, (i[0]+700, i[1]+18,39, 39)
alist = []

def update_list():
    with open('details.json' ,'r') as file:
        data = json.load(file)
    websites = data['Websites']
    for i in range(len(websites)):
        if i==0:
            alist.append([[50,100,900,200], True, [rocket.copy(), 0, False, False, [753, 122, 39,39]], True, [], True, [], websites[i]])
        else:
            b = alist[i-1]
            alist.append([[b[0][0],b[0][1]+250,b[0][2],b[0][3]], True, [rocket.copy(),0,False,False,[b[2][4][0],b[2][4][1]+250,b[2][4][2],b[2][4][3]]],True,[],True,[], websites[i]])


frame_num = 0
frame_num2 = 0

set_cursor_back3 = True
paused = False
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



with open("file_types.json",'r') as file_tp:
        a = json.load(file_tp)
os.environ['file_types'] = str(a['file_types_to_mime'])
    

loading_allow = False
checking = None


task_running = None


website_being_downloaded = None
webpage_possible = None
completed_checking = False

current_logs = []

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

while True:
    events = pygame.event.get()
    screen.fill((255, 255, 255))
    screen.blit(img, rect)
    pos = pygame.mouse.get_pos()
    if page_num == 1:
        textinput.update(events)
        
        screen.blit(main_logoji, (200, 0))
        
        
        pygame.draw.rect(screen, (30, 28, 34), [200, 233+119, 600, 200], border_radius=20)
        pygame.draw.rect(screen, (0, 0, 0), [200, 233+119, 600, 200], 8, border_radius=20)
        pygame.draw.rect(screen, (44, 42, 49), [220, 253+119, 560, 80], border_radius=20)
        pygame.draw.rect(screen, (0, 0, 0), [220, 253+119, 560, 80], 8, border_radius=20)
        
        
        pygame.draw.rect(screen, (0, 0, 0), [780, 49, 200, 25], border_radius=12)
        pygame.draw.rect(screen, (232, 232, 232), rectangle1 , border_radius=12)
        pygame.draw.rect(screen, (30, 28, 34), rectangle1, 3, border_radius=12)
        downloads = font.render("Downloads", True, (0,0,0))
        screen.blit(downloads, rectangle2)
        # pygame.draw.rect(screen, (0, 0, 0), [455, 340, 320, 80], 8, border_radius=20)
        some_text = font2.render("CRAWL & DOWNLOAD", True, (255, 191, 0))
        screen.blit(textinput.surface, (250,400))
        if not pressed:
            screen.blit(btn_img, rect2)
        else:
            screen.blit(btn_img_clicked, rect3)
        screen.blit(some_text, rect4)
        screen.blit(spider_img, rect5)
        screen.blit(spider_hanging_img, rect6)
        
        if completed_checking:
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
            else:
                if not something_done:
                    something_done = True
                    rectangle1.y += 3
                    rectangle2.y += 3
                pygame.mouse.set_cursor(nw_mouse)
            if change_page:
                change_page = False
                #rectangle1.y -= 5
                #rectangle2.y -= 5
                pygame.mouse.set_cursor(nw_mouse)
                pygame.display.update()
                time.sleep(0.25)
                update_list()
                page_num = 2
    elif page_num == 2:
        set_cursor_back = True
        set_cursor_back2 = True
        for j in alist:
            i = j[0]
            
            #BUTTONS
            # temprect_launch.add(pygame.Rect(i[0]+685,i[1]+14, 180, 45))
            pygame.draw.rect(screen, (211, 214, 219), (i[0]+685,i[1]+14, 180, 50), border_radius=12)
            pygame.draw.rect(screen, (0,0,0), (i[0]+685,i[1]+14, 180, 50),4, border_radius=12)
            if j[1]:
                c = font3.render("Launch", True, (0,0,0))
                screen.blit(c, (i[0]+750,i[1]+21, 200, 50))
                
            screen.blit(j[2][0], j[2][4])
            
            
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
            
            
            pygame.draw.rect(screen, (255, 0, 0), (i[0]+230,i[1]+135, 180, 50), border_radius=12)
            pygame.draw.rect(screen, (0,0,0), (i[0]+230,i[1]+135, 180, 50),4, border_radius=12)
            if j[5]:
                c = font3.render("DELETE", True, (0,0,0))
                screen.blit(c, (i[0]+290,i[1]+142, 200, 50))
            screen.blit(delete, (i[0]+250,i[1]+141, 200, 50))
            
            
            if not page_num==4:
                # Check for launch
                if pos[0]>i[0]+685 and pos[0]<i[0]+865 and pos[1]>i[1]+14 and pos[1]<i[1]+64:
                    set_cursor_back = False
                    if launch_press_allow:
                        change = True
                    else:
                        change = False
                        if not j[2][2]:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)
                else:
                    change = False

                # Check for Delete & Info
                if (pos[0]>i[0]+230 and pos[0]<i[0]+410 and pos[1]>i[1]+135 and pos[1]<i[1]+185) or (pos[0]>i[0]+30 and pos[0]<i[0]+210 and pos[1]>i[1]+135 and pos[1]<i[1]+185):
                    set_cursor_back = False
                    pygame.mouse.set_cursor(nw_mouse2)


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
                    j[2][4][0] += 20
                    if j[2][4][0]>i[0]+180+665:
                        j[2][3] = True
                    
        
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
        pygame.draw.rect(screen,  (234, 111, 0), [75, 48, 850, 570], border_radius=20)
        # screen.blit(simg, (75, 83), (0,0,850,100))
        pygame.draw.rect(screen, (0, 0, 0), [75, 48, 850, 570], 8, border_radius=20)
        screen.blit(img, (75, 0), (75, 0, 850, 48))
        screen.blit(img, (75, 583+48), (75, 583+48, 850, 667-(583+48)))
        
        a = font3.render(currently_settings['Name'],True,(255, 255, 255)) #NAME
        screen.blit(a, [100, 110-35])
        circle_rect = pygame.draw.circle(screen, (30, 28, 34), (795+125, 83-35), 28)
        pygame.draw.circle(screen, (0, 0, 0), (795+125, 83-35), 28, 5)
        screen.blit(cancel, (780+125, 68-35))
        
        # if website_being_downloaded:
        #     if website_being_downloaded.logs!=currently_settings['logs']:
        #         currently_settings['logs'] = website_being_downloaded.logs
        #         g = 0
        #         for i in website_being_downloaded.logs:
        #             if i.startswith("Downloading Webpage"):
        #                 current_logs.append((font.render(i,True, (0,0,0)),(870, 550) if g==0 else (870, current_logs[g-1][1][1]+30)))
        #             elif i.startswith("Download Success") or i.startswith("Resource Download Success"):
        #                 current_logs.append((font.render(i,True, (0,0,255)),(870, 550) if g==0 else (870, current_logs[g-1][1][1]+30)))
        #             elif i.startswith("Download Failed") or i.startswith("Resource Download Failed"):
        #                 current_logs.append((font.render(i,True, (255,0,0)),(870, 550) if g==0 else (870, current_logs[g-1][1][1]+30)))
        #             g+=1
        #         website_being_downloaded.logs = []
        #     if website_being_downloaded.done or website_being_downloaded.failed:
        #         if website_being_downloaded and (website_being_downloaded.done or website_being_downloaded.failed) and task_running:
        #             task_running.join()
        #             task_running = None
        #             if website_being_downloaded.done:
        #                 with open('details.json','r') as file:
        #                     tempdata = json.load(file)
        #                 a = tempdata['Websites']
        #                 a.append(currently_settings)
        #                 tempdata['Websites'] = a
        #                 print(tempdata)
        #                 with open('details.json','w') as file:
        #                     json.dump(tempdata, file)
        #     else:
        pygame.draw.rect(screen, (255, 215, 0), rect_play_pause, border_radius=12)
        pygame.draw.rect(screen, (0,0,0), rect_play_pause,4, border_radius=12)
        if paused:
            screen.blit(play, [537+125, 108-35])
        else:
            screen.blit(pause, [537+125, 108-35])
        pygame.draw.rect(screen, (210, 4, 45), rect_cancel, border_radius=12)
        pygame.draw.rect(screen, (0,0,0), rect_cancel,4, border_radius=12)
        b = font3.render("Cancel",True,cancel_color) #NAME
        screen.blit(b, [638+125, 107-35, 180, 50])
        pygame.draw.rect(screen, (44, 42, 49), [220-126, 285-60, 560+250, 280+70+25], border_radius=20)
        pygame.draw.rect(screen, (0, 0, 0), [220-125, 285-60, 560+250, 280+70+25], 4, border_radius=20)
        
        screen.blit(frames[frame_num], (420, 56))
        pygame.display.update()
        frame_num = (frame_num + 1) % len(frames)
        
        
        if not page_num==4:
            if (pos[0]>rect_play_pause[0] and pos[0]<(rect_play_pause[0]+rect_play_pause[2]) and pos[1]>rect_play_pause[1] and pos[1]<(rect_play_pause[1]+rect_play_pause[3])) or (pos[0]>rect_cancel[0] and pos[0]<(rect_cancel[0]+rect_cancel[2]) and pos[1]>rect_cancel[1] and pos[1]<(rect_cancel[1]+rect_cancel[3])) or (circle_rect.collidepoint(pos)):
                set_cursor_back3 = False
                pygame.mouse.set_cursor(nw_mouse2)
            else:
                set_cursor_back3 = True

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
        pygame.draw.rect(screen, (0, 0, 0), rects['d_resource_rect'], 4)
        if download_resources_enabled:
            screen.blit(tick, (650, 186))
        resources = font5.render("Download CORS Resources", True, (255,255,255))
        screen.blit(resources, (270, 250))
        pygame.draw.rect(screen, (0, 0, 0), rects['d_c_resource_rect'], 4)
        if download_cors_resources_enabled:
            screen.blit(tick, (650, 241))
        resources = font5.render("Same Origin Crawl Limit", True, (255,255,255))
        screen.blit(resources, (270, 300))
        screen.blit(left, rects['left_socl'])
        num = font5.render(str(same_origin_crawl_limit), True , (255, 255, 255))
        screen.blit(num, (657, 297))
        screen.blit(right, rects['right_socl'])
        # pygame.draw.rect(screen, (0, 0, 0), [650, 295, 30, 30], 4)
        resources = font5.render("Refetch", True, (255,255,255))
        screen.blit(resources, (270, 350))
        pygame.draw.rect(screen, (0, 0, 0), rects['refetch_rect'], 4)
        if refetch_enabled:
            screen.blit(tick, (650, 341))
        
        
        pygame.draw.line(screen, (0,0,0), (250, 395), (748, 395),4)
        resources = font5.render("Cross-Origin Sites", True, (255,255,255))
        screen.blit(resources, (270, 410))
        pygame.draw.rect(screen, (0, 0, 0), rects['cors_rect'], 4)
        if cors_enabled:
            screen.blit(tick, (650, 401))
        pygame.draw.line(screen, (0,0,0),(250, 453), (748, 453), 4)
        
        
        resources = font6.render("Resources", True, (255, 255, 255))
        aboi = pygame.Surface((25, 25))
        aboi.fill((47, 21, 68))
        resources2 = font6.render("Max Cors", True, (255, 255, 255))
        pygame.draw.rect(aboi, (0, 0, 0), [0, 0, 25, 25], 4)
        num = font5.render(str(Max_cors), True , (192, 192, 192))
            
        if cors_enabled:
            screen.blit(left, rects['left_max_cors'])
            screen.blit(right, rects['right_max_cors'])
        else:
            num.set_alpha(50)
            aboi.set_alpha(130)
            resources.set_alpha(50)
            resources2.set_alpha(50)
            screen.blit(left2, (565, 474, 30, 30))
            screen.blit(right2, (630, 473, 30, 30))
            
        screen.blit(num, (602, 471))
        screen.blit(resources, (335, 474))
        screen.blit(resources2, (485, 474))
        screen.blit(aboi, (435, 472))
        
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
            if rects[ji].collidepoint(pos):
                set_cursor_back4 = False
                pygame.mouse.set_cursor(nw_mouse2)
            
        if set_cursor_back4:
            pygame.mouse.set_cursor(nw_mouse)


    for event in events:
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not page_num==4:
                if rect2.collidepoint(event.pos) and page_num == 1 and not pressed:
                    pressed = True
                    rect4.y += 1
                    loading_allow = True
                    display_err = False
                    display_err_msg = ""
                    pygame.time.set_timer(STARTED, 3000)
                if rectangle1.collidepoint(event.pos) and page_num == 1:
                    pressed_downloads = True
                    rectangle1.y += 5
                    rectangle2.y += 5
                    pygame.time.set_timer(DOWNLOADS_PRESSED, 200)
                if rectji.collidepoint(event.pos) and page_num == 2:
                    time.sleep(0.25)
                    page_num = 1

                if page_num == 2 and launch_press_allow:
                    for j in alist:
                        i = j[0]
                        if event.pos[0]>i[0]+685 and event.pos[0]<i[0]+865 and event.pos[1]>i[1]+14 and event.pos[1]<i[1]+64:
                            j[2][2] = True
                            launch_press_allow = False

                if page_num == 3 and rect_play_pause.collidepoint(event.pos):
                    paused = not paused

                if page_num == 3 and rect_cancel.collidepoint(event.pos):
                    if not canceled:
                        canceled = True
                        cancel_color = (0,0,0)
                        pygame.time.set_timer(CANCEL_PRESSED, 100)

                if page_num == 3 and circle_rect.collidepoint(event.pos):
                    page_num = 1
                    
                    
            else:
                if circle_rect.collidepoint(event.pos):
                    page_num = 1
                    
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
                            if task_running == None:
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
                                    "logs": []
                                })
                                website_being_downloaded = temp_website
                                currently_settings = {
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
                                    "logs": []
                                }
                                page_num = 3
                                task_running = website.StoppableThread(target=temp_website.download)
                                task_running.start()
                
        if event.type == CANCEL_PRESSED and not page_num == 4:
            cancel_color = (255, 255, 255)     
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and page_num == 1:
            pressed = True
            rect4.y += 1
            loading_allow = True
            display_err = False
            display_err_msg = ""
            checking = website.StoppableThread(target=check_if_website_correct)
            checking.start()
            pygame.time.set_timer(STARTED, 3000)
                
        if event.type == pygame.MOUSEWHEEL:
            if event.y<0 and alist[-1][0][1]>400:
                for i in range(len(alist)):
                    alist[i][0][1] -= 50
                    alist[i][2][4][1] -= 50
            elif event.y>=0 and alist[0][0][1]<100:
                for i in range(len(alist)):
                    alist[i][0][1] += 50
                    alist[i][2][4][1] += 50
                
        if event.type == STARTED and pressed and not page_num==4:
            display_err = False
            rect4.y -= 1
            valid = None
            checking = website.StoppableThread(target=check_if_website_correct)
            checking.start()
            pygame.mouse.set_cursor(nw_mouse)
        if event.type == DOWNLOADS_PRESSED and pressed_downloads and page_num == 1 and not page_num==4:
            rectangle1.y -= 5
            rectangle2.y -= 5
            pressed_downloads = False
            change_page = True
            

    pygame.display.update()
    clock.tick(40)