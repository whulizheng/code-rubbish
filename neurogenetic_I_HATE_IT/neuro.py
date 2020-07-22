import numpy as np
import random


def random_clamped():
    return 2 * random.random()


def htan(sum):
    return (np.exp(sum) - np.exp(-sum)) / (np.exp(sum) + np.exp(-sum))


class Neuro():
    def __init__(self, n):
        self.biase = 1
        self.weights = []
        for i in range(n):
            self.weights.append(random_clamped())


class Layer():
    def __init__(self, index, n_input, n_neuro):
        self.index = index
        self.neuros = []
        for i in range(n_neuro):
            neuro = Neuro(n_input)
            self.neuros.append(neuro)


class NeuroNetwork():
    def __init__(self, inputs, hiddens, output):
        self.score = 0
        self.layers = []
        index = 0
        preNeuros = 0
        # init inputs
        layer = Layer(index, preNeuros, inputs)
        self.layers.append(layer)
        preNeuros = inputs
        index += 1
        # init hiddens
        for i in range(len(hiddens)):
            layer = Layer(index, preNeuros, hiddens[i])
            self.layers.append(layer)
            preNeuros = hiddens[i]
            index += 1
        # init output
        layer = Layer(index, preNeuros, output)
        self.layers.append(layer)

    def get_weights(self):
        data = {'network': [], 'weights': []}
        for layer in self.layers:
            data['network'].append(len(layer.neuros))
            for neuron in layer.neuros:
                for weight in neuron.weights:
                    data['weights'].append(weight)
        return data

    def set_weights(self, data):
        preNeuros = 0
        index = 0
        index_weights = 0
        self.layers = []
        for i in data['network']:
            layer = Layer(index, preNeuros, i)
            for j in range(len(layer.neuros)):
                for k in range(len(layer.neuros[j].weights)):
                    layer.neuros[j].weights[k] = data['weights'][index_weights]
                    index_weights += 1
            preNeuros = i
            index += 1
            self.layers.append(layer)

    def feed_forward(self, inputs):
        for i in range(len(inputs)):
            self.layers[0].neuros[i].biase = inputs[i]
        # input层
        prev_layer = self.layers[0]
        for i in range(len(self.layers)):
            # 第一层没有weights
            if i == 0:
                continue
            for j in range(len(self.layers[i].neuros)):
                sum = 0
                for k in range(len(prev_layer.neuros)):
                    sum += prev_layer.neuros[k].biase * self.layers[i].neuros[
                        j].weights[k]
                self.layers[i].neuros[j].biase = htan(sum)
            prev_layer = self.layers[i]

        out = []
        last_layer = self.layers[-1]
        for i in range(len(last_layer.neuros)):
            out.append(last_layer.neuros[i].biase)
        return out

    def print_info(self):
        for layer in self.layers:
            print(layer)
