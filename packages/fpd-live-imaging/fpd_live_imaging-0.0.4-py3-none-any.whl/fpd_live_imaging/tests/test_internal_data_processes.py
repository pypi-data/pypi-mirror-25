import unittest
import numpy as np
import time
from multiprocessing import Queue
from fpd_live_imaging.process_classes import (
    FullDiffractionImageProcess,
    DiffractionImageRollingProcess,
    SinglePixelProcess,
    BFDetectorProcess,
    ADFDetectorProcess,
    CoMxProcess,
    CoMyProcess,
    CoMxThresholdProcess,
    CoMyThresholdProcess,
    CoMxMaskDiskProcess,
    CoMyMaskDiskProcess,
    )

class test_full_diffraction_image_processes(unittest.TestCase):
    
    def setUp(self):
        self.test_image = np.arange(256*256).reshape(256,256)
    
    def tearDown(self):
        self.detector_process.stop_running()

    def test_diff_process(self):
        self.detector_process = FullDiffractionImageProcess(
                "Diff0",
                Queue())
        self.detector_process.start_process_function()
        self.detector_process.receive_queue.put(self.test_image)
        self.assertFalse((self.detector_process.output_queue.get()-self.test_image).any())


class test_diffraction_image_rolling_processes(unittest.TestCase):
    
    def setUp(self):
        self.test_image = np.ones(shape=(256, 256))*10
    
    def tearDown(self):
        self.detector_process.stop_running()

    def test_diff_rolling_process(self):
        self.detector_process = DiffractionImageRollingProcess(
                "rolling_diff",
                Queue())
        self.detector_process.start_process_function()
        for i in range(1, 11):
            self.detector_process.receive_queue.put(self.test_image)
            image = self.detector_process.output_queue.get()
            self.assertTrue((image==(np.ones((256, 256))*i)).all())

        for i in range(1, 11):
            self.detector_process.receive_queue.put(self.test_image)
            image = self.detector_process.output_queue.get()
            self.assertTrue((image==10.).all())


        self.detector_process.frames_to_average = 100 
        for i in range(1, 50):
            self.detector_process.receive_queue.put(self.test_image*10)
            image = self.detector_process.output_queue.get()
            self.assertTrue((image==(np.ones((256, 256))*i)).all())

        self.detector_process.frames_to_average = 1 
        for i in range(1, 10):
            self.detector_process.receive_queue.put(self.test_image)
            image = self.detector_process.output_queue.get()
            self.assertTrue((image==(np.ones((256, 256))*10)).all())


class test_single_pixel_data_processes(unittest.TestCase):
    
    def setUp(self):
        self.test_image = np.arange(256*256).reshape(256,256)
    
    def tearDown(self):
        self.detector_process.stop_running()

    def test_single_pixel_process(self):
        self.detector_process = SinglePixelProcess(
                "single_pixel0",
                Queue(),
                process_variables=[(100,100)])
        self.detector_process.start_process_function()
        self.detector_process.receive_queue.put(self.test_image)
        self.assertEqual(self.detector_process.output_queue.get(), 25700)

class test_bf_data_processes(unittest.TestCase):
    
    def setUp(self):
        self.test_image = np.arange(256*256).reshape(256,256)
    
    def tearDown(self):
        self.detector_process.stop_running()

    def test_bf_process(self):
        self.detector_process = BFDetectorProcess(
                "BF0",
                Queue())
        self.detector_process.start_process_function()
        self.detector_process.receive_queue.put(self.test_image)
        self.assertEqual(self.detector_process.output_queue.get(), 2147450880)

class test_adf_data_processes(unittest.TestCase):
    
    def setUp(self):
        self.test_image = np.arange(256*256).reshape(256,256)
    
    def tearDown(self):
        self.detector_process.stop_running()

    def test_adf_process(self):
        self.detector_process = ADFDetectorProcess(
                "ADF0",
                Queue())
        self.detector_process.generate_adf_detector(128, 128, 100, 200, 256, 256)
        self.detector_process.start_process_function()
        self.detector_process.receive_queue.put(self.test_image)
        self.assertEqual(self.detector_process.output_queue.get(), 1033493632.0)


class test_com_data_processes(unittest.TestCase):
    
    def setUp(self):
        self.test_image = np.zeros((256,256))
        self.test_image[160,100] = 100
        self.test_image[100,160] = 100
        self.test_image[110,110] = 50
        self.test_image[180,180] = 50

    def tearDown(self):
        self.detector_process_x.stop_running()
        self.detector_process_y.stop_running()

    def test_com_process(self):
        self.detector_process_x = CoMxProcess(
                "CoMx",
                Queue())
        self.detector_process_x.start_process_function()
        self.detector_process_x.receive_queue.put(self.test_image)
        self.detector_process_y = CoMyProcess(
                "CoMy",
                Queue())
        self.detector_process_y.start_process_function()
        self.detector_process_y.receive_queue.put(self.test_image)
        com_x = self.detector_process_x.output_queue.get()
        com_y = self.detector_process_y.output_queue.get()
        self.assertEqual((com_x, com_y), (135., 135.)) 


class test_com_threshold_data_processes(unittest.TestCase):
    
    def setUp(self):
        self.test_image = np.zeros((256,256))
        self.test_image[160,100] = 100
        self.test_image[100,160] = 100
        self.test_image[110,110] = 50
        self.test_image[180,180] = 50

    def tearDown(self):
        self.detector_process_x.stop_running()
        self.detector_process_y.stop_running()

    def test_com_threshold_process(self):
        self.detector_process_x = CoMxThresholdProcess(
                "CoMx",
                Queue())
        self.detector_process_x.start_process_function()
        self.detector_process_x.receive_queue.put(self.test_image)
        self.detector_process_y = CoMyThresholdProcess(
                "CoMy",
                Queue())
        self.detector_process_y.start_process_function()
        self.detector_process_y.receive_queue.put(self.test_image)
        com_x = self.detector_process_x.output_queue.get()
        com_y = self.detector_process_y.output_queue.get()
        self.assertEqual((com_x, com_y), (137., 137.)) 

class test_com_disk_mask_data_processes(unittest.TestCase):
    
    def setUp(self):
        self.test_image = np.zeros((256,256))
        self.test_image[160,100] = 100
        self.test_image[100,160] = 100
        self.test_image[110,110] = 50
        self.test_image[180,180] = 50

    def tearDown(self):
        self.detector_process_x.stop_running()
        self.detector_process_y.stop_running()

    def test_com_disk_mask_process(self):
        self.detector_process_x = CoMxMaskDiskProcess(
            "CoMx",
            Queue())
        self.detector_process_x._make_bf_mask(110, 110, 256, 256, 5)
        self.detector_process_x.start_process_function()
        self.detector_process_x.receive_queue.put(self.test_image)
        self.detector_process_y = CoMyMaskDiskProcess(
                "CoMy",
                Queue())
        self.detector_process_y._make_bf_mask(110, 110, 256, 256, 5)
        self.detector_process_y.start_process_function()
        self.detector_process_y.receive_queue.put(self.test_image)
        com_x = self.detector_process_x.output_queue.get()
        com_y = self.detector_process_y.output_queue.get()
        self.assertEqual((com_x, com_y), (140., 140.)) 
