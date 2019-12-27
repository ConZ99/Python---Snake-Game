import pygame as py
import tkinter as tk
from tkinter import messagebox
import random
import math

class square(object):
    rows = 20
    size = 500
    def __init__(self, start, dirX=1, dirY=0, color=(255, 0, 0)):
        self.pos = start
        self.dirX = 1
        self.dirY = 0
        self.color = color

    def move(self, x, y):
        self.dirX = x
        self.dirY = y
        self.pos = (self.pos[0] + self.dirX, self.pos[1] + self.dirY)
    
    def draw(self, surface, eyes=False):
        dist = self.size // self.rows
        i = self.pos[0]
        j = self.pos[1]

        py.draw.rect(surface, self.color, (i*dist+1, j*dist+1, dist-2, dist-2))
        if eyes:
            centre = dist // 2
            radius = 3
            circleMiddle = (i*dist+centre-radius,j*dist+8)
            circleMiddle2 = (i*dist + dist -radius*2, j*dist+8)
            py.draw.circle(surface, (0,0,0), circleMiddle, radius)
            py.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = square(pos)
        self.body.append(self.head)
        self.dirX = 0
        self.dirY = 1

    def move(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
            keys = py.key.get_pressed()
            for key in keys:
                if keys[py.K_UP]:
                    self.dirX = 0
                    self.dirY = -1
                    self.turns[self.head.pos[:]] = [self.dirX, self.dirY]
                elif keys[py.K_DOWN]:
                    self.dirX = 0
                    self.dirY = 1
                    self.turns[self.head.pos[:]] = [self.dirX, self.dirY]
                elif keys[py.K_RIGHT]:
                    self.dirX = 1
                    self.dirY = 0
                    self.turns[self.head.pos[:]] = [self.dirX, self.dirY]
                elif keys[py.K_LEFT]:
                    self.dirX = -1
                    self.dirY = 0
                    self.turns[self.head.pos[:]] = [self.dirX, self.dirY]
                

        for i, c in enumerate(self.body):
            pos = c.pos[:]
            if pos in self.turns: 
                #daca ultimul patrat face miscarea, o elimil din lista de miscari
                turn = self.turns[pos]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(pos)
            else:
                #daca ajung la limita ecranului, continui tranzitia
                if c.dirX == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dirX == 1 and c.pos[0] >= c.rows-1:
                    c.pos = (0,c.pos[1])
                elif c.dirY == 1 and c.pos[1] >= c.rows-1:
                    c.pos = (c.pos[0], 0)
                elif c.dirY == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0],c.rows-1)
                else:
                    c.move(c.dirX,c.dirY)

    def reset(self, pos):
        self.head = square(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirX = 0
        self.dirY = 1

    def addSquare(self):
        tail = self.body[-1]
        dx, dy = tail.dirX, tail.dirY

        if dx == 1 and dy == 0:
            self.body.append(square((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(square((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(square((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(square((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirX = dx
        self.body[-1].dirY = dy

    def draw(self, surface):
        for i, s in enumerate(self.body):
            if i == 0:
                s.draw(surface, True)
            else:
                s.draw(surface)

def drawTable(size, rows, surface):
    sizeBtwn = size // rows
    x = 0
    y = 0
    for lines in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        py.draw.line(surface, (255, 255, 255), (x, 0), (x, size))
        py.draw.line(surface, (255, 255, 255), (0, y), (size, y))

def redrawWin(surface):
    global size, rows, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawTable(size, rows, surface)
    py.display.update()

def randSnack(rows, snacks):
    pos = snacks.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        #singurul lucru pe care l-am invatat de la matei...
        if len(list(filter(lambda z:z.pos == (x, y), pos))) > 0:
            continue
        else:
            break
    return (x, y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global size, rows, s, snack
    size = 500
    rows = 20
    win = py.display.set_mode((size, size))
    s = snake((0, 0, 255), (10, 10))
    snack = square(randSnack(rows, s), color=(0, 255, 0))
    flag = True
    clock = py.time.Clock()

    while flag:
        py.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addSquare()
            snack = square(randSnack(rows, s), color=(0, 255, 0))

        for i in range(len(s.body)):
            if s.body[i].pos in list(map(lambda z:z.pos, s.body[i+1:])):
                print('Score: ', len(s.body-1))
                message_box('Game Over', 'Restart')
                s.reset((10, 10))
                break
        redrawWin(win)
    pass

main()