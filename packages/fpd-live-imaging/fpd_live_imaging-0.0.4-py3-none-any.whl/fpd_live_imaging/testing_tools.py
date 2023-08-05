import multiprocessing as mp
import socket
import numpy as np
import time
import h5py

_alphabet_numpy = np.array(
        list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'),
        dtype="|S1")


class TestDetectorBase(object):

    def __init__(
            self, sleep_time=0.05, number_of_frames=100):
        self.sleep_time = mp.Value('f')
        self.sleep_time.value = sleep_time
        self.number_of_frames = number_of_frames
        self.frame_number = mp.Value('i', 0)
        self.start_socket()

        self.image_x = 256
        self.image_y = 256

    def start_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 0))
        self.port = s.getsockname()[1]
        s.listen(1)
        self.s = s

    def start_data_listening(self):
        self.data_listen_process = mp.Process(
                target=self._socket_send_process)
        self.data_listen_process.start()

    def _socket_send_process(self):
        BUFFER_SIZE = 4096
        conn, addr = self.s.accept()
        self.conn = conn
        data = conn.recv(BUFFER_SIZE)
        if data == b'MPX,0000000021,CMD,STARTACQUISITION':
            for i in range(self.number_of_frames):
                test_data = self._make_detector_string()
                conn.sendall(test_data)
                self.frame_number.value += 1
                time.sleep(self.sleep_time.value)
        self.conn.close()
        self.s.close()

    def _random_string(self, length):
        string = np.random.choice(_alphabet_numpy, size=length).tostring()
        return(string)

    def _make_detector_string(self):
        detector_string = self._random_string(360)
        detector_data = self._get_detector_data()
        detector_string += detector_data.astype('uint16').tostring()
        detector_string += self._random_string(38)
        detector_string += b"\n"
        return(detector_string)


class TestDetectorRandom(TestDetectorBase):

    def _get_detector_data(self):
        detector_data = np.random.randint(0, 2**12, size=(256*256))
        return(detector_data)


class TestDetectorZero(TestDetectorBase):

    def _get_detector_data(self):
        detector_data = np.zeros(256*256)
        return(detector_data)


class TestDetectorSingleNonZeroRandom(TestDetectorBase):

    def _get_detector_data(self):
        random_pixel = np.random.randint(0, 256*256)
        detector_data = np.zeros(256*256)
        detector_data[random_pixel] = 1
        return(detector_data)


class TestSingleNonZero(TestDetectorBase):

    def __init__(self, x=128, y=128, *args, **kwds):
        self.x = x
        self.y = y
        self.index = np.ravel_multi_index((self.x, self.y), (256, 256))
        super(TestSingleNonZero, self).__init__(*args, **kwds)

    def _get_detector_data(self):
        im_x, im_y = self.image_x, self.image_y
        detector_data = np.zeros(im_x*im_y)
        detector_data[self.index] = 1
        return(detector_data)


class TestDetectorGrid(TestDetectorBase):

    def __init__(self, grid_x=3, grid_y=3, *args, **kwds):
        self.grid_x = grid_x
        self.grid_y = grid_y
        super(TestDetectorGrid, self).__init__(*args, **kwds)

    def _get_detector_data(self):
        im_x, im_y = self.image_x, self.image_y
        im_frame_num = self.frame_number.value % (im_x*im_y)
        x = im_frame_num % im_x
        y = int((im_frame_num - im_x)/im_y)
        if (x % self.grid_x is 0) or (y % self.grid_y is 0):
            detector_data = np.ones(256*256)
        else:
            detector_data = np.zeros(256*256)
        return(detector_data)


class TestDetectorInputImage(TestDetectorBase):

    def __init__(self, input_image, *args, **kwds):
        super(TestDetectorInputImage, self).__init__(*args, **kwds)
        self.image_x, self.image_y = input_image.shape
        self.input_image = input_image

    def _get_detector_data(self):
        im_x, im_y = self.image_x, self.image_y
        im_frame_num = self.frame_number.value % (im_x*im_y)
        x = im_frame_num % im_x
        y = int((im_frame_num - im_x)/im_y)
        detector_data = np.ones(256*256)*self.input_image[y, x]
        return(detector_data)


class TestDetectorReceive:

    def __init__(self, port, max_frames=20):
        self.port = port
        self.looper = True
        self.buffer_size = 1050000
        self.start_socket()
        self.max_frames = max_frames
        self.data_list = []
        self.frame_bytesize = 131471

    def start_socket(self):
        self.s = socket.socket()
        self.s.connect(('127.0.0.1', self.port))

    def start_data_receive(self):
        MESSAGE = b'MPX,0000000021,CMD,STARTACQUISITION'
        self.s.send(MESSAGE)
        number_of_frames = 0
        frame_bytesize = self.frame_bytesize
        received_data = b""
        while self.looper:
            received_data += self.s.recv(self.buffer_size)
            if len(received_data) == frame_bytesize:
                self.data_list.append(received_data)
                number_of_frames += 1
                if number_of_frames >= self.max_frames:
                    self.s.close()
                    break
                del received_data
                received_data = b""
            elif len(received_data) >= frame_bytesize:
                if len(received_data) % frame_bytesize == 0:
                    for i in range(
                            int(len(received_data)/frame_bytesize)):
                        self.data_list.append(received_data)
                        number_of_frames += 1
                        if number_of_frames >= self.max_frames:
                            self.s.close()
                            break
                    del received_data
                    received_data = b""


class TestDataFromFile(object):

    def __init__(
            self,
            processing_queue_list, fpd_hdf5_file, sleep_time=0.001,
            number_of_runs=100):
        self.processing_queue_list = processing_queue_list
        self.process_active = mp.Value('b', True)
        self.filename = fpd_hdf5_file
        self.sleep_time = sleep_time
        self.number_of_runs = number_of_runs

    def start_data_sending(self):
        self.data_sending_process = mp.Process(
                target=self._data_sending)
        self.data_sending_process.start()

    def _data_sending(self):
        file_hdf5 = h5py.File(self.filename, 'r')
        data_hdf5 = file_hdf5['fpd_expt/fpd_data/data']
        counter = 0
        while self.process_active.value:
            for iX in range(data_hdf5.shape[0]):
                for iY in range(data_hdf5.shape[1]):
                    time.sleep(self.sleep_time)
                    if data_hdf5.ndim == 5:
                        data = data_hdf5[iX, iY, 0, :, :]
                    elif data_hdf5.ndim == 4:
                        data = data_hdf5[iX, iY, :, :]
                    else:
                        raise Exception(
                            self.filename +
                            " doesn't have the correct dimensions")
                    for processing_queue in self.processing_queue_list:
                        processing_queue.put(data)
                    del data
            counter += 1
            if counter >= self.number_of_runs:
                self.process_active.value = False
        file_hdf5.close()
