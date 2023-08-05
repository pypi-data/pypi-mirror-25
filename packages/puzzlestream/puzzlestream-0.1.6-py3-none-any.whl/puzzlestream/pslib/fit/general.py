from .fit import Fit


class GeneralFit(Fit):

    def __init__(self, x, y, e_x=None, e_y=None, func=None, p0=None):
        if func is not None:
            self.fitFunction = func
        self.__p0 = p0
        super().__init__(x, y, e_x, e_y)

    def setStartValues(self, p0):
        self.__p0 = p0

    def setFitFunction(self, function):
        self.fitFunction = function

    def _runFit(self):
        self.opt, self.cov = curve_fit(self.fitFunction, self.xc, self.yc,
                                       self.__p0, sigma=self.e_yc,
                                       absolute_sigma=True)
