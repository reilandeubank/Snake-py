import pygame
import random

pygame.init()

class SnakeGame:

    def __init__(self, speed = 15):
        # Set up the screen
        self.speed = speed
        self.screen_width = 800
        self.screen_height = 800
        self.square_size = 32
        self.side_length = self.screen_width // self.square_size
        self.start_pos = (self.side_length // 2) * self.square_size
        self.head_x = self.start_pos
        self.head_y = self.start_pos
        self.snake_squares = [
            [self.start_pos, self.start_pos + self.square_size],
            [self.start_pos, self.start_pos]
        ]
        self.snake_len = 2

        self.directions = ['right', 'left', 'up', 'down']
        self.direction = [0, 0, 1, 0]
        self.curr_direction = ""


        # Set up the Pygame window
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen.fill((240, 240, 240))
        self.restart()
    
    def restart(self):
        self.head_x = self.start_pos
        self.head_y = self.start_pos
        self.snake_squares = [
            [self.start_pos, self.start_pos + self.square_size],
            [self.start_pos, self.start_pos]
        ]
        self.running = True
        self.snake_len = 2
        self.direction = [0, 0, 1, 0]
        self.curr_direction = ""
        self.apple_x = random.randint(0, (self.screen_width // self.square_size) - 1) * self.square_size
        self.apple_y = random.randint(0, (self.screen_height // self.square_size) - 1) * self.square_size

    def apple_handler(self):
        if self.head_x == self.apple_x and self.head_y == self.apple_y:
            self.apple_x = random.randint(0, (self.screen_width // self.square_size) - 1) * self.square_size
            self.apple_y = random.randint(0, (self.screen_height // self.square_size) - 1) * self.square_size
            self.snake_len += 1

        pygame.draw.rect(self.screen, (184, 0, 0), (self.apple_x, self.apple_y, self.square_size - 1, self.square_size - 1))

    def collision_detection(self):
        if self.head_x < 0 or self.head_x >= self.screen_width or self.head_y < 0 or self.head_y >= self.screen_height:
            return True

        for i in range(len(self.snake_squares) - 1):
            if self.snake_squares[i][0] == self.head_x and self.snake_squares[i][1] == self.head_y:
                return True

        return False

    def draw_snake(self):
        for square in self.snake_squares:
            pygame.draw.rect(self.screen, (0, 191, 0), (square[0], square[1], self.square_size - 2, self.square_size - 2))
    
    def draw_score(self):
        font = pygame.font.SysFont("Courier New", 35)
        text = font.render("Score: " + str(self.snake_len - 2), True, (0, 0, 0))
        text_rect = text.get_rect(topright=(self.screen_width - 10, 10))
        self.screen.blit(text, text_rect)

    def draw(self):
        self.head_x = self.head_x + self.direction[0] * self.square_size - self.direction[1] * self.square_size
        self.head_y = self.head_y + self.direction[3] * self.square_size - self.direction[2] * self.square_size
        self.curr_direction = self.directions[self.direction.index(1)]

        self.screen.fill((240, 240, 240))

        if self.collision_detection():
            self.running = False
            return
        self.snake_squares.append([self.head_x, self.head_y])
        if len(self.snake_squares) > self.snake_len:
            self.snake_squares.pop(0)

        self.draw_snake()
        self.apple_handler()
        self.draw_score()
        pygame.display.flip()



    def go(self):
        self.restart()
        while self.running:
            self.clock.tick(self.speed)  # Limit frame rate to 15 FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:         # If the right arrow key is pressed
                        if self.curr_direction != "left":
                            self.direction = [1, 0, 0, 0]
                    elif event.key == pygame.K_LEFT:        # If the left arrow key is pressed
                        if self.curr_direction != "right":
                            self.direction = [0, 1, 0, 0]
                    elif event.key == pygame.K_UP:          # If the up arrow key is pressed
                        if self.curr_direction != "down":
                            self.direction = [0, 0, 1, 0]
                    elif event.key == pygame.K_DOWN:        # If the down arrow key is pressed
                        if self.curr_direction != "up":
                            self.direction = [0, 0, 0, 1]
                    if event.key == pygame.K_r:
                        restart()
                    elif event.key == pygame.K_q:
                        self.running = False
            self.draw()

        # pygame.quit()
# go()



#Not working entirely. Might need to turn into a class in order to be used by other files for agent control.
