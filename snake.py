import pygame
import random
import numpy as np

pygame.init()

class SnakeGame:

    def __init__(self, speed):
        # Set up the screen
        self.speed = speed
        self.screen_width = 800
        self.screen_height = 800
        self.square_size = 32
        self.side_length = self.screen_width // self.square_size
        self.start_pos = (self.side_length // 2) * self.square_size
        self.frame_iteration = 0


        # Set up the Pygame window
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen.fill((240, 240, 240))
        self.clock.tick(self.speed)
        self.counter = 0
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
        self.curr_direction = "up"
        self.apple_x = random.randint(0, (self.screen_width // self.square_size) - 1) * self.square_size
        self.apple_y = random.randint(0, (self.screen_height // self.square_size) - 1) * self.square_size


    def apple_handler(self):
        pygame.draw.rect(self.screen, (184, 0, 0), (self.apple_x, self.apple_y, self.square_size - 1, self.square_size - 1))
        if self.head_x == self.apple_x and self.head_y == self.apple_y:
            self.apple_x = random.randint(0, (self.screen_width // self.square_size) - 1) * self.square_size
            self.apple_y = random.randint(0, (self.screen_height // self.square_size) - 1) * self.square_size
            self.snake_len += 1
            return True
        return False


    def collision_detection(self, point):
        if self.frame_iteration > 100 * self.snake_len:
            return True
        
        if point[0] < 0 or point[0] >= self.screen_width or point[1] < 0 or point[1] >= self.screen_height:
            return True

        for i in range(len(self.snake_squares) - 3):            # -3 because it is impossible to hit the snake's head or 2 squares behind the head
            if self.snake_squares[i][0] == point[0] and self.snake_squares[i][1] == point[1]:
                return True

        return False

    def vision(self):
        points = []
        
        for i in range(-2, 3):
            row = []
            for j in range(-2, 3):
                row.append(int(self.collision_detection([self.head_x + j*self.square_size, self.head_y+ i*self.square_size])))
                if self.apple_x == self.head_x + j*self.square_size and self.apple_y == self.head_y + i*self.square_size:
                    row[-1] = -1
            points.append(row)
        return points


    def draw_snake(self):
        for square in self.snake_squares:
            pygame.draw.rect(self.screen, (0, 191, 0), (square[0], square[1], self.square_size - 2, self.square_size - 2))
    
    def draw_score(self):
        font = pygame.font.SysFont("Courier New", 35)
        text = font.render("Score: " + str(self.snake_len - 2), True, (0, 0, 0))
        text_rect = text.get_rect(topright=(self.screen_width - 10, 10))
        self.screen.blit(text, text_rect)

    def draw(self):
        self.frame_iteration += 1
        reward = 0
        game_over = False
        self.screen.fill((240, 240, 240))

        if self.collision_detection([self.head_x, self.head_y]):
            self.running = False
            game_over = True
            reward = -10
            return reward, game_over, self.snake_len - 2
        self.snake_squares.append([self.head_x, self.head_y])
        if len(self.snake_squares) > self.snake_len:
            self.snake_squares.pop(0)

        self.draw_snake()
        if self.apple_handler():
            reward = 50
        self.draw_score()
        pygame.display.flip()
        # print(reward, game_over, self.snake_len - 2)
        return reward, game_over, self.snake_len - 2



    def go(self, action):
        self.screen.fill((240, 240, 240))
        speedChange = ""
        # self.restart()
        self.clock.tick(self.speed)  # Limit frame rate to 15 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:         # If the right arrow key is pressed
                    speedChange = "Up" 
                elif event.key == pygame.K_LEFT:        # If the left arrow key is pressed
                    speedChange = "Down"



        clock_wise = ["right", "down", "left", "up"]
        idx = clock_wise.index(self.curr_direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            new_dir = clock_wise[(idx + 1) % 4]
        else:
            new_dir = clock_wise[(idx - 1) % 4]

            self.curr_direction = new_dir

            if self.curr_direction == "right":
                self.direction = [1, 0, 0, 0]
            elif self.curr_direction == "left":
                self.direction = [0, 1, 0, 0]
            elif self.curr_direction == "up":
                self.direction = [0, 0, 1, 0]
            elif self.curr_direction == "down":
                self.direction = [0, 0, 0, 1]
        self.head_x = self.head_x + self.direction[0] * self.square_size - self.direction[1] * self.square_size
        self.head_y = self.head_y + self.direction[3] * self.square_size - self.direction[2] * self.square_size    

        # print(self.head_x, self.head_y)
        reward, game_over, score = self.draw()
        return reward, game_over, score, speedChange

