import os
import socket
import numpy as np
import time
import multiprocessing as mp
import copy
import psutil


class ReceiveDataMedipix(object):

    def __init__(self, ip_address='127.0.0.1', port=6342):
        self.ip_address = ip_address
        self.port = port

        self.raw_datastring_queue = mp.Queue()
        # Max size of the buffer which receives the
        # data from the detector
        self.buffer_size = 1050000

        # Size of the header of the received data from
        # the detector. Basically the stuff before the
        # image data itself
        self.header_size = 360

        # Size of the image received from the
        # detector in bytes. Since the detector
        # has a set size of 256 x 256, and (usually)
        # acquires in 2-byte mode.
        self.data_process_list = []
        self.processes_active = mp.Value('b', True)

        self._allowed_bit_modes = [1, 6, 12, 24]
        self.bit_mode = 12

        self.process_sleep_time = 1.e-8

        self._data_listen_process = None
        self._data_process_process = None

    def __repr__(self):
        process_list = []
        for data_process in self.data_process_list:
            process_list.append(data_process.name)
        process_string = ",".join(process_list)
        return '<%s %s:%s, (%s)>' % (
            self.__class__.__name__,
            self.ip_address,
            self.port,
            process_string)

    @property
    def bit_mode(self):
        return(self._bit_mode)

    @bit_mode.setter
    def bit_mode(self, value):
        if value in self._allowed_bit_modes:
            self._bit_mode = value
        else:
            raise ValueError(
                    '%s received unknown bitmode: %s' % (
                        self.__class__.__name__,
                        self.bit_mode))

    @property
    def frame_bytesize(self):
        if self.bit_mode == 12:
            return(131471)
        elif self.bit_mode == 24:
            return(262543)
        elif self.bit_mode == 6:
            return(65935)
        elif self.bit_mode == 1:
            return(65935)

    @property
    def frame_size(self):
        if self.bit_mode == 12:
            return(256*256*2)
        elif self.bit_mode == 24:
            return(256*256*4)
        elif self.bit_mode == 6:
            return(256*256*1)
        elif self.bit_mode == 1:
            return(256*256*1)

    @property
    def frame_dtype(self):
        if self.bit_mode == 12:
            return(np.uint16)
        elif self.bit_mode == 24:
            return(np.uint32)
        elif self.bit_mode == 6:
            return(np.uint8)
        elif self.bit_mode == 1:
            return(np.uint8)

    def stop_running(self):
        self.processes_active.value = False
        time.sleep(1)
        if self._data_listen_process is not None:
            self._data_listen_process.terminate()
        if self._data_process_process is not None:
            self._data_process_process.terminate()

    def startacquisition(self):
        MESSAGE = b'MPX,0000000021,CMD,STARTACQUISITION'
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip_address, self.port))
        s.send(MESSAGE)
        return(s)

    def _parse_detector_data(self):
        frame_bytesize = self.frame_bytesize
        received_data = b""
        clear_fragment_list = False
        frame_fragment_list = []
        frame_fragment_length = 0
        while self.processes_active.value:
            time.sleep(self.process_sleep_time)
            if not self.raw_datastring_queue.empty():
                received_data = self.raw_datastring_queue.get()
                length = len(received_data)
                if length == frame_bytesize:
                    self._send_detector_data(received_data)
                    clear_fragment_list = True
                elif length % frame_bytesize == 0:
                    for i in range(int(len(received_data)/frame_bytesize)):
                        temp_received_data = received_data[
                            frame_bytesize*i:frame_bytesize*(i+1)]
                        self._send_detector_data(temp_received_data)
                        del temp_received_data
                    clear_fragment_list = True
                elif length == 2063:
                    pass  # First data packet when starting acquisition
                else:
                    frame_fragment_length += length
                    frame_fragment_list.append(received_data)
                if frame_fragment_length == frame_bytesize:
                    combined_data = bytearray(frame_fragment_list[0])
                    for frame_fragment in frame_fragment_list[1:]:
                        combined_data.extend(frame_fragment)
                    self._send_detector_data(combined_data)
                    del combined_data
                    clear_fragment_list = True
                elif frame_fragment_length > frame_bytesize:
                    clear_fragment_list = True
                if clear_fragment_list:
                    if frame_fragment_list:
                        frame_fragment_list.clear()
                        frame_fragment_length = 0
                    clear_fragment_list = False
                del received_data

    def _send_detector_data(self, received_data):
        header_size = self.header_size
        frame_size = self.frame_size
        frame_dtype = self.frame_dtype
        received_string = received_data[
            header_size:header_size+frame_size]
        received_array = np.frombuffer(
                received_string,
                dtype=frame_dtype).reshape(256, 256)
        for data_process in self.data_process_list:
            data_process.receive_queue.put(
                            copy.deepcopy(received_array))
        del received_data, received_array, received_string

    def start_receive_detector_data_listening_process(self):
        self._data_listen_process = mp.Process(
                        target=self._receive_detector_data)
        self._data_listen_process.start()
        self._data_process_process = mp.Process(
                        target=self._parse_detector_data)
        self._data_process_process.start()

    def _receive_detector_data(self):
        if os.name == "nt":
            p = psutil.Process(os.getpid())
            p.nice(psutil.HIGH_PRIORITY_CLASS)
        s = self.startacquisition()
        while self.processes_active.value:
            received_data = s.recv(self.buffer_size)
            self.raw_datastring_queue.put(received_data)
            del received_data
        s.close()
