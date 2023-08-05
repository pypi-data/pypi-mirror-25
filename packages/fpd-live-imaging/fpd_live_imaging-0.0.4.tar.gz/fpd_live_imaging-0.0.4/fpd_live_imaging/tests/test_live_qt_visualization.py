import sys
import unittest
import time
import numpy as np
import multiprocessing as mp
from fpd_live_imaging.live_qt_visualization import (
        DataView, DataViewParallel, DataViewScanning)
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage
from PyQt5.QtTest import QTest
from PyQt5 import QtCore


class TestDataView(unittest.TestCase):

    def setUp(self):
        data = np.zeros((100, 100, 3))
        self.imagedata = np.require(data, np.uint8, 'C')
        h, w, r = self.imagedata.shape
        self.image = QImage(
                self.imagedata.data, h, w, QImage.Format_ARGB32_Premultiplied)

    def test_init(self):
        app = QApplication(sys.argv)
        dataview = DataView()

    def test_draw_detector_number(self):
        app = QApplication(sys.argv)
        dataview = DataView()
        dataview.draw_detector_number(self.image, 10, 10, 50, color='black')

    def test_draw_detector_circle(self):
        app = QApplication(sys.argv)
        dataview = DataView()
        dataview.draw_detector_circle(self.image, 15, 20, 7, color='blue')

    def test_update_image(self):
        app = QApplication(sys.argv)
        dataview = DataView()
        dataview.update_image(self.imagedata, plot_number=True)


class TestDataViewParallel(unittest.TestCase):

    def setUp(self):
        self.input_queue = mp.Queue()
        self.annotation_array = mp.Array('i', 4)
        self.data = np.zeros((256, 256))

    def test_init(self):
        app = QApplication(sys.argv)
        dataview = DataViewParallel(mp.Queue(), "test", mp.Array('i', 4))

    def test_update_data(self):
        app = QApplication(sys.argv)
        dataview = DataViewParallel(self.input_queue, "test", mp.Array('i', 4))
        self.input_queue.put(self.data)
        dataview.update_data()


