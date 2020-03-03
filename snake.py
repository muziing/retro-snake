class Point:
    row = 0
    col = 0
    def __init__(self,row,col):
        self.row=row
        self.col=col

    def copy(self):
        return Point(row=self.row,col=self.col)

#初始框架
import pygame
from random import randrange
from random import randint
from time import perf_counter,sleep

#初始化
pygame.init()
pygame.mixer.init()
pygame.joystick.init()

score=0

W = 900
H = 600

ROW = 30
COL = 45
size =(W, H)

#导入背景图片
background=pygame.image.load("image.jpg")
window = pygame.display.set_mode(size,0,32)
#Pygame窗口标题
pygame.display.set_caption('muzing 的贪吃蛇')

#若以纯色填充背景
#bg_coloe=(254,254,245)




#开始游戏计时
time_start=perf_counter()

pygame.mixer.music.load("bgm.mp3") # 载入背景音乐
pygame.mixer.music.set_volume(0.15) # 设置音量为 0.15
pygame.mixer.music.play(1000,0.0) # 播放音乐

end_sound = pygame.mixer.Sound("_A1#.wav") #载入音效（死亡）
end_sound.set_volume(0.12)

#设置颜色
head_color=(30,220,200)
body_color=(200,240,200)
food_color=(255,105,180)


#定义坐标
head=Point(row=int(ROW/2),col=int(COL/2))
bodys=[
    Point(row=head.row,col=head.col+1),
    Point(row=head.row,col=head.col+2),
    Point(row=head.row,col=head.col+3)
]

#生成食物
def gen_food():
    while True:
        pos=Point(row=randint(0,ROW-1),col=randint(0,COL-1))
        is_coll = False
        #是否和蛇头碰上
        if  (head.row==pos.row and head.col==pos.col):
            is_coll=True

        #是否和蛇身碰上
        for body in bodys:
            if body.row==pos.row and body.col==pos.col:
                is_coll=True
                break
        if not is_coll:
            break
    return pos

food= gen_food()



direct='left'  #left,right,up,down

def rect(point,color):
    cell_width = int(W/COL)
    cell_height = int(H/ROW)
    left=int(point.col*cell_width)
    top=int(point.row*cell_height)

    pygame.draw.rect(
        window,color,
        (left,top,cell_width,cell_height)
    )
    pass

#游戏循环
quit = False
clock = pygame.time.Clock()
while not quit:
    #处理事件
    events = pygame.event.get()
    for event in events:
        if event.type==pygame.QUIT:
            quit=True
        #用键盘控制 支持方向键和WSAD
        elif event.type==pygame.KEYDOWN:
            if (event.key==273 or event.key==119) and direct !='down':
                direct='up'
            elif (event.key==274 or event.key==115) and direct!='up':
                direct='down'
            elif (event.key==276 or event.key==97) and direct!='right':
                direct='left'
            elif (event.key==275 or event.key==100) and direct!='left':
                direct='right'

        #用游戏手柄控制
        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            #ABXY按键控制
            if event.type==pygame.JOYBUTTONDOWN:
                if (joystick.get_button(3)==1 ) and direct !='down':
                    direct='up'
                elif (joystick.get_button(0)==1) and direct!='up':
                    direct='down'
                elif (joystick.get_button(2)==1) and direct!='right':
                    direct='left'
                elif (joystick.get_button(1)==1) and direct!='left':
                    direct='right'
            #左摇杆控制
            elif event.type == pygame.JOYAXISMOTION:
                if (joystick.get_axis(1)<-0.3) and direct != 'down':
                    direct = 'up'
                elif (joystick.get_axis(1)>0.3) and direct != 'up':
                    direct = 'down'
                elif (joystick.get_axis(0)<-0.3) and direct != 'right':
                    direct = 'left'
                elif (joystick.get_axis(0)>0.3) and direct != 'left':
                    direct = 'right'




    #更新分数
    score = (len(bodys) -3)*10


    #吃东西
    eat=(head.row==food.row and head.col==food.col)
    #重新产生食物
    if eat:
        food = gen_food()

    #处理身子
    #1.把原来的头，插入到body的头上
    bodys.insert(0,head.copy())
    #2.把 body 的最后一个删掉
    if not eat:
        bodys.pop()

    #移动
    if direct=='left':
        head.col-=1
    elif direct=='right':
        head.col+=1
    elif direct=='up':
        head.row-=1
    elif direct=='down':
        head.row+=1

    #检测
    dead=False
    #1.撞墙
    if head.col<0 or head.col >COL-1 or head.row<0 or head.row>ROW-1:
        dead=True
    #2.撞自己
    for body in bodys:
        if head.col==body.col and head.row==body.row:
            dead=True
            break

    if dead:
        time_end=perf_counter()
        game_time = int(round(time_end - time_start,0))
        pygame.mixer.music.stop()
        end_sound.play()
        sleep(1)
        pygame.display.quit()
        print(''' 
  _____                         ____                   _ 
 / ____|                       / __ \                 | |
| |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __  | |
| | |_ |/ _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '__| | |
| |__| | (_| | | | | | |  __/ | |__| |\ V /  __/ |    |_|
 \_____|\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|    (_)
  ''')
        print("你的得分：" + str(score)+" 分")
        if score==0:
            print("  嗯？ 0分？ 天秀")
        print("你已经玩了 "+str(game_time)+" 秒\n")
        input("按回车键退出\n")
        #sleep(1)
        quit=True

    #渲染——画出来
    #背景
    #以纯色填充
    #pygame.draw.rect(background,bg_coloe,(0,0,W,H))

    #以背景图片填充
    if not dead:
        window.blit(background,(0,0))
    #蛇头
        for body in bodys:
            rect(body, body_color)
            rect(head,head_color)
            rect(food,food_color)

        pygame.display.update()

    #设置帧频,随蛇长度增加，速度会越来越快
    clock.tick(10+(score/50))