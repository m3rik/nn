from Assignment1_kinship.kinship_data import kinship_dataset

from cntk import Trainer, cntk_device, StreamConfiguration, learning_rate_schedule, UnitType
from cntk.utils import *
from cntk.device import cpu, set_default_device
from cntk.learner import *
from cntk.ops import *
from cntk.tensor import *
from cntk.axis import *
from cntk.initializer import *

import matplotlib.pyplot as plt


from CNTK101_logistic_regression import moving_average, print_training_progress



def linear_layer(input_var, output_dim):
    input_dim = input_var.shape[0]
    times_param = parameter(shape=(input_dim, output_dim),init=glorot_uniform())
    Parameter()
    bias_param = parameter(shape=(output_dim))
    t = times(input_var, times_param)
    return bias_param + t

def dense_layer_concat(input_var1, input_var2, output_dim, nonlinearity):
    input_dim1 = input_var1.shape[0]
    input_dim2 = input_var2.shape[0]

    times_param = parameter(shape=(input_dim1 + input_dim2, output_dim), init=glorot_uniform())
    bias_param = parameter(shape=(output_dim))
    t = times(splice((input_var1,input_var2), axis=0), times_param)

    return nonlinearity(bias_param + t)


def dense_layer(input, output_dim, nonlinearity):
    r = linear_layer(input, output_dim)
    r = nonlinearity(r)
    return r


def plot_training_error(plotdata):
    # Compute the moving average loss to smooth out the noise in SGD

    plotdata["avgloss"] = moving_average(plotdata["loss"])
    plotdata["avgerror"] = moving_average(plotdata["error"])
    plotdata["avgterror"] = moving_average(plotdata["test_error"])

    # Plot the training loss and the training error
    import matplotlib.pyplot as plt

    plt.figure(1)
    plt.subplot(211)
    plt.plot(plotdata["batchsize"], plotdata["avgloss"], 'b--')
    plt.xlabel('Minibatch number')
    plt.ylabel('Loss')
    plt.title('Minibatch run vs. Training loss')

    #plt.show()

    plt.subplot(212)
    plt.plot(plotdata["batchsize"], plotdata["avgerror"], 'r--')
    plt.xlabel('Minibatch number')
    plt.ylabel('Label Prediction Error')
    plt.title('Minibatch run vs. Label Prediction Error')
    plt.show()



if __name__ == '__main__':
    ds = kinship_dataset(shuffle=True, verbose=False)

    #spliting data
    test_len = 4
    train_len = ds['len'] - test_len

    train_p1 = ds['p1'][:train_len]
    train_r = ds['r'][:train_len]
    train_p2 = ds['p2'][:train_len]

    test_p1 = ds['p1'][train_len:]
    test_r = ds['r'][train_len:]
    test_p2 = ds['p2'][train_len:]


    #defining inputs
    input_p1 = input_variable(len(train_p1[0]))
    input_r = input_variable(len(train_r[0]))
    label_p2 = input_variable(len(train_p2[0]))

    #defining model
    nn1 = dense_layer(input_p1, 6, sigmoid)
    nn2 = dense_layer(input_r, 6, sigmoid)

    nn3 = dense_layer_concat(nn1, nn2, 12, sigmoid)
    nn3 = dense_layer(nn3, 6, sigmoid)
    nn4 = linear_layer(nn3, len(train_p2[0]))


    #defining loss and error
    loss = cross_entropy_with_softmax(nn4, label_p2)
    eval_error = classification_error(nn4, label_p2)


    #trainer instantiation
    learning_rate = 1
    lr_schedule = learning_rate_schedule(learning_rate, UnitType.minibatch)
    mom_schedule = momentum_schedule(0.1)
    learner = momentum_sgd(nn4.parameters, lr=lr_schedule, momentum=mom_schedule, l1_regularization_weight=0.0000002)
    trainer = Trainer(nn4, loss, eval_error, [learner])

    # Initialize the parameters for the trainer
    minibatch_size = int(train_len / 12)
    num_samples = train_len * 5000
    num_minibatches_to_train = num_samples / minibatch_size
    training_progress_output_freq = (train_len / minibatch_size)

    plotdata = {"batchsize": [], "loss": [], "error": [], "test_error":[]}

    ti = 0
    for i in range(0, int(num_minibatches_to_train)):
        batch_p1 = train_p1[ti:ti+minibatch_size]
        batch_r = train_r[ti:ti+minibatch_size]
        batch_p2 = train_p2[ti:ti+minibatch_size]

        ti = (ti + minibatch_size) % train_len

        # Specify the input variables mapping in the model to actual minibatch data for training
        trainer.train_minibatch({input_p1: batch_p1, input_r: batch_r, label_p2: batch_p2})
        batchsize, loss, error = print_training_progress(trainer, i,
                                                         training_progress_output_freq, verbose=0)

        if not (loss == "NA" or error == "NA"):
            plotdata["batchsize"].append(batchsize)
            plotdata["loss"].append(loss)
            plotdata["error"].append(error)
            plotdata["test_error"].append(trainer.test_minibatch({input_p1: test_p1, input_r: test_r, label_p2: test_p2}))

    plot_training_error(plotdata)

    #autotesting using trainer
    error = trainer.test_minibatch({input_p1: train_p1, input_r: train_r, label_p2: train_p2})
    print("Error trainset: " + str(error))
    error = trainer.test_minibatch({input_p1: test_p1, input_r: test_r, label_p2: test_p2})
    print("Error testset: " + str(error))


    #manual forwarding
    out = softmax(nn4)
    predicted_label_prob = out.eval({input_p1: test_p1, input_r: test_r})

    print("Label    :", np.argmax(test_p2, axis=1))
    print("Predicted:", np.argmax(predicted_label_prob[0, :, :], axis=1))