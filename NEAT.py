import pygame
from Game import Game
import neat
import os
import numpy as np


def play(network, num_games, display_on):
    total_score = 0

    for i in range(num_games):
        game = Game(440, 440, 0)
        move_count = 0
        current_score = 0

        if display_on:
            game.update_display()

        while not game.crash:

            # End game if score has not been updated after x moves
            if move_count >= 440:
                break

            if current_score < game.score:
                current_score = game.score
                move_count = 0

            state = game.get_state().T
            move = np.argmax(network.activate(state))

            # move right
            if move == 1:
                game.do_move([0, 1, 0])
            # move left
            elif move == 2:
                game.do_move([0, 0, 1])
            # move straight
            else:
                game.do_move([0, 0, 0])

            if display_on:
                game.update_display()
                pygame.time.wait(10)

            move_count += 1

        total_score += game.score

    return total_score / num_games


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        network = neat.nn.RecurrentNetwork.create(genome, config)
        genome.fitness = play(network, 1, False)


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

    best_genome = pop.run(eval_genomes, 50)

    network = neat.nn.RecurrentNetwork.create(best_genome, config)
    play(network, 5, True)

    pygame.quit()


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "NEAT-config")
    run(config_path)
