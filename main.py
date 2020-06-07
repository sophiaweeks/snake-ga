# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 18:01:15 2020

@author: sophia.weeks
"""

import pygame
from Game import Game
import argparse
from random import randint
from keras.utils import to_categorical

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
    params['weights_path'] = 'weights/weights.hdf5'
    params['load_weights'] = True
    params['train'] = False
    params['bayesian_optimization'] = False
    return params

def handle_game_event(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return True
        if event.type == pygame.KEYDOWN:
            game.crash = True
    return False

def run(display_on, speed, params):
    pygame.init()
    pygame.font.init()
    
    counter_games = 0
    #score_plot = []
    #counter_plot = []
    
    while counter_games < params['episodes']:
        game = Game(440, 440)
        
        if display_on:
            game.update_display()
        
        while not game.crash:
            if handle_game_event(game):
                return
            
            move = to_categorical(randint(0, 2), num_classes=3)
            game.do_move(move)
            
            if display_on:
                game.update_display()
                pygame.time.wait(speed)
            
        counter_games += 1
        print(f'Game {counter_games}      Score: {game.score}')


if __name__ == '__main__':
    # Set options to activate or deactivate the game view, and its speed

    parser = argparse.ArgumentParser()
    params = define_parameters()
    parser.add_argument("--display", type=bool, default=True)
    parser.add_argument("--speed", type=int, default=50)
    args = parser.parse_args()
    
    run(args.display, args.speed, params)
