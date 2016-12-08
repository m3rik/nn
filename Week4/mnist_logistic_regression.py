import matplotlib.pyplot as plt

import numpy as np
import sys
import os

from cntk import Trainer, cntk_device, StreamConfiguration, learning_rate_schedule, UnitType
from cntk.utils import get_train_eval_criterion, get_train_loss
from cntk.device import cpu, set_default_device
from cntk.learner import sgd
from cntk.ops import *

import pickle


# Ensure we always get the same amount of randomness
np.random.seed(0)


# Define a dictionary to store the model parameters
mydict = {"w":None,"b":None}

def linear_layer(input_var, output_dim):
    input_dim = input_var.shape[0]
    weight_param = parameter(shape=(input_dim, output_dim))
    bias_param = parameter(shape=(output_dim))

    mydict['w'], mydict['b'] = weight_param, bias_param
    return times(input_var, weight_param) + bias_param


# Define a utility function to compute the moving average sum.
# A more efficient implementation is possible with np.cumsum() function
def moving_average(a, w=10):
    if len(a) < w:
        return a[:]
    return [val if idx < w else sum(a[(idx-w):idx])/w for idx, val in enumerate(a)]


# Defines a utility that prints the training progress
def print_training_progress(trainer, mb, frequency, verbose=1):
    training_loss, eval_error = "NA", "NA"

    if mb % frequency == 0:
        training_loss = get_train_loss(trainer)
        eval_error = get_train_eval_criterion(trainer)
        if verbose:
            print ("Minibatch: {0}, Loss: {1:.4f}, Error: {2:.2f}".format(mb, training_loss, eval_error))

    return mb, training_loss, eval_error

def transform_labels(labels, classes=10):
    new_labels = np.zeros((labels.shape[0], classes), dtype=np.float32)
    for i in range(labels.shape[0]):
        new_labels[i, int(labels[i])] = 1
    return new_labels

if __name__ == '__main__':
    input_dim = 784
    num_output_classes = 10
    output_dim = num_output_classes

    trainfile = 'data/MNIST/train.pickle'
    testfile = 'data/MNIST/test.pickle'

    with open(trainfile, 'rb') as handle:
        traindata = pickle.load(handle)

    with open(testfile, 'rb') as handle:
        testdata = pickle.load(handle)

    traindata = np.array(traindata).astype(np.float32)
    testdata = np.array(testdata).astype(np.float32)

    limit = 1000

    features = traindata[:limit, :784] / 256
    labels = traindata[:limit, -1]

    labels = transform_labels(labels)

    tfeatures = testdata[:limit, :784] / 256
    tlabels = testdata[:limit, -1]

    tlabels = transform_labels(tlabels)


    input = input_variable(input_dim, np.float32)


    z = linear_layer(input, output_dim)

    label = input_variable(output_dim, np.float32)

    loss = cross_entropy_with_softmax(z, label)
    eval_error = classification_error(z, label)

    learning_rate = 0.1
    lr_schedule = learning_rate_schedule(learning_rate, UnitType.minibatch)
    learner = sgd(z.parameters, lr_schedule)
    trainer = Trainer(z, loss, eval_error, [learner])

    # Initialize the parameters for the trainer
    minibatch_size = 10
    num_samples_to_train = limit * 10
    num_minibatches_to_train = int(num_samples_to_train / minibatch_size)

    training_progress_output_freq = 50

    plotdata = {"batchsize": [], "loss": [], "error": []}


    j = 0
    for i in range(0, num_minibatches_to_train):
        features_batch = features[j:j+minibatch_size,:]
        labels_batch = labels[j:j+minibatch_size]
        j = (j + minibatch_size) % limit

        # Specify input variables mapping in the model to actual minibatch data to be trained with
        trainer.train_minibatch({input: features_batch, label: labels_batch})
        batchsize, loss, error = print_training_progress(trainer, i,
                                                         training_progress_output_freq, verbose=1)

        if not (loss == "NA" or error == "NA"):
            plotdata["batchsize"].append(batchsize)
            plotdata["loss"].append(loss)
            plotdata["error"].append(error)

    plotdata["avgloss"] = moving_average(plotdata["loss"])
    plotdata["avgerror"] = moving_average(plotdata["error"])

    plt.figure(1)
    plt.subplot(211)
    plt.plot(plotdata["batchsize"], plotdata["avgloss"], 'b--')
    plt.xlabel('Minibatch number')
    plt.ylabel('Loss')
    plt.title('Minibatch run vs. Training loss')

    plt.subplot(212)
    plt.plot(plotdata["batchsize"], plotdata["avgerror"], 'r--')
    plt.xlabel('Minibatch number')
    plt.ylabel('Label Prediction Error')
    plt.title('Minibatch run vs. Label Prediction Error')
    plt.show()

    test_minibatch_size = 10000

    error = trainer.test_minibatch( {input: tfeatures, label: tlabels})
    print("Error test: " + str(error))

    out = softmax(z)
    result = out.eval({input: features})

    print("Label    :", np.argmax(labels[:25], axis=1))
    print("Predicted:", np.argmax(result[0, :25, :], axis=1))

    bias_vector = mydict['b'].value
    weight_matrix = mydict['w'].value

    for wi in range(10):
        weight_mat = np.array(weight_matrix[:, wi]).reshape(28, 28)
        plt.matshow(weight_mat)
        plt.show()

