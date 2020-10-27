import pygame
from init_game import StartingBackground


def start_game(start_flag: bool, window: pygame.surface):
    quit_flag = False

    while start_flag and not quit_flag:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit_flag = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            break
        window.blit(StartingBackground, (0, 0))
        pygame.display.update()
    if quit_flag:
        pygame.display.quit()
