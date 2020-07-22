import config
import random


def getscore(elem):
    return elem.score


class Genome():
    def __init__(self, data, score):
        self.data = data
        self.score = score


class Gereration():
    def __init__(self):
        self.genomes = []

    def get_outstandings(self, last_gereration):  # 择优
        index = 0
        last_gereration.genomes.sort(reverse=True, key=getscore)
        for genome in last_gereration.genomes:

            # print(genome.score)
            index += 1
            if index <= config.Population/3:
                self.genomes.append(genome)
        # print("#############")

    def hybridization(self):  # 杂交
        index = len(self.genomes)
        for i in range(config.Population-index):
            data1 = self.genomes[random.randint(0, index-1)].data
            data2 = self.genomes[random.randint(0, index-1)].data
            for x in range(len(data1['weights'])):
                if random.random() < config.HybridizationLevel/100:
                    data1['weights'][x] = data2['weights'][x]
            Agenome = Genome(data1, 0)
            self.genomes.append(Agenome)

    def variation(self):  # 变异
        for i in range(len(self.genomes)):
            if random.random() <= config.VariationRate:
                for x in range(len(self.genomes[i].data['weights'])):
                    if random.random() < config.VariationLevel/100:
                        self.genomes[i].data['weights'][x] = random.random()
