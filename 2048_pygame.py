"""
Jasmehar Kaur
ICS3U0-A: Mr. Dutton's Class
Pygame Project - '2048'

About:
There is a 4x4 grid with tiles numbered with powers of 2 that the player can move using arrow keys.
The game starts with two tiles of value 2 at random positions in the grid.Every turn, a new tile of
value 2 appears at a random position. When the player presses an arrow key, all tiles slide in that
direction (up, down, left, or right) as far in the grid as possible. If two tiles of the same value
collide while moving, they merge into a new tile of a value of the two tiles combined. The value of
the new tile is added to the score.The game is won when the player merges two tiles into a new tile
of the value 2048. The game is lost when there are no more moves left for the player (when the grid
is full and there are no adjacent tiles with the same value.  
"""

#importing modules and libraries:
import random
import pygame
import math
import time

#initiating pygame:
pygame.init()

#initializing the screen
screen = pygame.display.set_mode([600, 750])
pygame.display.set_caption("2048")
icon = pygame.image.load("C:/Users/jasme/Downloads/icon.png")
pygame.transform.scale(icon, (32,32))
pygame.display.set_icon(icon)

# declaring global variables
grid = [[0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]]
empty = [i for i in range(16)] # this list contains all squares in the grid that don't contain a tile; the squares are numbered 0 to 16
game_over = False
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

#colour scheme:
bg = (229, 212, 206)
brown = (122, 101, 99)
l_brown = (172, 156, 154)

l_yellow = (255, 201, 92)
yellow = (255, 187, 51)
d_yellow = (245, 163, 0)
l_orange = (236, 171, 152)
orange = (238, 148, 89)
d_orange = (222, 110, 75)
l_pink = (237, 150, 187)
pink = (229, 99, 153)
d_pink = (209, 35, 111)
purple = (78, 84, 126)
d_purple = (47, 50, 76)

#coordinates for each square on the grid:
rows = {0:186, 1:321, 2:456, 3: 591}
columns = {0:36, 1:171, 2:306, 3:441}

#coordinates for elements:
ins_x = 210
ins_y = 400
start_x = 175
start_y = 490
back_x = 210
back_y = 510

#image elements:
start_bg = pygame.image.load("C:/Users/jasme/Downloads/2048 start_screen.png")
ins_bg = pygame.image.load("C:/Users/jasme/Downloads/2048 ins_screen.png")
ins_btn = pygame.image.load("C:/Users/jasme/Downloads/ins.png")
start_btn = pygame.image.load("C:/Users/jasme/Downloads/start.png")
back_btn = pygame.image.load("C:/Users/jasme/Downloads/back.png")
time_img = pygame.image.load("C:/Users/jasme/OneDrive/Desktop/Python/time.png")
score_img = pygame.image.load("C:/Users/jasme/OneDrive/Desktop/Python/score.png")
restart_img = pygame.image.load("C:/Users/jasme/OneDrive/Desktop/Python/restart.png")
exit_img = pygame.image.load("C:/Users/jasme/OneDrive/Desktop/Python/exit.png")
won_img = pygame.image.load("C:/Users/jasme/OneDrive/Desktop/Python/won.png")
lost_img = pygame.image.load("C:/Users/jasme/OneDrive/Desktop/Python/lost.png")

#tile images:
images = {}
for i in range(1, 12):
    images[2**i] = pygame.image.load("C:/Users/jasme/OneDrive/Desktop/Python/{}.png".format(2**i)).convert()
new_img = pygame.image.load("C:/Users/jasme/OneDrive/Desktop/Python/2 new.png")

# declaring sound effects:
slide_se = pygame.mixer.Sound("C:/Users/jasme/OneDrive/Desktop/Python/slide_se.wav")
won_se = pygame.mixer.Sound("C:/Users/jasme/OneDrive/Desktop/Python/won_se.wav")
lost_se = pygame.mixer.Sound("C:/Users/jasme/OneDrive/Desktop/Python/lost_se.wav")

# handles what happens when the player wins the game
def won(): 
    global game_over
    game_over = True
    screen.blit(won_img, (24, 174))
    pygame.display.update()
    pygame.mixer.Sound.play(won_se)
    
