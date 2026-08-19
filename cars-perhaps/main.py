import pygame

#ToDo list


version=0

#For the memes, (Will be removed later)
def version_counter():
    global version
    with open("versions.txt","r") as f:
        version=float(f.read())

    with open("versions.txt","w") as f:
        f.write(str(round(version,4)+0.0001))
version_counter()


#--Pygame setup
screen_width=700
screen_hight=600

pygame.init()
screen=pygame.display.set_mode((screen_width,screen_hight))
pygame.display.set_caption(f"Shifty Drifty | Version: {round(version,4)}")
clock=pygame.time.Clock()

#--Other game assets setup
#-Fonts
default_font = pygame.font.Font("assets/fonts/boss.ttf", 90)

#--Game variables
#-Screens (this has to do with what is being drawn)
screen_number=0  #title screen:0, main menu:1

def draw():
    #Clears the screen
    screen.fill("black")

    #----------------------Draws title screen--------------------
    if screen_number==0:
        screen.fill("white")
        text_surface = default_font.render("SHIFTY\nDRIFTY\n", True, "Black")
        text_rect=text_surface.get_rect()
        text_rect.center = (350, 200) 
        screen.blit(text_surface, text_rect)

    #Draws to the screen
    pygame.display.flip()

#--Main game loop
running=True
while running:
    #--Pygame events
    for event in pygame.event.get():
        #Quit event
        if event.type==pygame.QUIT:
            running=False

    #--Funtion calls
    draw()
    #Fps clock (makes the games timing actualy work)
    clock.tick(60)

pygame.quit()