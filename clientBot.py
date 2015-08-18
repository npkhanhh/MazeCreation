'''
Created on Aug 18, 2015

@author: ldhuy
'''
import socket
import time

class clientBot(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "Client bot created"
        soc.connect((socket.gethostname(), 51515))
        soc.sendall('Hello, world')
#         data = soc.recv(1024)
#         print "Received data from server {}".format(data)
        time.sleep(5)
        soc.close()
        print "Client: Done"
        
cb = clientBot()

