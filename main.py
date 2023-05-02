
# Program: Single player snake game
# Library with PyGame functions
import pygame
import random
# Define constants (in CAPITALS!) for our game settings
MAX_X = 640  # Define the size of the game display window in pixels
MAX_Y = 640
TILE_SIZE = 16  # Define the size in pixels of each tile in the game (same size as snake and apple)
FPS = 15  # Set the frames per second (refresh rate)
# Define constants for colours in (r,g,b)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
# Get PyGame initialised
pygame.init()
# Setup surface / canvas (Entered as a Tuple () - return pygame object
display = pygame.display.set_mode((MAX_X, MAX_Y))
# Define clock
clock = pygame.time.Clock()
#other things
backimg = pygame.image.load('back.png')
#make score
font = pygame.font.Font(None, 36)


class Snake:
    x = MAX_X / 2
    y = MAX_Y / 2
    ychange = 0
    xchange = 0
    direction = "right"
    img = pygame.image.load("snek.png").convert_alpha()
    body = pygame.image.load("snekback.png")
    end = pygame.image.load("snekend.png")
    tail = []
    taildirect =[]

class apple:
    x = random.randint(1, 40) * 16
    y = random.randint(1, 40) * 16
    img = pygame.image.load('apple.png').convert_alpha()

class Game:
    # States are "intro", "playing", "paused", "game_over", "quit"
    state = "intro"
    score = int(0)

def applechange():
    apple.x = random.randint(1, 39) * 16
    apple.y = random.randint(1, 39) * 16

def draw_text(text, colour, y_displace=0, size=24):
    font = pygame.font.SysFont("comicsanms", size)  # Generate the font at the specified size (24 is smallish, 48 is medium, 80 for titles)

    text_surface = font.render(text, True, colour)  # Get the surface containing the actual message drawn in the right colour
    text_rect = text_surface.get_rect()  # Get the rectangle the text is drawn in
    text_rect.center = (MAX_X / 2), (MAX_Y / 2) + y_displace  # Setup the centre point adjusted by the y_displace

    display.blit(text_surface, text_rect)  # Place the text on the display

def intro():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.state = "quit"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Game.state = "quit"
            elif event.key == pygame.K_RETURN:
                Game.state = 'playing'
    
    display.fill(BLACK)
    draw_text("SNEK", GREEN, -100, 72)
    draw_text("ENTER:START", GREEN, 200, 32)
    draw_text("ESC:EXIT", GREEN, 233, 32)
    
    

# Handle all the events while the game is being played
def game_events():
    for event in pygame.event.get():  # Loop through each event this frame
        if event.type == pygame.QUIT:  # Respond to clicking the quit button
            Game.state = "quit"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                Snake.ychange = -TILE_SIZE
                Snake.xchange = 0
                Snake.direction = 'up'
            if event.key == pygame.K_s:
                Snake.ychange = TILE_SIZE
                Snake.xchange = 0
                Snake.direction = 'down'
            if event.key == pygame.K_a:
                Snake.ychange = 0
                Snake.xchange = -TILE_SIZE
                Snake.direction = 'left'
            if event.key == pygame.K_d:
                Snake.ychange = 0
                Snake.xchange = TILE_SIZE
                Snake.direction = 'right'

# Run the game logic for each frame: move elements, check collisions etc.
def game_update():
    Snake.tail.append((Snake.x, Snake.y))
    Snake.x += Snake.xchange
    Snake.y += Snake.ychange
    if apple.x == Snake.x and apple.y == Snake.y:
        applechange()
        Game.score += int(1)
    else:
        Snake.tail.pop(0)
        Snake.taildirect.append((Snake.xchange, Snake.ychange))
    print(Snake.tail)
    
    if Snake.x < 0 or Snake.x > 640 or Snake.y < 0 or Snake.y > 640:
        Game.state = "game_over"

    if (Snake.x, Snake.y) in Snake.tail:
        Game.state = "game_over"
        print('e')
def game_over():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.state = "quit"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Game.state = "quit"
            elif event.key == pygame.K_RETURN:
                restart()

    img = pygame.image.load("dead.png").convert_alpha()
    display.blit(img, (0, 0))
    draw_text("GAME OVER", GREEN, -130, 72)
    draw_text("ENTER:TRY_AGAIN", GREEN, 200, 32)
    draw_text("ESC:EXIT", GREEN, 233, 32)
    
                
def restart():
    Snake.x = MAX_X / 2
    Snake.y = MAX_X / 2
    Snake.xchange = 0
    Snake.ychange = 0
    Snake.tail = []
    Game.score = 0
    applechange()
    Game.state = 'playing'

# Draw all the sprites that make up the game
def game_draw():
    global score_text
    # Draw the snake 🐍🐍🐍
    head = Snake.img
    aple = apple.img
    display.fill(BLACK)
    display.blit(backimg, (0, 0))

    if Snake.direction == 'right':
        head = pygame.transform.rotate(head, 270)
    if Snake.direction == 'left':
        head = pygame.transform.rotate(head, 90)
    if Snake.direction == 'down':
        head = pygame.transform.rotate(head, 180)

    display.blit(head, (Snake.x, Snake.y))
    display.blit(aple, (apple.x, apple.y))

    for xy in Snake.tail:
        display.blit(Snake.body, [xy[0], xy[1]])




# Game loop
while Game.state != "quit":
    if Game.state == 'playing':
        game_events()
        game_update()
        game_draw()
        score_text = font.render(str(Game.score), True, (255, 255, 255))
        display.blit(score_text, (10, 10))
    elif Game.state == 'game_over':
        game_over()
    elif Game.state == 'intro':
        intro()
    # 🎇 Actually update the display 🎇
    pygame.display.update()
    # ⏱ Tick the clock every frame by the desired FPS ⏱
    clock.tick(FPS)
pygame.quit()  # Close Pygame
quit()  # Close the program