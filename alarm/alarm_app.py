import pygame
import time
import datetime
import winsound

pygame.init()
    
#display
screen=pygame.display.set_mode((400, 300))
    
#title and icon
pygame.display.set_caption("Alarm Clock")
icon=pygame.image.load('clock.png')
pygame.display.set_icon(icon)
    
#playing alarm for testing
watch=pygame.image.load('clock_bg.png')
clx=200
cly=105
def draw(x, y):
    screen.blit(watch, (x, y))
#game loop
running=True
speed=0.02
direction = -1
while running:
    screen.fill((95, 150, 138))
    clx += speed * direction
    if clx<=150:
        direction=1
    elif clx>=250:
        direction=-1
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    draw(clx,cly)  
    pygame.display.update()