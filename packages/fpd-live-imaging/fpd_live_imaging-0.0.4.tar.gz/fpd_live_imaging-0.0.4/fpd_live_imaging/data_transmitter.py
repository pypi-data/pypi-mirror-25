#import numpy as np
#import pickle, socket
#import multiprocessing as mp
#import time
#
#def start_sender():
#    ip = '127.0.0.1'
#    port = 4123
#    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    s.connect((ip, port))
#    arr = np.random.random((50, 50))
#    data_string = pickle.dumps(arr)
#    s.send(data_string)
#
#def start_receiver():
#    ip = '127.0.0.1'
#    port = 4123
#    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    s.bind((ip, port))
#    s.listen(1)
#    conn, addr = s.accept()
#    print('Connected by', addr)
#    while True:
#        data_string = conn.recv(4096)
#        if data_string:
#            data = pickle.loads(data_string)
#            print(data)
#    
#receiver_process = mp.Process(target=start_receiver)
#receiver_process.start()
#
#time.sleep(1.)
#
#sender_process = mp.Process(target=start_sender)
#sender_process.start()

class DataTransmitting(object):
    def __init__(self, name, ip, port):
        self.name = name
        self.receive_queue = mp.Queue()

        self.process_sleep_time = 1.e-7
        self.ip = ip
        self.port = port
    
    def _data_transmitter_process(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        arr = np.random.random((50, 50))
        data_string = pickle.dumps(arr)
        s.send(data_string)

