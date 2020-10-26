"""初始化和加载资源相关代码"""
import pygame
from cfg import size

pygame.init()
pygame.mixer.init()
# pygame.joystick.init()

# 导入背景图片
GamingBackground = pygame.image.load("./resources/images/background_01.jpg")
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