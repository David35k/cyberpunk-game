# import the pygame library and initialise the game engine
import pygame
pygame.init()

# some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (150, 150, 150)
YELLOW = (255, 255, 0)

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
        # move the player
        if dir == "left":
            self.velx = -10
        elif dir == "right":
            self.velx = 10

    def jump(self):
        # make the player jump
        if self.jumpPressed:
            self.jumping = True

            self.vely = -20

    def draw(self):
        # draw the player
        pygame.draw.rect(screen, GREY, [self.posx, self.posy, self.width, self.height])

# create the players
p1 = Player(200, 600, 50, 50, 0, 0, False, False)
p2 = Player(400, 600, 50, 50, 0, 0, False, False)

class Ball:
    def __init__(self, posx, posy, velx, vely, size):
        self.posx = posx
        self.posy = posy
        self.velx = velx
        self.vely = vely
        self.size = size

    def bump(self):
        # bump the ball up
        self.vely = -20
    
    def draw(self):
        pygame.draw.circle(screen, YELLOW, [self.posx, self.posy], self.size)

        
ball = Ball(200, 200, 0, 0, 25)

# main Game Loop
while carryOn:

    # ---- check for user inputs ----

    for event in pygame.event.get(): #user did something
        if event.type == pygame.QUIT:
            carryOn = False

        # player 1 movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                p1.move("left")
            if event.key == pygame.K_d:
                p1.move("right")
            if event.key == pygame.K_w and not p1.jumping:
                p1.jumpPressed = True
                p1.jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                while p1.velx < 0:
                    p1.velx += 5
            if event.key == pygame.K_d:
                while p1.velx > 0:
                    p1.velx -= 5
            if event.key == pygame.K_w:
                p1.jumpPressed = False

        # player 2 movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                p2.move("left")
            if event.key == pygame.K_RIGHT:
                p2.move("right")
            if event.key == pygame.K_UP and not p2.jumping:
                p2.jumpPressed = True
                p2.jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                while p2.velx < 0:
                    p2.velx += 5
            if event.key == pygame.K_RIGHT:
                while p2.velx > 0:
                    p2.velx -= 5
            if event.key == pygame.K_UP:
                p2.jumpPressed = False

    # ---- main game logic ----

    print(ball.posy)

    # gravity players
    if p1.posy + p1.height > 600:
        p1.jumping = False
        p1.posy = 600 - p1.height
        p1.vely = 0

    if p2.posy + p2.height > 600:
        p2.jumping = False
        p2.posy = 600 - p2.height
        p2.vely = 0

    if p1.jumping:
        p1.vely += GRAVITY

    if p2.jumping:
        p2.vely += GRAVITY

    # gravity ball

    if ball.posy + ball.size > 600:
        ball.posy = 600 - ball.size
        ball.vely *= -0.9

    ball.vely += GRAVITY

    # update position of player 1
    if p1.posx + p1.velx >= 0 and p1.posx + p1.width + p1.velx <= WIDTH / 2:
        p1.posx += p1.velx
    p1.posy += p1.vely
    
    # update position of player 2
    if p2.posx + p2.velx + p2.width <= WIDTH and p2.posx + p2.velx >= WIDTH / 2:
        p2.posx += p2.velx
    p2.posy += p2.vely

    # update position ball
    ball.posx += ball.velx
    ball.posy += ball.vely
    
    # ---- draw onto screen ----

    # first clear the screen
    screen.fill(WHITE)

    # draw stuff
    p1.draw()
    p2.draw()
    ball.draw()

    # ground
    pygame.draw.rect(screen, BLACK, [0, HEIGHT - 100, WIDTH, 100])

    # update screen
    pygame.display.flip()

    # limit to 60fps
    clock.tick(60)

pygame.quit()