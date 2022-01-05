import pygame
from tkinter import *
from tkinter import messagebox

Tk().wm_withdraw()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)

WINDOW_SIZE = [560, 255]

MARGIN = 5
WIDTH = 20
HEIGHT = 20


def clear_battleground(bg):
    for i in range(0, len(bg)):
        for j in range(0, len(bg)):
            bg[i][j] = 0


def get_directions(direction):
    if direction == 0:
        return 0, 1
    elif direction == 1:
        return 1, 0
    elif direction == 2:
        return 0, -1
    elif direction == 3:
        return -1, 0


def check_if_position_is_valid(ship_pos, direction):
    dir_row, dir_col = get_directions(direction)

    print(ship_pos)
    if ship_pos is not None:
        for i in range(0, 4):
            if ship_pos[1] + i * dir_col < 0 or ship_pos[1] + i * dir_col >= 10 or ship_pos[0] + i * dir_row < 0 or \
                    ship_pos[0] + i * dir_row >= 10:
                return False
    return True


def draw_ship(ship_pos, direction, player_bg):
    dir_row, dir_col = get_directions(direction)

    if ship_pos is not None:
        for i in range(0, 4):
            if player_bg[ship_pos[0] + i * dir_row][ship_pos[1] + i * dir_col] <= 0:
                player_bg[ship_pos[0] + i * dir_row][ship_pos[1] + i * dir_col] = 1


def check_if_ship_is_sunk(grid):
    for i in range(0, 10):
        for j in range(0, 10):
            if grid[i][j] > 0:
                return False
    return True


def player_hits(grid, turn):
    pos = pygame.mouse.get_pos()
    t_row = pos[1] // (HEIGHT + MARGIN)
    if turn == 1:
        if pos[0] > 260:
            return False
        t_col = pos[0] // (WIDTH + MARGIN)
    else:
        if pos[0] < 295:
            return False
        t_col = (pos[0] - 305) // (WIDTH + MARGIN)
    if t_row == -1:
        t_row = 0
    if t_col == -1:
        t_col = 0
    if grid[t_row][t_col] == -2 or grid[t_row][t_col] == -1:
        return False
    if grid[t_row][t_col] > 0:
        messagebox.showinfo('', "HIT!")
        grid[t_row][t_col] = -2
    else:
        messagebox.showinfo('', "MISS!")
        grid[t_row][t_col] = -1
    return True


def create_view_player(grid, screen, is_second, started):
    for row in range(0, 10):
        for col in range(0, 10):
            color = BLUE
            if grid[row][col] > 0 and not started:
                color = YELLOW
            elif grid[row][col] == -1:
                color = GREY
            elif grid[row][col] == -2:
                color = RED
            if is_second:
                pygame.draw.rect(screen, color,
                                 [(MARGIN + WIDTH) * col + 305 + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH,
                                  HEIGHT])
            else:
                pygame.draw.rect(screen, color,
                                 [(MARGIN + WIDTH) * col + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])


def create_view_enemy(grid, screen, is_second):
    for row in range(0, 10):
        for col in range(0, 10):
            if grid[row][col] >= 0:
                color = GREEN
            else:
                if grid[row][col] == -1:
                    color = GREY
                else:
                    color = RED
            if is_second:
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * col + 305 + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH, HEIGHT])
            else:
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * col + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH, HEIGHT])


def create_final_view(grid1, grid2, screen):
    for row in range(0, 10):
        for col in range(0, 10):
            color1 = WHITE
            color2 = WHITE
            if grid1[row][col] > 0:
                color1 = YELLOW
            elif grid1[row][col] == -1:
                color1 = GREY
            elif grid1[row][col] == -2:
                color1 = RED
            if grid2[row][col] > 0:
                color2 = YELLOW
            elif grid2[row][col] == -1:
                color2 = GREY
            elif grid2[row][col] == -2:
                color2 = RED
            pygame.draw.rect(screen, color1,
                             [(MARGIN + WIDTH) * col + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
            pygame.draw.rect(screen, color2,
                             [(MARGIN + WIDTH) * col + 305 + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH,
                              HEIGHT])


def main():
    player_bg = [[[0 for _ in range(0, 10)] for _ in range(0, 10)] for _ in range(0, 2)]

    pygame.init()

    first_ship_set = False
    second_ship_set = False
    welcome = False
    screen = pygame.display.set_mode(WINDOW_SIZE)
    ship_position = None

    pygame.display.set_caption("Battleships")

    direction = 0
    loop = True
    started = False

    clock = pygame.time.Clock()
    turn = 0

    while loop:
        for e in pygame.event.get():
            if not welcome:
                messagebox.showinfo('Game is about to begin.',
                                    'Place each ship on the blue grid first and then shoot for enemy\'s '
                                    'ship on the green grid.')
                welcome = True
            if e.type == pygame.QUIT:
                loop = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if first_ship_set is True and second_ship_set is True:
                    if player_hits(player_bg[1 - turn], turn):
                        if check_if_ship_is_sunk(player_bg[1 - turn]):
                            create_final_view(player_bg[0], player_bg[1], screen)
                            pygame.display.flip()
                            messagebox.showinfo('', f'A ship was sunk! Player {turn + 1} won!')
                            pygame.quit()
                        turn = 1 - turn
                else:
                    pos = pygame.mouse.get_pos()
                    if (first_ship_set is False and pos[0] <= 255) or (second_ship_set is False and pos[0] >= 295):
                        t_col = (pos[0] - (turn * 305) - MARGIN) // (WIDTH + MARGIN)
                        t_row = (pos[1] - MARGIN) // (HEIGHT + MARGIN)
                        if t_row == -1:
                            t_row = 0
                        if t_col == -1:
                            t_col = 0
                        if (turn == 0 and pos[0] <= 255) or (turn == 1 and pos[0] >= 305):
                            if player_bg[turn][t_row][t_col] == 0 or player_bg[turn][t_row][t_col] == 1:
                                t_ship_pos = (t_row, t_col)
                                if check_if_position_is_valid(t_ship_pos, direction):
                                    clear_battleground(player_bg[turn])
                                    player_bg[turn][t_row][t_col] = 2
                                    ship_position = (t_row, t_col)
                                else:
                                    messagebox.showerror('', "Position is not valid!")
                            elif player_bg[turn][t_row][t_col] == 2:
                                t_direction = (direction + 1) % 4
                                if check_if_position_is_valid((t_row, t_col), t_direction):
                                    clear_battleground(player_bg[turn])
                                    player_bg[turn][t_row][t_col] = 2
                                    direction = t_direction
                                else:
                                    messagebox.showinfo('', "Rotation is not valid!")
                            draw_ship(ship_position, direction, player_bg[turn])
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE and (first_ship_set is False or second_ship_set is False):
                    if not first_ship_set:
                        messagebox.showinfo('', "First ship was placed!")
                        first_ship_set = True
                        turn = 1
                    elif not second_ship_set:
                        messagebox.showinfo('', "Second ship placed! Hit for enemy's ship on the green grid.")
                        second_ship_set = True
                        turn = 0
                        started = True

        screen.fill(BLACK)

        create_view_player(player_bg[turn], screen, turn == 1, started)
        create_view_enemy(player_bg[1 - turn], screen, (1 - turn) == 1)

        # clock.tick(60)
        pygame.display.flip()
    pygame.quit()


main()
