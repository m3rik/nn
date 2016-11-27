# Neural Networks with CNTK

## Requirements

CNTK: https://github.com/Microsoft/CNTK/releases

Pycharm Community Edition: https://www.jetbrains.com/pycharm/download/#section=windows

## Instalation

For CNTK, follow the steps in this wiki: https://github.com/Microsoft/CNTK/wiki/Setup-Windows-Binary-Script

For PyCharm, run the installer.

Now, you must do two things:
* update path variable with your path to %cntk_folder%\cntk (in my case: C:\Users\Paul\Desktop\cntk\cntk)
  * BEWARE: There is a folder named cntk inside the cntk folder.
* configure python interpretor in Pycharm to be C:\local\Anaconda3-4.1.1-Windows-x86_64\envs\cntk-py34\python.exe
  * It's a virtual environment created by the install script with all the requirements of CNTK.
  

To test if everything is alright, run the example of logistic regression: CNTK101_logistic_regression.py.

You're done :)
