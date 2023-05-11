# import the pygame library and initialise the game engine
import pygame, random

pygame.init()
pygame.mixer.init()

# Sounds and sound channels
jumpChannel = pygame.mixer.Channel(0)
jumpSound = pygame.mixer.Sound("sounds/jump.wav")

hitChannel = pygame.mixer.Channel(1)
hitSound = pygame.mixer.Sound("sounds/hit.wav")

passChannel = pygame.mixer.Channel(2)
passSound = pygame.mixer.Sound("sounds/pass.wav")
bounceSound = pygame.mixer.Sound("sounds/bounce.wav")

pointChannel = pygame.mixer.Channel(3)
pointSound = pygame.mixer.Sound("sounds/point.wav")

# some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (255, 0, 255)

# open new window
WIDTH, HEIGHT = 1000, 700
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Retro Volley")

# game will carry on until user exits
carryOn = True

# clock to control how fast screen updates
clock = pygame.time.Clock()

# screen shake shinenigans
screenShakeOffset = [0, 0]
screenShakeLength = 0

# stuff
GRAVITY = 1
GROUNDLEVEL = 600
NET_HEIGHT = 250
P1SCORED = False
P2SCORED = False
PAUSE_LENGTH = 0


# player class
class Player:
    def __init__(
        self,
        posx,
        posy,
        width,
        height,
        velx,
        vely,
        jumping,
        jumpPressed,
        jumpCount,
        attackPressed,
        score,
        canMove,
    ):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.velx = velx
        self.vely = vely
        self.jumping = jumping
        self.jumpPressed = jumpPressed
        self.jumpCount = jumpCount
        self.attackPressed = attackPressed
        self.score = score
        self.canMove = canMove

    def move(self, dir):
        if self.canMove:
            # move the player
            if dir == "left":
                self.velx = -10
            elif dir == "right":
                self.velx = 10

    def jump(self):
        if self.canMove:
            # make the player jump
            if self.jumpPressed and self.jumpCount < 2:
                jumpChannel.play(jumpSound)
                self.jumpCount += 1
                self.jumping = True
                self.vely = -20
                return

    def draw(self):
        # draw the player
        pygame.draw.rect(
            screen,
            WHITE,
            [
                self.posx + screenShakeOffset[0],
                self.posy + screenShakeOffset[1],
                self.width,
                self.height,
            ],
        )


# create the players
p1 = Player(50, 600, 50, 50, 0, 0, False, False, 0, False, 0, False)
p2 = Player(WIDTH - 100, 600, 50, 50, 0, 0, False, False, 0, False, 0, True)


class Ball:
    def __init__(
        self, posx, posy, velx, vely, size, p1Attacking, p2Attacking, serving, canTouch
    ):
        self.posx = posx
        self.posy = posy
        self.velx = velx
        self.vely = vely
        self.size = size
        self.p1Attacking = p1Attacking
        self.p2Attacking = p2Attacking
        self.serving = serving
        self.canTouch = canTouch

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

    def bumpHor(self, playerVelx):
        # bump the ball horizontally
        if playerVelx == 0:
            self.velx = 0
        elif not playerVelx == 0:
            self.velx = playerVelx * 1.4

        return

    def attack(self, player):
        hitChannel.play(hitSound)
        if player == p1:
            self.posx += 50
            self.velx = 40
        elif player == p2:
            self.posx -= 50
            self.velx = -40

        self.vely = 20

    def serve(self, player):
        self.serving = True
        self.velx = 0
        self.vely = 0
        if player == p1:
            p1.posx = 50
            p1.posy = HEIGHT - 100
            p1.canMove = False
            p2.canMove = True
            self.posx = 100
            self.posy = HEIGHT - 200
        elif player == p2:
            p2.posx = WIDTH - 100
            p2.posy = HEIGHT - 100
            p1.canMove = True
            p2.canMove = False
            self.posx = WIDTH - 100
            self.posy = HEIGHT - 200

    def draw(self):
        pygame.draw.circle(
            screen,
            WHITE,
            [self.posx + screenShakeOffset[0], self.posy + screenShakeOffset[1]],
            self.size,
        )


ball = Ball(700, 50, 0, 0, 25, False, False, True, True)

ball.serve(p1)


# restarts after a point
def restart(playerScored):
    screenShakeOffset[0] = 0
    screenShakeOffset[1] = 0

    ball.canTouch = True

    if playerScored == p1:
        ball.serve(p1)
    elif playerScored == p2:
        ball.serve(p2)


# particles
particles = []


def createParticles(
    posx, posy, minVelx, maxVelx, minVely, maxVely, minSize, maxSize, amount
):
    for i in range(amount):
        particles.append(
            [
                [posx, posy],
                [random.randint(minVelx, maxVelx), random.randint(minVely, maxVely)],
                random.randint(minSize, maxSize),
            ]
        )


# text
# ALLFONTS = pygame.font.get_fonts() # for testing fonts

