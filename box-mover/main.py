import pygame

screen_hight=590
screen_width=690

pygame.init()
screen=pygame.display.set_mode((screen_width,screen_hight))
pygame.display.set_caption("Box Mover")

clock=pygame.time.Clock()
seconds_counter=0
run_time=0

bg=pygame.image.load("assets/images/bg.png")

logo=pygame.image.load("assets/images/jpj-inc.png")
logo_alpha=0

screen_number=-1

def draw():
    """
    This draws all the assets on to the screen, it uses screen number to
    show what to display like the title or the game ect.
    -2:(WIP) Settings
    -1:JPJ logo
    0:main title
    2:levels
    3:game
    4:win/lose
    """
    global logo_alpha
    if screen_number==-1:
        screen.fill("white")

        if run_time>=1:
            if logo_alpha<255:
                logo_alpha+=2
            elif logo_alpha>=255:
                logo_alpha=255

        copy_logo=logo.copy()
        copy_logo.set_alpha(logo_alpha)
        screen.blit(copy_logo)

        pygame.display.flip()


    elif screen_number==0:
        screen.fill("white")
    elif screen_number==1:
        screen.fill("black")
        screen.blit(bg)
        pygame.display.flip()


def do_time():
    """
    This runs all the time and time calculations for the game
    """
    global seconds_counter,run_time
    clock.tick(60)

    seconds_counter+=1
    if seconds_counter>=60:
        run_time+=1
        seconds_counter=0


"""
This is the main loop where the game actualy runs
"""
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    draw()

    do_time()
pygame.quit()