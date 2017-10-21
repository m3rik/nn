from motor_controller import start_motor_controller
from web_server import start_webserver
from discovery_service import discovery
from multiprocessing import Process

if __name__ == '__main__':
    mc = start_motor_controller()
    p = Process(target=discovery)
    p.start()
    start_webserver(mc)