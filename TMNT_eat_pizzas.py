import pygame, sys, random
from pygame import mixer

mixer.init()
pygame.init()
clock = pygame.time.Clock()

WIDTH = 800
HEIGHT = WIDTH * 772//1200 #proportions of the background image
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TMNT Eats Pizza')
pygame.time.set_timer(pygame.USEREVENT, 1000) #Set a timer

#Colors
BLACK = (0, 0, 0)
RED = (255,0,0)

#constants
NEWFOOD = 60   #a new food will be placed every second
speed =6      #how fast ninja turtle moves per keydown

pickupSound = pygame.mixer.Sound("pickup.wav")
playerRect= pygame.Rect(WIDTH/2, HEIGHT/2, 40, 40)

foodImage = pygame.image.load('Pizza.png')   
playerImage = pygame.image.load("NinjaTurtle.png")
background = pygame.image.load("FortniteLair.png")

pygame.mixer.music.load("KaraiTMNTMainTheme.mp3")
pygame.mixer.music.play(-1, 0, 5000)
pygame.mixer.music.set_volume(0.5)

#functions
def setSpeed(seconds):
    """
    Returns the speed of the player based on the number of seconds that have passed
    
    Parameters:
    ----------
    seconds: int
        The number of seconds that have passed since the game started
    
    Returns:
    -------
    int
        The speed of the player"""
    if seconds < 4:
        return 6
    elif seconds < 8:
        return 8
    elif seconds < 12:
        return 10
    elif seconds < 16:
        return 12
    elif seconds < 20:
        return 14
    elif seconds < 24:
        return 16
    elif seconds < 28:
        return 18
    else:
        return 20
    

def showMessage(words, size, font, x, y, color, bg = None):
    """
    Displays a message on the screen
    
    Parameters:
    ----------
    words: str
        The message to be displayed
    size: int
        The size of the font
    font: str
        The font of the message
    x: int
        The x-coordinate of the message
    y: int
        The y-coordinate of the message
    color: tuple
        The color of the message
    bg: tuple
        The background color of the message (default is None)
    """
    
    text_font = pygame.font.SysFont(font, size, True, False)
    text = text_font.render(words, True, color, bg)
    textBounds = text.get_rect()
    textBounds.center = (x, y)
    surface.blit(text, textBounds)


def placePizza(num):
    """
    Places Pizza in the model at random locations
    
    Parameters:
    ----------
    num: int
        The number of Pizza to be placed
    
    Returns:
    -------
    Pizza
        A list of Rect objects representing the placement of Pizza
    """
    
    Pizza = []
    for _ in range(num):
        Pizza.append(pygame.Rect(random.randint(1,WIDTH-20),random.randint(1,HEIGHT-20),20,20))
    return Pizza


def eatPizza(PizzaList):
    """
    Checks if the player has intersected with any food squares and changes the player's size accordingly
    
    Parameters:
    ----------
    PizzaList: list
        A list of Rect objects representing the placement of Pizza
    
    Returns:
    -------
    None
    """
    
    # check if the block has intersected with any food squares.
    for PizzaRect in PizzaList:
        if playerRect.colliderect(PizzaRect):
            PizzaList.remove(PizzaRect)
            pickupSound.play()

            #increase size of monster
            playerRect.width +=.5
            playerRect.height +=.5
   
 
def movePlayer(keys, speed):
    """
    Moves the player based on the keys pressed and makes sure it stays within the confines of the screen

    Parameters:
    ----------
    keys: list
        A list of booleans representing which keys were pressed
    speed: int
        The speed of the player
    
    Returns:
    -------
    None
    """
    if keys[pygame.K_LEFT]:
        playerRect.left-=speed
    if keys[pygame.K_RIGHT]:
        playerRect.left+=speed
    if keys[pygame.K_UP]:
        playerRect.top-=speed
    if keys[pygame.K_DOWN]:
        playerRect.top+=speed

    #check if player hits edge of screen and move back
    if playerRect.left < 0:
        playerRect.left = 0
    if playerRect.right > WIDTH:
        playerRect.right = WIDTH
    if playerRect.top < 0:
        playerRect.top = 0
    if playerRect.bottom > HEIGHT:
        playerRect.bottom = HEIGHT
    
    
def quit():
    """
    Quits the game and closes the window
    
    Parameters:
    ----------
    None
    
    Returns:
    -------
    None
    """
    
    pygame.quit()
    sys.exit()
            

def drawScreen(Pizza, gameOver, seconds):
    """
    Draws the screen with the player, Pizza, and timer
    
    Parameters:
    ----------
    Pizza: list
        A list of Rect objects representing the placement of Pizza
    gameOver: bool
        A boolean representing whether the game is over
    seconds: int
        The number of seconds that have passed since the game started
    
    Returns:
    -------
    None
    """
    
    #scale the image
    playerStretched = pygame.transform.scale(playerImage,(playerRect.width,playerRect.height))
    backgroundShrink = pygame.transform.scale(background, (WIDTH, HEIGHT))
    pizzaShrink = pygame.transform.scale(foodImage, (WIDTH/30, WIDTH/30))
    surface.blit(backgroundShrink, (0, 0))
    showMessage("Timer: " + str(seconds), 30, "Consolas", 75, 15, RED, BLACK)
    if not gameOver:
        for PizzaRect in Pizza:
            surface.blit(pizzaShrink, PizzaRect)
    surface.blit(playerStretched,playerRect)
    
    if gameOver:
        showMessage("Game Over", 60, "Consolas", WIDTH//2, HEIGHT//2, RED)
        
        
def main():
    """
    The main function that runs the game. Where all the action happens
    
    Parameters:
    ----------
    None
    
    Returns:
    -------
    None
    """
    
    #set up game control variables
    gameOver = False
    Pizza = placePizza(80)
    food_counter =0  #will add food when divisible by 60
    seconds = 0
    
    # run the game loop
    while True:
        food_counter+=1
        if food_counter % NEWFOOD == 0:
            Pizza.append(pygame.Rect(random.randint(1,WIDTH-20),random.randint(1,HEIGHT-20),20,20))
        
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key ==pygame.K_ESCAPE or event.type == pygame.QUIT:
                quit()
            if event.type == pygame.USEREVENT:
                seconds += 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:        
                playerRect.top = random.randint(0, HEIGHT-playerRect.top)
                playerRect.left = random.randint(0, WIDTH-playerRect.left)
                
        if not gameOver:
            movePlayer(keys, setSpeed(seconds))
            eatPizza(Pizza)
            if len(Pizza)==0:
                gameOver=True
            surface.fill(BLACK)
        else:
            pygame.mixer.music.load("WinTheme.mp3")
            pygame.mixer.music.play(-1, 0, 5000)
            pygame.time.delay(9600) #9.6 seconds because thats when the next 'bang' in the wintheme.mp3 happens
            quit()

        drawScreen(Pizza,gameOver, seconds)
        pygame.display.update()
        clock.tick(40)

main()