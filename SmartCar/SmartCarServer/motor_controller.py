from threading import Timer
import time
import os


def timer_func(self):
    print(time.time() - self.timestamp)
    if time.time() - self.timestamp < 5:
        print(str(self.speed) + ' ' + str(self.balance))
        self.control_impl(self.speed, self.balance)
    elif self.speed > 0:
        print('Timestamp too old. ')
        self.speed = 0
        self.balance = 0
        self.control_impl(self.speed, self.balance)
    self.start_timer()

class MotorController:
    def __init__(self):
        self.timestamp = time.time()
        self.speed = 0
        self.balance = 0
        self.stopping = False
        self.start_timer()
        self.setup_rpi()

    def setup_rpi(self):
        if os.name != 'nt':
            import RPi.GPIO as GPIO

            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(17, GPIO.OUT)
            self.left_forward = GPIO.PWM(17, 100)
            self.left_forward.start(50)

    def start_timer(self):
        self.timer = Timer(1.0, timer_func, args=[self])
        if not self.stopping:
            self.timer.start()

    def stop(self):
        self.stopping = True
        self.timer.cancel()

    def control_motors(self, speed, balance):
        self.speed = speed
        self.balance = balance
        self.timestamp = time.time()
        return self.timestamp

    def control_impl(self, speed, balance):
        print('Control motors implementation: ' + str(speed) + ' ' + str(balance))
        if os.name != 'nt':
            import RPi.GPIO as GPIO



def start_motor_controller():
    return MotorController()


if __name__ == '__main__':
    start_motor_controller()