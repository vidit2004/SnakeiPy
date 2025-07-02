import pygame
from random import randrange
import mysql.connector
from datetime import datetime

time_start = datetime.now()

# global variables for the game
Size = 600    # size of canvas
scale = [10, 12, 15, 20]
while True:
    i = int(input("Enter snake width from 1-4: "))
    if i >= 1 and i <= 4:
        break
Scale = scale[i-1]
while True:
    Speed = int(input("Enter snake speed from 1-10: "))
    if i >= 1 and i <= 10:
        break
Speed += 10
x1_change = 0    # variables for changing direction / Moving
y1_change = 0
white = (255, 255, 255)    # colour tuples for pygame
red = (255, 0, 0)
black = (0, 0, 0)
grey = (100, 100, 100)
Snake = [(Size / 2, Size / 2)]    # snake at start position
food = (randrange(0, Size - Scale, Scale), randrange(0, Size - Scale, Scale))    # food initialisation
score = 0    #score counter
done = False    # Loop Intialisation condition


# draws the snake on the screen
def draw_snake():
    global Snake
    for body in Snake:
        pygame.draw.rect(screen, white, pygame.Rect(
            body[0], body[1], Scale, Scale))


# draws the food at the food's location
def draw_food():
    global Scale
    pygame.draw.rect(screen, red, pygame.Rect(
        food[0], food[1], Scale, Scale))


# moves the snake
def move():
    global Snake
    global x1_change
    global y1_change
    global Scale

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT and x1_change != Scale:
            x1_change = -1 * Scale
            y1_change = 0
        elif event.key == pygame.K_RIGHT and x1_change != -1 * Scale:
            x1_change = Scale
            y1_change = 0
        elif event.key == pygame.K_UP and y1_change != Scale:
            y1_change = -1 * Scale
            x1_change = 0
        elif event.key == pygame.K_DOWN and y1_change != -1 * Scale:
            y1_change = Scale
            x1_change = 0

    x2 = Snake[-1][0] + x1_change
    y2 = Snake[-1][1] + y1_change
    to_append = (x2, y2)
    Snake.append(to_append)
    Snake.pop(0)


# checks for boundaries
def boundary_check():
    global Snake
    global Size
    if 0 > Snake[-1][0] or Size - Scale < Snake[-1][0] or Size - Scale < Snake[-1][1] or 0 > Snake[-1][1]:
        return True


# eats the food and increses the length
def food_eat():
    global food
    global Size
    global Scale
    global score
    global x1_change
    global y1_change

    x1 = Snake[-1][0] + x1_change
    y1 = Snake[-1][1] + y1_change
    to_append = (x1, y1)
    Snake.append(to_append)
    while food in Snake:
        food = (randrange(0, Size - Scale, Scale),
                randrange(0, Size - Scale, Scale))
    score += 1
    print(score)


# checks in snake collides with itself
def body_check():
    global Snake
    global score
    head = Snake[-1]
    if head in Snake[0:score]:
        return True
    


# pygame initialisation
pygame.init()
screen = pygame.display.set_mode((Size, Size))
pygame.display.set_caption('Snake OP')
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render(str(score), True, grey)
textRect = text.get_rect(center=(Size/2, Size/2))

# main loop

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            break

    screen.fill(black)
    if boundary_check() or body_check():
        done = True
        break
    text = font.render(str(score), True, grey)
    screen.blit(text, textRect)
    draw_snake()
    draw_food()
    if food == Snake[-1]:
        food_eat()
    else:
        move()

    pygame.display.update()

    clock.tick(Speed)  
    
time_end = datetime.now()

#MySQL data storage
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="snakestats"
)
mycursor = db.cursor()
#If not table, create table
mycursor.execute("SHOW TABLES")
make_table = True
for result in mycursor:
    if result==('stats',):
        make_table = False

if make_table:
    mycursor.execute("CREATE TABLE stats(stime DATETIME, etime DATETIME, width INTEGER(10), speed INTEGER(10), score INTEGER(10))")
    db.commit()
#Insert data
mycursor.execute("INSERT INTO stats VALUES(%s,%s,%s,%s,%s)", (time_start, time_end, Scale, Speed, score))
db.commit()