# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 16:46:22 2020

@author: sophia.weeks
"""
import pygame
from Player import Player, Direction
from Food import Food
from random import randint
import numpy as np

class Game:
    def __init__(self, game_width, game_height, high_score):
        pygame.display.set_caption('SnakeGen')
        self.game_width = game_width
        self.game_height = game_height
        self.unit_size = 20
        self.left_boundary = self.unit_size
        self.right_boundary = game_width - (self.unit_size * 2)
        self.top_boundary = self.unit_size
        self.bottom_boundary = game_height - (self.unit_size * 2)
        self.gameDisplay = pygame.display.set_mode((game_width, game_height + 60))
        self.bg = pygame.image.load("img/background.png")
        self.font = pygame.font.SysFont('Segoe UI', 20)
        self.bold_font = pygame.font.SysFont('Segoe UI', 20, True)
        
        self.crash = False
        self.score = 0
        self.high_score = high_score
        self.initialize_player()
        self.initialize_food()
    
        
    def do_move(self, move):
        if self.player.do_move(move):
            # player crashed into self
            self.crash = True
            return
        
        if self.is_player_crashed():
            # player crashed into border
            self.crash = True
        self.try_eat()
        
    def get_state(self):
        return np.array([
            self.get_danger_player_right(),
            self.get_danger_player_straight(),
            self.get_danger_player_left(),
            self.get_moving_left(),
            self.get_moving_right(),
            self.get_moving_up(),
            self.get_moving_down(),
            self.get_food_left(),
            self.get_food_right(),
            self.get_food_up(),
            self.get_food_down()
            ])
        
    def update_ui(self):
        self.gameDisplay.fill((255, 255, 255))
        text_score = self.font.render('SCORE: ', True, (0, 0, 0))
        text_score_number = self.font.render(str(self.score), True, (0, 0, 0))
        text_highest = self.font.render('HIGHEST SCORE: ', True, (0, 0, 0))
        text_highest_number = self.bold_font.render(str(self.high_score), True, (0, 0, 0))
        self.gameDisplay.blit(text_score, (45, 440))
        self.gameDisplay.blit(text_score_number, (120, 440))
        self.gameDisplay.blit(text_highest, (190, 440))
        self.gameDisplay.blit(text_highest_number, (350, 440))
        self.gameDisplay.blit(self.bg, (10, 10))
        
    def initialize_player(self):
        x = (int)(randint(self.left_boundary, self.right_boundary) / self.unit_size)
        y = (int)(randint(self.top_boundary, self.bottom_boundary) / self.unit_size)
        self.player = Player(x, y)
        
    def initialize_food(self):
        self.food = Food()
        self.set_new_food_position()
            
    def is_player_crashed(self):
        player_x = self.player.x * self.unit_size
        player_y = self.player.y * self.unit_size
        return (player_x < self.left_boundary or 
            player_x > self.right_boundary or 
            player_y < self.top_boundary or 
            player_y > self.bottom_boundary)
    
    def try_eat(self):
        player = self.player
        food = self.food
        if player.x == food.x and player.y == food.y:
            self.set_new_food_position()
            self.player.eaten = True
            self.increment_score()
      
    def increment_score(self):
        self.score += 1
        if self.score > self.high_score:
            self.high_score = self.score
        
    def set_new_food_position(self):
        player = self.player
        
        x = (int)(randint(self.left_boundary, self.right_boundary) / self.unit_size)
        y = (int)(randint(self.top_boundary, self.bottom_boundary) / self.unit_size)

        if [x, y] not in player.body_positions:
            self.food.update_position(x, y)
        else:
            self.set_new_food_position()          
    
    def update_display(self):
        if self.crash:
            pygame.time.wait(300)
            return
        
        self.update_ui()
        self.display_player()
        self.display_food()
        pygame.display.update()
        
    def display_player(self):
        player = self.player
        unit_size = self.unit_size
        for bp in player.body_positions:
            self.gameDisplay.blit(player.image, (bp[0] * unit_size, bp[1] * unit_size))
            
    def display_food(self):
        food = self.food
        unit_size = self.unit_size
        self.gameDisplay.blit(food.image, (food.x * unit_size, food.y * unit_size))
        
    def get_danger_player_right(self):
        direction = self.player.current_direction

        if direction == Direction.left:
            return self.get_danger_up()
        if direction == Direction.right:
            return self.get_danger_down()
        if direction == Direction.up:
            return self.get_danger_right()
        if direction == Direction.down:
            return self.get_danger_left()
    
    def get_danger_player_straight(self):
        direction = self.player.current_direction

        if direction == Direction.left:
            return self.get_danger_left()
        if direction == Direction.right:
            return self.get_danger_right()
        if direction == Direction.up:
            return self.get_danger_up()
        if direction == Direction.down:
            return self.get_danger_down()
    
    def get_danger_player_left(self):
        direction = self.player.current_direction

        if direction == Direction.left:
            return self.get_danger_down()
        if direction == Direction.right:
            return self.get_danger_up()
        if direction == Direction.up:
            return self.get_danger_left()
        if direction == Direction.down:
            return self.get_danger_right()
    
    def get_danger_up(self):
        player = self.player
        next_position_up_y = self.player.y - 1
        return (int)(next_position_up_y * self.unit_size < self.top_boundary or 
                [player.x, next_position_up_y] in player.body_positions)
    
    def get_danger_right(self):
        player = self.player
        next_position_right_x = self.player.x + 1
        return (int)(next_position_right_x * self.unit_size > self.right_boundary or 
                [next_position_right_x, player.y] in player.body_positions)
    
    def get_danger_down(self):
        player = self.player
        next_position_down_y = self.player.y + 1
        return (int)(next_position_down_y * self.unit_size > self.bottom_boundary or 
                [player.x, next_position_down_y] in player.body_positions)
    
    def get_danger_left(self):
        player = self.player
        next_position_left_x = self.player.x - 1
        return (int)(next_position_left_x * self.unit_size < self.left_boundary or 
                [next_position_left_x, player.y] in player.body_positions)
   
    def get_moving_left(self):
        return (int)(self.player.current_direction == Direction.left)
   
    def get_moving_right(self):
        return (int)(self.player.current_direction == Direction.right)
   
    def get_moving_up(self):     
        return (int)(self.player.current_direction == Direction.up)
   
    def get_moving_down(self):
        return (int)(self.player.current_direction == Direction.down)
   
    def get_food_left(self):
        return (int)(self.food.x < self.player.x)
   
    def get_food_right(self):
        return (int)(self.food.x > self.player.x)
        
    def get_food_up(self):
        return (int)(self.food.y < self.player.y)
   
    def get_food_down(self):
        return (int)(self.food.y > self.player.y)
   
