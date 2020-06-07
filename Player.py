# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 16:50:39 2020

@author: sophia.weeks
"""
import pygame
import numpy as np
from enum import IntEnum

class Direction(IntEnum): 
    up = 0
    right = 1
    down = 2
    left = 3

    def turn_right(self):
        num = self + 1
        if (num > 3):
            num = 0
        return Direction(num)
        
    def turn_left(self):
        num = self - 1
        if (num < 0):
            num = 3
        return Direction(num)
    
class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.body_positions = [[self.x, self.y]]
        self.size = 1
        self.eaten = False
        self.image = pygame.image.load('img/snakeBody.png')
        self.current_direction = Direction.right
    
    def do_move(self, move):
        self.absorb_food()            
        self.process_move(move)
        self.increment_position()
        if self.get_crashed():
            return True # report crash
        self.update_body_positions()
        return False
    
    def absorb_food(self):
        if self.eaten:
            self.body_positions.append([self.x, self.y])
            self.eaten = False
            self.size += 1
    
    def process_move(self, move):
        if np.array_equal(move, [0, 1, 0]):  # turn right
            self.current_direction = self.current_direction.turn_right()
        elif np.array_equal(move, [0, 0, 1]):  # turn left
            self.current_direction = self.current_direction.turn_left()
            
    def increment_position(self):
        if self.current_direction == Direction.up:
            self.y -= 1
        elif self.current_direction == Direction.right:
            self.x += 1
        elif self.current_direction == Direction.down:
            self.y += 1
        elif self.current_direction == Direction.left:
            self.x -= 1
            
    def get_crashed(self):
        return [self.x, self.y] in self.body_positions
            
    def update_body_positions(self):
        if self.body_positions[-1][0] != self.x or self.body_positions[-1][1] != self.y:
            if self.size > 1:
                for i in range(0, self.size - 1):
                    self.body_positions[i][0], self.body_positions[i][1] = self.body_positions[i + 1]
                    
            self.body_positions[-1][0] = self.x
            self.body_positions[-1][1] = self.y