import requests
import pandas as pd
import json 
import pygame
import random
import os 
from bs4 import BeautifulSoup
import time
from pygame.locals import *

#參數數定
#畫面
WIDTH=800
HEIGHT=600
FPS=40
PLAYER_WIDTH=110
PLAYER_HEIGHT=85
SPECIAL_PLAYER_WIDTH=1.5*PLAYER_WIDTH
SPECIAL_PLAYER_HEIGHT=1.5*PLAYER_HEIGHT
DISPLAY_WIDTH=220
DISPLAY_HEIGHT=170
STUDENT_WIDTH=72
STUDENT_HEIGHT=54

#顏色
BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE=(0,0,255)
GRAY=(128,128,128)
YELLOW=(255,255,0)
GREEN=(0,255,0)
RED=(255,0,0)

#角色能力預設
WORDS=[]
player_scoring_ability=1
player_slowering_ability=1
pygame.init()
pygame.mixer.init()

#遊戲初始化(創建視窗)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("期末專題遊戲")#更改視窗名字
loading_png=pygame.image.load(os.path.join("img","loading.webp")).convert()
loading_png=pygame.transform.scale(loading_png,(WIDTH/2,HEIGHT/2))
screen.fill(WHITE)
screen.blit(loading_png,(WIDTH/4,HEIGHT/4))
pygame.display.update()

#角色圖片
spaceship1_jpeg=pygame.image.load(os.path.join("img","spaceship1.png")).convert()#就李柏宇畫的圖
spaceship1_jpeg=pygame.transform.scale(spaceship1_jpeg,(PLAYER_WIDTH,PLAYER_HEIGHT))
spaceship1_jpeg.set_colorkey(WHITE)
spaceship2_jpeg=pygame.image.load(os.path.join("img","spaceship2.png")).convert()
spaceship2_jpeg=pygame.transform.scale(spaceship2_jpeg,(PLAYER_WIDTH,PLAYER_HEIGHT))
spaceship2_jpeg.set_colorkey(WHITE)
spaceship3_jpeg=pygame.image.load(os.path.join("img","spaceship3.png")).convert()
spaceship3_jpeg=pygame.transform.scale(spaceship3_jpeg,(PLAYER_WIDTH,PLAYER_HEIGHT))
spaceship3_jpeg.set_colorkey(WHITE)
spaceship_jpeg=spaceship1_jpeg

enemy1_jpeg=pygame.image.load(os.path.join("img","enemy1.png")).convert()
enemy1_jpeg=pygame.transform.scale(enemy1_jpeg,(PLAYER_WIDTH,PLAYER_HEIGHT))
enemy1_jpeg.set_colorkey(WHITE)
enemy2_jpeg=pygame.image.load(os.path.join("img","enemy2.png")).convert()
enemy2_jpeg=pygame.transform.scale(enemy2_jpeg,(PLAYER_WIDTH,PLAYER_HEIGHT))
enemy2_jpeg.set_colorkey(WHITE)
enemy3_jpeg=pygame.image.load(os.path.join("img","enemy3.png")).convert()
enemy3_jpeg=pygame.transform.scale(enemy3_jpeg,(SPECIAL_PLAYER_WIDTH,SPECIAL_PLAYER_HEIGHT))
enemy3_jpeg.set_colorkey(WHITE)

#死亡圖片
wasted_png=pygame.image.load(os.path.join("img","wasted.png")).convert()
wasted_png=pygame.transform.scale(wasted_png,(WIDTH,HEIGHT))

#各式背景圖片
background_png=pygame.image.load(os.path.join("img","background.png")).convert()
background_png=pygame.transform.scale(background_png,(WIDTH,HEIGHT))
init_jpeg=pygame.image.load(os.path.join("img","init.jpg")).convert()
init_jpeg=pygame.transform.scale(init_jpeg,(WIDTH,HEIGHT))
garage_jpeg=pygame.image.load(os.path.join("img","garage.jpg")).convert()
garage_jpeg=pygame.transform.scale(garage_jpeg,(WIDTH,HEIGHT))
guideline_png=pygame.image.load(os.path.join("img","guideline.PNG")).convert()
guideline_png=pygame.transform.scale(guideline_png,(WIDTH,HEIGHT))
pause_png=pygame.image.load(os.path.join("img","pause.PNG")).convert()
pause_png=pygame.transform.scale(pause_png,(WIDTH,HEIGHT))

#爆炸特效
expl_imgs=[]
for i in range(9):
    expl_img=pygame.image.load(os.path.join("img",f"expl{i}.png")).convert()
    expl_img.set_colorkey(WHITE)
    expl_img==pygame.transform.scale(expl_img,(70,70))
    expl_imgs.append(expl_img)

#學生證
tnfsh_student_id=pygame.image.load(os.path.join("img","TNFSH_student_id.jpg")).convert()
tnfsh_student_id=pygame.transform.scale(tnfsh_student_id,(STUDENT_WIDTH,STUDENT_HEIGHT))
ntu_student_id=pygame.image.load(os.path.join("img","NTU_student_id.jpg")).convert()
ntu_student_id=pygame.transform.scale(ntu_student_id,(STUDENT_WIDTH,STUDENT_HEIGHT))

#音效調整
click_sound = pygame.mixer.Sound(os.path.join("sound", "click.mp3"))
click_sound.set_volume(0.4)
keyboard_sound=pygame.mixer.Sound(os.path.join("sound", "keyboard.mp3"))
keyboard_sound.set_volume(0.2)
explosion_sound=pygame.mixer.Sound(os.path.join("sound", "explosion.mp3"))
explosion_sound.set_volume(0.3)
init_screen_sound=pygame.mixer.Sound(os.path.join("sound", "init_screen.mp3"))
init_screen_sound.set_volume(0.4)
select_screen_sound=pygame.mixer.Sound(os.path.join("sound", "select_screen.mp3"))
select_screen_sound.set_volume(0.4)
die_screen_sound=pygame.mixer.Sound(os.path.join("sound", "die.mp3"))
die_screen_sound.set_volume(0.4)
shift_sound=pygame.mixer.Sound(os.path.join("sound", "shift.mp3"))
shift_sound.set_volume(0.2)
counter_sound=pygame.mixer.Sound(os.path.join("sound", "counter.mp3"))
counter_sound.set_volume(0.4)
pygame.mixer.music.load(os.path.join("sound", "mainscreen.mp3"))
pygame.mixer.music.set_volume(0.4)

#記錄當前畫面上單字
words_on_screen=[]
word_typed=[]

#角色特性庫
picture_lib=[spaceship1_jpeg,spaceship2_jpeg,spaceship3_jpeg]
scoring_ability=[1,2,3]
slowering_ability=[1,1,1.25]
feature=["No feature, so pathetic!","Higher scoring ability","Higher scoring ability % and rendering the text falling slower"]

