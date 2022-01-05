import tkinter as tk

import pygame
from tkinter import *
from tkinter import messagebox
# from random import randrange

root = tk.Tk()
root.destroy()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)


def clear_battleground(bg):
    for i in range(0, len(bg)):
        for j in range(0, len(bg)):
            bg[i][j] = 0


def get_directions(direction):
    if direction == 0:
        return (0, 1)
    elif direction == 1:
        return (1, 0)
    elif direction == 2:
        return (0, -1)
    elif direction == 3:
        return (-1, 0)


def check_if_position_is_valid(shipPos, direction):
    dir_row, dir_col = get_directions(direction)

    print(shipPos)
    if shipPos != None:
        for i in range(0, 4):
            if shipPos[1] + i * dir_col < 0 or shipPos[1] + i * dir_col >= 10 or shipPos[0] + i * dir_row < 0 or \
                    shipPos[0] + i * dir_row >= 10:
                return False
    return True


def draw_ship(shipPos, direction, player_bg):
    dir_row, dir_col = get_directions(direction)

    if shipPos != None:
        for i in range(0, 4):
            if player_bg[shipPos[0] + i * dir_row][shipPos[1] + i * dir_col] <= 0:
                player_bg[shipPos[0] + i * dir_row][shipPos[1] + i * dir_col] = 1


def check_if_ship_is_sunk(grid):
    for i in range(0, 10):
        for j in range(0, 10):
            if grid[i][j] > 0:
                return False
    return True


def playerHits(grid, WIDTH, HEIGHT, MARGIN, turn):
    pos = pygame.mouse.get_pos()
    t_row = pos[1] // (HEIGHT + MARGIN)
    t_col = None
    if turn == 1:
        if pos[0] > 260:
            return False
        t_col = pos[0] // (WIDTH + MARGIN)
    else:
        if pos[0] < 260:
            return False
        t_col = (pos[0] - 305) // (WIDTH + MARGIN)
    if grid[t_row][t_col] > 0:
        messagebox.showinfo('', "HIT!")
        grid[t_row][t_col] = -2
    else:
        messagebox.showinfo('', "MISS!")
        grid[t_row][t_col] = -1
    return True


def create_grid_player(player_bg, screen, MARGIN, WIDTH, HEIGHT, isSecond):
    for row in range(0, 10):
        for col in range(0, 10):
            color = None
            if player_bg[row][col] == 0:
                color = BLUE
            elif player_bg[row][col] > 0:
                color = YELLOW
            else:
                if player_bg[row][col] == -1:
                    color = GREY
                else:
                    color = RED
            if isSecond == True:
                pygame.draw.rect(screen, color,
                                 [(MARGIN + WIDTH) * col + 305 + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH,
                                  HEIGHT])
            else:
                pygame.draw.rect(screen, color,
                                 [(MARGIN + WIDTH) * col + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])


def create_view_enemy(grid, screen, MARGIN, WIDTH, HEIGHT, isSecond):
    for row in range(0, 10):
        for col in range(0, 10):
            color = None
            if grid[row][col] >= 0:
                color = GREEN
            else:
                if grid[row][col] == -1:
                    color = GREY
                else:
                    color = RED
            if isSecond == True:
                pygame.draw.rect(screen, color,
                                 [(MARGIN + WIDTH) * col + 305 + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH,
                                  HEIGHT])
            else:
                pygame.draw.rect(screen, color,
                                 [(MARGIN + WIDTH) * col + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])


def main():
    player_bg = [[[0 for i in range(0, 10)] for j in range(0, 10)] for t in range(0, 2)]

    WINDOW_SIZE = [560, 255]
    pygame.init()

    MARGIN = 5
    WIDTH = 20
    HEIGHT = 20

    firstShipIsSet = False
    secondShipIsSet = False
    warn = False
    screen = pygame.display.set_mode(WINDOW_SIZE)
    shipPos = None

    pygame.display.set_caption("Battleships")
    direction = 0

    loop = True

    clock = pygame.time.Clock()
    Tk().wm_withdraw()
    turn = 0

    while loop:
        for e in pygame.event.get():
            if warn == False:
                messagebox.showinfo('Game is about to begin',
                                    'First player will place his ship on blue grid,'
                                    'then second player place on blue grid!You hit on green grid!Have fun!')
                warn = True
            if e.type == pygame.QUIT:
                loop = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if firstShipIsSet == True and secondShipIsSet == True:
                    if playerHits(player_bg[1 - turn], WIDTH, HEIGHT, MARGIN, turn):
                        if check_if_ship_is_sunk(player_bg[1 - turn]):
                            messagebox.showinfo('', f'Ship was sunk! Player {turn} won!')
                            pygame.quit()
                        turn = 1 - turn
                else:
                    pos = pygame.mouse.get_pos()
                    if (firstShipIsSet == False and pos[0] <= 255) or (secondShipIsSet == False and pos[0] > 255):
                        t_row = None
                        t_col = None
                        if turn == 0:
                            t_row = pos[1] // (HEIGHT + MARGIN)
                            t_col = pos[0] // (WIDTH + MARGIN)
                        else:
                            t_row = pos[1] // (HEIGHT + MARGIN)
                            t_col = (pos[0] - 305) // (WIDTH + MARGIN)
                        if player_bg[turn][t_row][t_col] == 0 or player_bg[turn][t_row][t_col] == 1:
                            t_shipPos = (t_row, t_col)
                            if check_if_position_is_valid(t_shipPos, direction) == True:
                                clear_battleground(player_bg[turn])
                                player_bg[turn][t_row][t_col] = 2
                                shipPos = (t_row, t_col)
                            else:
                                messagebox.showinfo('', "Position is not valid!")
                        elif player_bg[turn][t_row][t_col] == 2:
                            t_direction = (direction + 1) % 4
                            if check_if_position_is_valid((t_row, t_col), t_direction) == True:
                                clear_battleground(player_bg[turn])
                                player_bg[turn][t_row][t_col] = 2
                                direction = t_direction
                            else:
                                messagebox.showinfo('', "Rotation is not valid!")
                        draw_ship(shipPos, direction, player_bg[turn])
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE and (firstShipIsSet == False or secondShipIsSet == False):
                    if firstShipIsSet == False:
                        messagebox.showinfo('', "First ship was placed!")
                        firstShipIsSet = True
                        turn = 1
                    elif secondShipIsSet == False:
                        messagebox.showinfo('', "Second ship placed! Have fun!")
                        secondShipIsSet = True
                        turn = 0

        screen.fill(BLACK)

        create_grid_player(player_bg[turn], screen, MARGIN, WIDTH, HEIGHT, turn == 1)
        create_view_enemy(player_bg[1 - turn], screen, MARGIN, WIDTH, HEIGHT, (1 - turn) == 1)

        clock.tick(60)
        pygame.display.flip()
    pygame.quit()


main()

