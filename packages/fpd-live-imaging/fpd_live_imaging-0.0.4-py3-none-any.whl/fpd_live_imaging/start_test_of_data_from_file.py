import fpd_live_imaging.testing_tools as tt
import fpd_live_imaging.acquisition_control_class as acc
from numpy import pi
from fpd_live_imaging.test_images.test_images import (
        linux_penguin_16,
        linux_penguin_32, linux_penguin_64,
        linux_penguin_128, linux_penguin_256)

if __name__ == '__main__':

    acquisition_control = acc.LiveImagingQt()

#    test_detector = tt.TestDetectorInputImage(
#            number_of_frames=200000,
#            input_image=linux_penguin_64)
#    test_detector.sleep_time.value = 0.001
#    test_detector.start_data_listening()
#    acquisition_control._comm_medi.port = test_detector.port

#    acquisition_control.start_bf_process()
    acquisition_control.start_full_diffraction_image_process()
#    acquisition_control.start_adf_process()
    acquisition_control.start_segmented_process_process()
    acquisition_control.start_segmented_process_process(name='Segment1')
    acquisition_control.process_dict['Segment0']['proc'].angle = 0
    acquisition_control.process_dict['Segment1']['proc'].angle = pi/2

#    bf0_queue = acquisition_control.process_dict['BF0']['proc'].receive_queue
    diff_queue = acquisition_control.process_dict['Diffraction']['proc'].receive_queue
#    adf0_queue = acquisition_control.process_dict['ADF0']['proc'].receive_queue
    seg0_queue = acquisition_control.process_dict['Segment0']['proc'].receive_queue
    seg1_queue = acquisition_control.process_dict['Segment1']['proc'].receive_queue
    processing_queue_list = [
#            bf0_queue,
            diff_queue,
#            adf0_queue,
            seg0_queue,
            seg1_queue]

    hdf5_file = '/media/storage/postdoc_extra_datasets/2017_05_04_FeRh/006_default1.hdf5'
    data_from_file = tt.TestDataFromFile(processing_queue_list, hdf5_file, sleep_time=0.0001) 

    acquisition_control.resize_scan(256, 256)
    data_from_file.start_data_sending()

#    adf0 = acquisition_control.process_dict['ADF0']['proc']
    seg0 = acquisition_control.process_dict['Segment0']['proc']
    seg1 = acquisition_control.process_dict['Segment1']['proc']

    seg0.centreX, seg0.centreY, seg0.radius0, seg0.radius1 = 130, 131, 5, 10
    seg1.centreX, seg1.centreY, seg1.radius0, seg1.radius1 = 130, 131, 5, 10
