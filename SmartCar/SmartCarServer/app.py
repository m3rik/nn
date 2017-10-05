from motor_controller import start_motor_controller
from web_server import start_webserver


if __name__ == '__main__':
    mc = start_motor_controller()
    start_webserver(mc)