#爬蟲結果已存入電腦

#得分機制
current_highest_score=0
history_highest_score=0
accumulated_score=0
history_level=1
level_scale=[]
for i in range(0,101,1):
    level_scale.append(i**2)

#combo 處理
combo_factor=1
combo_score=0
in_combo=False
combo_duration=20000
combo_score_reset=False
allow_combo_added=True
combo_starting_time=0
last_bar_color_update=0
bar_color=YELLOW


#學生證產生時間
tnfsh_id_starting_time=0
tnfsh_id_duration=51481#取質數
ntu_id_starting_time=0
ntu_id_duration=33391#取質數
bullet_number=15


#學生證庫
student_id_lib=[0,tnfsh_student_id,ntu_student_id]
student_id_discription=[0,"Refill your HP","Refill your bullets"]
id_name=[0,"Tu's TNFSH Student ID","NTU Student ID"]
#提取歷史資料
try:
    with open("game_data.txt","r") as game_data:
        content=game_data.read()
        data=eval(content)
        history_highest_score=int(data[0])
        history_level=int(data[1])
        accumulated_score=int(data[2])
        if history_highest_score>current_highest_score:
            current_highest_score=history_highest_score

except:
    pass

#選擇我要什麼單字庫
def selecting_word_bank(word):#word是單字類別 ex. math,biology
    global WORDS
    with open ("library.txt","r") as f:#單字庫存在這個檔案
        content=f.read()
        li=content.split("///\n")

    for i in li:
        if i.startswith(f"{word}"):
            k=i
        

    k=k.strip(f"{word}")
    k=k.split('%')
    #print(k)
    WORDS0=eval(k[0])#evaluate字串
    WORDS1=eval(k[1])
    WORDS2=eval(k[2])
    WORDS=WORDS0+WORDS1+WORDS2#建立好單字庫

#字體設定
font_name= pygame.font.match_font("arial")

#畫血條
def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 70
    BAR_HEIGHT = 20
    #當前血條還剩多少
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

#畫等級條
def draw_level(surf, level_gap,ac_acore, x, y):
    #print(level_gap)
    #print(ac_acore)
    BAR_LENGTH = 70
    BAR_HEIGHT = 20
    #當前血條還剩多少
    fill = (ac_acore/level_gap)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

#畫combo條
def draw_combo(surf, sc, x, y, color_decision):
    if sc < 0:
        sc = 0
    BAR_LENGTH = 70
    BAR_HEIGHT = 20
    #當前血條還剩多少
    fill = (sc/20)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    
    pygame.draw.rect(surf, color_decision, fill_rect)
    
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


#渲染字上去螢幕
def draw_text(surf, text, size, x, y, font_color=WHITE,special=False):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, font_color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)
    if special:
        return text_rect.right

#特殊渲染字體(提示單字要用)
def special_draw_text(surf, text, size, x, y, font_color=WHITE):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, font_color)
    text_rect = text_surface.get_rect()
    text_rect.left = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)
    
#等級評定
def level_criterion(exact_score):
    
    if exact_score==0:
        return 1
    for i in range(101):
        if i+1<=100:
            if level_scale[i]<=exact_score//10<level_scale[i+1]:
                return i

        else:
            return 100

#噴射尾流特效與爆炸特效(學生證)畵圓底圖
def circle_surf(radius, color):
    surf = pygame.Surface((radius , radius ))
    pygame.draw.circle(surf, color, (radius, radius), radius*0.7)
    surf.set_colorkey((0, 0, 0))
    return surf



#各種畫面設定

