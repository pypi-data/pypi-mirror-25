import numpy as np
import multiprocessing as mp
from scipy.ndimage.measurements import center_of_mass
from scipy.optimize import leastsq
import time


class DataProcessingBase(object):
    def __init__(self, name, output_queue, process_variables=[]):
        self.name = name
        self.receive_queue = mp.Queue()
        self.output_queue = output_queue
        self.process_variables = process_variables
        self.base_level_correction = mp.Value('f', 0.)
        self.fraction_correction = mp.Value('f', 1.)
        self.processes_active = mp.Value('b', True)

        self.process_sleep_time = 1.e-7

    def __repr__(self):
        return '<%s %s (B:%s,C:%s) (I:%s)>' % (
                self.__class__.__name__,
                self.name,
                self.base_level_correction.value,
                self.fraction_correction.value,
                self.receive_queue.qsize())

    def stop_running(self):
        self.processes_active.value = False

    def clear_queues(self):
        while not self.receive_queue.empty():
            self.receive_queue.queue.get()
        while not self.output_queue.empty():
            self.output_queue.queue.get()

    def start_process_function(self):
        self.process_process = mp.Process(target=self._data_parsing_process)
        self.process_process.start()

    def _data_parsing_process(self):
        while self.processes_active.value:
            time.sleep(self.process_sleep_time)
            if not self.receive_queue.empty():
                diffraction_image = self.receive_queue.get()
                pixel_value = self.process_function(
                                diffraction_image)
                pixel_value -= self.base_level_correction.value
                pixel_value /= self.fraction_correction.value
                self.output_queue.put(int(pixel_value))
                del diffraction_image, pixel_value

    def _make_circular_mask(
            self, centerX, centerY,
            imageSizeX, imageSizeY, radius):
        y, x = np.ogrid[
                -centerX:imageSizeX-centerX,
                -centerY:imageSizeY-centerY]
        mask = x*x + y*y <= radius*radius
        return(mask)

    def _make_adf_mask(
            self, centerX, centerY,
            imageSizeX, imageSizeY, radius0, radius1):
        inner_mask = self._make_circular_mask(
                centerX, centerY, imageSizeX, imageSizeY, radius0)
        outer_mask = self._make_circular_mask(
                centerX, centerY, imageSizeX, imageSizeY, radius1)
        return(np.logical_xor(inner_mask, outer_mask))

    def _make_segment_bool_array(
            self, centerX, centerY,
            angle0, angle1, imageSizeX, imageSizeY):
        angle0 = angle0 % (2*np.pi)
        angle1 = angle1 % (2*np.pi)
        y, x = np.ogrid[
            -centerX:imageSizeX - centerX,
            -centerY:imageSizeY - centerY]
        t = np.arctan2(x, y)+np.pi
        if angle0 < angle1:
            bool_array = (t > angle0) * (t < angle1)
        else:
            bool_array = (t > angle0) + (t < angle1)
        return(bool_array)

    def _make_segment_mask(
            self, centerX, centerY, imageSizeX, imageSizeY,
            radius0, radius1, angle0, angle1):
        inner_mask = self._make_circular_mask(
                centerX, centerY, imageSizeX, imageSizeY, radius0)
        outer_mask = self._make_circular_mask(
                centerX, centerY, imageSizeX, imageSizeY, radius1)
        segment_array = self._make_segment_bool_array(
                centerX, centerY, angle0, angle1, imageSizeX, imageSizeY)
        mask = np.logical_xor(inner_mask, outer_mask)
        mask *= segment_array
        return(mask)

    def _make_bf_mask(
            self, centerX=128, centerY=128,
            imageSizeX=256, imageSizeY=256, radius=20):
        self.bf_mask = self._make_circular_mask(
                centerX, centerY, imageSizeX, imageSizeY, radius)


class FullDiffractionImageProcess(DataProcessingBase):

    def _data_parsing_process(self):
        while self.processes_active.value:
            time.sleep(self.process_sleep_time)
            if not self.receive_queue.empty():
                diffraction_image = self.receive_queue.get()
                self.output_queue.put(diffraction_image)
                del diffraction_image


class DiffractionImageRollingProcess(DataProcessingBase):

    def __init__(self, *args, **kwds):
        super(DiffractionImageRollingProcess, self).__init__(
                *args, **kwds)
        self._frames_to_average = mp.Value('i', 10)
        self._framesize_x = mp.Value('i', 256)
        self._framesize_y = mp.Value('i', 256)
        self._refresh_frame_array = mp.Value('b', True)

    @property
    def frames_to_average(self):
        return self._frames_to_average.value

    @frames_to_average.setter
    def frames_to_average(self, value):
        self._frames_to_average.value = value
        self._refresh_frame_array.value = True

    def reset(self):
        self._refresh_frame_array.value = True

    def _data_parsing_process(self):
        index = 0
        frame_shape = (self._framesize_x.value, self._framesize_y.value)
        while self.processes_active.value:
            if self._refresh_frame_array.value:
                image_array = np.zeros(
                        shape=(
                            self._frames_to_average.value,
                            frame_shape[0], frame_shape[1]))
                self._refresh_frame_array.value = False
                index = 0

            time.sleep(self.process_sleep_time)
            if not self.receive_queue.empty():
                diffraction_image = self.receive_queue.get()
                image_array[index, :, :] = diffraction_image
                mean_image = np.mean(image_array, axis=0)
                self.output_queue.put(mean_image)
                del diffraction_image, mean_image
                index += 1
                if index > (self._frames_to_average.value-1):
                    index = 0


