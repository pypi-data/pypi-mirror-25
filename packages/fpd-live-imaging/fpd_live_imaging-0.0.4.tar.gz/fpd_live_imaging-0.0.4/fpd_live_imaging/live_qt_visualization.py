import sys
from PyQt5.QtWidgets import (
        QMainWindow, QLabel, QApplication, QCheckBox,
        QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSpinBox)
from PyQt5.QtGui import QPainter, QPen, QImage, QPixmap, QPalette
from PyQt5 import QtCore
import numpy as np
import multiprocessing as mp


class DataView(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setScaledContents(True)

        hbox_upper = self.make_upper_button_bar()
        hbox_lower = self.make_lower_button_bar()

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(hbox_upper)

        self.vbox.addWidget(self.imageLabel)

        self.vbox.addLayout(hbox_lower)

        self.widget0 = QWidget()
        self.widget0.setLayout(self.vbox)

        self.setCentralWidget(self.widget0)

    def make_upper_button_bar(self):
        hbox_upper = QHBoxLayout()
        return(hbox_upper)

    def make_lower_button_bar(self):
        hbox_lower = QHBoxLayout()
        return(hbox_lower)

    def draw_detector_number(self, image, x, y, value, color='red'):
        painter = QPainter()
        painter.begin(image)
        painter.setRenderHint(QPainter.Antialiasing)
        if color == 'black':
            Qcolor = QtCore.Qt.black
        elif color == 'red':
            Qcolor = QtCore.Qt.red
        elif color == 'blue':
            Qcolor = QtCore.Qt.blue
        else:
            Qcolor = QtCore.Qt.black
        painter.setPen(QPen(Qcolor))
        painter.drawText(x, y, str(value))
        painter.end()

    def draw_detector_circle(self, image, x, y, r, color='black'):
        painter = QPainter()
        painter.begin(image)
        painter.setRenderHint(QPainter.Antialiasing)
        if color == 'black':
            Qcolor = QtCore.Qt.black
        elif color == 'red':
            Qcolor = QtCore.Qt.red
        elif color == 'blue':
            Qcolor = QtCore.Qt.blue
        else:
            Qcolor = QtCore.Qt.black
        painter.setPen(QPen(Qcolor))
        painter.drawEllipse(x, y, r, r)
        painter.end()

    def update_image(self, imagedata, plot_number=None):
        h, w, r = imagedata.shape
        image = QImage(
                imagedata.data, h, w,
                QImage.Format_ARGB32_Premultiplied)

        if hasattr(self, 'annotation_array'):
            if not ((self.annotation_array[2] == 0) and (self.annotation_array[2] == 0)):
                self.draw_detector_circle(
                        image,
                        self.annotation_array[0]-self.annotation_array[2],
                        self.annotation_array[1]-self.annotation_array[2],
                        self.annotation_array[2]*2, color='red')
                self.draw_detector_circle(
                        image,
                        self.annotation_array[0]-self.annotation_array[3],
                        self.annotation_array[1]-self.annotation_array[3],
                        self.annotation_array[3]*2, color='red')

        if plot_number is not None:
            self.draw_detector_number(image, 10, 10, plot_number)

        pixmap = QPixmap.fromImage(image)
        pixmap = pixmap.scaled(self.widget0.size()*0.9)
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.adjustSize()


class DataViewParallel(DataView):

    def __init__(self, input_queue, name, annotation_array):
        """
        Parameters
        ----------
        input_queue : multiprocessing queue
        name : string
        annotation_array : multiprocessing array

        Examples
        --------
        >>> import multiprocess as mp
        >>> from PyQt5.QtWidgets import QApplication
        >>> from fpd_live_imaging.live_qt_visualization import DataViewParallel
        >>> app = QApplication(sys.argv)
        >>> dataview = DataViewParallel(mp.Queue(), "test", mp.Array('i', 4))
        """
        super().__init__()

        self.size_x = 256
        self.size_y = 256

        self.annotation_array = annotation_array

        self.data = np.zeros((self.size_x, self.size_y, 4))

        self.input_queue = input_queue

        self.auto_lim = mp.Value('b', True)

        self.max_value = 2**8-2
        self.min_lim = 0
        self.max_lim = 1

        self.setWindowTitle(name)
        self.resize(500, 500)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_data)
        timer.start(20)  # In msec

    def update_data(self):
        for i in range(100):
            if not self.input_queue.empty():
                self.data[:, :, 3] = self.input_queue.get()
        if self.auto_lim.value is True:
            self.min_lim = self.data[:, :, 3].min()
            self.max_lim = self.data[:, :, 3].max()
            if self.min_lim == self.max_lim:
                self.max_lim = self.min_lim + 0.1

        max_min_diff = self.max_lim-self.min_lim
        self.data[:] = (self.data-self.min_lim)*self.max_value/max_min_diff
        np.clip(self.data, 0, self.max_value, out=self.data)
        imagedata = np.require(self.data, np.uint8, 'C')
        self.update_image(imagedata)