#起始畫面
def init_screen(current_highest_score=current_highest_score):
    global history_level,word_typed
    word=""
    init_screen_sound.play(-1)
    #螢幕著色
    #screen.fill(WHITE)
    screen.blit(init_jpeg,(0,0))
    #要寫那些字
    c_a_score=history_level**2*10
    n_a_score=(history_level+1)**2*10
    d_a_score=n_a_score-c_a_score
    a_score=accumulated_score-c_a_score
    draw_level(screen,d_a_score,a_score,700,40)
    draw_text(screen, f'Highest Score: {current_highest_score}', 20, 80, 15,WHITE)
    draw_text(screen, f'LEVEL:  {history_level}', 20, 730, 15,WHITE)
    draw_text(screen, 'English Typing and Shooting Game', 40, WIDTH/2, HEIGHT/6,WHITE)
    draw_text(screen, 'Press the designated key to enter the game', 18, WIDTH/2, HEIGHT/4,WHITE)
    draw_text(screen, 'Press G for guidelines', 26, WIDTH/2, 210,WHITE)
    draw_text(screen, 'Press S to select your player', 26, WIDTH/2, 245,WHITE)

    #選項提示
    BAR_LENGTH = 500
    BAR_HEIGHT = 50
    outline_rect = pygame.Rect(WIDTH/2, 280, BAR_LENGTH, BAR_HEIGHT)
    outline_rect.centerx=WIDTH/2
    
    #fill_rect = pygame.Rect(WIDTH/2, 280, fill, BAR_HEIGHT)
    pygame.draw.rect(screen, RED, outline_rect)
    draw_text(screen, 'To Enter Math,Press M', 26, WIDTH/2, 290,BLACK)

    outline_rect = pygame.Rect(WIDTH/2, 350, BAR_LENGTH, BAR_HEIGHT)
    outline_rect.centerx=WIDTH/2
    
    #fill_rect = pygame.Rect(WIDTH/2, 280, fill, BAR_HEIGHT)
    pygame.draw.rect(screen, RED, outline_rect)
    draw_text(screen, 'To Enter Physics,Press P', 26, WIDTH/2, 360,BLACK)

    outline_rect = pygame.Rect(WIDTH/2, 420, BAR_LENGTH, BAR_HEIGHT)
    outline_rect.centerx=WIDTH/2
    
    #fill_rect = pygame.Rect(WIDTH/2, 280, fill, BAR_HEIGHT)
    pygame.draw.rect(screen, RED, outline_rect)
    draw_text(screen, 'To Enter Chemical,Press C', 26, WIDTH/2, 430,BLACK)

    outline_rect = pygame.Rect(WIDTH/2, 490, BAR_LENGTH, BAR_HEIGHT)
    outline_rect.centerx=WIDTH/2
    
    #fill_rect = pygame.Rect(WIDTH/2, 280, fill, BAR_HEIGHT)
    pygame.draw.rect(screen, RED, outline_rect)
    draw_text(screen, 'To Enter Biology,Press B', 26, WIDTH/2, 500,BLACK)

    pygame.display.update()#更新畫面

    #在初始畫面中等待玩家做決定
    waiting = True
    while waiting:
        clock.tick(FPS)

        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True,word
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    word="math"
                    outline_rect = pygame.Rect(WIDTH/2, 280, BAR_LENGTH, BAR_HEIGHT)
                    outline_rect.centerx=WIDTH/2
    
                    click_sound.play()
                    pygame.draw.rect(screen, YELLOW, outline_rect)
                    draw_text(screen, 'To Enter Math,Press M', 26, WIDTH/2, 290,BLACK)
                    pygame.display.update()
                    time.sleep(0.4)
                    
                    outline_rect = pygame.Rect(WIDTH/2, 280, BAR_LENGTH, BAR_HEIGHT)
                    outline_rect.centerx=WIDTH/2
    
    
                    pygame.draw.rect(screen, RED, outline_rect)
                    draw_text(screen, 'To Enter Math,Press M', 26, WIDTH/2, 290,BLACK)
                    pygame.display.update()
                    time.sleep(0.4)
                    waiting = False
                elif event.key == pygame.K_p:
                    word="physics"
                    outline_rect = pygame.Rect(WIDTH/2, 350, BAR_LENGTH, BAR_HEIGHT)
                    outline_rect.centerx=WIDTH/2
                    click_sound.play()
                    #fill_rect = pygame.Rect(WIDTH/2, 280, fill, BAR_HEIGHT)
                    pygame.draw.rect(screen, YELLOW, outline_rect)
                    draw_text(screen, 'To Enter Physics,Press P', 26, WIDTH/2, 360,BLACK)
                    pygame.display.update()
                    time.sleep(0.4)
                    outline_rect = pygame.Rect(WIDTH/2, 350, BAR_LENGTH, BAR_HEIGHT)
                    outline_rect.centerx=WIDTH/2
    
                    #fill_rect = pygame.Rect(WIDTH/2, 280, fill, BAR_HEIGHT)
                    pygame.draw.rect(screen, RED, outline_rect)
                    draw_text(screen, 'To Enter Physics,Press P', 26, WIDTH/2, 360,BLACK)
                    pygame.display.update()
                    time.sleep(0.4)
                    waiting = False
                elif event.key == pygame.K_c:
                    word="chemical"
                    outline_rect = pygame.Rect(WIDTH/2, 420, BAR_LENGTH, BAR_HEIGHT)
                    outline_rect.centerx=WIDTH/2
                    click_sound.play()
                    #fill_rect = pygame.Rect(WIDTH/2, 280, fill, BAR_HEIGHT)
                    pygame.draw.rect(screen, YELLOW, outline_rect)
                    draw_text(screen, 'To Enter Chemical,Press C', 26, WIDTH/2, 430,BLACK)
                    pygame.display.update()
                    time.sleep(0.4)
                    outline_rect = pygame.Rect(WIDTH/2, 420, BAR_LENGTH, BAR_HEIGHT)
                    outline_rect.centerx=WIDTH/2
    
                    #fill_rect = pygame.Rect(WIDTH/2, 280, fill, BAR_HEIGHT)
                    pygame.draw.rect(screen, RED, outline_rect)
                    draw_text(screen, 'To Enter Chemical,Press C', 26, WIDTH/2, 430,BLACK)
                    pygame.display.update()
                    time.sleep(0.4)
                    waiting = False
                elif event.key == pygame.K_b:
                    word="biology"
                    outline_rect = pygame.Rect(WIDTH/2, 490, BAR_LENGTH, BAR_HEIGHT)
                    outline_rect.centerx=WIDTH/2
                    click_sound.play()
                    #fill_rect = pygame.Rect(WIDTH/2, 280, fill, BAR_HEIGHT)
                    pygame.draw.rect(screen, YELLOW, outline_rect)
                    draw_text(screen, 'To Enter Biology,Press B', 26, WIDTH/2, 500,BLACK)
                    pygame.display.update()
                    time.sleep(0.4)
                    outline_rect = pygame.Rect(WIDTH/2, 490, BAR_LENGTH, BAR_HEIGHT)
                    outline_rect.centerx=WIDTH/2
    
                    #fill_rect = pygame.Rect(WIDTH/2, 280, fill, BAR_HEIGHT)
                    pygame.draw.rect(screen, RED, outline_rect)
                    draw_text(screen, 'To Enter Biology,Press B', 26, WIDTH/2, 500,BLACK)
                    pygame.display.update()
                    time.sleep(0.4)
                    waiting = False

                #玩家想看說明書
                elif event.key == pygame.K_g:
                    word="guidelines"
                    waiting = False


                #玩家想選角色
                elif event.key == pygame.K_s:
                    word="select"
                    waiting = False

                #玩家還沒想好
                else:
                    waiting = True
                
    init_screen_sound.fadeout(500)
    time.sleep(0.5)
    word_typed=[]
    return False,word


