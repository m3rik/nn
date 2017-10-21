from time import sleep
from socket import *

PORT = 5000
MAGIC = "smartcar " #to make sure we don't confuse or get confused by other programs

def get_ip_address():
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def discovery():

    s = socket(AF_INET, SOCK_DGRAM) #create UDP socket
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #this is a broadcast socket

    my_ip= get_ip_address()


    toks = my_ip.split('.')
    bcast_address = toks[0] + '.' + toks[1] + '.' + toks[2] + '.255'

    while 1:
        data = MAGIC+my_ip
        data = data + (' '*(256 - len(data)))
        s.sendto(data, (bcast_address, PORT))
        print "sent service announcement:" + my_ip
        sleep(3)


if __name__ == '__main__':
    discovery()
