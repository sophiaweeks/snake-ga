from enum import Enum

class InputModel(Enum):
    # For WORLD, the inputs to the algorithm are
    # the absolute position of the player, the movement direction,
    # the relative direction to food, and the state of the entire
    # game grid
    WORLD = 'world'

    # For LOCAL, the inputs to the algorithm are
    # the safety status of the square in front of, to the left of,
    # and to the right of the player, the movement direction, and the
    # relative direction to food
    LOCAL = 'local'

class World:
    def __init__(self, width, height, input_model):
        self.width = width
        self.height = height
        self.input_model = input_model

    def input_vector_len(self):
        if self.input_model == InputModel.WORLD:
            return 10 + self.width * self.height
        elif self.input_model == InputModel.LOCAL:
            return 11
