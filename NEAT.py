import pygame
from Game import Game
import neat
import os
import numpy as np
import random

EPSILON = 0.1


def play(network, num_games, display_on):
    total_score = 0

    for i in range(num_games):
        game = Game(400, 400, 0)

        if display_on:
            game.update_display()

        while not game.crash:

            state = game.get_state().T

            move = np.argmax(network.activate(state))
            if random.random() < EPSILON:
                move = random.randint(0, 2)

            if move == 1:
                game.do_move([0, 1, 0])
            elif move == 2:
                game.do_move([0, 0, 1])
            else:
                game.do_move([0, 0, 0])

            if display_on:
                game.update_display()
                pygame.time.wait(100)

        total_score += game.score

    return total_score / num_games


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        network = neat.nn.RecurrentNetwork.create(genome, config)
        genome.fitness = play(network, 10, False)


def run(config_file):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )
    pygame.init()

    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    # pop.add_reporter(neat.Checkpointer(5))

    best_genome = pop.run(eval_genomes, 100)

    network = neat.nn.RecurrentNetwork.create(best_genome, config)
    play(network, 2, True)

    pygame.quit()


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "NEAT-config")
    run(config_path)
