from setuptools import setup, find_packages
setup(
        name = 'fpd_live_imaging',
        packages = [
            'fpd_live_imaging',
            'fpd_live_imaging.test_images',
            'fpd_live_imaging.tests',
            'fpd_live_imaging.sample_scripts',
            ],
        version = '0.0.4',
        author = 'Magnus Nord',
        author_email = 'magnunor@gmail.com',
        license = 'GPL v3',
        url = 'https://fast_pixelated_detectors.gitlab.io/fpd_live_imaging/',
        download_url = 'https://gitlab.com/fast_pixelated_detectors/fpd_live_imaging/repository/master/archive.tar?ref=0.0.4',
        description = 'Library for live processing and visualization of STEM data acquired using a fast pixelated detector',
        keywords = [
            'STEM',
            'visualization',
            'microscopy',
            ],
        install_requires = [
            'h5py',
            'scipy',
            'numpy',
            'psutil',
            'pyqt5',
            ],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Science/Research',
            'Programming Language :: Python :: 3',
            ],
        package_data = {
            'fpd_live_imaging.test_images': [
                'linux_penguin.npz']
            }
)
