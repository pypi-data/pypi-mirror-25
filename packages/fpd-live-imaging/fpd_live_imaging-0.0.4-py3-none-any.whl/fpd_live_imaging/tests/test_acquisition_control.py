import unittest
import time
import fpd_live_imaging.testing_tools as tt
import fpd_live_imaging.acquisition_control_class as acc

class TestAcquisitionControl(unittest.TestCase):

    def setUp(self):
        self.test_detector = tt.TestDetectorZero(number_of_frames=10)
        self.da = acc.DummyAcquisition()

    def tearDown(self):
        self.da.cancel_all_processes()

    def test_receive_and_transmit_data(self):
        self.da._comm_medi.port = self.test_detector.port
        self.da.start_bf_process()
        self.da.start_medipix_receiver()
        time.sleep(1)
