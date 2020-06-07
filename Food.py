# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 16:51:27 2020

@author: sophia.weeks
"""
import pygame

class Food(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = pygame.image.load('img/food2.png')

    def update_position(self, x, y):
        self.x = x
        self.y = y
