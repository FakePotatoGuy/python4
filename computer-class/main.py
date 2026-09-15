import pygame,random

screen_width=800
screen_height=600

pygame.init()
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Pew Pew Game")
clock=pygame.time.Clock()


time=0
player=pygame.Rect(10,0,25,15)

player2=pygame.Rect(10,50,25,15)
ready_player2=False

bullets=[]

class bullet:
    def __init__(self,x,y):
        self.type="normal"
        self.x=x
        self.y=y
        self.color=(225,225,225)
        self.rect=pygame.Rect(x,y,15,10)

class big_bullet:
     def __init__(self,x,y):
             self.type="big"
             self.x=x
             self.y=y
             self.time=0
             self.color=(225,225,225)
             self.rect=pygame.Rect(x,y,15,75)

enemys=[]
class enemy:
    def __init__(self,x,y):
            self.x=x
            self.y=y
            self.rect=pygame.Rect(x,y,35,20)

def draw():
    screen.fill("black")
    

    for bullet in bullets:
        pygame.draw.rect(screen,bullet.color,bullet.rect)

    for enemy in enemys:
        pygame.draw.rect(screen,("red"),enemy.rect)

    pygame.draw.rect(screen,("white"),player)
    if ready_player2:
        pygame.draw.rect(screen,("green"),player2)

    pygame.display.flip()

def movement():
    key=pygame.key.get_pressed()
    

    if ready_player2:
        if key[pygame.K_s]:
            player.y+=6
        elif key[pygame.K_w]:
            player.y-=6
        if key[pygame.K_DOWN]:
            player2.y+=6
        elif key[pygame.K_UP]:
            player2.y-=6
    else:
        if key[pygame.K_s]:
            player.y+=6
        elif key[pygame.K_w]:
            player.y-=6
        elif key[pygame.K_DOWN]:
            player.y+=6
        elif key[pygame.K_UP]:
            player.y-=6

def logic():
    global time
    for bullet_index,bullet in enumerate(bullets):
            destroy_bullet=False
            if bullet.type=="big":
                bullet.rect.x+=3
                r, g, b = bullet.color
                bullet.color = (max(0, r - 5), max(0, g - 5), max(0, b - 5))
                if bullet.color==(0,0,0):
                    destroy_bullet=True
            else:
                bullet.rect.x+=8
                r, g, b = bullet.color
                bullet.color = (max(0, r - 2), max(0, g - 2), max(0, b - 2))
                if bullet.color==(0,0,0):
                    destroy_bullet=True
            if bullet.rect.right>screen_width:
                destroy_bullet=True

            hit_index = bullet.rect.collidelist(enemys)
            if hit_index != -1:
                enemys.pop(hit_index)
                destroy_bullet=True

            if destroy_bullet:
                bullets.pop(bullet_index)

    if player.top<=0:
        player.top=0
    if player.bottom>=screen_height:
            player.bottom=screen_height

    if ready_player2:
        if player2.top<=0:
            player2.top=0
        if player2.bottom>=screen_height:
            player2.bottom=screen_height

    time+=1
    if time>=60:
        time=0
        enemys.append(enemy(screen_width,random.randrange(0,screen_height)))
        if ready_player2:
            enemys.append(enemy(screen_width,random.randrange(0,screen_height)))

    for enemy_thing in enemys:
        enemy_thing.rect.x-=3

    

running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_BACKSLASH:
                if ready_player2:
                    ready_player2=False
                else:
                    ready_player2=True
            
            if event.key==pygame.K_SPACE:
                bullets.append(bullet(player.x,player.y))

            if event.key==pygame.K_q:
                new_bullet=big_bullet(player.x,player.y)
                new_bullet.rect.center=player.center
                new_bullet.rect.left=player.right
                bullets.append(new_bullet)

            #Add p2 controls
            if ready_player2:
                if event.key==pygame.K_RIGHT:
                    new_bullet=bullet(player2.x,player2.y)
                    new_bullet.color=(0,225,0)
                    bullets.append(new_bullet)
                
                if event.key==pygame.K_LEFT:
                    new_bullet=big_bullet(player2.x,player2.y)
                    new_bullet.rect.center=player2.center
                    new_bullet.rect.left=player2.right
                    new_bullet.color=(0,225,0)
                    bullets.append(new_bullet)

        #Clicks
        if event.type==pygame.MOUSEBUTTONDOWN:
            bullets.append(bullet(player.x,player.y))

    draw()
    movement()
    logic()

    clock.tick(60)
pygame.quit()