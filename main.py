# import the pygame library and initialise the game engine
import pygame
pygame.init()

# some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# open new window
size = (700, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("FIRST GAME IN PYTHON!!!")

# game will carry on until user exits
carryOn = True

# clock to control how fast screen updates
clock = pygame.time.Clock()

# main Game Loop
while carryOn:
    # check for user inputs
    for event in pygame.event.get(): #user did something
        if event.type == pygame.QUIT:
            carryOn = False
    # main game logic
    
    # draw onto screen

    # first clear the screen
    screen.fill(WHITE)

    # draw stuff
    pygame.draw.rect(screen, BLACK, [50, 50, 100, 100], 0)

    # update screen
    pygame.display.flip()

    # limit to 60fps
    clock.tick(60)

pygame.quit()