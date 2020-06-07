# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 16:46:22 2020

@author: sophia.weeks
"""
import pygame
from Player import Player
from Food import Food
from random import randint

class Game:
    def __init__(self, game_width, game_height):
        pygame.display.set_caption('SnakeGen')
        self.game_width = game_width
        self.game_height = game_height
        self.unit_size = 20
        self.left_boundary = self.unit_size
        self.right_boundary = game_width - (self.unit_size * 2)
        self.bottom_boundary = self.unit_size
        self.top_boundary = game_height - (self.unit_size * 2)
        self.gameDisplay = pygame.display.set_mode((game_width, game_height + 60))
        self.bg = pygame.image.load("img/background.png")
        self.font = pygame.font.SysFont('Segoe UI', 20)
        self.bold_font = pygame.font.SysFont('Segoe UI', 20, True)
        
        self.crash = False
        self.score = 0
        self.high_score = 0
        self.initialize_player()
        self.initialize_food()
    
        
    def do_move(self, move):
        self.player.do_move(move)
        if self.is_player_crashed():
            self.crash = True
        self.try_eat()
        
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
        y = (int)(randint(self.bottom_boundary, self.top_boundary) / self.unit_size)
        self.player = Player(x, y)
        
    def initialize_food(self):
        self.food = Food()
        self.set_new_food_position()
            
    def is_player_crashed(self):
        player_x = self.player.x * self.unit_size
        player_y = self.player.y * self.unit_size
        return (player_x < self.left_boundary or 
            player_x > self.right_boundary or 
            player_y < self.bottom_boundary or 
            player_y > self.top_boundary)
    
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
        y = (int)(randint(self.bottom_boundary, self.top_boundary) / self.unit_size)

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
