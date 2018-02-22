import curses
import numpy as np
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

HEIGHT = 20
WIDTH = 60
curses.initscr()
win = curses.newwin(HEIGHT, WIDTH, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)



def refresh():
    board = [['x']*WIDTH]
    for j in range(HEIGHT-2):
        row = ['x']
        for i in range(WIDTH-2):
                row.append('.')
        row.append('x')
        board.append(row)

    row = ['x']*WIDTH
    board.append(row)
    return board

board = refresh()

def addstr(x,y,s):
    c = list(s)
    for i in range(len(c)):
        board[x][y+i] = c[i]

def joinBoard():
    s = ""
    for i in range(HEIGHT):
        s+="".join(board[i])
        s+='\n'
    return s
key = KEY_RIGHT                                                    # Initializing values
score = 0

snake = [[4,10], [4,9], [4,8]]                                     # Initial snake co-ordinates
food = []                                                          # First food co-ordinates

f = open("snake_board.txt","w")


while key != 27:                                                   # While Esc key is not pressed
    board = refresh()

    while food == []:
            food = [randint(1, 18), randint(1, 58)]                 # Calculating next food's coordinates
            if food in snake: food = []
    win.addch(food[0], food[1], '*')  # Prints the food
    addstr(food[0], food[1], '*')

    win.border(0)
    win.addstr(0, 2, 'Score : ' + str(score) + ' ')                # Printing 'Score' and
    win.addstr(0, 27, ' SNAKE ')                                   # 'SNAKE' strings
    win.timeout(150 - int(len(snake)/5 + len(snake)/10)%120)          # Increases the speed of Snake as its length increases
    addstr(0, 2, str('Score : ' + str(score) + ' '))
    addstr(0, 27, str(' SNAKE '))

    prevKey = key                                                  # Previous key pressed
    event = win.getch()
    key = key if event == -1 else event 


    if key == ord(' '):                                            # If SPACE BAR is pressed, wait for another
        key = -1                                                   # one (Pause/Resume)
        while key != ord(' '):
            key = win.getch()
        key = prevKey
        continue

    if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:     # If an invalid key is pressed
        key = prevKey

    # Calculates the new coordinates of the head of the snake. NOTE: len(snake) increases.
    # This is taken care of later at [1].
    snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

    # If snake runs over itself
    if snake[0] in snake[1:]: break

    if snake[0] == food:                                            # When snake eats the food
        food = []
        score += 10
    else:    
        last = snake.pop()                                          # [1] If it does not eat the food, length decreases
        win.addch(last[0], last[1], ' ')
        addstr(last[0], last[1], '.')
    win.addch(snake[0][0], snake[0][1], '#')
    for i in range(len(snake)):
        addstr(snake[i][0], snake[i][1], '#')
    s = joinBoard()
    f.write(s)
    score+=1

    # Exit if snake crosses the boundaries 
    if snake[0][0] == 0 or snake[0][0] == 19 or snake[0][1] == 0 or snake[0][1] == 59: break

curses.endwin()
f.close()
print("\nScore - " + str(score))