class TestDataViewScanning(unittest.TestCase):

    def setUp(self):
        self.input_queue = mp.Queue()
        self.annotation_array = mp.Array('i', 4)
        self.data = np.zeros((256, 256))
        self.restart_scan_flag = mp.Value('b', False)
        self.plus_one_pixel_to_scan_position = mp.Value('b', False)
        self.minus_one_pixel_to_scan_position = mp.Value('b', False)
        self.reset_autolim_flag = mp.Value('b', False)
        self.clim_min = mp.Value('i', 0)
        self.clim_max = mp.Value('i', 1)
        self.auto_clim = mp.Value('b', True)
        self.size_x = mp.Value('i', 256)
        self.size_y = mp.Value('i', 256)

    def test_init(self):
        input_queue = mp.Queue()
        app = QApplication(sys.argv)
        dataview = DataViewScanning(
                input_queue,
                self.restart_scan_flag,
                self.plus_one_pixel_to_scan_position,
                self.minus_one_pixel_to_scan_position,
                self.reset_autolim_flag,
                self.clim_min, self.clim_max, self.auto_clim,
                self.size_x, self.size_y, "test")

    def test_scan_size(self):
        size_x, size_y = mp.Value('i', 256), mp.Value('i', 256)
        input_queue = mp.Queue()
        app = QApplication(sys.argv)
        dataview = DataViewScanning(
                input_queue,
                self.restart_scan_flag,
                self.plus_one_pixel_to_scan_position,
                self.minus_one_pixel_to_scan_position,
                self.reset_autolim_flag,
                self.clim_min, self.clim_max, self.auto_clim,
                size_x, size_y, "test")

        size_x.value = 512
        size_y.value = 512
        self.assertEqual(dataview.size_x, 512)
        self.assertEqual(dataview.size_y, 512)

        size_x.value = 101
        size_y.value = 51
        self.assertEqual(dataview.size_x, 101)
        self.assertEqual(dataview.size_y, 51)

    def test_scanning_simple(self):
        size_x, size_y = mp.Value('i', 256), mp.Value('i', 256)
        input_queue = mp.Queue()
        app = QApplication(sys.argv)
        dataview = DataViewScanning(
                input_queue,
                self.restart_scan_flag,
                self.plus_one_pixel_to_scan_position,
                self.minus_one_pixel_to_scan_position,
                self.reset_autolim_flag,
                self.clim_min, self.clim_max, self.auto_clim,
                size_x, size_y, "test")
        self.assertEqual(dataview.x, 0)
        self.assertEqual(dataview.y, 0)

        input_queue.put(5)
        time.sleep(0.1)
        dataview.update_data()
        self.assertEqual(dataview.x, 1)
        self.assertEqual(dataview.y, 0)

    def test_scanning_several(self):
        size_x, size_y = mp.Value('i', 256), mp.Value('i', 256)
        input_queue = mp.Queue()
        app = QApplication(sys.argv)
        dataview = DataViewScanning(
                input_queue,
                self.restart_scan_flag,
                self.plus_one_pixel_to_scan_position,
                self.minus_one_pixel_to_scan_position,
                self.reset_autolim_flag,
                self.clim_min, self.clim_max, self.auto_clim,
                size_x, size_y, "test")
        size_x.value, size_y.value = 22, 11
        self.assertEqual(dataview.x, 0)
        self.assertEqual(dataview.y, 0)

        for i in range(21):
            input_queue.put(i)
        time.sleep(0.1)
        for i in range(3):
            dataview.update_data()
        self.assertEqual(dataview.x, 21)
        self.assertEqual(dataview.y, 0)

        input_queue.put(10)
        time.sleep(0.1)
        dataview.update_data()
        self.assertEqual(dataview.x, 0)
        self.assertEqual(dataview.y, 1)

        for i in range(22*10-1):
            input_queue.put(i)
        time.sleep(0.1)
        for i in range(25):
            dataview.update_data()
        self.assertEqual(dataview.x, 21)
        self.assertEqual(dataview.y, 10)

        input_queue.put(10)
        time.sleep(0.1)
        dataview.update_data()
        self.assertEqual(dataview.x, 0)
        self.assertEqual(dataview.y, 0)

    def test_reset_scan(self):
        restart_scan_flag = mp.Value('b', False)
        plus_one_pixel_to_scan_position = mp.Value('b', False)
        minus_one_pixel_to_scan_position = mp.Value('b', False)
        size_x, size_y = mp.Value('i', 21), mp.Value('i', 12)
        input_queue = mp.Queue()
        app = QApplication(sys.argv)
        dataview = DataViewScanning(
                input_queue,
                restart_scan_flag,
                plus_one_pixel_to_scan_position,
                minus_one_pixel_to_scan_position,
                self.reset_autolim_flag,
                self.clim_min, self.clim_max, self.auto_clim,
                size_x, size_y, "test")

        for i in range(5):
            input_queue.put(i)
        time.sleep(0.1)
        for i in range(3):
            dataview.update_data()
        self.assertEqual(dataview.x, 5)
        self.assertEqual(dataview.y, 0)
        restart_scan_flag.value = True
        dataview.update_data()
        self.assertEqual(dataview.x, 0)
        self.assertEqual(dataview.y, 0)

        for i in range(25):
            input_queue.put(i)
        time.sleep(0.1)
        for i in range(10):
            dataview.update_data()
        self.assertEqual(dataview.x, 4)
        self.assertEqual(dataview.y, 1)
        restart_scan_flag.value = True
        dataview.update_data()
        self.assertEqual(dataview.x, 0)
        self.assertEqual(dataview.y, 0)

    def test_plus_one_pixel_to_scan_position(self):
        restart_scan_flag = mp.Value('b', False)
        plus_one_pixel_to_scan_position = mp.Value('b', False)
        minus_one_pixel_to_scan_position = mp.Value('b', False)
        size_x, size_y = mp.Value('i', 21), mp.Value('i', 12)
        input_queue = mp.Queue()
        app = QApplication(sys.argv)
        dataview = DataViewScanning(
                input_queue, restart_scan_flag,
                plus_one_pixel_to_scan_position,
                minus_one_pixel_to_scan_position,
                self.reset_autolim_flag,
                self.clim_min, self.clim_max, self.auto_clim,
                size_x, size_y, "test")

        for i in range(7):
            input_queue.put(i)
        time.sleep(0.1)
        for i in range(3):
            dataview.update_data()
        self.assertEqual(dataview.x, 7)
        self.assertEqual(dataview.y, 0)
        plus_one_pixel_to_scan_position.value = True
        dataview.update_data()
        self.assertEqual(dataview.x, 8)
        self.assertEqual(dataview.y, 0)

    def test_scan_ui_click(self):
        restart_scan_flag = mp.Value('b', False)
        plus_one_pixel_to_scan_position = mp.Value('b', False)
        minus_one_pixel_to_scan_position = mp.Value('b', False)
        size_x, size_y = mp.Value('i', 21), mp.Value('i', 12)
        input_queue = mp.Queue()
        app = QApplication(sys.argv)
        dataview = DataViewScanning(
                input_queue, restart_scan_flag,
                plus_one_pixel_to_scan_position,
                minus_one_pixel_to_scan_position,
                self.reset_autolim_flag,
                self.clim_min, self.clim_max, self.auto_clim,
                size_x, size_y, "test")
        QTest.qWaitForWindowActive(dataview)

        QTest.keyClick(dataview.scan_x_input, QtCore.Qt.Key_Delete)
        QTest.keyClicks(dataview.scan_x_input, "50")
        self.assertEqual(dataview.size_x, 21)
        QTest.keyClick(dataview.scan_x_input, QtCore.Qt.Key_Return)
        self.assertEqual(dataview.size_x, 50)

        QTest.keyClick(dataview.scan_y_input, QtCore.Qt.Key_Delete)
        QTest.keyClicks(dataview.scan_y_input, "87")
        self.assertEqual(dataview.size_y, 12)
        QTest.keyClick(dataview.scan_y_input, QtCore.Qt.Key_Return)
        self.assertEqual(dataview.size_y, 87)
