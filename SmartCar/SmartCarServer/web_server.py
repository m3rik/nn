import cherrypy
from cherrypy.process import servers
from motor_controller import start_motor_controller


class CarControlAPI:
    def __init__(self, motor_controller):
        self.motor_controller = motor_controller
        cherrypy.engine.subscribe('stop', self.stop)

    def stop(self):
        self.motor_controller.stop()


    @cherrypy.expose
    def index(self):
        return "OK"

    @cherrypy.expose
    def control(self, speed=0, balance=0):
        ts = self.motor_controller.control_motors(speed, balance)
        return str(speed) + ' ' + str(balance) + ' ' + str(ts)

def fake_wait_for_occupied_port(host, port): return

def start_webserver(motor_controller):
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.server.socket_port = 8082
    servers.wait_for_occupied_port = fake_wait_for_occupied_port
    cherrypy.quickstart(CarControlAPI(motor_controller))

if __name__ == '__main__':
    mc = start_motor_controller()
    start_webserver(mc)