class FullDiffractionThresholdedImageProcess(DataProcessingBase):
    def __init__(self, *args, **kwds):
        super(FullDiffractionThresholdedImageProcess, self).__init__(
                *args, **kwds)
        self.threshold_multiplier = mp.Value('f', 1.)

    def _data_parsing_process(self):
        while self.processes_active.value:
            time.sleep(self.process_sleep_time)
            if not self.receive_queue.empty():
                diffraction_image = self.receive_queue.get()
                threshold = np.mean(
                        diffraction_image)*self.threshold_multiplier.value
                diffraction_image[diffraction_image < threshold] = 0
                diffraction_image[diffraction_image >= threshold] = 1
                self.output_queue.put(diffraction_image)
                del diffraction_image


class BFDetectorProcess(DataProcessingBase):
    def process_function(self, diffraction_image):
        pixel_value = diffraction_image.sum(dtype=np.uint32)
        return(pixel_value)


class ADFDetectorProcess(DataProcessingBase):
    def __init__(self, *args, **kwds):
        super(ADFDetectorProcess, self).__init__(*args, **kwds)
        self._centreX = mp.Value('f', 128.)
        self._centreY = mp.Value('f', 128.)
        self._radius0 = mp.Value('f', 10.)
        self._radius1 = mp.Value('f', 20.)
        self._refresh_mask = mp.Value('b', True)
        self.annotation_array = None

    def process_function(self, diffraction_image):
        if self._refresh_mask.value:
            self.generate_adf_detector(
                    self._centreX.value, self._centreY.value,
                    self._radius0.value, self._radius1.value)
        masked_diffraction_image = diffraction_image
        masked_diffraction_image[self.adf_mask] = 0
        pixel_value = masked_diffraction_image.sum(dtype=np.uint32)
        return(pixel_value)

    @property
    def centreX(self):
        return self._centreX.value

    @centreX.setter
    def centreX(self, value):
        self._centreX.value = value
        self.annotation_array[0] = value
        self._refresh_mask.value = True

    @property
    def centreY(self):
        return self._centreY.value

    @centreY.setter
    def centreY(self, value):
        self._centreY.value = value
        self.annotation_array[1] = value
        self._refresh_mask.value = True

    @property
    def radius0(self):
        return self._radius0.value

    @radius0.setter
    def radius0(self, value):
        self._radius0.value = value
        self.annotation_array[2] = value
        self._refresh_mask.value = True

    @property
    def radius1(self):
        return self._radius1.value

    @radius1.setter
    def radius1(self, value):
        self._radius1.value = value
        self.annotation_array[3] = value
        self._refresh_mask.value = True

    def generate_adf_detector(
            self, centerX, centerY, radius0, radius1,
            imageSizeX=256, imageSizeY=256):
        self.adf_mask = self._make_adf_mask(
                centerX, centerY, imageSizeX, imageSizeY, radius0, radius1)
        self._refresh_mask.value = False


class SegmentedProcess(DataProcessingBase):
    def __init__(self, *args, **kwds):
        super(SegmentedProcess, self).__init__(*args, **kwds)
        self._centreX = mp.Value('f', 128.)
        self._centreY = mp.Value('f', 128.)
        self._radius0 = mp.Value('f', 10.)
        self._radius1 = mp.Value('f', 20.)
        self._angle = mp.Value('f', 0.)
        self._refresh_mask = mp.Value('b', True)
        self.annotation_array = None

    def process_function(self, diffraction_image):
        if self._refresh_mask.value:
            self.generate_segmented_detector(
                self._centreX.value, self._centreY.value,
                self._radius0.value, self._radius1.value,
                self._angle.value)
        sum0 = diffraction_image[self.mask0].sum(dtype=np.int64)
        sum1 = diffraction_image[self.mask1].sum(dtype=np.int64)
        pixel_value = np.uint32((sum0 - sum1 + 0.5*(2**32)))
        return(pixel_value)

    @property
    def centreX(self):
        return self._centreX.value

    @centreX.setter
    def centreX(self, value):
        self._centreX.value = value
        self.annotation_array[0] = value
        self._refresh_mask.value = True

    @property
    def centreY(self):
        return self._centreY.value

    @centreY.setter
    def centreY(self, value):
        self._centreY.value = value
        self.annotation_array[1] = value
        self._refresh_mask.value = True

    @property
    def radius0(self):
        return self._radius0.value

    @radius0.setter
    def radius0(self, value):
        self._radius0.value = value
        self.annotation_array[2] = value
        self._refresh_mask.value = True

    @property
    def radius1(self):
        return self._radius1.value

    @radius1.setter
    def radius1(self, value):
        self._radius1.value = value
        self.annotation_array[3] = value
        self._refresh_mask.value = True

    @property
    def angle(self):
        return self._angle.value

    @angle.setter
    def angle(self, value):
        self._angle.value = value
        self._refresh_mask.value = True

    def generate_segmented_detector(
            self, centreX, centreY, radius0, radius1,
            angle, imageSizeX=256, imageSizeY=256):
        self.mask0 = self._make_segment_mask(
                centreX, centreY, imageSizeX, imageSizeY,
                radius0, radius1, angle, angle+(np.pi/2))
        self.mask1 = self._make_segment_mask(
                centreX, centreY, imageSizeX, imageSizeY,
                radius0, radius1, angle+np.pi, angle+(np.pi/2)+np.pi)
        self._refresh_mask.value = False