scoreFont = pygame.font.SysFont(None, 150)
messageFont = pygame.font.SysFont(None, 50)

p1ScoredRect = messageFont.render("Player 1 scored!", True, WHITE)
p2ScoredRect = messageFont.render("Player 2 scored!", True, WHITE)

# main Game Loop
while carryOn:
    # Time between scoring a point and next serve
    if PAUSE_LENGTH > 0:
        PAUSE_LENGTH -= 1

    if screenShakeLength > 0:
        screenShakeLength -= 1
        screenShakeOffset[0] = random.randint(-10, 10)
        screenShakeOffset[1] = random.randint(-10, 10)
    elif screenShakeLength == 0:
        screenShakeOffset[0] = 0
        screenShakeOffset[1] = 0

    # ---- check for user inputs ----

    for event in pygame.event.get():  # user did something
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

        # attacking
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f and ball.canTouch:
                if ball.serving and not p1.canMove:
                    ball.velx = 15
                    ball.vely = -25
                    ball.serving = False
                    p1.canMove = True
                elif (
                    ball.posx + ball.velx + ball.size >= p1.posx + p1.width / 1.5
                    and ball.posx + ball.velx - ball.size <= p1.posx + p1.width * 1.5
                    and ball.posy + ball.vely + ball.size >= p1.posy - p1.height
                    and ball.posy + ball.vely - ball.size <= p1.posy + p1.height * 1.5
                ):
                    screenShakeLength = 10
                    ball.p1Attacking = True
                    ball.attack(p1)
            if event.key == pygame.K_l and ball.canTouch:
                if ball.serving and not p2.canMove:
                    ball.velx = -15
                    ball.vely = -25
                    ball.serving = False
                    p2.canMove = True
                elif (
                    ball.posx + ball.velx + ball.size
                    >= p2.posx - p2.width / 1.5 - p2.width / 2
                    and ball.posx + ball.velx - ball.size <= p2.posx + p2.width * 1.5
                    and ball.posy + ball.vely + ball.size >= p2.posy - p2.height
                    and ball.posy + ball.vely - ball.size <= p2.posy + p2.height * 1.5
                ):
                    screenShakeLength = 10
                    ball.p1Attacking = True
                    ball.attack(p2)

    # ---- main game logic ----

    if not ball.serving:
        ball.vely += GRAVITY

    # ground check

    if ball.posy + ball.size >= 600:
        # if the ball is on the left side of the court give player 2 the point, otherwise give player 1 the point
        if ball.posx < WIDTH / 2 and ball.canTouch:
            PAUSE_LENGTH = 120
            pointChannel.play(pointSound)
            ball.canTouch = False
            p2.score += 1
            print("Score: " + str(p1.score) + " : " + str(p2.score))
            P2SCORED = True
            p1.canMove = False
        elif ball.posx > WIDTH / 2 and ball.canTouch:
            PAUSE_LENGTH = 120
            pointChannel.play(pointSound)
            ball.canTouch = False
            p1.score += 1
            print("Score: " + str(p1.score) + " : " + str(p2.score))
            P1SCORED = True
            p2.canMove = False
        else:
            passChannel.play(bounceSound)

        print(int(ball.vely) * 3)

        createParticles(
            ball.posx,
            ball.posy + ball.size,
            -6,
            6,
            int(ball.vely / -5),
            0,
            2,
            5,
            int(ball.vely) * 5,
        )
        ball.posy = 600 - ball.size
        ball.vely *= -0.7

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

    # bounce off players
    # player 1
    if (
        ball.posx + ball.size > p1.posx
        and ball.posx - ball.size < p1.posx + p1.width
        and ball.posy + ball.size + ball.vely / 2 >= p1.posy
        and ball.posy - ball.size < p1.posy + p1.height
        and ball.canTouch
    ):
        ball.bumpVert(p1.velx, p1.vely, p1.jumping)
        passChannel.play(passSound)

    if (
        ball.posx + ball.size >= p1.posx
        and ball.posy + ball.size + ball.vely / 2 >= p1.posy
        and ball.posy - ball.size < p1.posy + p1.height
        and ball.posx < p1.posx + p1.width
        or ball.posx - ball.size <= p1.posx + p1.width
        and ball.posy + ball.size + ball.vely / 2 >= p1.posy
        and ball.posy - ball.size < p1.posy + p1.height
        and ball.posx > p1.posx
        and ball.canTouch
    ):
        ball.bumpHor(p1.velx)
        passChannel.play(passSound)

    # player 2
    if (
        ball.posx + ball.size > p2.posx
        and ball.posx - ball.size < p2.posx + p2.width
        and ball.posy + ball.size + ball.vely / 2 >= p2.posy
        and ball.posy - ball.size < p2.posy + p2.height
        and ball.canTouch
    ):
        ball.bumpVert(p2.velx, p2.vely, p2.jumping)
        passChannel.play(passSound)

    if (
        ball.posx + ball.size >= p2.posx
        and ball.posy + ball.size + ball.vely / 2 >= p2.posy
        and ball.posy - ball.size < p2.posy + p2.height
        and ball.posx < p2.posx + p2.width
        or ball.posx - ball.size <= p2.posx + p2.width
        and ball.posy + ball.size + ball.vely / 2 >= p2.posy
        and ball.posy - ball.size < p2.posy + p2.height
        and ball.posx > p2.posx
        and ball.canTouch
    ):
        ball.bumpHor(p2.velx)
        passChannel.play(passSound)

    # bounce off net
    if (
        ball.posx + ball.size + ball.velx >= WIDTH / 2 - 5
        and ball.posx + ball.size < WIDTH / 2 + 5 + ball.velx
        and ball.posy + ball.size >= HEIGHT - NET_HEIGHT
    ):
        ball.velx *= -0.3
        passChannel.play(bounceSound)

    if (
        ball.posx - ball.size + ball.velx <= WIDTH / 2 + 5
        and ball.posx - ball.size > WIDTH / 2 - 5 + ball.velx
        and ball.posy + ball.size >= HEIGHT - NET_HEIGHT
    ):
        ball.velx *= -0.3
        passChannel.play(bounceSound)

    if (
        ball.posy + ball.size >= HEIGHT - NET_HEIGHT
        and ball.posy + ball.size < HEIGHT - NET_HEIGHT + 20
        and ball.posx + ball.size >= WIDTH / 2 - 5
        and ball.posx - ball.size <= WIDTH / 2 + 5
    ):
        ball.vely *= -0.8
        passChannel.play(bounceSound)

    # ball boing boing
    if (
        ball.posx + ball.size + ball.velx >= WIDTH
        or ball.posx - ball.size + ball.velx <= 0
    ):
        ball.velx *= -0.7
        passChannel.play(bounceSound)

    # update position of player 1
    if p1.posx + p1.velx >= 0 and p1.posx + p1.width + p1.velx <= WIDTH / 2 - 5:
        p1.posx += p1.velx
    p1.posy += p1.vely

    # update position of player 2
    if p2.posx + p2.velx + p2.width <= WIDTH and p2.posx + p2.velx >= WIDTH / 2 + 5:
        p2.posx += p2.velx
    p2.posy += p2.vely

    # ---- draw onto screen ----

    # first clear the screen
    screen.fill(BLACK)

    # draw particles
    for particle in particles:
        particle[0][0] += particle[1][0]  # x
        particle[0][1] += particle[1][1]  # y
        particle[2] -= 0.1
        particle[1][1] += GRAVITY / 2
        pygame.draw.circle(screen, WHITE, particle[0], int(particle[2]))
        if particle[2] <= 0:
            particles.remove(particle)

    # draw stuff
    p1.draw()
    p2.draw()
    ball.draw()

    p1ScoreRect = scoreFont.render(str(p1.score), True, WHITE)
    p2ScoreRect = scoreFont.render(str(p2.score), True, WHITE)

    screen.blit(p1ScoreRect, (WIDTH * 1 / 4, 20))
    screen.blit(p2ScoreRect, (WIDTH * 3 / 4, 20))

    if P1SCORED:
        screen.blit(
            p1ScoredRect,
            (
                WIDTH / 2 - p1ScoredRect.get_width() / 2,
                HEIGHT / 2 - p1ScoredRect.get_height() / 2 - 100,
            ),
        )
    elif P2SCORED:
        screen.blit(
            p2ScoredRect,
            (
                WIDTH / 2 - p2ScoredRect.get_width() / 2,
                HEIGHT / 2 - p2ScoredRect.get_height() / 2 - 100,
            ),
        )

    # hitboxes for debuggin and stuff
    # pygame.draw.rect(screen, PURPLE, [p1.posx + p1.width/1.5, p1.posy - p1.height - 10, p1.width*1.5, p1.height*1.5])
    # pygame.draw.rect(screen, PURPLE, [p2.posx - p2.width/1.5 - p2.width/2, p2.posy - p2.height - 10, p2.width*1.5, p2.height*1.5])

    # ground and net
    pygame.draw.rect(
        screen,
        WHITE,
        [
            0 + screenShakeOffset[0] - 50,
            HEIGHT - 100 + screenShakeOffset[1],
            WIDTH + 100,
            200,
        ],
    )
    pygame.draw.rect(
        screen,
        WHITE,
        [
            WIDTH / 2 - 5 + screenShakeOffset[0],
            HEIGHT - NET_HEIGHT + screenShakeOffset[1],
            10,
            NET_HEIGHT,
        ],
    )

    # update screen
    pygame.display.flip()

    if P1SCORED and PAUSE_LENGTH == 0:
        restart(p1)
        P1SCORED = False
    elif P2SCORED and PAUSE_LENGTH == 0:
        restart(p2)
        P2SCORED = False

    # update position ball
    ball.posx += ball.velx
    ball.posy += ball.vely

    # limit to 60fps
    clock.tick(60)

pygame.quit()
