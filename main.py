# import the pygame library and initialise the game engine
import pygame
pygame.init()

# some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (150, 150, 150)
YELLOW = (246, 190, 0)

# open new window
WIDTH, HEIGHT = 700, 700
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("VOLLEYBALL GAME!!!!!")

# game will carry on until user exits
carryOn = True

# clock to control how fast screen updates
clock = pygame.time.Clock()

# stuff
GRAVITY = 1
GROUNDLEVEL = 600
NET_HEIGHT = 250

# player class
class Player:
    def __init__(self, posx, posy, width, height, velx, vely, jumping, jumpPressed, jumpCount):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.velx = velx
        self.vely = vely
        self.jumping = jumping
        self.jumpPressed = jumpPressed
        self.jumpCount = jumpCount

    def move(self, dir):
        # move the player
        if dir == "left":
            self.velx = -10
        elif dir == "right":
            self.velx = 10

    def jump(self):
        # make the player jump
        if self.jumpPressed and self.jumpCount < 2:
            self.jumpCount += 1
            self.jumping = True

            self.vely = -20
            return

    def draw(self):
        # draw the player
        pygame.draw.rect(screen, GREY, [self.posx, self.posy, self.width, self.height])

# create the players
p1 = Player(200, 600, 50, 50, 0, 0, False, False, 0)
p2 = Player(400, 600, 50, 50, 0, 0, False, False, 0)

class Ball:
    def __init__(self, posx, posy, velx, vely, size, pressing):
        self.posx = posx
        self.posy = posy
        self.velx = velx
        self.vely = vely
        self.size = size
        self.pressing = pressing

    def bumpVert(self, playerVelx, playerVely, playerJumping):
        # bump the ball vertically
        if playerVely == 0 and not playerJumping:
            self.vely = -25
            self.velx = playerVelx * 0.3
        elif playerVely < 0:
            self.vely = playerVely * 1.6
            self.velx = playerVelx * 0.3
        else:
            self.vely = -5
            self.velx = playerVelx * 0.3

    def bumpHor(self, playerVelx, playerVely):
        # bump the ball horizontally
        if playerVelx == 0:
            self.velx = 0
        elif not playerVelx == 0:
            self.velx = playerVelx * 1.5

        return

    def boing(self) :
        if self.pressing:
            self.velx += 10
    
    def draw(self):
        pygame.draw.circle(screen, YELLOW, [self.posx, self.posy], self.size)

        
ball = Ball(350, 50, 0, 0, 25, False)

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
            if event.key == pygame.K_w:
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
            if event.key == pygame.K_UP:
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

        # random ball stuff lawl
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball.pressing = True
                ball.boing()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                ball.pressing = False

    # ---- main game logic ----

    # gravity players
    if p1.posy + p1.height > 600:
        p1.jumping = False
        p1.jumpCount = 0
        p1.posy = 600 - p1.height
        p1.vely = 0

    if p2.posy + p2.height > 600:
        p2.jumping = False
        p2.jumpCount = 0
        p2.posy = 600 - p2.height
        p2.vely = 0

    if p1.jumping:
        p1.vely += GRAVITY

    if p2.jumping:
        p2.vely += GRAVITY

    # gravity ball
    if ball.posy + ball.size >= 600:
        ball.posy = 600 - ball.size
        ball.vely *= -0.9
    
    ball.vely += GRAVITY

    # bounce off players
    # player 1
    if ball.posx + ball.size > p1.posx and ball.posx - ball.size < p1.posx + p1.width and ball.posy + ball.size + ball.vely / 2  >= p1.posy and ball.posy - ball.size < p1.posy + p1.height:
        ball.bumpVert(p1.velx, p1.vely, p1.jumping)
    
    if ball.posx + ball.size >= p1.posx and ball.posy + ball.size + ball.vely / 2  >= p1.posy and ball.posy - ball.size < p1.posy + p1.height and ball.posx < p1.posx + p1.width or ball.posx - ball.size <= p1.posx + p1.width and ball.posy + ball.size + ball.vely / 2  >= p1.posy and ball.posy - ball.size < p1.posy + p1.height and ball.posx > p1.posx:
         ball.bumpHor(p1.velx, p1.vely)

    # player 2
    if ball.posx + ball.size > p2.posx and ball.posx - ball.size < p2.posx + p2.width and ball.posy + ball.size + ball.vely / 2  >= p2.posy and ball.posy - ball.size < p2.posy + p2.height:
        ball.bumpVert(p2.velx, p2.vely, p2.jumping)
    
    if ball.posx + ball.size >= p2.posx and ball.posy + ball.size + ball.vely / 2  >= p2.posy and ball.posy - ball.size < p2.posy + p2.height and ball.posx < p2.posx + p2.width or ball.posx - ball.size <= p2.posx + p2.width and ball.posy + ball.size + ball.vely / 2  >= p2.posy and ball.posy - ball.size < p2.posy + p2.height and ball.posx > p2.posx:
         ball.bumpHor(p2.velx, p2.vely)

    # bounce off net
    if ball.posx + ball.size + ball.velx >= WIDTH / 2 - 5 and ball.posx + ball.size < WIDTH / 2 + 5 + ball.velx and ball.posy + ball.size >= HEIGHT - NET_HEIGHT:
        ball.velx *= -0.3
    
    if ball.posx - ball.size + ball.velx <= WIDTH / 2 + 5 and ball.posx - ball.size > WIDTH / 2 - 5 + ball.velx and ball.posy + ball.size >= HEIGHT - NET_HEIGHT:
        ball.velx *= -0.3

    if ball.posy + ball.size >= HEIGHT - NET_HEIGHT and ball.posy + ball.size < HEIGHT - NET_HEIGHT + 20 and ball.posx + ball.size >= WIDTH / 2 - 5 and ball.posx - ball.size <= WIDTH / 2 + 5:
        ball.vely *= -0.4

    # ball boing boing
    if ball.posx + ball.size + ball.velx >= WIDTH or ball.posx - ball.size + ball.velx <= 0:
        ball.velx *= -0.7

    # update position of player 1
    if p1.posx + p1.velx >= 0 and p1.posx + p1.width + p1.velx <= WIDTH / 2 - 5:
        p1.posx += p1.velx
    p1.posy += p1.vely
    
    # update position of player 2
    if p2.posx + p2.velx + p2.width <= WIDTH and p2.posx + p2.velx >= WIDTH / 2 + 5:
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

    # ground and net
    pygame.draw.rect(screen, BLACK, [0, HEIGHT - 100, WIDTH, 100])
    pygame.draw.rect(screen, BLACK, [WIDTH / 2 - 5, HEIGHT - NET_HEIGHT, 10, NET_HEIGHT])

    # update screen
    pygame.display.flip()

    # limit to 60fps
    clock.tick(60)

pygame.quit()