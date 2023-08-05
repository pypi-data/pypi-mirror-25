import numpy as np
import os

my_path = os.path.dirname(__file__)

filename = os.path.join(my_path, "linux_penguin.npz")

linux_penguin_512 = np.load(filename)['s512']
linux_penguin_256 = np.load(filename)['s256']
linux_penguin_128 = np.load(filename)['s128']
linux_penguin_64 = np.load(filename)['s64']
linux_penguin_32 = np.load(filename)['s32']
linux_penguin_16 = np.load(filename)['s16']
