# import the pygame library and initialise the game engine
import pygame
pygame.init()

# some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (150, 150, 150)

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
GROUNDLEVEL = 600

# player class
class Player:
    def __init__(self, posx, posy, width, height, velx, vely, jumping, jumpPressed):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
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

            self.vely = -20

    def draw(self):
        # draw the player
        pygame.draw.rect(screen, GREY, [self.posx, self.posy, self.width, self.height])

            
# platform class
class Platform:
    def __init__(self, posx, posy, width, height):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height

    def draw(self):
        pygame.draw.rect(screen, BLACK, [self.posx, self.posy, self.width, self.height])
        

p1 = Player(300, 600, 50, 50, 0, 0, False, False)

thing = Platform(500, 500, 100, 20)

platforms = [thing]

# main Game Loop
while carryOn:

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

    # check current ground level
    for platform in platforms:
        if(p1.posx + p1.width > platform.posx and
           p1.posx < platform.posx + platform.width and
           p1.posy + p1.height - GRAVITY <= platform.posy):
            GROUNDLEVEL = platform.posy
        elif (GROUNDLEVEL == 600 and not p1.jumping and p1.posy + p1.height < GROUNDLEVEL):
            p1.jumping = True
        else:
            GROUNDLEVEL = 600

    # gravity
    if p1.posy + p1.height > GROUNDLEVEL:
        p1.jumping = False
        p1.posy = GROUNDLEVEL - p1.height
        p1.vely = 0

    if p1.jumping:
        p1.vely += GRAVITY


    # update position of player
    p1.posx += p1.velx
    p1.posy += p1.vely
    
    # -- draw onto screen

    # first clear the screen
    screen.fill(WHITE)

    # draw stuff
    p1.draw()
    thing.draw()
   

    # ground
    pygame.draw.rect(screen, BLACK, [0, 600, WIDTH, 100])

    # update screen
    pygame.display.flip()

    # limit to 60fps
    clock.tick(60)

pygame.quit()