import torch
import numpy as np
from collections import deque
from model import Linear_QNet, QTrainer
from game import Game
from snake import Snake
from display import Display
from apple import Apple
import random

MAX_MEMORY = 10**5
BATCH_SIZE = 10**3
LR = 0.001


class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(12, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0, 0]  # [up, down, right, left]

        if np.random.randint(0, 200) < self.epsilon:
            move = np.random.randint(0, 4)
            final_move[move] = 1

        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    total_score = 0
    record = 0
    agent = Agent()
    game = Game(Snake, Apple, Display)
    while True:
        # get old state
        state_old = game.get_state()
        # get move
        final_move = agent.get_action(state_old)

        if final_move[0] == 1:
            direction = (0, -1)
        elif final_move[1] == 1:
            direction = (0, 1)
        elif final_move[2] == 1:
            direction = (1, 0)
        elif final_move[3] == 1:
            direction = (-1, 0)

        reward, game_over, score = game.play_step(direction)
        state_new = game.get_state()

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)

        # remember
        agent.remember(state_old, final_move, reward, state_new, game_over)

        if game_over is True:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)
            total_score += score
