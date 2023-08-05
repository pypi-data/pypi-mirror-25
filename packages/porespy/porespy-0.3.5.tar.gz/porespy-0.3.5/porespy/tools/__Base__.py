from porespy.metrics import porosity


class Base():

    def __init__(self, im):
        self._im = im
        self._phi = None

    @property
    def porosity(self):
        if self._phi is None:
            self._phi = porosity(self._im)
        return self._phi

    @property
    def im(self):
        return self._im

    @property
    def shape(self):
        return self.im.shape

    @property
    def ndim(self):
        return self.im.ndim

    @property
    def xdim(self):
        return self.im.shape[0]

    @property
    def ydim(self):
        return self.im.shape[1]

    @property
    def zdim(self):
        if self.ndim == 3:
            return self.im.shape[2]
