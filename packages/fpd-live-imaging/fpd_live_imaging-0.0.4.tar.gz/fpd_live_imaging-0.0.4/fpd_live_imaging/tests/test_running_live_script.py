import unittest
import fpd_live_imaging.testing_tools as tt
from multiprocessing import Queue
import fpd_live_imaging.acquisition_control_class as acc
from fpd_live_imaging.test_images.test_images import linux_penguin_64
import time


class TestRunningLiveScript(unittest.TestCase):

    def tearDown(self):
        self.acquisition_control.cancel_all_processes()

    def test_running_live_script(self):
        self.acquisition_control = acc.LiveImagingQt()

        test_detector = tt.TestDetectorInputImage(number_of_frames=10, input_image=linux_penguin_64)
        test_detector.sleep_time.value = 0.001
        test_detector.start_data_listening()

        self.acquisition_control._comm_medi.port = test_detector.port
        self.acquisition_control.start_bf_process()
        self.acquisition_control.resize_scan(64, 64)
        self.acquisition_control.start_medipix_receiver()
        time.sleep(0.1)
