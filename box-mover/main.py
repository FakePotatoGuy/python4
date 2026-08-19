import pygame

screen_hight=600
screen_width=700

pygame.init()
screen=pygame.display.set_mode((screen_width,screen_hight))
pygame.display.set_caption("Box Mover")
clock=pygame.time.Clock()

running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    clock.tick(60)
pygame.quit()