from PIL import Image
import pygame

# Load animated GIF frames


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((frames[0].get_width(), frames[0].get_height()))
clock = pygame.time.Clock()

i = 0
running = True
while running:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(frames[i], (0, 0))
    pygame.display.update()
    i = (i + 1) % len(frames)
    clock.tick(30)  # ~10 FPS
