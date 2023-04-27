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

# stuff
GRAVITY = 1

# player class
class Player:
    def __init__(self, posx, posy, velx, vely, jumping, jumpPressed):
        self.posx = posx
        self.posy = posy
        self.velx = velx
        self.vely = vely
        self.jumping = jumping
        self.jumpPressed = jumpPressed

    def move(self, dir):
        if dir == "left":
            self.velx = -10
        elif dir == "right":
            self.velx = 10

    def jump(self):
        if self.jumpPressed:
            self.jumping = True

            self.vely = -10
            

p1 = Player(300, 600, 0, 0, False, False)

# main Game Loop
while carryOn:

    print(p1.jumping)

    # -- check for user inputs
    for event in pygame.event.get(): #user did something
        if event.type == pygame.QUIT:
            carryOn = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                p1.move("left")
            if event.key == pygame.K_RIGHT:
                p1.move("right")
            if event.key == pygame.K_UP and not p1.jumping:
                p1.jumpPressed = True
                p1.jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                while p1.velx < 0:
                    p1.velx += 5
            if event.key == pygame.K_RIGHT:
                while p1.velx > 0:
                    p1.velx -= 5
            if event.key == pygame.K_UP:
                p1.jumpPressed = False



    # -- main game logic

    # gravity
    if p1.posy > 600:
        p1.jumping = False
        p1.posy = 600

    if p1.jumping:
        p1.vely += GRAVITY


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