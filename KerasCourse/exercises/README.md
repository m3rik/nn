# Exercises in Keras

## MLP network

In mnist_mlp.py, you will find a neural network with fully connected layers that learns MNIST dataset.

### Problems

* Run the script and find out what is the accuracy after the learning is over.
* Try to improve the score by changing the number of hidden units.
* Try to improve the score by changing the number of hidden layers.
* Try to reproduce underfitting. What is the smallest network? Conclusion?
* Set a reference network architecture. Compare relu vs signoid units. What do you observe during learning?
* Use other optimizer than stochastic gradient descent. Read more at: 
** how they work: http://ruder.io/optimizing-gradient-descent/
** how to use: https://keras.io/optimizers/
* Try to obtain an accuracy higher than 98 % on the test set.

## Conv network

In mnist_cnn.py, you will find a neural network with convolutional layers that learns MNIST dataset.

### Problems

* Run the script and find out what is the accuracy after the learning is over.
* Change network architecture by using more or less convolutions.
* Try stacking consecutive convolutions.
* Make the network fully convolutional. Get rid of the fully connected layers. Use average pooling.
* Try to obtain accuracy higher than 99 % on the test set.
* Try to use: Dropout or Noise layers for improving the generalization.
* Read about Separable Convolutions and try them.
* Try to make fastest network which still achieves over 99 % on the test set.
