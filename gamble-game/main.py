import pygame,random

money=100

def generate_random():
    global money
    print(f"You have ${money}")
    if money>=10:
        input("Play? ($10)")
        money-=10
        num=random.randrange(1,100)
        if num==1:
            prize=100
        if num>=2 and num<=10:
            prize=25
        if num>10 and num<=45:
            prize=10
        else:
            prize=0

        print(f"You won ${prize}")
    else:
        print("You lose")
        input()
        money=100
