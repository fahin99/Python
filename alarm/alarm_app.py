import pygame

pygame.init()
    
#display
screen=pygame.display.set_mode((400, 300))
    
#title and icon
pygame.display.set_caption("Alarm Clock")
icon=pygame.image.load('clock.png')
pygame.display.set_icon(icon)
    
#playing alarm for testing
watch=pygame.image.load('clock_bg.png')
clx=170
cly=105
def draw(x, y):
    screen.blit(watch, (x, y))
#game loop
running=True
while running:
    screen.fill((95, 150, 138))
    draw(clx)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        
    pygame.display.update()