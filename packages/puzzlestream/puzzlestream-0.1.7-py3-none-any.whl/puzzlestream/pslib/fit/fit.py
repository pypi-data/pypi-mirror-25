import numpy as np
from scipy.optimize import curve_fit
import collections


class Fit:

    def __init__(self, x, y, e_x=None, e_y=None):
        self.__x, self.__y, self.__e_x, self.__e_y = (x, y, e_x, e_y)
        self.__xc, self.__yc, self.__e_xc, self.__e_yc = (x, y, e_x, e_y)
        self.__opt = None
        self.__cov = None
        self.__chi2 = None
        self.__lowCut = None
        self.__highCut = None

    def fit(self):
        self._runFit()
        self._calcChi2()

    def fitFunction(self):
        pass

    def fitFunctionFitted(self, x):
        return self.fitFunction(x, *self.opt)

    def _runFit(self):
        pass

    def _calcChi2(self):
        if isinstance(self.__e_y, collections.Iterable):
            yFit = self.fitFunction(self.__xc, *self.__opt)
            self.__chi2 = np.sum(((yFit - self.__yc) / self.__e_yc)**2)
            self.__chi2 /= (len(self.__xc) - len(self.__opt))
        else:
            self.__chi2 = -1

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def e_x(self):
        return self.__e_x

    @property
    def e_y(self):
        return self.__e_y

    @property
    def xc(self):
        return self.__xc

    @property
    def yc(self):
        return self.__yc

    @property
    def e_xc(self):
        return self.__e_xc

    @property
    def e_yc(self):
        return self.__e_yc

    def __getXIndex(self, value):
        return np.argmin(np.abs(self.__x - value))

    def setLowerCut(self, cut):
        lowerI = self.__getXIndex(cut)
        self.__lowCut = lowerI
        if self.__highCut is not None:
            upperI = self.__highCut
            self.__cut(lowerI, upperI)
        else:
            self.__cut(lowerI, None)

    def setUpperCut(self, cut):
        upperI = self.__getXIndex(cut) + 1
        self.__highCut = upperI
        if self.__lowCut is not None:
            lowerI = self.__lowCut
            self.__cut(lowerI, upperI)
        else:
            self.__cut(None, upperI)

    def setCuts(self, lower, upper):
        lowerI = self.__getXIndex(lower)
        upperI = self.__getXIndex(upper)
        self.__lowCut = lowerI
        self.__highCut = upperI + 1
        self.__cut(lowerI, upperI)

    def __cut(self, lower=None, upper=None):
        if lower is not None and upper is not None:
            self.__xc = self.__x[lower:upper]
            self.__yc = self.__y[lower:upper]
            if self.__e_x is not None:
                self.__e_xc = self.__e_x[lower:upper]
            if self.__e_y is not None:
                self.__e_yc = self.__e_y[lower:upper]
        elif lower is None:
            self.__xc = self.__x[:upper]
            self.__yc = self.__y[:upper]
            if self.__e_x is not None:
                self.__e_xc = self.__e_x[:upper]
            if self.__e_y is not None:
                self.__e_yc = self.__e_y[:upper]
        else:
            self.__xc = self.__x[lower:]
            self.__yc = self.__y[lower:]
            if self.__e_x is not None:
                self.__e_xc = self.__e_x[lower:]
            if self.__e_y is not None:
                self.__e_yc = self.__e_y[lower:]

    @property
    def opt(self):
        return self.__opt

    @opt.setter
    def opt(self, value):
        self.__opt = value

    @property
    def cov(self):
        return self.__cov

    @cov.setter
    def cov(self, value):
        self.__cov = value

    def getErrorString(self, index, latex=False):
        return getValueErrorString(self.opt[index],
                                   sqrt(self.cov[index, index]), latex)

    def getAllErrorStrings(self, latex=False):
        return [getValueErrorString(self.opt[i], sqrt(self.cov[i, i]),
                                    latex) for i in range(len(self.opt))]

    @property
    def chi2(self):
        return round(self.__chi2, 2)

    @chi2.setter
    def chi2(self, chi2):
        self.__chi2 = chi2

    @property
    def markFitted(self):
        if self.__lowCut is None and self.__highCut is None:
            markFitted = None
        else:
            if self.__lowCut is None:
                lowCut = 0
            else:
                lowCut = self.__lowCut
            if self.__highCut is None:
                highCut = len(self.__x)
            else:
                highCut = self.__highCut
            markFitted = np.arange(lowCut, highCut)

        return markFitted