class DataViewScanning(DataView):

    def __init__(
            self, input_queue, restart_scan_flag,
            plus_one_pixel_to_scan_position,
            minus_one_pixel_to_scan_position,
            reset_autolim_flag, clim_min, clim_max, auto_clim,
            size_x, size_y, name):
        super().__init__()

        self.x = 0
        self.y = 0
        self._size_x = size_x
        self._size_y = size_y
        self._size_x_max = 512
        self._size_y_max = 512
        self.restart_scan_flag = restart_scan_flag

        self.plus_one_pixel_to_scan_position = plus_one_pixel_to_scan_position
        self.minus_one_pixel_to_scan_position = minus_one_pixel_to_scan_position

        self.reset_autolim_flag = reset_autolim_flag
        self._clim_min, self._clim_max = clim_min, clim_max

        self.data = np.zeros((self._size_x_max, self._size_y_max, 4))
        self.visualization_data = np.zeros(
                (self._size_x_max, self._size_y_max, 4))
        self.data_bool = np.zeros(
                (self._size_x_max, self._size_y_max), dtype=np.bool)

        self.update_plot = False

        self.input_queue = input_queue

        self._auto_clim = auto_clim

        self.max_value = 2**8-1
        self.min_lim = 0
        self.max_lim = 1

        self.setWindowTitle(name)
        self.resize(500, 500)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_data)
        timer.start(20)  # In msec

    @property
    def size_x(self):
        return(self._size_x.value)

    @size_x.setter
    def size_x(self, value):
        self._size_x.value = value
        self.scan_x_input.setValue(value)

    @property
    def size_y(self):
        return(self._size_y.value)

    @size_y.setter
    def size_y(self, value):
        self._size_y.value = value
        self.scan_y_input.setValue(value)

    @property
    def auto_clim(self):
        return(self._auto_clim.value)

    @auto_clim.setter
    def auto_clim(self, value):
        self._auto_clim.value = value
        self._auto_clim_input.setChecked(value)

    @property
    def clim_min(self):
        return(self._clim_min.value)

    @clim_min.setter
    def clim_min(self, value):
        self._clim_min.value = value
        self._clim_min_input.setValue(value)

    @property
    def clim_max(self):
        return(self._clim_max.value)

    @clim_max.setter
    def clim_max(self, value):
        self._clim_max.value = value
        self._clim_max_input.setValue(value)

    def make_upper_button_bar(self):
        hbox = QHBoxLayout()

        button_pm = QPushButton('-1 pixel')
        button_pm.clicked.connect(
                lambda: setattr(
                    self.minus_one_pixel_to_scan_position,
                    'value', True))
        hbox.addWidget(button_pm)

        button_pp = QPushButton('+1 pixel')
        button_pp.clicked.connect(
                lambda: setattr(
                    self.plus_one_pixel_to_scan_position,
                    'value', True))
        hbox.addWidget(button_pp)

        button_rs = QPushButton('Reset scan')
        button_rs.clicked.connect(
                lambda: setattr(self.restart_scan_flag, 'value', True))
        hbox.addWidget(button_rs)

        button_ra = QPushButton('Reset autolim')
        button_ra.clicked.connect(
                lambda: setattr(
                    self.reset_autolim_flag, 'value', True))
        hbox.addWidget(button_ra)

        self.scan_x_input = QSpinBox(
                minimum=1., maximum=512, keyboardTracking=False)
        self.scan_x_input.valueChanged.connect(
                lambda x: setattr(self, 'size_x', x))
        hbox.addWidget(self.scan_x_input)

        self.scan_y_input = QSpinBox(
                minimum=1., maximum=512, keyboardTracking=False)
        self.scan_y_input.valueChanged.connect(
                lambda y: setattr(self, 'size_y', y))
        hbox.addWidget(self.scan_y_input)
        return(hbox)

    def make_lower_button_bar(self):
        lim = 2**30
        hbox = QHBoxLayout()

        self._auto_clim_input = QCheckBox("Auto clim")
        self._auto_clim_input.stateChanged.connect(
                lambda x: setattr(self, 'auto_clim', x))
        hbox.addWidget(self._auto_clim_input)

        self._clim_min_input = QSpinBox(
                minimum=-lim, maximum=lim, keyboardTracking=False)
        self._clim_min_input.valueChanged.connect(
                lambda x: setattr(self, 'clim_min', x))
        hbox.addWidget(self._clim_min_input)

        self._clim_max_input = QSpinBox(
                minimum=-lim, maximum=lim, keyboardTracking=False)
        self._clim_max_input.valueChanged.connect(
                lambda x: setattr(self, 'clim_max', x))
        hbox.addWidget(self._clim_max_input)

        return(hbox)

    def _update_data_array(self):
        self._pixel_data = 0
        for i in range(10):
            if not self.input_queue.empty():
                self._pixel_data = self.input_queue.get()
                self.data[self.y, self.x, 3] = self._pixel_data
                if not self.data_bool[0:self.size_y, 0:self.size_x].all():
                    self.data_bool[self.y, self.x] = True
                if self.x >= (self.size_x-1):
                    self.x = 0
                    self.y = self.y + 1
                    if self.y >= (self.size_y):
                        self.y = 0
                else:
                    self.x = self.x + 1
                self.update_plot = True

    def _calculate_clim(self):
        if self.auto_clim:
            if self.data_bool.any():
                bool_array = self.data_bool[
                        0:self.size_y, 0:self.size_x]
                std = self.data[
                        0:self.size_y,
                        0:self.size_x, 3][bool_array].std()
                mean = self.data[
                        0:self.size_y,
                        0:self.size_x, 3][bool_array].mean()
                self.min_lim = mean - std*2
                self.max_lim = mean + std*2
            if self.min_lim == self.max_lim:
                self.max_lim = self.min_lim + 0.1
        else:
            self.min_lim, self.max_lim = self.clim_min, self.clim_max
        self.max_min_diff = self.max_lim-self.min_lim

    def _get_plotting_data(self):
        temp_scaling = self.max_value/self.max_min_diff
        self.visualization_data[:] = (
                self.data[:, :, :] - self.min_lim)*temp_scaling
        self.visualization_data[np.invert(self.data_bool), :] = 0.0
        np.clip(
                self.visualization_data, 0, self.max_value,
                out=self.visualization_data)
        imagedata = np.require(
                self.visualization_data[
                    0:self.size_y, 0:self.size_x, :],
                np.uint8, 'C')
        return(imagedata)

    def update_data(self):
        if self.restart_scan_flag.value:
            self.restart_scan_flag.value = False
            self.x = 0
            self.y = 0
        if self.plus_one_pixel_to_scan_position.value:
            self.plus_one_pixel_to_scan_position.value = False
            self.x = self.x + 1
        if self.minus_one_pixel_to_scan_position.value:
            self.minus_one_pixel_to_scan_position.value = False
            self.x = self.x - 1
        if self.reset_autolim_flag.value:
            self.reset_autolim_flag.value = False
            self.data_bool[:] = False
        if self.size_x != self._size_x.value:
            self.size_x = self._size_x.value
        self._update_data_array()
        if self.update_plot:
            self._calculate_clim()
            imagedata = self._get_plotting_data()
            self.update_image(imagedata, plot_number=self._pixel_data)
            self.update_plot = False


