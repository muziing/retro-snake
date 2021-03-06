# muzing的贪吃蛇
# 初始框架
from init_game import *
from sprites import *
import cfg
from interfaces import StartGame
from time import perf_counter, sleep

# 游戏主窗口
window = pygame.display.set_mode(cfg.size, 0, 32)

# 创建蛇、食物实例
snake1 = Snake()
food1 = Food(snake1)


def game_main_loop():
    # 游戏循环
    quit_flag = False  # 设置一个标志，判断蛇是否死亡
    clock = pygame.time.Clock()  # 设置游戏运行的帧率
    time_start = perf_counter()  # 开始游戏计时

    while not quit_flag:
        # 处理事件
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit_flag = True
            keys = pygame.key.get_pressed()
            # 用键盘控制 支持方向键和WSAD
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                snake1.turn('up')
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                snake1.turn('down')
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                snake1.turn('left')
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                snake1.turn('right')

            # 用游戏手柄控制
            joystick_count = pygame.joystick.get_count()
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                # ABXY 按键控制
                if event.type == pygame.JOYBUTTONDOWN:
                    if (joystick.get_button(3) == 1):
                        snake1.turn('up')
                    elif (joystick.get_button(0) == 1):
                        snake1.turn('down')
                    elif (joystick.get_button(2) == 1):
                        snake1.turn('left')
                    elif (joystick.get_button(1) == 1):
                        snake1.turn('right')
                # 左摇杆控制
                elif event.type == pygame.JOYAXISMOTION:
                    if (joystick.get_axis(1) < -0.3):
                        snake1.turn('up')
                    elif (joystick.get_axis(1) > 0.3):
                        snake1.turn('down')
                    elif (joystick.get_axis(0) < -0.3):
                        snake1.turn('left')
                    elif (joystick.get_axis(0) > 0.3):
                        snake1.turn('right')

        # 更新分数
        score = (len(snake1) - 3) * 10

        # 吃东西
        eat = (snake1.head.row == food1.pos.row and snake1.head.col == food1.pos.col)
        # 重新产生食物
        if eat:
            eat_sound.play()  # 播放吃东西音效
            food1.gen(snake1)  # 生成新的食物

        # 处理身子
        # 1.把原来的头，插入到body的头上
        snake1.bodies.insert(0, snake1.head.copy())
        # 2.把 body 的最后一个删掉
        if not eat:
            snake1.bodies.pop()  # 蛇每次移动，就是把蛇头移到新的格点，并把原来的蛇尾删去。这里从列表中把最后一个元素删去即可

        # 移动
        snake1.move()

        # 检测
        dead = False
        # 1.撞墙
        if snake1.head.col < 0 or snake1.head.col > cfg.COL - 1 or snake1.head.row < 0 or snake1.head.row > cfg.ROW - 1:
            dead = True
        # 2.撞自己
        for body in snake1.bodies:
            if snake1.head.col == body.col and snake1.head.row == body.row:
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
            if (snake1.head.row == 0 or snake1.head.row == -1) and (
                    snake1.head.col == cfg.COL or snake1.head.col == cfg.COL - 1):
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
            window.blit(GamingBackground, (0, 0))
            snake1.draw(window)
            food1.draw(window)

            pygame.display.update()

        clock.tick(cfg.FPS + (score / 50))  # 设置帧频,随蛇长度增加，速度会越来越快


start_flag = True
StartGame.start_game(start_flag, window)
game_main_loop()