# checks if the player lost the game:
#    this is called if there is no blank space left in the grid
def check_lost():
    for row in range (4): # checks if there are two equal tiles side-by-side in a row
        for col in range (3):
            val = grid[row][col]
            if val == grid[row][col+1]:
                return
    for row in range (3): # checks if there are two equal tiles side-by-side in a column
        for col in range (4):
            val = grid[row][col]
            if val == grid[row+1][col]:
                return
    # the following code will only be ran if there are no to tiles that can still be
    # combined left in the grid: 
    global game_over
    game_over = True
    pygame.time.wait(1500)
    screen.blit(lost_img, (24, 174))
    pygame.display.update()
    pygame.mixer.Sound.play(lost_se)

# updates the score variable as well as the score displayed on the screen
def set_score(points):
    global score
    screen.blit(score_img, (columns[1],25))
    score += points
    score_txt = font.render(str(score), True, (255,255,255))
    screen.blit(score_txt, (columns[1]+10, 100))

# handles the time displayed on the screen
def set_time(time):
    time_txt = font.render(str(time), True, (255,255,255))
    screen.blit(time_img, (columns[0],25))
    screen.blit(time_txt, (columns[0] + 30, 100))
    pygame.display.update()
    
#updates the grid on the screen -> matches the screen with the contents in the grid nested lists
def update_screen():
    pygame.draw.rect(screen, brown, pygame.Rect(24,174,552,552), 0, border_radius = 8) # background of the playing square
    pygame.draw.rect(screen, l_brown, pygame.Rect(36, 186, 528, 528), 0, border_radius = 8)
    for i in range(0,3):
        pygame.draw.rect(screen, brown, pygame.Rect(159 + (i*135), 186, 12, 528), 0) # drawing vertical gridlines
    for i in range (0,3):
        pygame.draw.rect(screen, brown, pygame.Rect(36,309 + (i*135), 528, 12), 0) # drawing horizontal gridlines
        
    for row in range(4):
        for col in range(4):
            val = grid[row][col]
            if val != 0:
                screen.blit(images[val],(columns[col],rows[row])) # blit the tile on the screen
    pygame.display.update()

#updates the empty list
def update_empty():
    global empty
    empty = []
    for row in range(4):
        for col in range(4):
            if grid[row][col] == 0:
                empty.append(4*row + col)
    if empty == []:
        check_lost() # if there are no empty spaces left on the grid, check if the player has lost

#creates a new tile at a random position in the grid
def new_rand_sq(val):
    global grid, empty
    sq = empty[random.randint(0, len(empty)-1)] # the position is a random empty space left on the grid
    row = math.floor(sq/4)
    col = sq % 4
    grid[row][col] = val # updates the grid list
    empty.remove(sq)
    update_screen()
    screen.blit(new_img, (columns[col], rows[row]))
    pygame.display.update()    
    

# this is called when the user presses left or right arrow keys
# handles the collision and horizontal movement of tiles
def move_h(dire):
    global grid
    if dire == "left":
        range1 = range(1,4)
    elif dire == "right":
        range1 = range(2,-1,-1)
    moved = False
    for row in range(4):
        for col in range1:
            val = grid[row][col]
            new_val = val
            if val != 0:
                new_col = col
                if dire == "left":
                    range2 = range(col-1, -1, -1)
                elif dire == "right":
                    range2 = range(col+1, 4)
                for i in range2:
                    if grid[row][i] == val and new_val == val:# if the tile beside val is of the same value, combine them together as a new tile
                        new_val = val*2
                        grid[row][i] = 0
                        set_score(val*2)
                        if new_val == 2048: # if the value of the combined tiles is 2048, the player has won the game
                            won()
                            return
                    if grid[row][i] == 0: # if the next tile is empty, move the val tile there
                        new_col = i
                        moved = True
                    else:
                        break  
                grid[row][col] = 0
                grid[row][new_col] = new_val
    update_empty()
    if moved == True: 
        new_rand_sq(2)
        pygame.mixer.Sound.play(slide_se)

