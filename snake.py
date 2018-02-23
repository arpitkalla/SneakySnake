import curses
import numpy as np
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
from nn import Agent


class Snake():

    def refresh(self):
        self.board = [['x']*self.WIDTH]
        for j in range(self.HEIGHT-2):
            row = ['x']
            for i in range(self.WIDTH-2):
                    row.append('.')
            row.append('x')
            self.board.append(row)

        row = ['x']*self.WIDTH
        self.board.append(row)
        return self.board


    def addstr(self,x,y,s):
            c = list(s)
            for i in range(len(c)):
                self.board[x][y+i] = c[i]

    def join_board(self):
        s = ""
        for i in range(self.HEIGHT):
            s+="".join(self.board[i])
            s+='\n'
        return s

    def __init__(self):
        self.HEIGHT = 20
        self.WIDTH = 60

        self.board = self.refresh()

        curses.initscr()
        self.win = curses.newwin(self.HEIGHT, self.WIDTH, 0, 0)
        self.win.keypad(1)
        curses.noecho()
        curses.curs_set(0)
        self.win.border(0)
        self.win.nodelay(1)

        self.key = KEY_RIGHT
        self.score = 0

        self.snake = [[4,10], [4,9], [4,8]]                                     # Initial snake co-ordinates
        self.food = []                                                          # First food co-ordinates
        self.agent = Agent()
        self.f = open("snake_board.txt","w")

    def run(self):
        while self.key != 27:                                                   # While Esc key is not pressed
            self.board = self.refresh()

            while self.food == []:
                    self.food = [randint(1, self.HEIGHT-2), randint(1, self.WIDTH-2)]                 # Calculating next food's coordinates
                    if self.food in self.snake: self.food = []
            self.win.addch(self.food[0], self.food[1], '*')  # Prints the food
            self.addstr(self.food[0], self.food[1], '*')

            self.win.border(0)
            # self.win.addstr(0, 2, 'Score : ' + str(self.score) + ' ')                # Printing 'Score' and
            # self.win.addstr(0, 27, ' SNAKE ')                                   # 'SNAKE' strings
            self.win.timeout(150 - int(len(self.snake)/5 + len(self.snake)/10)%120)          # Increases the speed of Snake as its length increases
            # self.addstr(0, 2, str('Score : ' + str(self.score) + ' '))
            # self.addstr(0, 27, str(' SNAKE '))

            prevKey = self.key                                                  # Previous key pressed
            
            # Uncomment if want to play as the user
            # event = self.win.getch()

            # Uncomment when agent plays the game
            event = self.agent.predict(self.board,self.score)

            self.key = self.key if event == -1 else event 


            if self.key == ord(' '):                                            # If SPACE BAR is pressed, wait for another
                self.key = -1                                                   # one (Pause/Resume)
                while self.key != ord(' '):
                    self.key = self.win.getch()
                self.key = prevKey
                continue

            if self.key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:     # If an invalid key is pressed
                self.key = prevKey

            # Calculates the new coordinates of the head of the snake. NOTE: len(snake) increases.
            # This is taken care of later at [1].
            self.snake.insert(0, [self.snake[0][0] + (self.key == KEY_DOWN and 1) + (self.key == KEY_UP and -1), 
                self.snake[0][1] + (self.key == KEY_LEFT and -1) + (self.key == KEY_RIGHT and 1)])

            # If snake runs over itself  
            if self.snake[0] in self.snake[1:]: break

            if self.snake[0] == self.food:                                            # When snake eats the food
                self.food = []
                self.score += 10
            else:    
                last = self.snake.pop()                                          # [1] If it does not eat the food, length decreases
                self.win.addch(last[0], last[1], ' ')
                self.addstr(last[0], last[1], '.')
            self.win.addch(self.snake[0][0], self.snake[0][1], '#')
            for i in range(len(self.snake)):
                self.addstr(self.snake[i][0], self.snake[i][1], '#')
            s = self.join_board()
            self.f.write(s)
            self.score+=1

            # Exit if snake crosses the boundaries 
            if self.snake[0][0] == 0 or self.snake[0][0] == 19 or self.snake[0][1] == 0 or self.snake[0][1] == 59: break

        curses.endwin()
        self.f.close()
        print("\nScore - " + str(self.score))

    def get_state(self):
        return {
            'snake': self.snake,
            'food_x': self.food[0],
            'food_y': self.food[1],
            'score': self.score
        }

    def get_board(self):
        return self.board

    def get_score(self):
        return self.score


if __name__ == '__main__':
    snakeGame = Snake();
    snakeGame.run()
