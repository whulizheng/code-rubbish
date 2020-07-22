from tensorflow.keras.layers import Input, Dense, Reshape, Flatten, Dropout
from tensorflow.keras.layers import BatchNormalization, Activation, ZeroPadding2D
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.layers import UpSampling2D, Conv2D
from tensorflow.keras.models import Sequential, Model, load_model
from tensorflow.keras.optimizers import Adam
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import os


class generator():
    def __init__(self):
        self.flag = 4
        self.img_rows = 64  # 4的倍数
        self.img_cols = 64
        self.channels = 3
        self.img_shape = (self.img_rows, self.img_cols, self.channels)
        self.latent_dim = 100
        if os.path.exists('wtf_GAN/model.h5'):
            self.model = load_model('wtf_GAN/model.h5')
            print("Read succeed")
        else:
            self.model = self.build_model()
        optimizer = Adam(0.0002, 0.5)
        self.model.compile(optimizer=optimizer, loss='binary_crossentropy')

    def build_model(self):
        model = Sequential()
        model.add(Dense(128*int(self.img_rows/4) * int(self.img_cols/4),
                        activation="relu", input_dim=self.latent_dim))
        model.add(Reshape((int(self.img_rows/4), int(self.img_cols/4), 128)))
        model.add(UpSampling2D())
        model.add(Conv2D(128, kernel_size=3, padding="same"))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Activation("relu"))
        model.add(UpSampling2D())
        model.add(Conv2D(64, kernel_size=3, padding="same"))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Activation("relu"))
        model.add(Conv2D(self.channels, kernel_size=3, padding="same"))
        model.add(Activation("tanh"))
        model.summary()
        noise = Input(shape=(self.latent_dim,))
        img = model(noise)
        return Model(noise, img)

    def train(self):
        noise = np.random.normal(0, 1, (1, self.latent_dim))
        gen_img = self.model.predict(noise)[0]
        # Rescale images 0 - 1
        gen_img_r = 126 * gen_img + 126
        img = np.asarray(gen_img_r, dtype=int)
        valid = []
        if self.flag != 0:
            x = '0'
            self.flag -= 1
        else:
            plt.imshow(img)
            plt.show()
            x = input("")
            if x == '0':
                self.flag = 4
        if x == '1':
            valid = gen_img
        elif x == '0':
            img = mpimg.imread("wtf_GAN/test.jpg")
            from skimage import transform
            img = transform.resize(img, (self.img_cols, self.img_rows))
            img = np.array(img) * 255
            valid = img
        elif x == 'reset':
            os.remove("wtf_GAN/model.h5")
            self.__init__()
            return
        self.model.train_on_batch(noise, valid)

        mp = "wtf_GAN/model.h5"
        try:
            self.model.save(mp)
            print("Saving model to disk ")
        except:
            print("Permission denied")


generator = generator()
while(1):
    generator.train()
