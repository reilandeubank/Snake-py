import torch
import random
import numpy as np
from collections import deque
from snake import SnakeGame
from model import Linear_QNet, QTrainer
from helper import plot

# print(torch.cuda.is_available())
# print(torch.cuda.get_device_name(0))

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(11, 150, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def get_state(self, game):
        # point_l = [game.head_x - game.square_size, game.head_y]
        # point_r = [game.head_x + game.square_size, game.head_y]
        # point_u = [game.head_x, game.head_y - game.square_size]
        # point_d = [game.head_x, game.head_y + game.square_size]
        
        dir_r = game.direction[0]
        dir_l = game.direction[1]
        dir_u = game.direction[2]
        dir_d = game.direction[3]

        state = []
        
        if dir_r:
            state.append(game.vision([1, 0, 0, 0]))       #straight (right)
            state.append(game.vision([0, 0, 0, 1]))       #right (down)
            state.append(game.vision([0, 0, 1, 0]))       #left (up)
        elif dir_l:
            state.append(game.vision([0, 1, 0, 0]))       #straight (left)
            state.append(game.vision([0, 0, 1, 0]))       #right(up)
            state.append(game.vision([0, 0, 0, 1]))       #left (down)
        elif dir_u:
            state.append(game.vision([0, 0, 1, 0]))       #straight (up) 
            state.append(game.vision([1, 0, 0, 0]))       #right (right)
            state.append(game.vision([0, 1, 0, 0]))       #left (left) 
        elif dir_d:
            state.append(game.vision([0, 0, 0, 1]))       #straight (down)
            state.append(game.vision([0, 1, 0, 0]))       #right (left) 
            state.append(game.vision([1, 0, 0, 0]))       #left (right) 

        state.append(dir_r)
        state.append(dir_l)
        state.append(dir_u)
        state.append(dir_d)

            # Food location 
        if dir_u: # facing up
            state.append(game.apple_x < game.head_x)  # food left
            state.append(game.apple_x > game.head_x)  # food right
            state.append(game.apple_y < game.head_y)  # food up
            state.append(game.apple_y > game.head_y)  # food down
        elif dir_d:
            state.append(game.apple_x > game.head_x)
            state.append(game.apple_x < game.head_x)
            state.append(game.apple_y > game.head_y)
            state.append(game.apple_y < game.head_y)
        elif dir_l:
            state.append(game.apple_y > game.head_y)
            state.append(game.apple_y < game.head_y)
            state.append(game.apple_x < game.head_x)
            state.append(game.apple_x > game.head_x)
        elif dir_r:
            state.append(game.apple_y < game.head_y)
            state.append(game.apple_y > game.head_y)
            state.append(game.apple_x > game.head_x)
            state.append(game.apple_x < game.head_x)

        # print(state)
        return np.array(state, dtype=float)

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
        self.epsilon = min(25, 400 - self.n_games)
        final_move = [0,0,0]
        # if state[0] <= 0.05:
        #     self.epsilon = max(250, self.epsilon)
        if random.randint(0, 500) < self.epsilon:
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