def start_scanning_image_viewer(
        input_queue,
        restart_scan_flag,
        plus_one_pixel_to_scan_position,
        minus_one_pixel_to_scan_position,
        reset_autolim_flag,
        clim_min, clim_max, auto_clim,
        size_x, size_y, name=""):
    app = QApplication(sys.argv)
    dataview = DataViewScanning(
            input_queue,
            restart_scan_flag,
            plus_one_pixel_to_scan_position,
            minus_one_pixel_to_scan_position,
            reset_autolim_flag,
            clim_min, clim_max, auto_clim,
            size_x, size_y, name)
    dataview.show()
    sys.exit(app.exec_())


def start_parallel_image_viewer(input_queue, name, annotation_array):
    app = QApplication(sys.argv)
    dataview = DataViewParallel(input_queue, name, annotation_array)
    dataview.show()
    sys.exit(app.exec_())


class LiveScanningImageQt(object):

    def __init__(self, name=""):
        self.input_queue = mp.Queue()
        self.name = name
        self._restart_scan = mp.Value('b', False)
        self._plus_one_pixel_to_scan_position = mp.Value('b', False)
        self._minus_one_pixel_to_scan_position = mp.Value('b', False)
        self._reset_autolim_flag = mp.Value('b', False)
        self.clim_min = mp.Value('i', 0)
        self.clim_max = mp.Value('i', 1)
        self.auto_clim = mp.Value('b', True)
        self.size_x = mp.Value('i', 256)
        self.size_y = mp.Value('i', 256)

    def start_data_listening(self):
        self.process = mp.Process(
                target=start_scanning_image_viewer,
                args=(
                    self.input_queue,
                    self._restart_scan,
                    self._plus_one_pixel_to_scan_position,
                    self._minus_one_pixel_to_scan_position,
                    self._reset_autolim_flag,
                    self.clim_min, self.clim_max,
                    self.auto_clim,
                    self.size_x, self.size_y,
                    self.name))
        self.process.start()

    def stop_running(self):
        self.process.terminate()


class LiveParallelImageQt(object):

    def __init__(self, annotation_array, name=""):
        self.input_queue = mp.Queue()
        self.name = name
        self.annotation_array = annotation_array

    def start_data_listening(self):
        args = (self.input_queue, self.name, self.annotation_array)
        self.process = mp.Process(
                target=start_parallel_image_viewer, args=args)
        self.process.start()

    def stop_running(self):
        self.process.terminate()
