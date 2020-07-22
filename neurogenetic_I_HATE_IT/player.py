import neuro
import config


class Player():
    def __init__(self):
        self.score = 0
        self.neuronetwork = neuro.NeuroNetwork(
            config.Inputs, config.Hiddens, config.Outputs)

    def feed_forward(self, inputs):
        return self.neuronetwork.feed_forward(inputs)

    def get_data(self):
        return self.neuronetwork.get_weights()
