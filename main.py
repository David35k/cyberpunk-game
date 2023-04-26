# import the pygame library and initialise the game engine
import pygame
pygame.init()

# some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# open new window
WIDTH, HEIGHT = 700, 700
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("FIRST GAME IN PYTHON!!!")

# game will carry on until user exits
carryOn = True

# clock to control how fast screen updates
clock = pygame.time.Clock()

# player class
class Player:
    def __init__(self, posx, posy, velx, vely):
        self.posx = posx
        self.posy = posy
        self.velx = velx
        self.vely = vely

    def move(self, dir):
        if dir == "left":
            self.velx = -10
        elif dir == "right":
            self.velx = 10

    # def stop(self):
    #     self.velx = 0
            

p1 = Player(50, 50, 0, 0)

# main Game Loop
while carryOn:
    # -- check for user inputs
    for event in pygame.event.get(): #user did something
        if event.type == pygame.QUIT:
            carryOn = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                p1.move("left")
            if event.key == pygame.K_d:
                p1.move("right")

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                p1.velx = 0
            if event.key == pygame.K_d:
                p1.velx = 0



    # -- main game logic

    # gravity


    # update position of player
    p1.posx += p1.velx
    p1.posy += p1.vely
    
    # -- draw onto screen

    # first clear the screen
    screen.fill(WHITE)

    # draw stuff
    pygame.draw.rect(screen, BLACK, [p1.posx, p1.posy, 50, 50])

    # update screen
    pygame.display.flip()

    # limit to 60fps
    clock.tick(60)

pygame.quit()