class SinglePixelProcess(DataProcessingBase):
    def process_function(self, diffraction_image):
        x, y = self.process_variables[0]
        pixel_value = diffraction_image[x, y]
        return(pixel_value)


class CoMxProcess(DataProcessingBase):
    def process_function(self, diffraction_image):
        CoMx, CoMy = center_of_mass(diffraction_image)
        return(CoMx)


class CoMyProcess(DataProcessingBase):
    def process_function(self, diffraction_image):
        CoMx, CoMy = center_of_mass(diffraction_image)
        return(CoMy)


class CoMxThresholdProcess(DataProcessingBase):
    def __init__(self, *args, **kwds):
        super(CoMxThresholdProcess, self).__init__(*args, **kwds)
        self.threshold_multiplier = mp.Value('f', 1.)

    def process_function(self, diffraction_image):
        threshold = np.mean(diffraction_image)*self.threshold_multiplier.value
        diffraction_image[diffraction_image < threshold] = 0
        diffraction_image[diffraction_image >= threshold] = 1
        CoMx, CoMy = center_of_mass(diffraction_image)
        return(CoMx)


class CoMyThresholdProcess(DataProcessingBase):
    def __init__(self, *args, **kwds):
        super(CoMyThresholdProcess, self).__init__(*args, **kwds)
        self.threshold_multiplier = mp.Value('f', 1.)

    def process_function(self, diffraction_image):
        threshold = np.mean(diffraction_image)*self.threshold_multiplier.value
        diffraction_image[diffraction_image < threshold] = 0
        diffraction_image[diffraction_image >= threshold] = 1
        CoMx, CoMy = center_of_mass(diffraction_image)
        return(CoMy)


class CoMxMaskDiskProcess(DataProcessingBase):
    def process_function(self, diffraction_image):
        diffraction_image[self.bf_mask] = 0.0
        CoMx, CoMy = center_of_mass(diffraction_image)
        return(CoMx)


class CoMyMaskDiskProcess(DataProcessingBase):
    def process_function(self, diffraction_image):
        diffraction_image[self.bf_mask] = 0.0
        CoMx, CoMy = center_of_mass(diffraction_image)
        return(CoMy)


class HolzProcessing(DataProcessingBase):
    # This is completely untested, will probably not run on first try
    def process_function(self, diffraction_image):
        annulus_sum0 = (self.annulus0*diffraction_image).sum(dtype=np.uint32)
        annulus_sum1 = (self.annulus1*diffraction_image).sum(dtype=np.uint32)
        annulus_sum2 = (self.annulus2*diffraction_image).sum(dtype=np.uint32)
        annulus_sum3 = (self.annulus3*diffraction_image).sum(dtype=np.uint32)

        xdata = np.array([self.radius0, self.radius1, self.radius2])
        ydata = np.array([annulus_sum0, annulus_sum1, annulus_sum2])

        qout, success = leastsq(
                self.errfunc, [max(ydata), -1, -0.5],
                args=(xdata, ydata), maxfev=3000)

        background_value = self._fitfunc(
                [qout[0], qout[1], qout[2]],
                self.integrate_radius3)
        pixel_value = annulus_sum3 - background_value
        return(pixel_value)

    def _fitfunc(self, p, x):
        return p[0] + p[1] * (x ** p[2])

    def _errfunc(self, p, x, y):
        return y - self.fitfunc(p, x)

    def generate_annular_masks(
            self, centerX, centerY,
            imageSizeX, imageSizeY,
            radius00, radius01, radius10, radius11,
            radius20, radius21, radius30, radius31):
        self.radius0 = (radius01+radius00)*0.5
        self.radius1 = (radius11+radius10)*0.5
        self.radius2 = (radius21+radius20)*0.5
        self.integrate_radius3 = (radius31+radius30)*0.5
        self.annulus0 = self._make_adf_mask(
                centerX, centerY, imageSizeX, imageSizeY, radius00, radius01)
        self.annulus1 = self._make_adf_mask(
                centerX, centerY, imageSizeX, imageSizeY, radius10, radius11)
        self.annulus2 = self._make_adf_mask(
                centerX, centerY, imageSizeX, imageSizeY, radius20, radius21)
        self.integrate_annulus3 = self._make_adf_mask(
                centerX, centerY, imageSizeX, imageSizeY, radius30, radius31)
