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
            GPIO.setup(27, GPIO.OUT)

            GPIO.setup(22, GPIO.OUT)
            GPIO.setup(23, GPIO.OUT)

            self.right_forward = GPIO.PWM(17, 100)
            self.right_forward.start(0)

            self.right_backward = GPIO.PWM(27, 100)
            self.right_backward.start(0)

            self.left_forward = GPIO.PWM(22, 100)
            self.left_forward.start(0)

            self.left_backward = GPIO.PWM(23, 100)
            self.left_backward.start(0)

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
        speed = float(speed)
        balance = float(balance)
        if os.name != 'nt':
            import RPi.GPIO as GPIO
            left_speed = speed * 100
            right_speed = speed * 100
            modified_speed = (1 - abs(balance)) * 2 * abs(speed)
            if balance > 0:
                if speed > 0:
                    right_speed = (-speed + modified_speed) * 100
                else:
                    right_speed = (speed - modified_speed) * 100
            else:
                if speed > 0:
                    left_speed = (-speed + modified_speed) * 100
                else:
                    left_speed = (speed - modified_speed) * 100

            if right_speed > 0:
                self.right_forward.ChangeDutyCycle(right_speed)
                self.right_backward.ChangeDutyCycle(0)
            else:
                self.right_forward.ChangeDutyCycle(0)
                self.right_backward.ChangeDutyCycle(-right_speed)

            if left_speed > 0:
                self.left_forward.ChangeDutyCycle(left_speed)
                self.left_backward.ChangeDutyCycle(0)
            else:
                self.left_forward.ChangeDutyCycle(0)
                self.left_backward.ChangeDutyCycle(-left_speed)




def start_motor_controller():
    return MotorController()


if __name__ == '__main__':
    start_motor_controller()