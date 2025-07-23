import pygame_textinput
import pygame
import time
pygame.init()

font = pygame.font.Font("assets/VarelaRound-Regular.ttf", 24)
font2 = pygame.font.Font("assets/LuckiestGuy-Regular.ttf", 30)

# Create TextInput-object
manager = pygame_textinput.TextInputManager(validator=lambda input: len(input) <= 35)
textinput = pygame_textinput.TextInputVisualizer(manager=manager, font_object=font)

textinput.font_color = (255, 255, 255)

screen = pygame.display.set_mode((1000, 667))
clock = pygame.time.Clock()

logo = pygame.image.load("assets/spider_logo_main.png")
logo3 = pygame.transform.scale(logo, (96, 96))
logo2 = pygame.transform.scale(logo, (64,64))
pygame.display.set_icon(logo2)
pygame.display.set_caption("Webber")

aleft = pygame.image.load("assets/arrow_left.svg")


img = pygame.image.load("assets/bgimg.png")
# img.set_alpha(10)
btn_img = pygame.image.load("assets/w_button_ji.png")
btn_img_clicked = pygame.image.load("assets/w_button_ji_animated.png")
spider_img = pygame.image.load("assets/spider.png")
spider_hanging_img = pygame.image.load("assets/hanging_spider.png")

btn_img = pygame.transform.scale(btn_img, (314, 74))
btn_img_clicked = pygame.transform.scale(btn_img_clicked, (314, 74))
spider_img = pygame.transform.scale(spider_img, (254, 186))
spider_hanging_img = pygame.transform.scale(spider_hanging_img, (313, 267))

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


something_done = True
change_page = False
do = True

alist = [[50,100,900,200], [50,350,900,200], [50,600,900,200]]

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
        for i in alist:
            pygame.draw.rect(screen, (26, 26, 26), i, border_radius=12)
            pygame.draw.rect(screen, (0, 0, 0), i, 8, border_radius=12)
            screen.blit(logo3, (i[0]+840,i[1]+140,96,96))
            a = font.render("Summer of Making",True,(188, 186, 255))
            screen.blit(a, (i[0]+30, i[1]+30,i[2],i[3]))
            pygame.draw.line(screen, (0,0,0), (i[0]+30, i[1]+70), (i[0]+i[2]-30, i[1]+70),6)
        
        pygame.draw.rect(screen, (232, 232, 232), rectji , border_radius=12)
        back = font.render("Go Back", True, (0,0,0))
        if do:
            screen.blit(back, (85, 20, 200, 50))
        pygame.draw.rect(screen, (74, 222, 128), rectji2 , border_radius=12)
        screen.blit(aleft, rectji3)
        
        if rectji.collidepoint(pos):
            pygame.mouse.set_cursor(nw_mouse2)
            do = False
            if rectji2.w<=180:
                rectji2.w += 10
            if rectji3.x<=80:
                rectji3.x += 10
        else:
            pygame.mouse.set_cursor(nw_mouse)
            do = True
            if rectji2.w>=50:
                rectji2.w -= 10
            if rectji3.x>=30:
                rectji3.x -= 10
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
        if event.type == pygame.MOUSEWHEEL:
            if event.y<0 and alist[-1][1]>400:
                for i in range(len(alist)):
                    alist[i] = (alist[i][0], alist[i][1]-30, alist[i][2], alist[i][3])
                for i in alist:
                    i = (i[0],i[1]-2,i[2],i[3])
            elif event.y>=0 and alist[0][1]<100:
                for i in range(len(alist)):
                    alist[i] = (alist[i][0], alist[i][1]+30, alist[i][2], alist[i][3])
                for i in alist:
                    i = (i[0],i[1]-2,i[2],i[3])
                
        if event.type == STARTED and pressed and page_num == 1:
            rect4.y -= 1
            pressed = False
        if event.type == DOWNLOADS_PRESSED and pressed_downloads and page_num == 1:
            rectangle1.y -= 5
            rectangle2.y -= 5
            pressed_downloads = False
            change_page = True

    pygame.display.update()
    clock.tick(30)