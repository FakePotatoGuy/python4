import random

#This ceates a matrix in order to hold the information and location of things on a screen
grid=[]

#This sets up rows and collums for the grid
width=40
height=20
for y in range(height):
    row=[]
    for x in range(width):
            row.append(0)
    grid.append(row)
    
playerx=width//2
playery=height//2
grid[playery][playerx]=1

def main_loop():
    """
    This is the main game loop
    """
    running=True
    while running:
        display_grid()
        movement()
    
def movement():
    """
    Takes the inputs (W,A,S,D)
    and translates to movement
    
    this also clears the old player
    location replacing it with a new one
    """
    global playerx,playery
    grid[playery][playerx]=0
    guess=input()
    if guess=="w" or guess=="W":
        if playery>0:
            if not grid[playery-1][playerx]==2:
                if grid[playery-1][playerx]==3:
                    death()
                else:
                    playery-=1
    elif guess=="s" or guess=="S":
        if playery<height-1:
            if not grid[playery+1][playerx]==2:
                if grid[playery+1][playerx]==3:
                    death()
                else:
                    playery+=1
    elif guess=="a" or guess=="A":
        if playerx>0:
            if not grid[playery][playerx-1]==2:
                if grid[playery][playerx-1]==3:
                    death()
                else:
                    playerx-=1
    elif guess=="d" or guess=="D":
        if playerx<width-1:
            if not grid[playery][playerx+1]==2:
                if grid[playery][playerx+1]==3:
                    death()
                else:
                    playerx+=1
            
    grid[playery][playerx]=1
        
def display_grid():
    """
    Basicaly just prints out the grid row
    by row to show the screen
    """
    print("\n\n\n\n\n\n\n\n\n\n\n"*3)
    print(" "+"_"*width)
    for thing in grid:
        line="("
        for thingy in thing:
            if thingy==0:
                line+=" "
            elif thingy==1:
                line+="@"
            elif thingy==2:
                line+="#"
            elif thingy==3:
                line+="^"
            #line+=str(thingy)
        print(line+")")
    print(" "+"_"*width)
    #print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

def make_terrain():
    global grid
    #Adds some spikes
    
    #Draws the walls
    for i in range(6):
        wally=random.randrange(0,height-1)
        wallx=random.randrange(0,width-1)
        
        for i in range(23):
            if not grid[wally][wallx]==1:
                grid[wally][wallx]=2
                
            num=random.randrange(1,5)
            if num==1:
                if not wally+1>height-1:
                    wally+=1
            elif num==2:
                if not wally-1<0:
                    wally-=1
            elif num==3:
                if not wallx+1>width-1:
                    wallx+=1
            elif num==4:
                if not wallx-1<0:
                    wallx-=1
              
    for i in range(8):  
        num1=random.randrange(0,height-1)
        num2=random.randrange(0,width-1)
        if not grid[num1][num2]==1 or not grid[num1][num2]==2:
            grid[num1][num2]=3
                    
def start():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"*3)
    
    print("""
    ---------------------------------------
    MRS TAYLORS DUNGEON OF DOOM AND DESPAIR
    ---------------------------------------
          -Press any button to start-
    """)
    input()
  
def death():
    global grid,playerx,playery
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"*3)
    print("""
    ---------------------------------------
                   YOU DIED
    ---------------------------------------
          -Press any button to start-
    """)
    #print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    #print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    input()
    
    #This ceates a matrix in order to hold the information and location of things on a screen
    grid=[]
    
    #This sets up rows and collums for the grid
    for y in range(height):
        row=[]
        for x in range(width):
                row.append(0)
        grid.append(row)
        
    playerx=width//2
    playery=height//2
    grid[playery][playerx]=1
    make_terrain()
    
start()
make_terrain()

main_loop()