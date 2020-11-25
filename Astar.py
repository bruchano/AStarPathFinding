import pygame as pg
import random
import tkinter as tk
import math

row = 60
column = 90
node_x = 15
node_y = 15
screen_width = column * node_x
screen_height = row * node_y
red = (225, 0, 0)
orange = (255, 140, 0)
yellow = (255, 210, 0)
green = (0, 100, 0)
light_green = (0, 200, 0)
blue = (0, 0, 255)
grey = (220, 220, 220)
white = (255, 255, 255)
black = (0, 0, 0)
open_list = []
checked_list = []
start_x, start_y = None, None
end_x, end_y = None, None

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("A* Pathfinding")
screen.fill(black)


class N:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.neighbours = []
        self.obstacle = False
        self.checked = False
        self.previous = None
        self.set = False

    def get_neighbours(self):
        i = self.y
        j = self.x
        if i < row - 1 and maze[i + 1][j].obstacle is False and maze[i + 1][j].checked is False:
            self.neighbours.append(maze[i + 1][j])
        if i > 0 and maze[i - 1][j].obstacle is False and maze[i - 1][j].checked is False:
            self.neighbours.append(maze[i - 1][j])
        if j < column - 1 and maze[i][j + 1].obstacle is False and maze[i][j + 1].checked is False:
            self.neighbours.append(maze[i][j + 1])
        if j > 0 and maze[i][j - 1].obstacle is False and maze[i][j - 1].checked is False:
            self.neighbours.append(maze[i][j - 1])

    def draw(self, color=green, style=1):
        i = self.y
        j = self.x
        pg.draw.rect(screen, color, (j * node_x, i * node_y, node_x, node_y), style)
        pg.display.update()


def create_cancel_start(position):
    global start_x, start_y
    x = position[0] // node_x
    y = position[1] // node_y
    if not start_x and not start_y:
        start_x, start_y = x, y
        maze[y][x].draw(red, 0)
    elif x != start_x or y != start_y:
        maze[start_y][start_x].draw(black, 0)
        maze[start_y][start_x].draw()
        start_x, start_y = x, y
        maze[y][x].draw(red, 0)
    else:
        maze[start_y][start_x].draw(black, 0)
        maze[start_y][start_x].draw()
        start_x, start_y = None, None


def create_cancel_end(position):
    global end_x, end_y
    x = position[0] // node_x
    y = position[1] // node_y
    if not end_x and not end_y:
        end_x, end_y = x, y
        maze[y][x].draw(blue, 0)
    elif x != end_x or y != end_y:
        maze[end_y][end_x].draw(black, 0)
        maze[end_y][end_x].draw()
        end_x, end_y = x, y
        maze[y][x].draw(blue, 0)
    else:
        maze[end_y][end_x].draw(black, 0)
        maze[end_y][end_x].draw()
        end_x, end_y = None, None


def create_obstacle(position):
    x = position[0] // node_x
    y = position[1] // node_y
    if maze[y][x] != start and maze[y][x] != end:
        if not maze[y][x].obstacle:
            maze[y][x].obstacle = True
            maze[y][x].draw(white, 0)


def cancel_obstacle(position):
    x = position[0] // node_x
    y = position[1] // node_y
    if maze[y][x] != start and maze[y][x] != end:
        if maze[y][x].obstacle:
            maze[y][x].obstacle = False
            maze[y][x].draw(black, 0)
            maze[y][x].draw()


def check_legit_maze():
    current = start
    if current == end:
        return True
    else:
        current.get_neighbours()
        for neighbour in current.neighbours:
            if neighbour not in open_list:
                open_list.append(neighbour)
            if neighbour.g == 0 or neighbour.g > current.g + 1:
                neighbour.g = current.g + 1
                neighbour.previous = current
            neighbour.h = abs(neighbour.x - end_x) + abs(neighbour.y - end_y)
            neighbour.f = neighbour.g + neighbour.h
        if len(open_list) > 0:
            lowest_f_node = 0
            for i in range(len(open_list)):
                if open_list[i].f < open_list[lowest_f_node].f:
                    lowest_f_node = i
            current = open_list[lowest_f_node]
            current.checked = True
            checked_list.append(open_list[lowest_f_node])
            open_list.pop(lowest_f_node)
        else:
            return False


