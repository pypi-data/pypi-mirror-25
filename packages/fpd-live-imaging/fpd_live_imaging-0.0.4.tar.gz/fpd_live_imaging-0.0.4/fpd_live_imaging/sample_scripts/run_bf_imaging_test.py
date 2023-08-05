import fpd_live_imaging.testing_tools as tt
import fpd_live_imaging.acquisition_control_class as acc
from fpd_live_imaging.test_images.test_images import linux_penguin_64

if __name__ == '__main__':

    acquisition_control = acc.LiveImagingQt()

    delay_factor = 3.5
    number_of_frames, sleep_time = 64*64, 0.001
    test_detector = tt.TestDetectorInputImage(
            number_of_frames=number_of_frames,
            input_image=linux_penguin_64)
    test_detector.sleep_time.value = 0.001
    test_detector.start_data_listening()
    acquisition_control._comm_medi.port = test_detector.port
    acquisition_control.start_bf_process()
    acquisition_control.resize_scan(64, 64)
    acquisition_control.start_medipix_receiver()
    time.sleep(number_of_frames*sleep_time*delay_factor)

    acquisition_control.cancel_all_processes()
