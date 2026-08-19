import pygame

screen_hight=590
screen_width=690

pygame.init()
screen=pygame.display.set_mode((screen_width,screen_hight))
pygame.display.set_caption("Box Mover")
clock=pygame.time.Clock()

bg=pygame.image.load("assets/images/bg.png")

def draw():
    screen.fill("black")
    screen.blit(bg)
    pygame.display.flip()

running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    draw()

    clock.tick(60)
pygame.quit()