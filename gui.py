import pygame_textinput
from PIL import Image
import pygame
import time
import cv2

pygame.init()

font = pygame.font.Font("assets/VarelaRound-Regular.ttf", 24)
font2 = pygame.font.Font("assets/LuckiestGuy-Regular.ttf", 30)
font3 = pygame.font.Font("assets/FiraSans-Bold.ttf", 30)

# Create TextInput-object
manager = pygame_textinput.TextInputManager(validator=lambda input: len(input) <= 35)
textinput = pygame_textinput.TextInputVisualizer(manager=manager, font_object=font)

textinput.font_color = (255, 255, 255)

screen = pygame.display.set_mode((1000, 667))
clock = pygame.time.Clock()

logo = pygame.image.load("assets/spider_logo_main.png")
logo3 = pygame.transform.scale(logo, (96, 96))
logo2 = pygame.transform.scale(logo, (64,64))
pygame.display.set_icon(logo)
pygame.display.set_caption("Webber")

aleft = pygame.image.load("assets/arrow_left.svg")


img = pygame.image.load("assets/bgimg.png")
# img.set_alpha(10)
btn_img = pygame.image.load("assets/w_button_ji.png")
btn_img_clicked = pygame.image.load("assets/w_button_ji_animated.png")
spider_img = pygame.image.load("assets/spider.png")
spider_hanging_img = pygame.image.load("assets/hanging_spider.png")
rocket = pygame.image.load("assets/rocket_icon.png")
exclamation = pygame.image.load("assets/exclamation.png")
delete = pygame.image.load("assets/delete.png")
pause = pygame.image.load("assets/pause.png")
play = pygame.image.load("assets/play.png")
cancel = pygame.image.load("assets/cancel.png")


btn_img = pygame.transform.scale(btn_img, (314, 74))
btn_img_clicked = pygame.transform.scale(btn_img_clicked, (314, 74))
spider_img = pygame.transform.scale(spider_img, (254, 186))
spider_hanging_img = pygame.transform.scale(spider_hanging_img, (313, 267))
# rocket = pygame.transform.scale(rocket, (39, 39))
exclamation = pygame.transform.scale(exclamation, (32, 35))
delete = pygame.transform.scale(delete, (35, 35))
pause = pygame.transform.scale(pause, (35, 35))
play = pygame.transform.scale(play, (35, 35))
cancel = pygame.transform.scale(cancel, (30, 30))


rect = img.get_rect()
rect2 = btn_img.get_rect()
rect3 = btn_img.get_rect()
# print(rect)
rect2.x = 465
rect2.y = 340
rect3.x = 465
rect3.y = 340
screen.fill((225, 225, 225))

pygame.key.set_repeat(200, 25)
pressed = False
STARTED = pygame.USEREVENT

hover_downloads = False
DOWNLOADS_HOVER = pygame.USEREVENT
pressed_downloads = False
DOWNLOADS_PRESSED = pygame.USEREVENT
CANCEL_PRESSED = pygame.USEREVENT

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
rect5.x += 200
rect5.y += 60
rect5.w = 254
rect5.h = 186

rect6 = rect2.copy()
rect6.x = 0
rect6.y = 0
rect6.w = 313
rect6.h = 267
page_num = 1

rectangle1 = pygame.Rect(780, 20, 200, 50)
rectangle2 = pygame.Rect(815, 30, 200, 50)

rectji = pygame.Rect(10, 10, 200, 50)
rectji2 = pygame.Rect(15, 15, 50, 40)
rectji3 = pygame.Rect(30, 25, 40, 40)

gif = Image.open("assets/spiderrr.gif")
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

something_done = True
change_page = False
do = True
launch_text = True
launch_press_allow = True

# rect, launch text, rocket img, rotation, launched?, animation_complete?, (i[0]+700, i[1]+18,39, 39)
alist = [[[50,100,900,200], True, [rocket.copy(), 0, False, False,[753, 122,39, 39]], True, [], True, []], [[50,350,900,200], True, [rocket.copy(), 0, False, False,[753, 372,39, 39]], True, [], True, []], [[50,600,900,200], True, [rocket.copy(), 0, False, False,[753, 622,39, 39]], True, [], True, []]]

frame_num = 0

set_cursor_back3 = True
paused = False
canceled = False
rect_play_pause = pygame.Rect(530, 100, 50, 50)
cancel_color = (255, 255, 255)
rect_cancel = pygame.Rect(600, 100, 180, 50)
circle_rect = pygame.draw.circle(screen, (30, 28, 34), (795, 83), 28)

