import fpd_live_imaging.testing_tools as tt
import fpd_live_imaging.acquisition_control_class as acc
from fpd_live_imaging.test_images.test_images import (
        linux_penguin_16,
        linux_penguin_32, linux_penguin_64,
        linux_penguin_128, linux_penguin_256)
from math import pi

if __name__ == '__main__':

    acquisition_control = acc.LiveImagingQt()

    if True:
        test_detector = tt.TestDetectorInputImage(
                number_of_frames=200000,
                input_image=linux_penguin_64)
        test_detector.sleep_time.value = 1
        test_detector.start_data_listening()
        acquisition_control._comm_medi.port = test_detector.port
    elif False:
        test_detector = tt.TestSingleNonZero(
                number_of_frames=200000,
                x=100, y=100)
        test_detector.sleep_time.value = 0.1
        test_detector.start_data_listening()
        acquisition_control._comm_medi.port = test_detector.port
#    acquisition_control.start_bf_process()
#    acquisition_control.start_adf_process()
#    acquisition_control.start_com_x_threshold_process()
#    acquisition_control.start_com_y_threshold_process()
    acquisition_control.start_full_diffraction_image_process()
    acquisition_control.start_segmented_process_process(name="Segment0")
    acquisition_control.start_segmented_process_process(name="Segment1")
#    acquisition_control.start_full_diffraction_thresholded_image_process()


#    acquisition_control.resize_scan(129, 128)
    acquisition_control.resize_scan(64, 64)

    acquisition_control.start_medipix_receiver()
#    com_x = acquisition_control.process_dict['CoMxT']['comm']
#    com_y = acquisition_control.process_dict['CoMyT']['comm']
#    bf0 = acquisition_control.process_dict['BF0']['comm']
#    adf0 = acquisition_control.process_dict['ADF0']['proc']
    seg0 = acquisition_control.process_dict['Segment0']['proc']
    seg1 = acquisition_control.process_dict['Segment1']['proc']
    seg0.centreX, seg0.centreY, seg0.radius0, seg0.radius1 = 130, 131, 30, 50
    seg1.centreX, seg1.centreY, seg1.radius0, seg1.radius1 = 130, 131, 30, 50
    seg1.angle = pi/2
