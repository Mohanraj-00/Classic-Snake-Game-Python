import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define screen size
width = 800
height = 600

# Define snake block size
block_size = 10

# Define initial snake speed
snake_speed = 15

# Initialize Pygame
pygame.init()

# Define font for score
font_style = pygame.font.SysFont(None, 25)

# Define screen
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Define clock
clock = pygame.time.Clock()

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    game_display.blit(mesg, [width / 6, height / 3])

def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(game_display, GREEN, [x[0], x[1], block_size, block_size])

def display_score(score):
    value = font_style.render("Your Score: " + str(score), True, WHITE)
    game_display.blit(value, [0, 0])

def place_food(snake_list):
    valid = False
    while not valid:
        food_x = round(random.randrange(0, width - block_size) / 10.0) * 10.0
        food_y = round(random.randrange(0, height - block_size) / 10.0) * 10.0
        valid = not any(segment == [food_x, food_y] for segment in snake_list)
    return food_x, food_y

def handle_collision(snake_list, food_x, food_y, score):
    if snake_list[0] == [food_x, food_y]:
        food_x, food_y = place_food(snake_list)  # Generate new food location
        snake_list.append(snake_list[-1])  # Extend snake by one block
        score += 1
    else:
        snake_list.pop()  # Remove tail if no collision
    return snake_list, food_x, food_y, score

def game_loop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2
    x1_change = 0
    y1_change = 0

    snake_list = [[x1, y1]]
    length_of_snake = 1

    food_x, food_y = place_food(snake_list)  # Initial food placement

    score = 0

    while not game_over:

        while game_close:
            game_display.fill(BLACK)
            message("You Lost! Press Q-Quit or C-Play Again", RED)
            display_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = block_size
                    x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change

        game_display.fill(BLACK)
        pygame.draw.rect(game_display, RED, [food_x, food_y, block_size, block_size])

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.insert(0, snake_head)
        snake_list, food_x, food_y, score = handle_collision(snake_list, food_x, food_y, score)

        draw_snake(snake_list)
        display_score(score)

        pygame.display.update()

        clock.tick(snake_speed)

    pygame.quit()
    quit()

game_loop()
