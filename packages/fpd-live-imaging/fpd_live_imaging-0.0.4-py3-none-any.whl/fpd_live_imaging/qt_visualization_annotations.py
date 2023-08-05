import multiprocessing as mp


class Circle(object):

    def __init__(self, x, y, r, name=''):
        self._x = mp.Value('f', x)
        self._y = mp.Value('f', y)
        self._r = mp.Value('f', r)
        self.name = name
        self._annotation_type = 'circle'

    @property
    def x(self):
        return self._x.value

    @x.setter
    def x(self, x):
        self._x.value = x

    @property
    def y(self):
        return self._y.value

    @y.setter
    def y(self, y):
        self._y.value = y

    @property
    def r(self):
        return self._r.value

    @r.setter
    def r(self, r):
        self._r.value = r
