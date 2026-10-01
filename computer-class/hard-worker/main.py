import pygame,random

pygame.init()
screen_height=500
screen_width=600
screen=pygame.display.set_mode((screen_width,screen_height))
clock=pygame.time.Clock()
time_played=0

players=[]
class player:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.health=20
        self.max_health=20
        self.bullets=10
        self.rect=pygame.Rect(self.x,self.y,20,20)

    #This function is for when a player collects the enemys drops
    def picked_up_package(self,the_package):
        self.bullets+=the_package.bullets
        self.health+=the_package.health_healed
        if self.health>=self.max_health:
            self.health=self.max_health
        self.max_health+=the_package.max_health_increase
        packages.remove(the_package)

    def shoot(self):
        self.mousex,self.mousey=pygame.mouse.get_pos()
        bullets.append(bullet_class(self.x,self.y,self.mousex,self.mousey))

bullets=[]
class bullet_class:
    def __init__(self,x,y,mousex,mousey):
        self.x=x
        self.y=y

        #Math
        point1=x,y
        point2=mousex,mousey

        rise=y-mousey
        run=x-mousex
        print(f"{rise}/{run}")

    def update(self):
        pass

players.append(player(screen_width//2,screen_height//2))
current_player=players[len(players)-1]

packages=[]
class package:
    """
    This is for the things dropped adter you kill something, to give back to the player
    """
    def __init__(self,max_bullets=10,health_gain=0,max_health_gain=0):
        self.bullets=random.randrange(1,max_bullets) #Chooses random amount of bullets based on enemy strength
        if health_gain>=0:
            self.heath_healed=random.randrange(0,self.heath_healed) #Gives random or no health based on how strong enemy was
        if max_health_gain>=0:
            self.max_health_increase=random.randrange(0,self.max_heath_increase)

def draw():
    screen.fill("white")
    for player in players:
        pygame.draw.rect(screen,"red",player.rect)

    pygame.display.flip()


running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            current_player.shoot()
            

    draw()

    time_played=round(pygame.time.get_ticks()/1000)
    clock.tick(60)
    
pygame.quit()




















import math

class BulletClass:
    def __init__(self, x, y, mousex, mousey):
        self.x = x
        self.y = y
        self.speed = 10  # Change this to make the bullet faster or slower

        # 1. Calculate the distance (rise and run) from bullet to mouse
        # Target - Current gives the correct direction vector
        run = mousex - x
        rise = mousey - y
        
        # 2. Calculate the straight-line distance (hypotenuse)
        distance = math.hypotenuse(run, rise) # Or math.sqrt(run**2 + rise**2)
        
        # 3. Normalize the vector (break down into a 1-unit step) and multiply by speed
        if distance != 0: # Prevent division by zero if clicking exactly on the player
            self.dx = (run / distance) * self.speed
            self.dy = (rise / distance) * self.speed
        else:
            self.dx = 0
            self.dy = 0

    def update(self):
        # 4. Move the bullet by its velocity components each frame
        self.x += self.dx
        self.y += self.dy
