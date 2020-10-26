# muzing的贪吃蛇
# 初始框架
from cfg import *
import pygame
from random import randint
from time import perf_counter, sleep

# 初始化一些参数
score = 0  # 初始得分为0
# 初始化
pygame.init()
pygame.mixer.init()
pygame.joystick.init()


# 导入背景图片
background = pygame.image.load("./resources/images/background_01.jpg")
window = pygame.display.set_mode(size, 0, 32)
pygame.display.set_caption('muzing 的贪吃蛇')  # Pygame窗口标题

# 若以纯色填充背景
# bg_color=(254,254,245)


pygame.mixer.music.load("./resources/audios/bgm.mp3")  # 载入背景音乐
pygame.mixer.music.set_volume(0.15)  # 设置音量为 0.15
pygame.mixer.music.play(1000, 0.0)  # 播放音乐

end_sound = pygame.mixer.Sound("./resources/audios/_A1#.wav")  # 载入音效（死亡）
end_sound.set_volume(0.12)

eat_sound = pygame.mixer.Sound("./resources/audios/eat4.wav")  # 载入音效（吃东西）
eat_sound.set_volume(0.12)


class Point:
    """定义格点类，游戏都是基于这种格点的"""
    row = 0
    col = 0

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def copy(self):
        return Point(row=self.row, col=self.col)


# 定义坐标
head = Point(row=int(ROW / 2), col=int(COL / 2))
bodys = [
    Point(row=head.row, col=head.col + 1),
    Point(row=head.row, col=head.col + 2),
    Point(row=head.row, col=head.col + 3)
    # 初始蛇身为蛇头向右的三个格
]


def gen_food():
    """生成食物"""
    while True:
        pos = Point(row=randint(0, ROW - 1), col=randint(0, COL - 1))
        is_coll = False  # 标志，为True时生成新的食物
        # 是否和蛇头碰上，碰上即为吃掉，再生成一个新的
        if head.row == pos.row and head.col == pos.col:
            is_coll = True

        # 检查是否和蛇身碰上，防止新生成的食物在当前蛇身的格点里
        for body in bodys:
            if body.row == pos.row and body.col == pos.col:
                is_coll = True
                break
        if not is_coll:
            break
    return pos


food = gen_food()  # 先调用一次gen_food函数，生成第一个食物


def rect(point, color):
    """调用pygame中绘制矩形的方法，绘制蛇"""
    cell_width = int(W / COL)
    cell_height = int(H / ROW)
    left = int(point.col * cell_width)
    top = int(point.row * cell_height)

    pygame.draw.rect(
        window, color,
        (left, top, cell_width, cell_height)
    )


direct = 'left'  # 定义蛇初始运动方向为向左 还可选right,up,down

# 游戏循环

time_start = perf_counter()  # 开始游戏计时

quit_flag = False  # 设置一个标志，判断蛇是否死亡

clock = pygame.time.Clock()  # 设置游戏运行的帧率

while not quit_flag:
    # 处理事件
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            quit_flag = True
        # 用键盘控制 支持方向键和WSAD
        elif event.type == pygame.KEYDOWN:
            if (event.key == 273 or event.key == 119) and direct != 'down':
                direct = 'up'
            elif (event.key == 274 or event.key == 115) and direct != 'up':
                direct = 'down'
            elif (event.key == 276 or event.key == 97) and direct != 'right':
                direct = 'left'
            elif (event.key == 275 or event.key == 100) and direct != 'left':
                direct = 'right'

        # 用游戏手柄控制
        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            # ABXY 按键控制
            if event.type == pygame.JOYBUTTONDOWN:
                if (joystick.get_button(3) == 1) and direct != 'down':
                    direct = 'up'
                elif (joystick.get_button(0) == 1) and direct != 'up':
                    direct = 'down'
                elif (joystick.get_button(2) == 1) and direct != 'right':
                    direct = 'left'
                elif (joystick.get_button(1) == 1) and direct != 'left':
                    direct = 'right'
            # 左摇杆控制
            elif event.type == pygame.JOYAXISMOTION:
                if (joystick.get_axis(1) < -0.3) and direct != 'down':
                    direct = 'up'
                elif (joystick.get_axis(1) > 0.3) and direct != 'up':
                    direct = 'down'
                elif (joystick.get_axis(0) < -0.3) and direct != 'right':
                    direct = 'left'
                elif (joystick.get_axis(0) > 0.3) and direct != 'left':
                    direct = 'right'

    # 更新分数
    score = (len(bodys) - 3) * 10

    # 吃东西
    eat = (head.row == food.row and head.col == food.col)
    # 重新产生食物
    if eat:
        eat_sound.play()  # 播放吃东西音效
        food = gen_food()  # 生成新的食物

    # 处理身子
    # 1.把原来的头，插入到body的头上
    bodys.insert(0, head.copy())
    # 2.把 body 的最后一个删掉
    if not eat:
        bodys.pop()  # 蛇每次移动，就是把蛇头移到新的格点，并把原来的蛇尾删去。这里从列表中把最后一个元素删去即可

    # 移动
    if direct == 'left':
        head.col -= 1
    elif direct == 'right':
        head.col += 1
    elif direct == 'up':
        head.row -= 1
    elif direct == 'down':
        head.row += 1

    # 检测
    dead = False
    # 1.撞墙
    if head.col < 0 or head.col > COL - 1 or head.row < 0 or head.row > ROW - 1:
        dead = True
    # 2.撞自己
    for body in bodys:
        if head.col == body.col and head.row == body.row:
            dead = True
            break
    # 死亡
    if dead:
        time_end = perf_counter()
        game_time = int(round(time_end - time_start, 0))
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
        print("你的得分：" + str(score) + " 分")
        # 彩蛋1:禁止摸鱼！
        if score == 0:
            print("嗯？ 0分？ 这里禁止摸鱼！")
        print("你已经玩了 " + str(game_time) + " 秒\n")
        # 彩蛋3：边边角角
        if (head.row == 0 or head.row == -1) and (head.col == COL or head.col == COL - 1):
            print("答应我，下一次当你想要关掉游戏的时候，用鼠标去点这个 X ，而不是用头去撞，好吗？\n")
        # 彩蛋2：你是来听歌的？
        if 352 > game_time > 342:
            print("曲终蛇亡，你是来听歌的？\n")
        input("按回车键退出\n")
        # sleep(1)
        quit_flag = True

    # 以纯色填充
    # pygame.draw.rect(background,bg_color,(0,0,W,H))

    # 以背景图片填充
    if not dead:
        window.blit(background, (0, 0))
        # 蛇头
        for body in bodys:
            rect(body, body_color)
            rect(head, head_color)
            rect(food, food_color)

        pygame.display.update()

    clock.tick(10 + (score / 50))  # 设置帧频,随蛇长度增加，速度会越来越快
