# Keras Course

Keras, probably the best documented dnn framework in the world!

## What is Keras?

Keras is a high-level neural networks API, written in Python and capable of running on top of TensorFlow, CNTK, or Theano. 
We will use TensorFlow as a backend.


## Documentation 

* Keras official docs 2017: https://keras.io/
* Keras forum: https://github.com/fchollet/keras/issues
** Note: Issues are not really issues. Mostly are questions from users.
* Keras examples: https://github.com/fchollet/keras/tree/master/examples

## Requirements

What do you need to Kerasing?

### High level workflow:
We want to install Keras with TensorFlow as a backend and with GPU support.
TensorFlow needs to be installed first and afterward Keras.


### Steps for getting things working:

1. Anaconda3 - Python3 Distribution with lots of useful libraries (https://www.anaconda.com/download/) (64bit installer + Python 3.6)
2. Pycharm Community Edition - Python IDE (https://www.jetbrains.com/pycharm/download/#section=windows)
3.1. Update Nvidia Driver to R390. www.nvidia.com/drivers
3.2. CUDA 9.1 - https://developer.nvidia.com/cuda-downloads
4. Add to PATH CUDA binaries if installer did not do that.
4. cuDNN v7 - https://developer.nvidia.com/cudnn
5. Add to PATH cuDNN binaries.
6. Anaconda3 comes with Python 3.6. Open Anaconda3 Prompt from start menu and run: 
```
conda install python=3.5
```
7. Install TensorFlow with GPU support.
```
pip3 install --upgrade tensorflow-gpu
```
8. Install Keras.
```
pip3 install keras
```

## Practice

In exercises folder, you will find some practical problems. 
More details, in the readme file.
