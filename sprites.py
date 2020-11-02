from random import randint

import cfg
import pygame.rect


class Point:
    """定义格点类，游戏都是基于这种格点的"""
    row = 0
    col = 0

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def copy(self):
        return Point(row=self.row, col=self.col)


def rect(point, color, window):
    """调用pygame中绘制矩形的方法，绘制蛇或食物方块"""
    cell_width = int(cfg.W / cfg.COL)
    cell_height = int(cfg.H / cfg.ROW)
    left = int(point.col * cell_width)
    top = int(point.row * cell_height)

    pygame.draw.rect(
        window, color,
        (left, top, cell_width, cell_height)
    )


class Snake:
    def __init__(self, head_pos=cfg.snake_head_pos, direct='left', head_clr=cfg.head_color, body_clr=cfg.body_color):
        super().__init__()
        self.head = Point(*head_pos)
        head = self.head
        self.bodies = [
            Point(row=head.row, col=head.col + 1),
            Point(row=head.row, col=head.col + 2),
            Point(row=head.row, col=head.col + 3)
            # 初始蛇身为蛇头向右的三个格
        ]
        self.direct = direct
        self.head_clr = head_clr
        self.body_clr = body_clr

    def set_color(self, head_clr, body_clr):
        """用来改变蛇的颜色"""
        self.head_clr = head_clr
        self.body_clr = body_clr

    def move(self):
        if self.direct == 'left':
            self.head.col -= 1
        elif self.direct == 'right':
            self.head.col += 1
        elif self.direct == 'up':
            self.head.row -= 1
        elif self.direct == 'down':
            self.head.row += 1

    def turn(self, to_direct):
        if self.direct != 'down' and to_direct == 'up':
            self.direct = 'up'
        elif self.direct != 'up' and to_direct == 'down':
            self.direct = 'down'
        elif self.direct != 'right' and to_direct == 'left':
            self.direct = 'left'
        elif self.direct != 'left' and to_direct == 'right':
            self.direct = 'right'

    def draw(self, window):
        rect(self.head, self.head_clr, window)
        for body in self.bodies:
            rect(body, self.body_clr, window)

    def __len__(self):
        return len(self.bodies)


class Food:
    def __init__(self, snake, color=cfg.food_color):
        super().__init__()
        self.color = color
        self.gen(snake)

    def gen(self, snake):
        """生成食物"""
        while True:
            random_pos = Point(row=randint(0, cfg.ROW - 1), col=randint(0, cfg.COL - 1))  # 先生成一个随机点位
            is_coll = False  # 标志，为True时生成新的食物
            # 是否和蛇头碰上，碰上即为吃掉，再生成一个新的
            if snake.head.row == random_pos.row and snake.head.col == random_pos.col:
                is_coll = True

            # 检查是否和蛇身碰上，防止新生成的食物在当前蛇身的格点里
            for body in snake.bodies:
                if body.row == random_pos.row and body.col == random_pos.col:
                    is_coll = True
                    break
            if not is_coll:
                break
        self.pos = random_pos  # 此时已经跳出循环，需要把食物的位置重置为这个新的随机位置（相当于生成一个新的食物）

    def draw(self, window):
        """绘制食物"""
        rect(self.pos, cfg.food_color, window)

    def set_color(self, new_color):
        self.color = new_color