#說明畫面
def guideline_screen():
    selection=0
    screen.blit(guideline_png,(0,0))
    draw_text(screen, 'To hit the word, you should type in the corresponding text as shown', 26, WIDTH/2, HEIGHT/3,WHITE)
    draw_text(screen, 'Word bank is given according to the keyboard you pressed,i.e. B,C', 26, WIDTH/2, 300,WHITE)
    draw_text(screen, 'While in the game, press ESC to return to home or press PAGE UP to pause', 26, WIDTH/2, 350,WHITE)
    draw_text(screen, 'To submit your word, press ENTER', 26, WIDTH/2, 400,WHITE)

    draw_text(screen, 'Press B to go back to home or resume your game', 26, WIDTH/2, 450,WHITE)
    draw_text(screen, 'Press LEFT/RIGHT to switch', 26, WIDTH/2, 527,WHITE)
    pygame.display.update()
    waiting = True
    word=""
    TEXT_DISPLAY_X=490
    PIC_WIDTH=320
    PIC_HEIGHT=240
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True,word
            elif event.type == pygame.KEYDOWN:
                #返回初始畫面
                if event.key == pygame.K_b:
                    word="back"
                    waiting = False
                elif event.key == pygame.K_RIGHT:
                    if selection+1<=2:
                        screen.blit(guideline_png,(0,0))
                        shift_sound.play()
                        selection+=1
                        id=student_id_lib[selection]
                        id=pygame.transform.scale(id,(PIC_WIDTH,PIC_HEIGHT))
                        screen.blit(id,(80,200))
                        draw_text(screen, id_name[selection], 30, TEXT_DISPLAY_X+50, 205,YELLOW)
                        draw_text(screen, "Function:", 26, TEXT_DISPLAY_X, 305,WHITE)
                        draw_text(screen, student_id_discription[selection], 26, TEXT_DISPLAY_X, 335,WHITE)
                        draw_text(screen, 'Press B to go back to home or resume your game', 26, WIDTH/2, 450,WHITE)
                        draw_text(screen, 'Press LEFT/RIGHT to switch', 26, WIDTH/2, 527,WHITE)
                        pygame.display.update()
                    waiting=True
                elif event.key == pygame.K_LEFT:
                    if selection-1>=0:
                        shift_sound.play()
                        selection-=1

                        if selection==0:
                            screen.blit(guideline_png,(0,0))
                            draw_text(screen, 'To hit the word, you should type in the corresponding text as shown', 26, WIDTH/2, HEIGHT/3,WHITE)
                            draw_text(screen, 'Word bank is given according to the keyboard you pressed,i.e. B,C', 26, WIDTH/2, 300,WHITE)
                            draw_text(screen, 'While in the game, press ESC to return to home or press PAGE UP to pause', 26, WIDTH/2, 350,WHITE)
                            draw_text(screen, 'To submit your word, press ENTER', 26, WIDTH/2, 400,WHITE)

                            draw_text(screen, 'Press B to go back to home or resume your game', 26, WIDTH/2, 450,WHITE)
                            draw_text(screen, 'Press LEFT/RIGHT to switch', 26, WIDTH/2, 527,WHITE)
                            pygame.display.update()

                        else:
                            id=student_id_lib[selection]
                            id=pygame.transform.scale(id,(PIC_WIDTH,PIC_HEIGHT))
                            screen.blit(guideline_png,(0,0))
                            screen.blit(id,(80,200))
                            draw_text(screen, id_name[selection], 30, TEXT_DISPLAY_X+50, 205,YELLOW)
                            draw_text(screen, "Function:", 26, TEXT_DISPLAY_X, 305,WHITE)
                            draw_text(screen, student_id_discription[selection], 26, TEXT_DISPLAY_X, 335,WHITE)
                            draw_text(screen, 'Press B to go back to home or resume your game', 26, WIDTH/2, 450,WHITE)
                            draw_text(screen, 'Press LEFT/RIGHT to switch', 26, WIDTH/2, 527,WHITE)
                            pygame.display.update()
                    waiting=True

    return False,word


#暫停畫面
def pause_screen():
    
    screen.blit(pause_png,(0,0))

    draw_text(screen, 'LEAVE,press H', 26, WIDTH/2, HEIGHT/3,WHITE)
    draw_text(screen, 'Resume, press R', 26, WIDTH/2, 300,WHITE)
    draw_text(screen, 'Guideline, press G', 26, WIDTH/2, 400,WHITE)

    pygame.display.update()
    waiting = True
    word=""
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True,word
            elif event.type == pygame.KEYDOWN:
                #玩家想回首頁
                if event.key == pygame.K_h:
                    word="home"
                    waiting = False

                #繼續遊戲
                elif event.key == pygame.K_r:
                    word="resume"
                    waiting=False

                #看說明
                elif event.key == pygame.K_g:
                    
                    word="guidelines"
                    waiting=False

    return False,word

