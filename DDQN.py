from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
from keras.utils import to_categorical
import random
import numpy as np
import pandas as pd
from operator import add
import collections

class DDQNAgent(object):
    def __init__(self, params):
        self.gamma = 0.9
        self.short_memory = np.array([])
        self.learning_rate = params['learning_rate']        
        self.epsilon = 0
        self.first_layer = params['first_layer_size']
        self.second_layer = params['second_layer_size']
        self.third_layer = params['third_layer_size']
        self.memory = collections.deque(maxlen=params['memory_size'])
        self.model = self.network()
        self.target_model = self.network()
        self.tau = params['tau']
        self.weights_path = params['ddqn_weights_path']
        self.target_weights_path = params['ddqn_target_weights_path']

        if params['load_weights']:
            self.model.load_weights(params['ddqn_weights_path'])
            self.model.load_weights(params['ddqn_target_weights_path'])
        if params['train']:
            self.epsilon = 1

    def network(self):
        model = Sequential()
        model.add(Dense(units=self.first_layer, activation='relu', input_dim=11))
        model.add(Dense(units=self.second_layer, activation='relu'))
        model.add(Dense(units=self.third_layer, activation='relu'))
        model.add(Dense(units=3, activation='softmax'))
        opt = Adam(self.learning_rate)
        model.compile(loss='mse', optimizer=opt)

        return model

    def get_move(self, state):
        # perform random actions based on agent.epsilon, or choose the action
        if random.randint(0, 1) < self.epsilon:
            return to_categorical(random.randint(0, 2), num_classes=3)
            
        # predict action based on the old state
        prediction = self.model.predict(state)
        return to_categorical(np.argmax(prediction[0]), num_classes=3)


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay_memory(self, batch_size):
        memory = self.memory
        if len(memory) > batch_size:
            minibatch = random.sample(memory, batch_size)
        else:
            minibatch = memory
        for state, action, reward, next_state, done in minibatch:
            self.train_short_memory(state, action, reward, next_state, done)

    # this is where the magic happens
    def train_short_memory(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            # use target_model to determine action (argmax_a'Q'(s',a')) 
            action_index = np.argmax(self.target_model.predict(next_state)[0])
            # use model teo determine value (Q*(s,a) = r + gamma * Q(s', argmax_a'Q'(s',a')))
            target = reward + self.gamma * self.model.predict(next_state)[0][action_index]
        
        # update Q(s,a) with target value
        target_f = self.model.predict(state)
        target_f[0][np.argmax(action)] = target
        self.model.fit(state, target_f, epochs=1, verbose=0)
        
        # "slowly" update target weights using Polyak averaging (theta' = tau* theta + (1 - tau) * theta')
        weights_term_1 = self.tau * np.asarray(self.model.get_weights())
        weights_term_2 = (1 - self.tau) * np.asarray(self.target_model.get_weights())
        self.target_model.set_weights((weights_term_1 + weights_term_2).tolist())
        
    def save_weights(self):
        self.model.save_weights(self.weights_path)
        self.target_model.save_weights(self.target_weights_path)    
