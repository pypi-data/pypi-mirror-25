import unittest
import shutil, tempfile
from os import path
import time
import fpd_live_imaging.testing_tools as tt
import numpy as np
from multiprocessing import Queue
import h5py


class TestTestDetectorReceive(unittest.TestCase):

    def setUp(self):
        self.header_size = 360
        self.frame_size = 256*256*2
        number_of_frames = 20
        self.test_detector = tt.TestDetectorZero(
                number_of_frames=number_of_frames)
        self.test_receiver = tt.TestDetectorReceive(
                self.test_detector.port,
                max_frames=number_of_frames)
        self.data_string_length = 131471

        self.data_string = self.test_detector._make_detector_string()

    def test_receive_and_transmit_test_data(self):
        header_size, frame_size = self.header_size, self.frame_size
        self.test_detector.start_data_listening()
        self.test_receiver.start_data_receive() 
        
        time.sleep(1)
        self.assertEqual(len(self.test_receiver.data_list), 20)

        bool_list = []
        for data_string in self.test_receiver.data_list:
            received_data = data_string[header_size:header_size+frame_size]
            compare_data = self.data_string[header_size:header_size+frame_size]

            bool_list.append(received_data==compare_data)
        bool_list = np.array(bool_list)
        self.assertTrue(bool_list.all())


class TestTestDetectorZero(unittest.TestCase):

    def setUp(self):
        self.test_detector = tt.TestDetectorZero()

    def test_get_detector_data(self):
        data = self.test_detector._get_detector_data()
        self.assertTrue(len(data) == 256*256)
        self.assertFalse(data.any())


class TestTestDetectorRandom(unittest.TestCase):

    def setUp(self):
        self.test_detector = tt.TestDetectorRandom()

    def test_get_detector_data(self):
        data = self.test_detector._get_detector_data()
        self.assertTrue(len(data) == 256*256)


class TestDetectorSingleNonZeroRandom(unittest.TestCase):

    def setUp(self):
        self.test_detector = tt.TestDetectorRandom()

    def test_get_detector_data(self):
        data = self.test_detector._get_detector_data()
        self.assertTrue(len(data) == 256*256)
        self.assertTrue(data.any())
        self.assertFalse(data.all())


class TestTestSingleNonZero(unittest.TestCase):

    def setUp(self):
        x, y = 50, 10
        self.test_detector = tt.TestSingleNonZero(x=x, y=y)
        self.index = np.ravel_multi_index((x, y), (256, 256))

    def test_get_detector_data(self):
        data = self.test_detector._get_detector_data()
        self.assertTrue(data[self.index] == 1)
        data[self.index] = 0
        self.assertTrue((data==0).all())


class TestTestDataFromFile(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp() 
        self.hdf5_file = path.join(self.test_dir, 'test.hdf5')
        f = h5py.File(self.hdf5_file, 'w')
        self.x, self.y = 10, 10
        self.number_of_runs = 1
        data = np.zeros((self.x, self.y, 1, 256, 256), dtype=np.uint16)
        f.create_dataset('fpd_expt/fpd_data/data', data=data)
        f.close()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_data(self):
        output_queue = Queue()
        test_data_object = tt.TestDataFromFile(
                [output_queue],
                self.hdf5_file,
                number_of_runs=self.number_of_runs)
        test_data_object.start_data_sending()
        time.sleep(1.5)
        test_data_object.process_active.value = False
        print(output_queue.qsize())
        self.assertTrue(output_queue.qsize() == (self.number_of_runs*self.x*self.y))
        bool_array = []
        for image_index in range(output_queue.qsize()):
            image_data = output_queue.get()
            bool_array.append((image_data == 0).all())      
        self.assertTrue(np.array(bool_array).all())
