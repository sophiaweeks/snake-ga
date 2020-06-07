from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import random
import numpy as np
import pandas as pd
from operator import add
import collections

class DQNAgent(object):
    def __init__(self, params):
        self.reward = 0
        self.gamma = 0.9
        self.dataframe = pd.DataFrame()
        self.short_memory = np.array([])
        self.agent_target = 1
        self.agent_predict = 0
        self.learning_rate = params['learning_rate']        
        self.epsilon = 1
        self.actual = []
        self.first_layer = params['first_layer_size']
        self.second_layer = params['second_layer_size']
        self.third_layer = params['third_layer_size']
        self.memory = collections.deque(maxlen=params['memory_size'])
        self.weights = params['weights_path']
        self.load_weights = params['load_weights']
        self.model = self.network()
        
        if (params['load_weights']):
            self.model.load_weights(params['weights_path'])

    def network(self):
        model = Sequential()
        model.add(Dense(units=self.first_layer, activation='relu', input_dim=11))
        model.add(Dense(units=self.second_layer, activation='relu'))
        model.add(Dense(units=self.third_layer, activation='relu'))
        model.add(Dense(units=3, activation='softmax'))
        opt = Adam(self.learning_rate)
        model.compile(loss='mse', optimizer=opt)

        return model

    def set_reward(self, crash, eaten, player_direction, direction_to_food):
        self.reward = 0
        if crash:
            self.reward = -10
        elif eaten:
            self.reward = 10
        # Now check if it is moving in the opposite direction as the food and lower reward accordingly
        else:
            if (direction_to_food[0] == 1 and player_direction[1] == 1) or (direction_to_food[1] == 1 and player_direction[0] == 1):
                self.reward = -1
            elif (direction_to_food[2] == 1 and player_direction[3] == 1) or (direction_to_food[3] == 1 and player_direction[2] == 1):
                self.reward = -1
                

    def remember(self, state, action, next_state, done):
        self.memory.append((state, action, self.reward, next_state, done))

    def replay_new(self, memory, batch_size):
        if len(memory) > batch_size:
            minibatch = random.sample(memory, batch_size)
        else:
            minibatch = memory
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
            target_f = self.model.predict(np.array([state]))
            target_f[0][np.argmax(action)] = target
            self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)

    def train_short_memory(self, state, action, next_state, done):
        target = self.reward
        if not done:
            target = self.reward + self.gamma * np.amax(self.model.predict(next_state.reshape((1, 11)))[0])
        target_f = self.model.predict(state.reshape((1, 11)))
        target_f[0][np.argmax(action)] = target
        self.model.fit(state.reshape((1, 11)), target_f, epochs=1, verbose=0)
