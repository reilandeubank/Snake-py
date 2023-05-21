import torch
import random
import numpy as np
from collections import deque
from snake import SnakeGame
from model import Linear_QNet, QTrainer
from helper import plot

# print(torch.cuda.is_available())
# print(torch.cuda.get_device_name(0))

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def get_state(self, game):
        point_l = [game.head_x - game.square_size, game.head_x]
        point_r = [game.head_x + game.square_size, game.head_x]
        point_u = [game.head_x, game.head_y - game.square_size]
        point_d = [game.head_x, game.head_y + game.square_size]
        
        dir_r = game.direction[0]
        dir_l = game.direction[1]
        dir_u = game.direction[2]
        dir_d = game.direction[3]

        state = [
            # Danger straight
            (dir_r and game.collision_detection(point_r)) or 
            (dir_l and game.collision_detection(point_l)) or 
            (dir_u and game.collision_detection(point_u)) or 
            (dir_d and game.collision_detection(point_d)),

            # Danger right
            (dir_u and game.collision_detection(point_r)) or 
            (dir_d and game.collision_detection(point_l)) or 
            (dir_l and game.collision_detection(point_u)) or 
            (dir_r and game.collision_detection(point_d)),

            # Danger left
            (dir_d and game.collision_detection(point_r)) or 
            (dir_u and game.collision_detection(point_l)) or 
            (dir_r and game.collision_detection(point_u)) or 
            (dir_l and game.collision_detection(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.apple_x < game.head_x,  # food left
            game.apple_x > game.head_x,  # food right
            game.apple_y < game.head_y,  # food up
            game.apple_y > game.head_y  # food down
            ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    speed = 300
    game = SnakeGame(speed)
    game.restart()
    while True:
        # game.clock.tick(game.speed)
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score, speedChange = game.go(final_move)

        # print(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if speedChange == "Up":
            speed += 10
            print("speed: ", speed)
        elif speedChange == "Down":
            speed -= 10
            print("speed:", speed)
        if done:
            # train long memory, plot result
            del game
            game = SnakeGame(speed)
            # game.restart()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()