#暫停緩衝畫面
def pause_waiting_screen():
    word=""
    screen.blit(background_png,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return True,word 

    #倒數計時
    draw_text(screen, '3', 40, WIDTH/2, HEIGHT/2-20,WHITE)
    
    pygame.display.update()
    counter_sound.play()
    time.sleep(1)
    screen.blit(background_png,(0,0))
    draw_text(screen, '2', 40, WIDTH/2, HEIGHT/2-20,WHITE)
    
    pygame.display.update()
    counter_sound.play()
    time.sleep(1)
    screen.blit(background_png,(0,0))
    draw_text(screen, '1', 40, WIDTH/2, HEIGHT/2-20,WHITE)

    
    pygame.display.update()
    counter_sound.play()
    time.sleep(1)
    word="done"


    return False,word

#死亡畫面
def die_screen(score):
    global history_level,accumulated_score
    word=""
    accumulated_score+=score
    die_screen_sound.play()
    history_level=level_criterion(accumulated_score)
    #自動存入高分紀錄
    if score>history_highest_score:
        with open("game_data.txt","w") as game_data:
            game_data.write(f"[{str(score)},{str(history_level)},{str(accumulated_score)}]")

    else:
        with open("game_data.txt","w") as game_data:
            game_data.write(f"[{str(history_highest_score)},{str(history_level)},{str(accumulated_score)}]")

    screen.blit(wasted_png,(0,0))

    draw_text(screen, f'Your Score: {score}', 26, WIDTH/2, 400,WHITE)
    draw_text(screen, 'Return to Home,press H', 26, WIDTH/2, 500,WHITE)
    
    pygame.display.update()
    time.sleep(1)
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True,word
            elif event.type == pygame.KEYDOWN:

                #回初始畫面
                if event.key == pygame.K_h:
                    word="home"
                    waiting = False


    die_screen_sound.stop()
    return False,word

#角色選擇畫面
def select_screen():
    global spaceship_jpeg,feature
    select_screen_sound.play(-1)
    #預設角色能力
    sc_a=1
    sl_a=1
    word=""
    #預設為第一個角色
    selection=0
    screen.blit(garage_jpeg,(0,0))
    TEXT_DISPLAY_X=470
    TEXT_DISPLAY_Y=305
    draw_text(screen, 'Choose your player', 26, WIDTH/2, 100,WHITE)
    draw_text(screen, 'Press LEFT or RIGHT to select player', 26, WIDTH/2, 150,WHITE)
    draw_text(screen, 'Press S to confirm your selection', 26, WIDTH/2, 500,BLACK)
    draw_text(screen, 'Feature:', 26, TEXT_DISPLAY_X, TEXT_DISPLAY_Y,BLACK)
    draw_text(screen, feature[selection], 26, TEXT_DISPLAY_X, 335,BLACK)

    #角色圖片
    spaceship=picture_lib[selection]
    spaceship=pygame.transform.scale(spaceship,(DISPLAY_WIDTH,DISPLAY_HEIGHT))
    screen.blit(spaceship,(180,300))

    #繪製角色能力條
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    BAR_DISPLAY_X=440
    BAR_DISPLAY_Y=410
    sc_a_bar = sc_a*BAR_LENGTH
    sl_a_bar = sl_a*BAR_LENGTH
    sc_a_rect = pygame.Rect(BAR_DISPLAY_X, BAR_DISPLAY_Y, sc_a_bar, BAR_HEIGHT)
    sl_a_rect = pygame.Rect(BAR_DISPLAY_X, BAR_DISPLAY_Y+30, sl_a_bar, BAR_HEIGHT)
    pygame.draw.rect(screen, RED, sc_a_rect)
    pygame.draw.rect(screen, RED, sl_a_rect)
    draw_text(screen, 'Scoring', 18, 390, 400,BLACK)
    draw_text(screen, 'Slowering', 18, 400, 430,BLACK)
    pygame.display.update()
    spaceship=pygame.transform.scale(spaceship,(PLAYER_WIDTH,PLAYER_HEIGHT))
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True,word
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if selection+1<=2:
                        shift_sound.play()
                        #玩家切換角色
                        screen.blit(garage_jpeg,(0,0))
                        selection+=1
                        spaceship=picture_lib[selection]
                        draw_text(screen, 'Choose your player', 26, WIDTH/2, 100,WHITE)
                        draw_text(screen, 'Press LEFT or RIGHT to select player', 26, WIDTH/2, 150,WHITE)
                        draw_text(screen, 'Press S to confirm your selection', 26, WIDTH/2, 500,BLACK)
                        draw_text(screen, 'Feature:', 26, TEXT_DISPLAY_X, TEXT_DISPLAY_Y,BLACK)

                        #角色特性切換
                        if selection==2:
                            f=feature[selection].split("%")
                            draw_text(screen, f[0], 26, TEXT_DISPLAY_X, 335,BLACK)
                            draw_text(screen, f[1], 26, TEXT_DISPLAY_X+70, 365,BLACK)
                        else:
                            draw_text(screen, feature[selection], 26, TEXT_DISPLAY_X, 335,BLACK)

                        #先把角色圖片放大給玩家看
                        spaceship=pygame.transform.scale(spaceship,(DISPLAY_WIDTH,DISPLAY_HEIGHT))
                        screen.blit(spaceship,(180,300))
                        draw_text(screen, 'Scoring', 18, 390, 400,BLACK)
                        draw_text(screen, 'Slowering', 18, 400, 430,BLACK)
                        sc_a=scoring_ability[selection]
                        sl_a=slowering_ability[selection]
                        
                        spaceship_jpeg=spaceship
                        #能力條繪製
                        BAR_LENGTH = 100
                        BAR_HEIGHT = 10
                        sc_a_bar = sc_a*BAR_LENGTH
                        sl_a_bar = sl_a*BAR_LENGTH
                        sc_a_rect = pygame.Rect(BAR_DISPLAY_X, BAR_DISPLAY_Y, sc_a_bar, BAR_HEIGHT)
                        sl_a_rect = pygame.Rect(BAR_DISPLAY_X, BAR_DISPLAY_Y+30, sl_a_bar, BAR_HEIGHT)
                        pygame.draw.rect(screen, RED, sc_a_rect)
                        pygame.draw.rect(screen, RED, sl_a_rect)
                        pygame.display.update()

                        #調回正常角色圖片大小，不然等下遊戲中角色圖片會太大
                        spaceship=pygame.transform.scale(spaceship,(PLAYER_WIDTH,PLAYER_HEIGHT))
                    
                        waiting=True
                elif event.key == pygame.K_LEFT:
                    if selection-1>=0:
                        #玩家切換角色
                        shift_sound.play()
                        screen.blit(garage_jpeg,(0,0))
                        selection-=1
                        spaceship=picture_lib[selection]
                        draw_text(screen, 'Choose your player', 26, WIDTH/2, 100,WHITE)
                        draw_text(screen, 'Press LEFT or RIGHT to select player', 26, WIDTH/2, 150,WHITE)
                        draw_text(screen, 'Press S to confirm your selection', 26, WIDTH/2, 500,BLACK)
                        draw_text(screen, 'Feature:', 26, TEXT_DISPLAY_X, TEXT_DISPLAY_Y,BLACK)

                        #角色特性切換
                        if selection==2:
                            f=feature[selection].split("%")
                            draw_text(screen, f[0], 26, TEXT_DISPLAY_X, 335,BLACK)
                            draw_text(screen, f[1], 26, TEXT_DISPLAY_X+70, 365,BLACK)
                        else:
                            draw_text(screen, feature[selection], 26, TEXT_DISPLAY_X, 335,BLACK)

                        #先把角色圖片放大給玩家看
                        spaceship=pygame.transform.scale(spaceship,(DISPLAY_WIDTH,DISPLAY_HEIGHT))
                        screen.blit(spaceship,(180,300))
                        sc_a=scoring_ability[selection]
                        sl_a=slowering_ability[selection]
                        draw_text(screen, 'Scoring', 18, 390, 400,BLACK)
                        draw_text(screen, 'Slowering', 18, 400, 430,BLACK)
                        spaceship_jpeg=spaceship

                        #能力條繪製
                        BAR_LENGTH = 100
                        BAR_HEIGHT = 10
                        sc_a_bar = sc_a*BAR_LENGTH
                        sl_a_bar = sl_a*BAR_LENGTH
                        sc_a_rect = pygame.Rect(BAR_DISPLAY_X, BAR_DISPLAY_Y, sc_a_bar, BAR_HEIGHT)
                        sl_a_rect = pygame.Rect(BAR_DISPLAY_X, BAR_DISPLAY_Y+30, sl_a_bar, BAR_HEIGHT)
                        pygame.draw.rect(screen, RED, sc_a_rect)
                        pygame.draw.rect(screen, RED, sl_a_rect)
                        pygame.display.update()
                        #調回正常角色圖片大小，不然等下遊戲中角色圖片會太大
                        spaceship=pygame.transform.scale(spaceship,(PLAYER_WIDTH,PLAYER_HEIGHT))

                        waiting=True
                elif event.key == pygame.K_s:
                    #玩家選好角色了
                    word="selected"
                    waiting=False
    select_screen_sound.fadeout(500)
    time.sleep(0.5)
    return False,word,sc_a,sl_a




#sprite

#玩家
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(spaceship_jpeg,(PLAYER_WIDTH,PLAYER_HEIGHT))#pygame.Surface((50,40))
        self.image.set_colorkey(WHITE)

        self.rect=self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
        self.health=100

    def update(self):
        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_RIGHT]:#按右鍵以移動發射器
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:#按左鍵以移動發射器
            self.rect.x -= self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


