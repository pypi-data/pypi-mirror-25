from fpd_live_imaging.receive_data_medipix_class import ReceiveDataMedipix
from fpd_live_imaging.process_classes import \
        BFDetectorProcess, CoMxThresholdProcess, CoMyThresholdProcess,\
        FullDiffractionImageProcess, FullDiffractionThresholdedImageProcess,\
        ADFDetectorProcess, SegmentedProcess
from fpd_live_imaging.communicate_data_dm_class import DataCommDM
import time
from fpd_live_imaging.live_qt_visualization import (
        LiveScanningImageQt, LiveParallelImageQt)
from fpd_live_imaging.receive_control_communication_class import \
        ReceiveControlComm
import multiprocessing as mp


class AcquisitionControlBase(object):

        def __init__(self, data_send_ip='127.0.0.1', debug=False):
            self._comm_medi = None
            self.process_dict = {}
            self._debug = debug
            self._comm_medi = ReceiveDataMedipix()
            self._control_comm = ReceiveControlComm(data_send_ip)
            self._control_comm.acquisition_control = self
            self.annotation_array = mp.Array('i', 4)

        def __repr__(self):
            process_list = []
            for process in self.process_dict.keys():
                process_list.append(process)
            process_string = ",".join(process)
            return '<%s (%s)>' % (
                self.__class__.__name__, process_string)

        def start_medipix_receiver(self):
            self._comm_medi.start_receive_detector_data_listening_process()

        def change_brightness_contrast(
                self, process_name, brightness, contrast):
            process = self.process_dict[process_name]['proc']
            process.base_level_correction = brightness
            process.fraction_correction = contrast

        def clear_all_queues(self):
            for process in self.process_dict.values():
                process['comm'].clear_queues()
                process['proc'].clear_queues()

        def cancel_process(self, name):
            proc = self.process_dict[name]['proc']
            comm = self.process_dict[name]['comm']
            proc.stop_running()
            comm.stop_running()
            time.sleep(0.1)
            del proc
            del comm

        def cancel_all_processes(self):
            self._comm_medi.stop_running()
            time.sleep(0.1)
            del self._comm_medi
            self._comm_medi = None
            time.sleep(0.1)
            for process_name in self.process_dict.keys():
                self.cancel_process(process_name)
            self.process_dict.clear()

        def _start_process(self, name, ProcessClass, annotation_array=None):
            comm = self._get_comm_object(name=name)
            comm.name = name + "Comm"
            if annotation_array is None:
                proc = ProcessClass(name, output_queue=comm.input_queue)
            else:
                proc = ProcessClass(name, output_queue=comm.input_queue)
                proc.annotation_array = annotation_array
            self.process_dict[proc.name] = {'comm': comm, 'proc': proc}
            self._comm_medi.data_process_list.append(proc)

            comm.start_data_listening()
            proc.start_process_function()
            if self._debug:
                print(proc)
                print(comm)

        def restart_scan(self):
            for process in list(self.process_dict.values()):
                comm = process['comm']
                if type(comm) == LiveScanningImageQt:
                    comm._restart_scan.value = True

        def resize_scan(self, x, y):
            for process in list(self.process_dict.values()):
                comm = process['comm']
                if type(comm) == LiveScanningImageQt:
                    comm.size_x.value = x
                    comm.size_y.value = y

        def plus_one_pixel_to_scan_postition(self):
            for process in list(self.process_dict.values()):
                comm = process['comm']
                if type(comm) == LiveScanningImageQt:
                    comm._plus_one_pixel_to_scan_position.value = True

        def minus_one_pixel_to_scan_postition(self):
            for process in list(self.process_dict.values()):
                comm = process['comm']
                if type(comm) == LiveScanningImageQt:
                    comm._minus_one_pixel_to_scan_position.value = True

        def reset_autolim_scanning(self):
            for process in list(self.process_dict.values()):
                comm = process['comm']
                if type(comm) == LiveScanningImageQt:
                    comm._reset_autolim_flag.value = True

        def start_bf_process(self, name="BF0"):
            self._start_process(name, BFDetectorProcess)
            return(name)

        def start_adf_process(self, name="ADF0"):
            self._start_process(
                    name, ADFDetectorProcess,
                    annotation_array=self.annotation_array)
            return(name)

        def start_com_x_threshold_process(self, name="CoMxT"):
            self._start_process(name, CoMxThresholdProcess)
            return(name)

        def start_com_y_threshold_process(self, name="CoMyT"):
            self._start_process(name, CoMyThresholdProcess)
            return(name)

        def start_segmented_process_process(self, name="Segment0"):
            self._start_process(
                    name, SegmentedProcess,
                    annotation_array=self.annotation_array)
            return(name)

        def start_full_diffraction_image_process(self, name="Diffraction"):
            comm = LiveParallelImageQt(self.annotation_array)
            comm.name = name

            proc = FullDiffractionImageProcess(
                    name, output_queue=comm.input_queue)
            self.process_dict[proc.name] = {'comm': comm, 'proc': proc}
            self._comm_medi.data_process_list.append(proc)

            comm.start_data_listening()
            proc.start_process_function()
            if self._debug:
                print(proc)
                print(comm)

        def start_full_diffraction_thresholded_image_process(
                self, name="DiffractionThresholded"):
            comm = LiveParallelImageQt()
            comm.name = name

            proc = FullDiffractionThresholdedImageProcess(
                    name, output_queue=comm.input_queue)
            self.process_dict[proc.name] = {'comm': comm, 'proc': proc}
            self._comm_medi.data_process_list.append(proc)

            comm.start_data_listening()
            proc.start_process_function()
            if self._debug:
                print(proc)
                print(comm)


class LiveImagingDM(AcquisitionControlBase):

        def __init__(self, data_send_ip='127.0.0.1', *args, **kwds):
            super(LiveImagingDM, self).__init__(*args, **kwds)
            self.data_send_ip = data_send_ip
            self.port_range = range(6344, 6350)

        def _get_comm_object(self, name=""):
            port = self._get_free_port()
            comm = DataCommDM(
                    ip_address=self.data_send_ip, port=port)
            return(comm)

        def _get_used_ports(self):
            used_ports = []
            for process in self.process_dict.values():
                used_ports.append(process['comm'].port)
            return(used_ports)

        def _get_free_port(self):
            used_ports = self._get_used_ports()
            for port in self.port_range:
                if not (port in used_ports):
                    return(port)


class LiveImagingQt(AcquisitionControlBase):

        def _get_comm_object(self, name=''):
            comm = LiveScanningImageQt()
            comm.name = name
            return(comm)


class DummyAcquisition(AcquisitionControlBase):

        class DummyComm(object):

            def __init__(self, name=''):
                self.name = name
                self.input_queue = mp.Queue()

            def start_data_listening(self):
                pass

            def stop_running(self):
                pass

        def _get_comm_object(self, name=""):
            comm = self.DummyComm(name=name)
            return(comm)
