import unittest
import time
from multiprocessing import Queue, Process
from fpd_live_imaging.receive_data_medipix_class import ReceiveDataMedipix
import fpd_live_imaging.testing_tools as tt

class DummyClass:

    def __init__(self):
        self.receive_queue = Queue()

class TestReceiveDataMedipix(unittest.TestCase):

    def setUp(self):
        self.number_of_frames = 15
        self.test_detector = tt.TestDetectorZero(
                number_of_frames=self.number_of_frames)

    def tearDown(self):
        self.comm_medi.stop_running()

    def test_receive_and_transmit_data(self):
        self.test_detector.start_data_listening()
        self.comm_medi = ReceiveDataMedipix(port=self.test_detector.port)
        test_process = DummyClass()
        self.comm_medi.data_process_list.append(test_process)
        self.comm_medi.start_receive_detector_data_listening_process()
        time.sleep(1.)
        self.assertEqual(
                test_process.receive_queue.qsize(),
                self.number_of_frames)
        bool_list = []
        while not test_process.receive_queue.empty():
            data_array = test_process.receive_queue.get()
            data_shape_bool = (data_array.shape == (256, 256))
            data_value_bool = (not data_array.any())
            if data_shape_bool and data_value_bool:
                bool_list.append(True)
            else:
                bool_list.append(False)
        self.assertTrue(all(bool_list))
