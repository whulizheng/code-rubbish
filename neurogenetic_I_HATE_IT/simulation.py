import player
import genetic
import config


class Simulation():
    def __init__(self):
        self.players = []
        for i in range(config.Population):
            Aplayer = player.Player()
            self.players.append(Aplayer)

    def Clearing(self):
        self.generation = genetic.Gereration()
        for player in self.players:
            genome = genetic.Genome(player.get_data(), player.score)
            self.generation.genomes.append(genome)
        #

    def Generate(self):
        next_generation = genetic.Gereration()
        next_generation.get_outstandings(self.generation)
        next_generation.hybridization()
        next_generation.variation()
        self.generation = next_generation
        for i in range(config.Population):
            self.players[i].neuronetwork.set_weights(
                self.generation.genomes[i].data)
