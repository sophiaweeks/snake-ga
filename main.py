# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 18:01:15 2020

@author: sophia.weeks
"""

import pygame
from Game import Game
import argparse
from DQN import DQNAgent
from DDQN import DDQNAgent
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def define_parameters():
    params = dict()
    params['epsilon_decay_linear'] = 1/75
    params['learning_rate'] = 0.0005
    params['first_layer_size'] = 150   # neurons in the first layer
    params['second_layer_size'] = 150   # neurons in the second layer
    params['third_layer_size'] = 150    # neurons in the third layer
    params['episodes'] = 150            
    params['memory_size'] = 2500
    params['batch_size'] = 500
    params['dqn_weights_path'] = 'weights/dqn/weights.hdf5'
    params['ddqn_weights_path'] = 'weights/ddqn/weights.hdf5'
    params['ddqn_target_weights_path'] = 'weights/ddqn/target_weights.hdf5'
    params['load_weights'] = True
    params['train'] = False
    params['bayesian_optimization'] = False
    params['agent_type'] = 'ddqn'
    params['tau'] = .01
    return params

def plot_seaborn(array_counter, array_score):
    sns.set(color_codes=True)
    ax = sns.regplot(
        np.array([array_counter])[0],
        np.array([array_score])[0],
        color="b",
        x_jitter=.1,
        line_kws={'color': 'green'}
    )
    ax.set(xlabel='games', ylabel='score')
    plt.show()
    
def get_reward(game):
    if game.crash:
        return -10
    elif game.player.eaten:
        return 10
    else:
        return 0
    
def handle_game_event(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return True
        if event.type == pygame.KEYDOWN:
            game.crash = True
    return False

def play(display_on, speed, params):
    pygame.init()
    pygame.font.init()
    
    agent = DQNAgent(params)
    if params['agent_type'] == 'ddqn':
        agent = DDQNAgent(params)
    
    counter_games = 0
    high_score = 0;
    score_plot = []
    counter_plot = []
    
    while counter_games < params['episodes']:
        game = Game(440, 440, high_score)
        
        if display_on:
            game.update_display()
        
        while not game.crash:
            if handle_game_event(game):
                return
            
            state = game.get_state()          
            move = agent.get_move(state)
            
            game.do_move(move)
            
            if display_on:
                game.update_display()
                pygame.time.wait(speed)
            
        counter_games += 1
        print(f'Game {counter_games}      Score: {game.score}')
        high_score = game.high_score
        
        score_plot.append(game.score)
        counter_plot.append(counter_games)

    pygame.quit()
    plot_seaborn(counter_plot, score_plot)

        
def train(display_on, speed, params):
    pygame.init()
    pygame.font.init()
    
    agent = DQNAgent(params)
    if params['agent_type'] == 'ddqn':
        agent = DDQNAgent(params)
    
    counter_games = 0
    high_score = 0;
    score_plot = []
    counter_plot = []
    
    while counter_games < params['episodes']:
        game = Game(440, 440, high_score)
        
        if display_on:
            game.update_display()
        
        while not game.crash:
            if handle_game_event(game):
                return
            
            # agent.epsilon is set to give randomness to actions
            agent.epsilon = 1 - (counter_games * params['epsilon_decay_linear'])
            
            state = game.get_state()          
            move = agent.get_move(state)
            game.do_move(move)
            
            new_state = game.get_state()
            reward = get_reward(game)
            
            # train short memory base on the new action and state
            agent.train_short_memory(state, move, reward, new_state, game.crash)
            
            agent.remember(state, move, reward, new_state, game.crash)
            
            if display_on:
                game.update_display()
                pygame.time.wait(speed)
            
        counter_games += 1
        print(f'Game {counter_games}      Score: {game.score}')
        high_score = game.high_score
        
        score_plot.append(game.score)
        counter_plot.append(counter_games)
        
        agent.replay_memory(params['batch_size'])
        
    agent.save_weights()
    pygame.quit()
    plot_seaborn(counter_plot, score_plot)


if __name__ == '__main__':
    # Set options to activate or deactivate the game view, and its speed

    parser = argparse.ArgumentParser()
    params = define_parameters()
    parser.add_argument("--display", type=bool, default=True)
    parser.add_argument("--speed", type=int, default=10)
    args = parser.parse_args()
    
    if params['train']:
        train(args.display, args.speed, params)
    else:
        play(args.display, args.speed, params)