while True:
    events = pygame.event.get()
    screen.fill((255, 255, 255))
    screen.blit(img, rect)
    pos = pygame.mouse.get_pos()
    if page_num == 1:
        textinput.update(events)
        pygame.draw.rect(screen, (30, 28, 34), [200, 233, 600, 200], border_radius=20)
        pygame.draw.rect(screen, (0, 0, 0), [200, 233, 600, 200], 8, border_radius=20)
        pygame.draw.rect(screen, (44, 42, 49), [220, 253, 560, 80], border_radius=20)
        pygame.draw.rect(screen, (0, 0, 0), [220, 253, 560, 80], 8, border_radius=20)
        
        
        pygame.draw.rect(screen, (0, 0, 0), [780, 49, 200, 25], border_radius=12)
        pygame.draw.rect(screen, (232, 232, 232), rectangle1 , border_radius=12)
        pygame.draw.rect(screen, (30, 28, 34), rectangle1, 3, border_radius=12)
        downloads = font.render("Downloads", True, (0,0,0))
        screen.blit(downloads, rectangle2)
        # pygame.draw.rect(screen, (0, 0, 0), [455, 340, 320, 80], 8, border_radius=20)
        some_text = font2.render("CRAWL & DOWNLOAD", True, (255, 191, 0))
        screen.blit(textinput.surface, (250,281))
        if not pressed:
            screen.blit(btn_img, rect2)
        else:
            screen.blit(btn_img_clicked, rect3)
        screen.blit(some_text, rect4)
        screen.blit(spider_img, rect5)
        screen.blit(spider_hanging_img, rect6)
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
            a = font3.render("Summer of Making",True,(255, 255, 255)) #NAME
            screen.blit(a, (i[0]+33, i[1]+26,i[2],i[3]))
            
            pygame.draw.line(screen, (0,0,0), (i[0]+30, i[1]+70), (i[0]+i[2]-30, i[1]+70),6) #LINE SEPARATION
            
            b = font.render("https://summer.hackclub.com",True,(255, 255, 255)) #URL
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
                j[2][4][0] += 20
                if j[2][4][0]>i[0]+180+665:
                    j[2][3] = True
                    
        
        pygame.draw.rect(screen, (232, 232, 232), rectji , border_radius=12)
        back = font.render("Go Back", True, (0,0,0))
        if do:
            screen.blit(back, (85, 20, 200, 50))
        pygame.draw.rect(screen, (157,0,255), rectji2 , border_radius=12)
        screen.blit(aleft, rectji3)
        
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
        pygame.draw.rect(screen, (30, 28, 34), [200, 83, 600, 500], border_radius=20)
        pygame.draw.rect(screen, (0, 0, 0), [200, 83, 600, 500], 8, border_radius=20)
        
        a = font3.render("Summer of Making",True,(255, 255, 255)) #NAME
        screen.blit(a, [225, 110, 600, 500])
        
        pygame.draw.rect(screen, (255, 215, 0), rect_play_pause, border_radius=12)
        pygame.draw.rect(screen, (0,0,0), rect_play_pause,4, border_radius=12)
        if paused:
            screen.blit(play, [537, 108])
        else:
            screen.blit(pause, [537, 108])
            
        pygame.draw.rect(screen, (210, 4, 45), rect_cancel, border_radius=12)
        pygame.draw.rect(screen, (0,0,0), rect_cancel,4, border_radius=12)
        
        b = font3.render("Cancel",True,cancel_color) #NAME
        screen.blit(b, [638, 107, 180, 50])
        
        pygame.draw.rect(screen, (44, 42, 49), [220, 285, 560, 280], border_radius=20)
        pygame.draw.rect(screen, (0, 0, 0), [220, 285, 560, 280], 4, border_radius=20)
        
        circle_rect = pygame.draw.circle(screen, (30, 28, 34), (795, 83), 28)
        pygame.draw.circle(screen, (0, 0, 0), (795, 83), 28, 5)
        screen.blit(cancel, (780, 68))
        
        screen.blit(frames[frame_num], (420, 198))
        pygame.display.update()
        frame_num = (frame_num + 1) % len(frames)
        
        
        if (pos[0]>600 and pos[0]<780 and pos[1]>100 and pos[1]<150) or (pos[0]>530 and pos[0]<580 and pos[1]>100 and pos[1]<150) or (circle_rect.collidepoint(pos)):
            set_cursor_back3 = False
            pygame.mouse.set_cursor(nw_mouse2)
        else:
            set_cursor_back3 = True
            
        if set_cursor_back3:
            pygame.mouse.set_cursor(nw_mouse)

    for event in events:
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect2.collidepoint(event.pos) and page_num == 1:
                pressed = True
                rect4.y += 1
                pygame.time.set_timer(STARTED, 300)
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
                
        if event.type == CANCEL_PRESSED:
            cancel_color = (255, 255, 255)        
                
        if event.type == pygame.MOUSEWHEEL:
            if event.y<0 and alist[-1][0][1]>400:
                for i in range(len(alist)):
                    alist[i][0][1] -= 50
                    alist[i][2][4][1] -= 50
            elif event.y>=0 and alist[0][0][1]<100:
                for i in range(len(alist)):
                    alist[i][0][1] += 50
                    alist[i][2][4][1] += 50
                
        if event.type == STARTED and pressed and page_num == 1:
            rect4.y -= 1
            pressed = False
            page_num = 3
        if event.type == DOWNLOADS_PRESSED and pressed_downloads and page_num == 1:
            rectangle1.y -= 5
            rectangle2.y -= 5
            pressed_downloads = False
            change_page = True

    pygame.display.update()
    clock.tick(30)