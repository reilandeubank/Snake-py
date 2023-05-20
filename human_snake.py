import pygame
import random

pygame.init()

# Set up the screen
screen_width = 800
screen_height = 800
square_size = 32
side_length = screen_width // square_size
start_pos = (side_length // 2) * square_size
head_x = start_pos
head_y = start_pos
snake_squares = [
    [start_pos, start_pos + square_size],
    [start_pos, start_pos]
]
snake_len = 2
started = False

directions = ['right', 'left', 'up', 'down']
direction = [0, 0, 0, 0]
curr_direction = ""

apple_x = random.randint(0, (screen_width // square_size) - 1) * square_size
apple_y = random.randint(0, (screen_height // square_size) - 1) * square_size

# Set up the Pygame window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

screen.fill((240, 240, 240))
def restart():
    global started, head_x, head_y, snake_squares, snake_len, direction, apple_x, apple_y
    started = False
    head_x = start_pos
    head_y = start_pos
    snake_squares = [
        [start_pos, start_pos + square_size],
        [start_pos, start_pos]
    ]
    snake_len = 2
    direction = [0, 0, 0, 0]
    apple_x = random.randint(0, (screen_width // square_size) - 1) * square_size
    apple_y = random.randint(0, (screen_height // square_size) - 1) * square_size
    draw() # Start a new frame

def game_over():
    screen.fill((240, 240, 240))
    draw_snake()
    font = pygame.font.SysFont("Courier New", 35)
    text = font.render("GAME OVER", True, (184, 0, 0))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)
    text = font.render("Press 'restart' or 'R' to try again", True, (184, 0, 0))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    screen.blit(text, text_rect)
    pygame.display.flip()
    running = False

def apple_handler():
    global snake_len, apple_x, apple_y
    if head_x == apple_x and head_y == apple_y:
        apple_x = random.randint(0, (screen_width // square_size) - 1) * square_size
        apple_y = random.randint(0, (screen_height // square_size) - 1) * square_size
        snake_len += 1

    pygame.draw.rect(screen, (184, 0, 0), (apple_x, apple_y, square_size - 1, square_size - 1))

def collision_detection():
    if head_x < 0 or head_x >= screen_width or head_y < 0 or head_y >= screen_height:
        game_over()
        return True

    for i in range(len(snake_squares) - 1):
        if snake_squares[i][0] == head_x and snake_squares[i][1] == head_y:
            game_over()
            return True

    return False

def draw_snake():
    for square in snake_squares:
        pygame.draw.rect(screen, (0, 191, 0), (square[0], square[1], square_size - 2, square_size - 2))
    
def draw_score():
    font = pygame.font.SysFont("Courier New", 35)
    text = font.render("Score: " + str(snake_len - 2), True, (0, 0, 0))
    text_rect = text.get_rect(topright=(screen_width - 10, 10))
    screen.blit(text, text_rect)

def draw():
    global count, head_x, head_y, snake_squares, direction, started, curr_direction

    if started:
        head_x = head_x + direction[0] * square_size - direction[1] * square_size
        head_y = head_y + direction[3] * square_size - direction[2] * square_size
        curr_direction = directions[direction.index(1)]
        
        screen.fill((240, 240, 240))

        if collision_detection():
            return
        snake_squares.append([head_x, head_y])
        if len(snake_squares) > snake_len:
            snake_squares.pop(0)
    else:
        screen.fill((240, 240, 240))
        font = pygame.font.SysFont("Courier New", 35)
        text = font.render("Welcome to Snake", True, (184, 0, 0))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
        screen.blit(text, text_rect)
        text = font.render("Use the arrow keys to start", True, (184, 0, 0))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(text, text_rect)
        if direction[1]:
            snake_squares = [
                [start_pos, start_pos]
                [start_pos, start_pos + square_size]
            ]

    draw_snake()
    apple_handler()
    draw_score()
    pygame.display.flip()

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(15)  # Limit frame rate to 15 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:         # If the right arrow key is pressed
                if curr_direction != "left":
                    direction = [1, 0, 0, 0]
                started = True
            elif event.key == pygame.K_LEFT:        # If the left arrow key is pressed
                if curr_direction != "right":
                    direction = [0, 1, 0, 0]
                started = True
            elif event.key == pygame.K_UP:          # If the up arrow key is pressed
                if curr_direction != "down":
                    direction = [0, 0, 1, 0]
                started = True
            elif event.key == pygame.K_DOWN:        # If the down arrow key is pressed
                if curr_direction != "up":
                    direction = [0, 0, 0, 1]
                started = True
            if event.key == pygame.K_r:
                restart()
    draw()

pygame.quit()