# this is called when the user presses up or down arrow keys
# handles the collision and vertical movement of tiles
# basically the previous function but in the vertical direction
def move_v(dire):
    global grid
    if dire == "up":
        range1 = range(1,4)
    elif dire == "down":
        range1 = range(2,-1,-1)
    moved = False    
    for col in range(4):
        for row in range1:
            val = grid[row][col]
            new_val = val
            if val != 0:
                new_row = row
                if dire == "up":
                    range2 = range(row-1, -1, -1)
                elif dire == "down":
                    range2 = range(row+1, 4)
                for i in range2:
                    if grid[i][col] == val and new_val == val:
                        new_val = val*2
                        grid[i][col]= 0
                        set_score(val*2)
                        if new_val == 2048:
                            won()
                            return
                    if grid[i][col] == 0:
                        new_row = i
                        moved = True
                    else:
                        break       
                grid[row][col] = 0
                grid[new_row][col] = new_val
    update_empty()
    if moved == True:
        new_rand_sq(2)
        pygame.mixer.Sound.play(slide_se)

# handles the instruction screen
def ins_screen():
    screen.blit(ins_bg, (0,0))
    screen.blit(back_btn, (back_x, back_y))
    back_rect = pygame.Rect(back_x, back_y, 180, 60)
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    start_screen()
                    return

# handles the screen where the game is played
def main_screen():

    # re-declaring the game variables
    global grid, empty, game_over, time, score
    grid = [[0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]]
    empty = [i for i in range(16)]
    game_over = False
    score = 0
    time = 0

    # to test what happens when the player loses, uncomment the following 2 lines:
    # grid = [[0, 4, 8, 16], [16, 8, 4, 0], [2, 4, 8, 16], [16, 8, 4,2]]
    # empty = [0,7]

    # display all elements on the screen
    screen.fill(bg) # fill the background with light pink
    screen.blit(time_img, (columns[0],25))
    screen.blit(score_img, (columns[1],25))
    screen.blit(restart_img, (columns[2], 25))
    screen.blit(exit_img, (columns[3], 25))
    restart_rect = pygame.Rect(columns[2], 25, 123, 123)
    exit_rect = pygame.Rect(columns[3], 25, 123, 123)
    
    pygame.draw.rect(screen, brown, pygame.Rect(24,174,552,552), 0, border_radius = 8) # background of the playing square
    pygame.draw.rect(screen, l_brown, pygame.Rect(36, 186, 528, 528), 0, border_radius = 8)

    for i in range(0,3):
        pygame.draw.rect(screen, brown, pygame.Rect(159 + (i*135), 186, 12, 528), 0) # drawing vertical gridlines
    for i in range (0,3):
        pygame.draw.rect(screen, brown, pygame.Rect(36,309 + (i*135), 528, 12), 0) # drawing horizontal gridlines

    # start with two tiles at random position
    # to test what happens when the player wins, change the arguments to 1024
    new_rand_sq(2)
    new_rand_sq(2)
    
    pygame.display.update()
    start_time = pygame.time.get_ticks()
    while True:
        current_time = pygame.time.get_ticks()
        if current_time % 1000 == 0 and game_over == False:
            set_time(int((current_time - start_time)/1000)) # calls the set_time function every second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN and game_over == False:
                if event.key == pygame.K_LEFT:
                    move_h("left")
                elif event.key == pygame.K_RIGHT:
                    move_h("right")
                elif event.key == pygame.K_UP:
                    move_v("up")
                elif event.key == pygame.K_DOWN:
                    move_v("down")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos): # if the player presses the restart button, restart the main_screen function
                    main_screen()
                    return
                elif exit_rect.collidepoint(event.pos): # if the player presses the exit button, go back to start_screen and quit the main_screen function
                    start_screen()
                    return

# handles the home screen
def start_screen():
    screen.blit(start_bg, (0,0))
    screen.blit(ins_btn, (ins_x, ins_y))
    ins_rect = pygame.Rect(ins_x, ins_y, 180, 60)
    screen.blit(start_btn, (start_x, start_y))
    start_rect = pygame.Rect(start_x, start_y, 250, 90)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos): # if the player presses the start button, go the main game screen
                    main_screen()
                    return
                elif ins_rect.collidepoint(event.pos):# if the player presses the instructions button, go to the instructions screen
                    ins_screen()
                    return
                
start_screen()