def reset():
    open_list.clear()
    checked_list.clear()
    for i in range(row):
        for j in range(column):
            maze[i][j].g, maze[i][j].h, maze[i][j].f, maze[i][j].previous = 0, 0, 0, None
            maze[i][j].neighbours.clear()


def auto_create():
    global maze
    if start and end:
        for i in range(row):
            for j in range(column):
                if maze[i][j] != start and maze[i][j] != end:
                    if not maze[i][j].set:
                        maze[i][j].obstacle = random.choice([True, False])
                        maze[i][j].set = True

                        if maze[i][j].obstacle is True:
                            maze[i][j].draw(white, 0)
                        else:
                            maze[i][j].draw(black, 0)
                            maze[i][j].draw()

                        if check_legit_maze():
                            auto_create()
                        maze[i][j].set = False
                        return


maze = [[0 for x in range(column)] for y in range(row)]
for i in range(row):
    for j in range(column):
        maze[i][j] = N(j, i)
        maze[i][j].draw()

active = True
while active:
    for event in pg.event.get():
        position = pg.mouse.get_pos()

        if event.type == pg.QUIT:
            active = False
            pg.quit()
            break

        if pg.mouse.get_pressed()[0]:
            create_cancel_start(position)

        if pg.mouse.get_pressed()[2]:
            create_cancel_end(position)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                if start_x and start_y and end_x and end_y:
                    active = False
                    break

start = maze[start_y][start_x]
current = maze[start_y][start_x]
checked_list.append(current)
current.checked = True
end = maze[end_y][end_x]

active = True
while active:
    for event in pg.event.get():
        position = pg.mouse.get_pos()

        if event.type == pg.QUIT:
            active = False
            pg.quit()
            break

        if pg.mouse.get_pressed()[0]:
            create_obstacle(position)

        if pg.mouse.get_pressed()[2]:
            cancel_obstacle(position)

        if event.type == pg.KEYDOWN:
            # if event.key == pg.K_SPACE:
            #     auto_create()
            #     active = False
            #     break
            if event.key == pg.K_RETURN:
                active = False
                break

active = True
while active:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            active = False
            pg.quit()
            break

    if current == end:
        current.draw(blue, 0)
        print(f"Done. Cost: {current.f}")

        backtracking = True
        while backtracking:
            if current.previous == start:
                backtracking = False
                wait = True
                while wait:
                    pg.display.update()
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            wait = False
                            active = False
                            pg.quit()
                            break
            else:
                current.previous.draw(light_green, 0)
                current = current.previous
        break

    else:
        current.get_neighbours()
        for neighbour in current.neighbours:
            if neighbour not in open_list:
                open_list.append(neighbour)
                neighbour.draw(orange, 0)
            if neighbour.g == 0 or neighbour.g > current.g + 1:
                neighbour.g = current.g + 1
                neighbour.previous = current
            neighbour.h = abs(neighbour.x - end_x) + abs(neighbour.y - end_y)
            neighbour.f = neighbour.g + neighbour.h
        if len(open_list) > 0:
            lowest_f_node = 0
            for i in range(len(open_list)):
                if open_list[i].f < open_list[lowest_f_node].f:
                    lowest_f_node = i
            current = open_list[lowest_f_node]
            current.checked = True
            checked_list.append(open_list[lowest_f_node])
            current.draw(yellow, 0)
            open_list.pop(lowest_f_node)
        else:
            print("No route.")
            wait = True
            while wait:
                pg.display.update()
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        wait = False
                        active = False
                        pg.quit()
                        break

