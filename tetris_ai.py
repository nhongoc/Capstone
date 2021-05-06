import pygame

counter = 0


class Event:
    type = None
    key = None

    def __init__(self, type, key):
        self.type = type
        self.key = key


def intersects(game_field, x, y, game_width, game_height, game_figure_image):
    intersection = False
    for i in range(4):
        for j in range(4):
            if i * 4 + j in game_figure_image:
                if i + y > game_height - 1 or j + x > game_width - 1 or j + x < 0 or game_field[i + y][j + x] > 0:
                    intersection = True
    return intersection


def best_rotation_and_position(game_field, game_figure, game_width, game_height):
    best_height = game_height
    best_num_holes = game_height * game_width
    best_position = None
    best_rotation = None

    for rotation in range(len(game_figure.figures[game_figure.type])):
        figure = game_figure.figures[game_figure.type][rotation]
        for j in range(-3, game_width):
            if intersects(game_field, j, 0, game_width, game_height, figure):
                continue
            else:
                num_holes, height = simulate(game_field, j, 0, game_width, game_height, figure)
                if best_position is None or best_num_holes > num_holes or \
                        (best_num_holes == num_holes and best_height > height):
                    best_height = height
                    best_num_holes = num_holes
                    best_position = j
                    best_rotation = rotation
    return best_rotation, best_position


def run_ai(game_field, game_figure, game_width, game_height):
    global counter
    counter += 1
    if counter < 3:
        return []
    counter = 0
    rotation, position = best_rotation_and_position(game_field, game_figure, game_width, game_height)
    if game_figure.rotation != rotation:
        event = Event(pygame.KEYDOWN, pygame.K_UP)
    elif game_figure.x < position:
        event = Event(pygame.KEYDOWN, pygame.K_RIGHT)
    elif game_figure.x > position:
        event = Event(pygame.KEYDOWN, pygame.K_LEFT)
    else:
        event = Event(pygame.KEYDOWN, pygame.K_SPACE)
    return [event]


def simulate(game_field, x, y, game_width, game_height, game_figure_image):
    while not intersects(game_field, x, y, game_width, game_height, game_figure_image):
        y += 1
    y -= 1

    new_height = game_height
    num_holes = 0
    filled = []
    num_breaks = 0
    for height in range(game_height - 1, -1, -1):
        full = True
        prev_holes = num_holes
        for width in range(game_width):
            u = False
            if game_field[height][width] != 0:
                u = True
            for ii in range(4):
                for jj in range(4):
                    if ii * 4 + jj in game_figure_image:
                        if jj + x == width and ii + y == height:
                            u = True

            if u and height < new_height:
                new_height = height
            if u:
                filled.append((height, width))
                for k in range(height, game_height):
                    if (k, width) not in filled:
                        num_holes += 1
                        filled.append((k, width))
            else:
                full = False
        if full:
            num_breaks += 1
            num_holes = prev_holes

    return num_holes, game_height - new_height - num_breaks
