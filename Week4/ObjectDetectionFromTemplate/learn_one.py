import numpy as np
from skimage.io import *
from skimage.measure import *
from skimage.transform import *
from skimage.morphology import *
from skimage import morphology


from sklearn.linear_model import *
from sklearn.tree import *
from sklearn.svm import *

import matplotlib.pyplot as plt

from cntk import Trainer
from cntk.utils import *
from cntk.layers import *
from cntk.io import MinibatchSource, CTFDeserializer, StreamDef, StreamDefs, INFINITELY_REPEAT, FULL_DATA_SWEEP
from cntk.learner import momentum_sgd, learning_rate_schedule, momentum_as_time_constant_schedule, UnitType, sgd
from cntk.ops import *
import random


def shuffle_arrays(inputs, targets):
    for time in range(len(inputs)):
        i = random.randint(0, len(inputs) - 1)
        j = random.randint(0, len(inputs) - 1)
        inputs[i], inputs[j] = inputs[j], inputs[i]
        targets[i], targets[j] = targets[j], targets[i]


def fill_data(img, mask, insz, outsz, inputs, targets):
    props = regionprops(mask)
    if len(props) == 0:
        imshow_collection([img, mask])
        show()
    bbox = props[0].bbox
    d0 = bbox[2] - bbox[0]
    d1 = bbox[3] - bbox[1]

    d0 = int(d0 * 0.25)
    d1 = int(d1 * 0.25)

    bbox = [bbox[0] - d0, bbox[1] - d1, bbox[2] + d0, bbox[3] + d1]


    pos_in = []
    pos_tar = []
    neg_in = []
    neg_tar = []

    diff = int((insz - outsz) / 2)
    for y in range(bbox[0], bbox[2] - insz, outsz):
        for x in range(bbox[1], bbox[3] - insz, outsz):
            in_patch = np.array(img[y:y+insz, x:x+insz, :])
            tar_patch = np.array(mask[y+diff:y+diff+outsz, x+diff:x+diff+outsz])
            if tar_patch.sum() > 0:
                pos_in.append(in_patch)
                pos_tar.append(tar_patch)
            else:
                neg_in.append(in_patch)
                neg_tar.append(tar_patch)

    shuffle_arrays(neg_in, neg_tar)

    inputs.extend(pos_in)
    targets.extend(pos_tar)
    inputs.extend(neg_in[:len(pos_in)])
    targets.extend(neg_tar[:len(pos_in)])


def get_train_data(img, mask, insz, outsz, step=5):
    inputs = []
    targets = []
    for angle in range(0, 360, step):
        img_r = rotate(img, angle, resize=True)
        mask_r = rotate(mask, angle, resize=True).astype(np.uint8)
        fill_data(img_r, mask_r, insz, outsz, inputs, targets)

    shuffle_arrays(inputs, targets)

    return inputs, targets


class NeuralNet:
    def __init__(self, insz, outsz):
        self.input_var = input_variable((3, insz, insz), np.float32)
        self.label_var = input_variable((outsz, outsz), np.float32)

        conv = Convolution((3, 3), 5, activation=relu)(self.input_var)
        conv = Convolution((5, 5), 5, activation=relu)(conv)
        #conv = Convolution((5, 5), 5, activation=relu)(conv)
        #conv = Convolution((5, 5), 5, activation=relu)(conv)
        # conv = Convolution((3, 3), 5, activation=relu)(conv)
        # conv = Convolution((3, 3), 5, activation=relu)(conv)
        self.z = Convolution((5, 5), 1, activation=sigmoid)(conv)

        self.loss = squared_error(self.z, self.label_var)
        self.eval = squared_error(self.z, self.label_var)



    def fit(self, X, y):
        X = np.array(X).astype(np.float32)
        y = np.array(y).astype(np.float32)
        learning_rate = 0.005
        lr_schedule = learning_rate_schedule(learning_rate, UnitType.minibatch)
        learner = sgd(self.z.parameters, lr_schedule)
        trainer = Trainer(self.z, self.loss, self.eval, [learner])

        # Initialize the parameters for the trainer
        minibatch_size = 1
        num_samples_to_train = len(X) * 5
        num_minibatches_to_train = int(num_samples_to_train / minibatch_size)

        count = 0
        for i in range(0, num_minibatches_to_train):
            # Specify input variables mapping in the model to actual minibatch data to be trained with
            trainer.train_minibatch({self.input_var: X[count:count+1], self.label_var: y[count:count+1]})
            count = (count + 1) % len(X)

    def predict(self, X):
        X = np.array(X).astype(np.float32)
        return self.z.eval({self.input_var: X})


if __name__ == '__main__':
    path = "../data/similar_objects/"
    img = path + "8.JPG"
    mask = path + "8m.jpg"

    img = imread(img)
    mask = imread(mask, as_grey=True).astype(np.uint8)


    contours = find_contours(mask, 0.8)

    props = regionprops(mask)

    limit_area = 64 * 64
    insz = 12
    outsz = 2
    diff = int((insz - outsz) / 2)
    step = 5

    scale_ratio = float(limit_area) / props[0].area

    img = rescale(img, scale_ratio)
    mask = rescale(mask * 255, scale_ratio)

    inputs, targets = get_train_data(img, mask, insz, outsz, step=step)

    inputs = inputs[:3000]
    targets = targets[:3000]

    #inputs = [x.reshape(-1) for x in inputs]
    inputs = [x.transpose(2, 0, 1) for x in inputs]
    #targets = [x.reshape(-1) for x in targets]

    print("Inputs: " + str(len(inputs)))
    print("Shape of img: " + str(img.shape))

    clf = NeuralNet(insz, outsz)
    clf.fit(inputs,targets)

    print("Finished learning.\n")

    output = np.zeros((img.shape[0], img.shape[1]), dtype=np.float32)

    for y in range(0, img.shape[0]- insz, outsz):
        for x in range(0, img.shape[1] - insz, outsz):
            patch = [img[y:y+insz, x:x+insz, :].transpose(2,0,1)]
            result = clf.predict(patch)[0]
            result = result.reshape(outsz, outsz)
            output[y+diff:y+diff+outsz, x+diff:x+diff+outsz] = result

    imshow(output)
    show()


