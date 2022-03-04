import pygame, sys
import random, math, time
pygame.init()

# formatting variables
size = width, height = 1000, 680
white = pygame.Color(255, 255, 255)


# fps
fps = 228
clock = pygame.time.Clock()

# images
spaceship_1 = pygame.image.load('spaceship_1.png')
space = pygame.image.load('space.gif')
bullet = pygame.image.load('bullet.png')
bullet = pygame.transform.scale(bullet, (50, 50))
bullet = pygame.transform.rotate(bullet, 45)
enemyBullet = pygame.image.load('lightning.png')


# window
space = pygame.transform.scale(space, size) # transform.scale = resizing
screen = pygame.display.set_mode(size)
position = [450, 550] # position = (x, y)

# movement
nextDirection = None
check = "go"
key = 0

# functions
def showStatus(status):
    # Frame logic
    font = pygame.font.SysFont('ariel',40)
    test = font.render(f'Status : {status}', True, white)
    rect = test.get_rect()
    rect.midtop = (20,20)
    screen.blit(test,rect)
    pygame.display.update()

def blitAliens(x,y,i):
    screen.blit(pygame.transform.rotate(enemyImg[i], 180), (x,y))

def kaboom(ex, ey, bx, by):
    distance = math.sqrt(math.pow(ex - bx, 2) + (math.pow(ey - by, 2)))

    if distance < 30:
        return True
    
    else:
        return False

# state = 'fire' / 'ready'
def bullets_fire(x, y):
    screen.blit(bullet, (x,y))

state = 'ready'
font = pygame.font.SysFont('ariel',70)
white = pygame.Color(255,255,255)

def gameOver():
    text = font.render('Game Over',True,white)
    screen.blit(text,(width/4,height/2))


def enemyFire(x, y):
    screen.blit(enemyBullet, (x, y)) 

enemyState = True


enemyImg = []
enemyX  = []
enemyY = []
enemyX_change = [] # Changes every time
enemyY_change = [] # Changes after every oscillation.
num_of_enemies = 10

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    
    enemyX.append(random.randrange(50, width - 100, 50))
    enemyY.append(random.randrange(50, 150, 30))
    enemyX_change.append(2) # [4,4,4,4,4]
    enemyY_change.append(10)

"""
speed = 0.1

going left -> alien[0] < 0
speed * -1
going right -> alien[-1] > width -20
speed * -1

"""
bulletX = 0
bulletY = 550

while True:
    # printing
    screen.fill(white)
    screen.blit(space, (0, 0)) 
    screen.blit(spaceship_1, position)

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            check = 'go'
            key = event.key
            
            if event.key == pygame.K_LEFT:
                nextDirection = 'LEFT'
                
            if event.key == pygame.K_RIGHT:
                nextDirection = 'RIGHT'
            
            if event.key == pygame.K_SPACE:
                if state == 'ready':
                    bulletX = position[0]

                    state = "fire"
                    
                

        if event.type == pygame.KEYUP:
            check = 'stop'

    
    if state == 'fire':
        bullets_fire(bulletX, bulletY)
        bulletY -= 3

    if bulletY <= 0: 
        bulletY = 550
        state = "ready"

    
    if nextDirection == 'RIGHT' and check != 'stop' and borderRight == False and key == 1073741903:
        position[0] += 3

    if nextDirection == 'LEFT' and check != 'stop' and borderLeft == False and key == 1073741904:
        position[0] -= 3
    
      
    if position[0] < 0 + 50:
        borderLeft = True
    
    else:
        borderLeft = False
    
    if position[0] > width - 100: 
        borderRight = True 
    
    else:
        borderRight = False
    
    # Enemies Movements
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 50:
            enemyX_change[i] = 2

            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= width - 100:
            enemyX_change[i] = -2

            enemyY[i] += enemyY_change[i]
        
        elif enemyY[i] >= 520:
            state = ""
            gameOver()

            print(enemyY[i])

        blitAliens(enemyX[i],enemyY[i],i)
        
        # num_of_connect = 0

        if kaboom(enemyX[i], enemyY[i], bulletX, bulletY): 
            print("KABOOM!")

            # num_of_enemies -= 1
            # num_of_connect += 1

            enemyX[i] = 20000
            enemyY[i] = -100000

            bulletY = 550
            state = "ready"
    
    enemybulletX = random.choice(enemyX)
    enemybulletY = random.choice(enemyY)


    if enemyState:
        enemyFire(enemybulletX, enemybulletY)
        enemybulletY += 3

    # refresh
    clock.tick(fps)
    pygame.display.update()