trail_occupied=[]#避免字重疊，單字佔有位置列表
#單字
class Meteorite(pygame.sprite.Sprite):

    def __init__(self,Firsttime=False,t=0):
        pygame.sprite.Sprite.__init__(self)
        init_list=[0,1,2,3,4]
        my_font = pygame.font.SysFont("arial", 24)
        #print(t)

        #調整單字難度
        if t<=5:
            i = random.randrange(len(WORDS)//3)

        elif 5<t<=10:
            i = random.randrange(len(WORDS)//5,len(WORDS)*2//3)
        elif 10<t<=15:
            i = random.randrange(len(WORDS)//2,len(WORDS))

        else:
            i = random.randrange(len(WORDS)*2//3,len(WORDS))
        self.word=WORDS[i]
        self.word_length=len(WORDS[i])
        if self.word in words_on_screen:
            if t<=5:
                i = random.randrange(len(WORDS)//3)

            elif 5<t<=10:
                i = random.randrange(len(WORDS)//5,len(WORDS)*2//3)
            elif 10<t<=15:
                i = random.randrange(len(WORDS)//2,len(WORDS))

            else:
                i = random.randrange(len(WORDS)*2//3,len(WORDS))
            self.word=WORDS[i]
            self.word_length=len(WORDS[i])

        if self.word_length<=5:
            word_back_color=GRAY
        elif 5<self.word_length<=10:
            word_back_color=BLUE

        else:
            word_back_color=RED
        text_surface = my_font.render(WORDS[i], True, WHITE, word_back_color)
        
        words_on_screen.append(WORDS[i])
        self.image = text_surface
        
        self.rect=self.image.get_rect()

        #單字出現位置參數設定
        factor = random.sample(range(0 , 5),1)[0]
        if Firsttime==True:
            while factor in trail_occupied:
             
                factor = random.sample(range(0 , 5),1)[0]

        
        if factor in trail_occupied:
            for i in trail_occupied:
                init_list.remove(i)
                
            factor = random.sample(init_list,1)[0]

       
        
        trail_occupied.append(factor)
        
        self.factor=factor
        self.rect.x=factor*150+50
        self.rect.y = 0
        self.speedy = 2#random.randrange(2 , 3)
        self.speedy=self.speedy/player_slowering_ability

        
    def update(self):
        self.rect.y +=self.speedy
        if self.rect.top>HEIGHT/4.5 and self.factor in trail_occupied:#防止單字出現位置重疊
            trail_occupied.remove(self.factor)
        if self.rect.top > HEIGHT :
            player.health-=self.word_length//1.5#生命值扣減
            if self.word in words_on_screen:
                words_on_screen.remove(self.word)
            self.kill()
            '''
            factor = random.sample(range(0 , 5),1)[0]
            
            if factor in trail_occupied:
                
                factor = random.sample(range(0 , 5),1)[0]
            if factor in trail_occupied:
                
                factor = random.sample(range(0 , 5),1)[0]
            trail_occupied.append(factor)
            self.factor=factor
            self.rect.x=factor*150+50
            self.rect.y = 0
            self.speedy = random.randrange(1 , 2)
'''

#子彈
class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,20))
        self.image.fill(YELLOW)
        self.rect=self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -8

    def update(self):
        self.rect.y += self.speedy
        #if WORDS[i]=='apple':
        if self.rect.bottom < 0:
            self.kill()#角色自殺

#爆炸特效(單字)        
class Explosion(pygame.sprite.Sprite):

    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = expl_imgs[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:#允許下一幀
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_imgs):#特效播放完畢
                self.kill()
            else:
                self.image = expl_imgs[self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

#單字角色
class Enemy(pygame.sprite.Sprite):

    def __init__(self,word,x,y):
        pygame.sprite.Sprite.__init__(self)
        

        self.word=word
        self.word_length=len(word)
        #依照單字難度調整角色圖片與特性
        if self.word_length<=5:
            self.image=enemy1_jpeg
            self.rect=self.image.get_rect()
            self.rect.x=x-30
            self.rect.y = y+10
        elif 5<self.word_length<=10:
            self.image=enemy2_jpeg
            self.rect=self.image.get_rect()
            self.rect.x=x-10
            self.rect.y = y+10
        else:
            self.image=enemy3_jpeg
            self.rect=self.image.get_rect()
            self.rect.x=x-25
            self.rect.y = y+16.5

        
        
        self.speedy = 2
        self.speedy=self.speedy/player_slowering_ability

        
    def update(self):
        self.rect.y +=self.speedy
        
        if self.rect.top > HEIGHT :
            player.health-=self.word_length//4#生命值扣減
            
            if self.word in words_on_screen:
                words_on_screen.remove(self.word)
            self.kill()#

#南一中學生證
class TNFSH(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = tnfsh_student_id
        
        self.rect=self.image.get_rect()
        self.rect.x = random.sample(range(50 , WIDTH - 150),1)[0]#角色自殺
        self.rect.y = 0
        self.speedy = 4#下墜速度
        

        
    def update(self):
        self.rect.y +=self.speedy
        if self.rect.top>HEIGHT:
            self.kill()#角色自殺

#台大學生證
class NTU(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = ntu_student_id
        
        self.rect=self.image.get_rect()
        self.rect.x = random.sample(range(50 , WIDTH - 150),1)[0]#隨機產生位置
        self.rect.y = 0
        self.speedy = 4#下墜速度
        

        
    def update(self):
        self.rect.y +=self.speedy
        if self.rect.top>HEIGHT:
            self.kill()#角色自殺



#遊戲迴圈
allow_running=False#可以開始執行了，已不在初始畫面或說明畫面
show_init=True#顯示出始畫面
show_pause=False#顯示暫停
show_guideline=False#顯示說明
show_die=False#顯示死亡
show_select=False#顯示角色選擇
show_pause_waiting=False#顯示暫停緩衝
running=True#遊戲整體運行
in_game=False#遊戲中
t=0
dt=0.005
score=0
pygame.mixer.music.play()
word_bank=["math","physics","biology","chemical"]

#角色庫創建
tnfsh_ids=pygame.sprite.Group()
ntu_ids=pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
meteorites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies=pygame.sprite.Group()

#爆炸特效庫(學生證)
particles = []
particles_tnfsh = []
particles_ntu=[]
while running:
    #取得輸入
    
    get_word=""
    clock.tick(FPS)  #1秒執行最多幾次(fps)
    #如果起始畫面允許執行
    if show_init:
        bullet_number=15
        pygame.mixer.music.rewind()#音樂倒帶
        pygame.mixer.music.pause()
        in_game=False
        t=0
        dt=0.005
        score=0
        close ,word= init_screen(current_highest_score=current_highest_score)
        try:#如果是從死亡畫面回來，則須重置血量
            player.health=100
            show_die=False
            
        except:
            pass
        if word=="guidelines":#前往說明
            
            allow_running=False
            show_guideline=True
            

        elif word=="select":#前往選擇角色
            allow_running=False
            show_select=True

        if close:
            break
       
        
        #判斷訊息是否已允許遊戲進行
        if word in word_bank:
            allow_running=True
            selecting_word_bank(word)
            
            #死亡畫面回來要角色庫重建
            player = Player()
            tnfsh_ids=pygame.sprite.Group()
            ntu_ids=pygame.sprite.Group()
            all_sprites = pygame.sprite.Group()
            meteorites = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            enemies=pygame.sprite.Group()
            
            all_sprites.add(player)

            #初始單字產生
            for i in range(2):
                meteorite = Meteorite(Firsttime=True,t=t)
                xx=meteorite.rect.x
                yy=meteorite.rect.y
                wword=meteorite.word
                enemy=Enemy(wword,xx,yy)
                all_sprites.add(meteorite)
                all_sprites.add(enemy)
                meteorites.add(meteorite)
                enemies.add(enemy)

        pygame.mixer.music.unpause()
        show_init = False

    #允許說明頁面執行
    if show_guideline:
        pygame.mixer.music.pause()
        close,word=guideline_screen()
        if close:
            break
        if word=="back" and in_game==False:#原本從初始畫面進入
            close ,word= init_screen()
            show_guideline=False
            show_init = True
        elif word=="back" and in_game==True:#原本從遊戲暫停進入
            close,word=pause_screen()
            show_guideline=False
            show_pause = True

        pygame.mixer.music.unpause()
        show_guideline=False   
    
    #允許暫停畫面執行
    if show_pause:
        pygame.mixer.music.pause()
        close,word=pause_screen()
        if word=="home":
            show_init=True

        if close:
            break
        if word=="resume":#回到遊戲
            #time.sleep(3)
            show_pause_waiting=True
            pass

        elif word=="guidelines":#前往說明
            show_guideline=True
            '''
            show_guideline=True
            show_init = False
            continue
            '''
        
        if close:
            break
        pygame.mixer.music.unpause()
        show_pause=False

    #允許暫停緩衝
    if show_pause_waiting:
        pygame.mixer.music.pause()
        close,word=pause_waiting_screen()
        if word=="done":#暫停緩衝完
            pass

        if close:
            break
        pygame.mixer.music.unpause()
        show_pause_waiting=False

    #允許死亡畫面執行
    if show_die:
        pygame.mixer.music.pause()
        if score>current_highest_score:
            current_highest_score=score
        allow_running=False
        close,word=die_screen(score=score)

        if word=="home":#回到首頁
            show_init=True

        if close:
            break
        pygame.mixer.music.unpause()
        show_die=False

    #允許選擇角色畫面執行
    if show_select:
        pygame.mixer.music.pause()
        close,word,sc_a,sl_a=select_screen()

        #更新遊戲角色能力值
        player_scoring_ability=sc_a
        player_slowering_ability=sl_a
        if word=="selected":#遊戲角色挑選完成
            show_init=True

        if close:
            break
        pygame.mixer.music.unpause()
        show_select=False

    #combo 處理
    if combo_score>0 and allow_combo_added:
        combo_score-=dt*5
    
    if combo_score>21:
        in_combo=True#處在combo狀態
        combo_score=20#combo分數定格
        combo_starting_time=pygame.time.get_ticks()#取得combo模式起始時間
        combo_score_reset=True
        allow_combo_added=False

    if in_combo:
        combo_factor=3#combo模式下分數3倍

    #取得當前時間
    now=pygame.time.get_ticks()

    #判斷combo執行時間是否已夠久
    if now-combo_starting_time>combo_duration and combo_score_reset==True:
        in_combo=False
        combo_score=0
        combo_factor=1
        combo_score_reset=False
        allow_combo_added=True

    #判斷學生證是否可掉落
    if now-tnfsh_id_starting_time>tnfsh_id_duration:
        tnfsh_id_starting_time=now
        tnfsh_id=TNFSH()
        tnfsh_ids.add(tnfsh_id)
        all_sprites.add(tnfsh_id)

    #判斷學生證是否可掉落
    if now-ntu_id_starting_time>ntu_id_duration:
        ntu_id_starting_time=now
        ntu_id=NTU()
        ntu_ids.add(ntu_id)
        all_sprites.add(ntu_id)

    
    #回傳所有發生事件的列表
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if bullet_number>0:
                    player.shoot()#射擊子彈
                    bullet_number-=1

            elif event.key == pygame.K_ESCAPE:#回到首頁
                show_init=True

            elif event.key == pygame.K_PAGEUP:#暫停
                show_pause=True

            #取得英打輸入
            elif event.key == pygame.K_a:
                keyboard_sound.play()
                word_typed.append("a")
        
            elif event.key == pygame.K_b:
                keyboard_sound.play()
                word_typed.append("b")

            elif event.key == pygame.K_c:
                keyboard_sound.play()
                word_typed.append("c")

            elif event.key == pygame.K_d:
                keyboard_sound.play()
                word_typed.append("d")

            elif event.key == pygame.K_e:
                keyboard_sound.play()
                word_typed.append("e")

            elif event.key == pygame.K_f:
                keyboard_sound.play()
                word_typed.append("f")

            elif event.key == pygame.K_g:
                keyboard_sound.play()
                word_typed.append("g")

            elif event.key == pygame.K_h:
                keyboard_sound.play()
                word_typed.append("h")

            elif event.key == pygame.K_i:
                keyboard_sound.play()
                word_typed.append("i")

            elif event.key == pygame.K_j:
                keyboard_sound.play()
                word_typed.append("j")

            elif event.key == pygame.K_k:
                keyboard_sound.play()
                word_typed.append("k")

            elif event.key == pygame.K_l:
                keyboard_sound.play()
                word_typed.append("l")

            elif event.key == pygame.K_m:
                keyboard_sound.play()
                word_typed.append("m")

            elif event.key == pygame.K_n:
                keyboard_sound.play()
                word_typed.append("n")

            elif event.key == pygame.K_o:
                keyboard_sound.play()
                word_typed.append("o")

            elif event.key == pygame.K_p:
                keyboard_sound.play()
                word_typed.append("p")

            elif event.key == pygame.K_q:
                keyboard_sound.play()
                word_typed.append("q")

            elif event.key == pygame.K_r:
                keyboard_sound.play()
                word_typed.append("r")

            elif event.key == pygame.K_s:
                keyboard_sound.play()
                word_typed.append("s")

            elif event.key == pygame.K_t:
                keyboard_sound.play()
                word_typed.append("t")

            elif event.key == pygame.K_u:
                keyboard_sound.play()
                word_typed.append("u")

            elif event.key == pygame.K_v:
                keyboard_sound.play()
                word_typed.append("v")

            elif event.key == pygame.K_w:
                keyboard_sound.play()
                word_typed.append("w")

            elif event.key == pygame.K_x:
                keyboard_sound.play()
                word_typed.append("x")

            elif event.key == pygame.K_y:
                keyboard_sound.play()
                word_typed.append("y")
                
            elif event.key == pygame.K_z:
                keyboard_sound.play()
                word_typed.append("z")
                
            elif event.key == pygame.K_SPACE:
                keyboard_sound.play()
                word_typed.append(" ")

            elif event.key == pygame.K_MINUS:
                keyboard_sound.play()
                word_typed.append("-")


            elif event.key == pygame.K_RETURN:
                get_word=""
                for i in word_typed:
                    get_word=get_word+i
                word_typed=[]

            elif event.key == pygame.K_BACKSPACE:
                if len(word_typed)>0:
                    word_typed.pop()
            
    #更新遊戲

    if allow_running:
        in_game=True
        number_of_meteorite=2+t//8#讓單字掉落量隨時間增加
        #補足單字量
        if len(meteorites)<number_of_meteorite:
            meteorite = Meteorite(Firsttime=False,t=t)
            xx=meteorite.rect.x
            yy=meteorite.rect.y
            wword=meteorite.word
            enemy=Enemy(wword,xx,yy)
            all_sprites.add(meteorite)
            all_sprites.add(enemy)
            meteorites.add(meteorite)
            enemies.add(enemy)
        #角色顯示更新
        all_sprites.update()

        #保留射擊功能
        hits1 = pygame.sprite.groupcollide(tnfsh_ids, bullets, True, True)
        hits2 = pygame.sprite.groupcollide(ntu_ids, bullets, True, True)
        
        #TNFSH學生證被打中
        for hit in hits1:
            
            #特效元素產生
            mx, my =hit.rect.x+STUDENT_WIDTH/2,hit.rect.y
            for i in range(50):
                particles_tnfsh.append([[mx, my], [random.randint(-10, 30) / 10 - 1, random.randint(-10, 5)], random.randint(6, 11)])

            #補血
            if player.health<100:
                player.health=100
        #特效產生
        for particle in particles_tnfsh:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.05
            particle[1][1] += 0.5
            pygame.draw.circle(screen, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))

            radius = particle[2] * 2
            screen.blit(circle_surf(radius, (20, 20, 60)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=BLEND_RGB_ADD)

            if particle[2] <= 0:
                particles_tnfsh.remove(particle)

        #專為特效刷新螢幕
        pygame.display.update()

        #NTU學生證被打中  
        for hit in hits2:
            #特效元素產生
            mx, my =hit.rect.x+STUDENT_WIDTH/2,hit.rect.y
            for i in range(50):
                particles_ntu.append([[mx, my], [random.randint(-10, 30) / 10 - 1, random.randint(-10, 5)], random.randint(6, 11)])

            #補子彈
            if bullet_number<15:
                bullet_number=15

        #特效產生
        for particle in particles_ntu:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.05
            particle[1][1] += 0.5
            pygame.draw.circle(screen, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))

            radius = particle[2] * 6
            screen.blit(circle_surf(radius, (20, 20, 60)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=BLEND_RGB_ADD)

            if particle[2] <= 0:
                particles_ntu.remove(particle)
        #專為特效刷新螢幕
        pygame.display.update()
            # if hit.factor in trail_occupied:
            #     trail_occupied.remove(hit.factor)
            # if hit.word in words_on_screen:
            #     words_on_screen.remove(hit.word)
            # score+=hit.word_length//2*history_level#得分機制，還可以再調
            # for i in enemies:
            #     if i.word==hit.word:
            #         i.kill()
            # meteorite = Meteorite()
            # xx=meteorite.rect.x
            # yy=meteorite.rect.y
            # wword=meteorite.word
            # enemy=Enemy(wword,xx,yy)
            # all_sprites.add(meteorite)
            # all_sprites.add(enemy)
            # meteorites.add(meteorite)
            # enemies.add(enemy)
        
        #玩家血被扣光       
        if player.health<=0:
            show_die=True
        
        #當前輸入
        current_type=""
        for i in word_typed:
            current_type=current_type+i

        #判斷目前輸入對不對，不對會變色
        word_color=YELLOW
        allow_suggest=False
        for i in words_on_screen:
            if i.startswith(current_type):
                allow_suggest=True
                suggest_word=""
                if len(current_type)>0:
                    #提示字眼
                    suggest_word=i
                    for j in range(len(current_type)):
                        suggest_word=suggest_word[1:]

                special_word_color=BLUE
                word_color=WHITE

        #判斷輸入的自有沒有在螢幕上
        if get_word in words_on_screen:
            for i in meteorites:#逐一單字檢查
                if i.word==get_word:#單字正確
                    score+=i.word_length*player_scoring_ability//2*history_level*combo_factor
                    if allow_combo_added:
                        combo_score+=i.word_length
                    expl = Explosion(i.rect.center)#爆炸特效產生
                    all_sprites.add(expl)
                    words_on_screen.remove(i.word)
                    explosion_sound.play()
                    for j in enemies:#角色圖片檢查
                        if j.word==i.word:
                            j.kill()
                    i.kill()
                    break

        #畫面顯示 
        screen.blit(background_png,(0,0))
        all_sprites.draw(screen)
        draw_text(screen,str(score),26,110,25)
        if in_combo:
            draw_text(screen,str(history_level)+"X",26,770,5,YELLOW)
        else:
            draw_text(screen,str(history_level)+"X",26,770,5)
        draw_health(screen, player.health, 50, 5)
        if in_combo:
            noww=pygame.time.get_ticks()
            if noww-last_bar_color_update>500 and bar_color==YELLOW:
                bar_color=RED
                last_bar_color_update=noww

            elif noww-last_bar_color_update>500 and bar_color==RED:
                bar_color=YELLOW
                last_bar_color_update=noww
            draw_combo(screen,combo_score,720,40,bar_color)

        else:
            draw_combo(screen,combo_score,720,40,YELLOW)

        rect_right=draw_text(screen,current_type,26,WIDTH/2,15,font_color=word_color,special=True)
        if allow_suggest:#單字提示
            special_draw_text(screen,suggest_word,26,rect_right,15,font_color=special_word_color)

        bullet_rect = pygame.Rect(735, 70, 10, 20)
    
        pygame.draw.rect(screen, YELLOW,bullet_rect)
        draw_text(screen,"X"+str(bullet_number),26,770,65)

        #子彈噴射尾流特效
        for bullet_shown in bullets: 
            mx, my = bullet_shown.rect.x+5,bullet_shown.rect.y+20
            particles.append([[mx, my], [random.randint(0, 10) / 10 - 1, -5], random.randint(9, 11)])

        for particle in particles:
            #particle[0][0] += particle[1][0]
            particle[0][1] -= particle[1][1]
            particle[2] -= 0.1
            particle[1][1] -= 0.2
            pygame.draw.circle(screen, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))

            radius = particle[2] * 2
            screen.blit(circle_surf(radius, (20, 20, 60)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=BLEND_RGB_ADD)

            if particle[2] <= 8:
                #     #particles.clear()
                particles.remove(particle)
        pygame.display.update()
        
        t+=dt
        
    
    

    




