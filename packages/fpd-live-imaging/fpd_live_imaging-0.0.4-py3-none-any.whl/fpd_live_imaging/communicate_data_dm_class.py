import socket
import numpy as np
import time
import multiprocessing as mp

class DataCommDM:


        def __init__(self, ip_address='127.0.0.1', port=6343):
                self.ip_address = ip_address
                self.port = port
                self.input_queue = mp.Queue()
                self.send_queue = mp.Queue()
                self.threads_active = mp.Value('b', True)
                self._data_string_list = []
                self.name = ""
        
        def __repr__(self):
            return '<%s %s %s:%s (I:%s,Q:%s,O:%s)>' % (
                self.__class__.__name__, 
                self.name,
                self.ip_address,
                self.port,
                len(self._data_string_list),
                len(self.input_queue.queue),
                len(self.send_queue.queue))

        def stop_running(self):
                self.threads_active.value = False
                self.running = False

        def start_socket(self):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((self.ip_address, self.port))
                s.listen(1)
                return(s)

        def start_data_listening(self):
                self.make_data_string_thread = mp.Process(
                                target=self.make_data_string)
                self.make_data_string_thread.start()
                self.data_listen_thread = mp.Process(target=self.send_data) 
                self.data_listen_thread.start()
        
        def make_data_string(self):
                while self.threads_active.value:
                        if not self.input_queue.empty():
                            pixel_value = self.input_queue.get()
                            data_string = str(pixel_value).zfill(4)
                            self._data_string_list.append(data_string)
                            if len(self._data_string_list) == 100:
                                 self.send_queue.put(
                                         "".join(
                                                 self._data_string_list)) 
                                 del self._data_string_list[:]

        def send_data(self):
                s = self.start_socket()
                while self.threads_active.value:
                    conn, addr = s.accept()
                    data_recv = conn.recv(2048)
                    if not self.send_queue.empty():
                        data_string = self.send_queue.get()
                        if data_recv:
                            conn.send(data_string)
                        conn.close()
                    else:
                        conn.send(b"false")

                temp_s = socket.socket(
                        socket.AF_INET,socket.SOCK_STREAM)
                temp_s.connect(('127.0.0.1', self.port))
                s.close()
                temp_s.close()

        def clear_queues(self):
            self.input_queue.queue.clear() 
            self.send_queue.queue.clear() 
            del self._data_string_list[:]

        def start_testdetector(self):
                number_array0 = np.random.randint(0,4000,128).tolist()
                number_array1 = np.random.randint(0,4000,128).tolist()
                string_list0 = ""
                string_list1 = ""
                for index, (number0, number1) in enumerate(
                        zip(number_array0, number_array1)):
                    string_number0 = str(number0).zfill(4)
                    string_number1 = str(number1).zfill(4)
                    string_list0 += string_number0
                    string_list1 += string_number1

                counter = 0
                while counter < 256*256:
                    self.queue.put(string_list0)
                    time.sleep(0.01)
                    self.queue.put(string_list1)
                    time.sleep(0.01)
                    counter += 1
                    print(counter)

        def start_data_test_listening_thread(self):
                self.data_test_listen_thread = Thread(target=self.send_data_test) 
                self.data_test_listen_thread.start()

        def send_data_test(self):
                while True:
                    if not self.queue.empty():
                        pixel_value = self.queue.get()

