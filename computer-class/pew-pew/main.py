import pygame,random

#Screen height and width
screen_width=800
screen_height=600

#Pygame setup
pygame.init()
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Pew Pew Game")
clock=pygame.time.Clock()

#Health setup incuding font
maxhp=10
health=10

smfont = pygame.font.SysFont("couriernew", 16)
font = pygame.font.SysFont("couriernew", 32)
bgfont = pygame.font.SysFont("couriernew", 64)


time=0

#player stuff setup
player=pygame.Rect(10,0,25,15)

player2=pygame.Rect(10,50,25,15)
ready_player2=False
controls=False

#Shows what screen we are on
on_screen=0

#Bullet and enemy lists and classes
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

#Draws things to screen
def draw():
    """This funtion draws all of the things we need to draw"""
    screen.fill("black") #clears screen
    if on_screen==1 or on_screen==0:
        for bullet in bullets: #Draws bullets
            pygame.draw.rect(screen,bullet.color,bullet.rect)

        for enemy in enemys: #Draws enemys
            pygame.draw.rect(screen,("red"),enemy.rect)

        #Draws player(s)
        pygame.draw.rect(screen,("white"),player)
        if ready_player2:
            pygame.draw.rect(screen,("green"),player2)

        #Draws health or play button
        if on_screen==1:
            text_surface = font.render(f"HEALTH: {health}/{maxhp}", False, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.right=screen_width
            screen.blit(text_surface, text_rect)
        else:
            if controls==False:
                text_surface = bgfont.render(f"Pew-Pew", False, (255, 255, 255))
                old_rect = text_surface.get_rect()
                old_rect.center=(screen_width//2,screen_height//2)
                screen.blit(text_surface, old_rect)

                text_surface = smfont.render(f"press space to start", False, (255, 255, 255))
                text_rect = text_surface.get_rect()
                text_rect.center=old_rect.center
                text_rect.top=old_rect.bottom
                screen.blit(text_surface, text_rect)

                text_surface = smfont.render(f"press e for controls", False, (255, 255, 255))
                text_rect2 = text_surface.get_rect()
                text_rect2.right=screen_width
                text_rect2.bottom=screen_height
                screen.blit(text_surface, text_rect2)
            else:
                text_surface = bgfont.render("Controls", False, (255, 255, 255))
                old_rect = text_surface.get_rect()
                old_rect.center = (screen_width // 2, screen_height // 2 - screen_height // 3)
                screen.blit(text_surface, old_rect)

                # 2. Define the multiline control text
                controls_text = (
                    "Back to main menu: e\n"
                    "Shoot: Space\n"
                    "Shield: q\n"
                    "Up: w (or Up while in single player)\n"
                    "Down: s (or Down while in single player)\n"
                    "Exit game to main: escape\n"
                    "Activate multiplayer: \\\n"
                    "Player2 shoot: right arrow\n"
                    "Player2 shield: left arrow\n"
                    "Player2 up: up arrow\n"
                    "Player 2 down: down arrow"
                )

                # 3. Split the text into lines and render them dynamically
                lines = controls_text.split("\n")
                current_top = old_rect.bottom + 10  # Start 10 pixels below the header
                line_spacing = 5                    # Pixels between each line of text

                for line in lines:
                    # Render an individual line
                    line_surface = smfont.render(line, False, (255, 255, 255))
                    line_rect = line_surface.get_rect()
                    
                    # Center the line horizontally, and position it vertically
                    line_rect.centerx = old_rect.centerx
                    line_rect.top = current_top
                    
                    # Blit to screen
                    screen.blit(line_surface, line_rect)
                    
                    # Move the vertical anchor down for the next line
                    current_top = line_rect.bottom + line_spacing


    elif on_screen==2:
        text_surface = bgfont.render(f"YOU DIED", False, (255, 255, 255))
        old_rect = text_surface.get_rect()
        old_rect.center=(screen_width//2,screen_height//2)
        screen.blit(text_surface, old_rect)
        text_surface = smfont.render(f"press space to continue", False, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center=old_rect.center
        text_rect.top=old_rect.bottom
        screen.blit(text_surface, text_rect)

    #Updates it all
    pygame.display.flip()

#Moves player
def movement():
    """Moves player"""
    key=pygame.key.get_pressed()
    
    #If player2 then adds their controls
    if ready_player2:
        if key[pygame.K_s]:
            player.y+=6
        elif key[pygame.K_w]:
            player.y-=6
        if key[pygame.K_DOWN]:
            player2.y+=6
        elif key[pygame.K_UP]:
            player2.y-=6
    else: #Single player controls
        if key[pygame.K_s]:
            player.y+=6
        elif key[pygame.K_w]:
            player.y-=6
        elif key[pygame.K_DOWN]:
            player.y+=6
        elif key[pygame.K_UP]:
            player.y-=6

#Runs most of the logic for the program
def logic():
    """
    This function runs most of the logic
    for my program incuding:
    Bullet movement
    Collisons
    Enemy movement
    screen animation
    health
    player logic
    
    """
    global time,health,on_screen,bullets,ready_player2,enemys,startup_screen_seed_index
    for bullet_index in range(len(bullets) - 1, -1, -1):   #Goes backwards through the list of bullets doing logic
            bullet_obj = bullets[bullet_index]
            destroy_bullet=False
            if bullet_obj.type=="big": #Big bullet logic
                bullet_obj.rect.x+=3
                r, g, b = bullet_obj.color
                bullet_obj.color = (max(0, r - 5), max(0, g - 5), max(0, b - 5))
                if bullet_obj.color==(0,0,0): #Drains color then removes bullet
                    destroy_bullet=True
            else: #Normal bullet logic or undefined
                bullet_obj.rect.x+=8
                r, g, b = bullet_obj.color
                bullet_obj.color = (max(0, r - 2), max(0, g - 2), max(0, b - 2))
                if bullet_obj.color==(0,0,0): #Drains color then removes bullet
                    destroy_bullet=True
            if bullet_obj.rect.right>screen_width: #Removes any old bullets that sneak through
                destroy_bullet=True

            hit_index = bullet_obj.rect.collidelist(enemys) #Checks collisons
            
            if hit_index != -1: #Removes colliding enemys and bullets
                enemys.pop(hit_index)
                destroy_bullet=True

            

            if destroy_bullet:
                bullets.pop(bullet_index)

    for enemy_index in range(len(enemys) - 1, -1, -1):   #Goes backwards through the list of enemys doing logic
        enemy_obj = enemys[enemy_index]
        if enemy_obj.rect.colliderect(player):
            health-=3
            enemys.pop(enemy_index)


    #Keeps player(s) on screen
    if player.top<=0:
        player.top=0
    if player.bottom>=screen_height:
            player.bottom=screen_height

    if ready_player2:
        if player2.top<=0:
            player2.top=0
        if player2.bottom>=screen_height:
            player2.bottom=screen_height

    #Spawns enemys
    time+=1
    if time>=60:
        time=0
        enemys.append(enemy(screen_width,random.randrange(0,screen_height)))
        if ready_player2:
            enemys.append(enemy(screen_width,random.randrange(0,screen_height)))

    for index,enemy_thing in enumerate(enemys): #Moves enemys
        enemy_thing.rect.x-=3
        if enemy_thing.rect.right<0:
            if on_screen==1:
                health-=1
            enemys.pop(index)

    #Runs logic for the menu screen, mostly things like
    #the simmulation in the background
    if on_screen==0: #Cycles through a seed to move the fake player up and down
        if startup_screen_seed[startup_screen_seed_index]=="1":
            player.y+=6
        else:
            player.y-=6

        #Random small bullets
        num=random.randrange(1,15)
        if num==1:
            bullets.append(bullet(player.x,player.y))

        #Randomly summons big bullet
        num=random.randrange(1,50)
        if num==1:
            new_bullet=big_bullet(player.x,player.y)
            new_bullet.rect.center=player.center
            new_bullet.rect.left=player.right
            bullets.append(new_bullet)

        #Moves the index forward
        startup_screen_seed_index+=1
        if startup_screen_seed_index>=len(startup_screen_seed):
            startup_screen_seed_index=0



    if health<=0: #Handles death
        on_screen=2
        health=maxhp
        ready_player2=False
        enemys=[]
        bullets=[]

#Seed generater thing
def generate_sticky_bits(length, stickiness=0.95):
    """Helps generate the movement for startup #ThankYouGoogleAi"""
    result = [random.choice(['0', '1'])]
    for _ in range(length - 1):
        # If the random roll is under our stickiness threshold, keep the last bit
        if random.random() < stickiness:
            result.append(result[-1])
        else:
            # Otherwise, flip the bit
            result.append('1' if result[-1] == '0' else '0')
            
    return "".join(result)


#Seed generation for title screen animation stuff
startup_screen_seed=generate_sticky_bits(500)
startup_screen_seed_index=0


#Main loop
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: #Checks for player quiting game and clicking the x
            running=False
        
        if event.type==pygame.MOUSEBUTTONDOWN: #Clicks shoot too
            if on_screen==1:
                if event.button == 1:
                    bullets.append(bullet(player.x,player.y))
                elif event.button == 3:
                    new_bullet=big_bullet(player.x,player.y)
                    new_bullet.rect.center=player.center
                    new_bullet.rect.left=player.right
                    bullets.append(new_bullet)


        if event.type==pygame.KEYDOWN: #Checks for player pressing key
            if on_screen==1: #Checks if in game
                if event.key==pygame.K_ESCAPE:
                    on_screen=0
                    health=maxhp
                    ready_player2=False
                    enemys=[]
                    player.y=screen_height//2
                    bullets=[]

                if event.key==pygame.K_BACKSLASH: #Toggles player 2
                    if ready_player2:
                        ready_player2=False
                        enemys=[]
                        health=10
                        maxhp=10
                    else:
                        ready_player2=True
                        enemys=[]
                        health=20
                        maxhp=20

                #Fires gun small bullets
                if event.key==pygame.K_SPACE:
                    bullets.append(bullet(player.x,player.y))

                #Fires Big Bullets
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


            elif on_screen==0:
                if event.key==pygame.K_SPACE:
                    on_screen=1
                    enemys=[]
                    bullets=[]
                    health=maxhp
                    ready_player2=False
                    player.y=screen_height//2

                if event.key==pygame.K_e: #Toggles controls
                    if controls:
                        controls=False
                    else:
                        controls=True

            elif on_screen==2:
                if event.key==pygame.K_SPACE:
                    on_screen=0
                    enemys=[]
                    bullets=[]
                    health=maxhp
                    ready_player2=False
                    player.y=screen_height//2

            

    draw() #Draws things on screen
    if on_screen==1:  #Checks if in game for player movement
        movement()
    logic() #Runs most of the games logic

    clock.tick(60) #This thing handles fps
pygame.quit()