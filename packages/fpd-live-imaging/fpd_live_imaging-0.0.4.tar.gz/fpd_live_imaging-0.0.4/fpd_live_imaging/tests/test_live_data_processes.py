import unittest
import fpd_live_imaging.testing_tools as tt
from multiprocessing import Queue
from fpd_live_imaging.receive_data_medipix_class import ReceiveDataMedipix
from fpd_live_imaging.process_classes import BFDetectorProcess
import time

class TestLiveDataProcess(unittest.TestCase):
    
    def setUp(self):
        self.number_of_frames = 15
        self.test_detector = tt.TestDetectorZero(
                number_of_frames=self.number_of_frames)
    
    def tearDown(self):
        self.comm_medi.stop_running()
        self.detector_process.stop_running()

    def test_live_data_process(self):
        output_queue = Queue()
        self.detector_process = BFDetectorProcess(
                "test_BF",
                output_queue)
        self.detector_process.start_process_function()

        self.test_detector.start_data_listening()
        time.sleep(1)
        self.comm_medi = ReceiveDataMedipix(port=self.test_detector.port)
        self.comm_medi.data_process_list.append(self.detector_process)

        self.comm_medi.start_receive_detector_data_listening_process()

        time.sleep(1)
        self.assertEqual(output_queue.qsize(), self.number_of_frames)
