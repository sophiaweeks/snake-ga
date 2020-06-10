# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 16:46:22 2020

@author: sophia.weeks
"""
import pygame
from Player import Player, Direction
from Food import Food
from World import InputModel
from random import randint
import numpy as np

class Game:
    def __init__(self, world, high_score):
        pygame.display.set_caption('SnakeGen')
        self.game_width = world.width
        self.game_height = world.height
        self.input_model = world.input_model

        # initialize rendering info
        self.display_unit_size = 20
        self.display_width = self.display_unit_size * self.game_width
        self.display_height = self.display_unit_size * self.game_height
        self.display_border = 20
        self.display_origin = (self.display_border, self.display_border)

        self.ui_display_height = 60
        self.ui_display_y = self.display_height + self.display_border * 2
        window_width = self.display_width + self.display_border * 2
        window_height = self.display_height + self.display_border * 2 + self.ui_display_height
        self.gameDisplay = pygame.display.set_mode((window_width, window_height))
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
        if self.input_model == InputModel.WORLD:
            state = np.array([np.concatenate([
                [self.player.x / self.game_width,
                self.player.y / self.game_height,
                self.get_moving_left(),
                self.get_moving_right(),
                self.get_moving_up(),
                self.get_moving_down(),
                self.get_food_left(),
                self.get_food_right(),
                self.get_food_up(),
                self.get_food_down()],
                self.get_bp_grid().flatten(),
            ])])
            return state
        elif self.input_model == InputModel.LOCAL:
            return np.array([[
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
                ]])

    def update_ui(self):
        self.gameDisplay.fill((255, 255, 255))
        text_score = self.font.render('SCORE: ', True, (0, 0, 0))
        text_score_number = self.font.render(str(self.score), True, (0, 0, 0))
        text_highest = self.font.render('HIGHEST SCORE: ', True, (0, 0, 0))
        text_highest_number = self.bold_font.render(str(self.high_score), True, (0, 0, 0))
        self.gameDisplay.blit(text_score, (45, self.ui_display_y))
        self.gameDisplay.blit(text_score_number, (120, self.ui_display_y))
        self.gameDisplay.blit(text_highest, (190, self.ui_display_y))
        self.gameDisplay.blit(text_highest_number, (350, self.ui_display_y))
        self.gameDisplay.blit(self.bg, (10, 10))

    def initialize_player(self):
        x = randint(0, self.game_width - 1)
        y = randint(0, self.game_height - 1)
        self.player = Player(x, y)

    def initialize_food(self):
        self.food = Food()
        self.set_new_food_position()

    def is_player_crashed(self):
        player_x = self.player.x
        player_y = self.player.y
        return (player_x < 0 or
            player_x >= self.game_width or
            player_y < 0 or
            player_y >= self.game_height)

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

        x = randint(0, self.game_width - 1)
        y = randint(0, self.game_height - 1)

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
        display_unit_size = self.display_unit_size
        origin_x = self.display_origin[0]
        origin_y = self.display_origin[1]
        for bp in player.body_positions:
            self.gameDisplay.blit(player.image, (origin_x + bp[0] * display_unit_size, origin_y + bp[1] * display_unit_size))

    def display_food(self):
        food = self.food
        display_unit_size = self.display_unit_size
        origin_x = self.display_origin[0]
        origin_y = self.display_origin[1]
        self.gameDisplay.blit(food.image, (origin_x + food.x * display_unit_size, origin_y + food.y * display_unit_size))

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
        return (int)(next_position_up_y < 0 or
                [player.x, next_position_up_y] in player.body_positions)

    def get_danger_right(self):
        player = self.player
        next_position_right_x = self.player.x + 1
        return (int)(next_position_right_x >= self.game_width or
                [next_position_right_x, player.y] in player.body_positions)

    def get_danger_down(self):
        player = self.player
        next_position_down_y = self.player.y + 1
        return (int)(next_position_down_y >= self.game_height or
                [player.x, next_position_down_y] in player.body_positions)

    def get_danger_left(self):
        player = self.player
        next_position_left_x = self.player.x - 1
        return (int)(next_position_left_x < 0 or
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

    def get_pos_validity(self, pos):
        [x, y] = pos
        return (0 <= x and x < self.game_width and
            0 <= y and y < self.game_height)

    def get_bp_grid(self):
        grid = np.zeros((self.game_width, self.game_height))
        for bp in self.player.body_positions:
            if self.get_pos_validity(bp):
                grid[bp] = 1
        return grid

