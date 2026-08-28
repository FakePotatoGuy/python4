import pygame

screen_width=500
screen_height=600

pygame.init()
screen=pygame.display.set_mode(())
pygame.display.set_caption("swift'n'simple")
clock=pygame.time.Clock()

running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    clock.tick(60)
pygame.quit()