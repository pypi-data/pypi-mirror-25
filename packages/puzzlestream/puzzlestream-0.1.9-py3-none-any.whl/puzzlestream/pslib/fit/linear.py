from puzzlestream.pslib.fit.fit import Fit
import numpy as np


class LinearFit(Fit):

    def __init__(self, x, y, e_x=None, e_y=None, nameDict={}):
        self._dict = nameDict
        self.__setDefaultNames()
        super().__init__(x, y, e_x, e_y)

        xLabel = "$" + self._dict["x name"]
        if self._dict["x unit"] != "":
            xLabel += " / " + self._dict["x unit"]
        xLabel += "$"
        self.__xlabel = xLabel

        yLabel = "$" + self._dict["function name"]
        yLabel += "(" + self._dict["x name"] + ")"
        if self._dict["y unit"] != "":
            yLabel += " / " + self._dict["y unit"]
        yLabel += "$"
        self.__ylabel = yLabel

    def __setDefaultNames(self):
        defaults = {"function name": "f", "x name": "x",
                    "x unit": "", "y unit": ""}
        for key in defaults:
            if key not in self._dict:
                self._dict[key] = defaults[key]

    def _getXWithUnit(self):
        if self._dict["x unit"] == "":
            return self._dict["x name"]
        return (r"\frac{" + self._dict["x name"] + "}{" + self._dict["x unit"] + "}")

    def calculate(self):
        self.fit()
        self._calcChi2()

        title = "$ " + self._dict["function name"] + "("
        title += self._dict["x name"] + ") "
        if self._dict["y unit"] != "":
            title += " / " + self._dict["y unit"]
        title += " = "
        title += "(" + getValueErrorString(self.opt[0],
                                           sqrt(self.cov[0, 0]),
                                           latex=True) + ") "
        title += self._getXWithUnit()
        title += " + (" + getValueErrorString(
            self.opt[1], sqrt(self.cov[1, 1]), latex=True) + ")" + "$"
        self.__title = title

    def _runFit(self):
        if isinstance(self.e_x, collections.Iterable):
            a, ea, b, eb, corr = self.__linearRegression_xy(
                self.xc, self.yc, self.e_xc, self.e_yc)
        else:
            a, ea, b, eb, corr = self.__linearRegression(
                self.xc, self.yc, self.e_yc)
        self.opt = np.array([a, b])
        self.cov = np.array([[ea**2, corr**2], [corr**2, eb**2]])

    def fitFunction(self, x, *args):
        return args[0] * x + args[1]

    @property
    def xlabel(self):
        return self.__xlabel

    @property
    def ylabel(self):
        return self.__ylabel

    @property
    def title(self):
        return self.__title

    def __linearRegression(self, x, y, ey):
        """
        Lineare Regression.

        Parameters
        ----------
        x : array_like
            x-Werte der Datenpunkte
        y : array_like
            y-Werte der Datenpunkte
        ey : array_like
            Fehler auf die y-Werte der Datenpunkte

        Diese Funktion benoetigt als Argumente drei Listen:
        x-Werte, y-Werte sowie eine mit den Fehlern der y-Werte.
        Sie fittet eine Gerade an die Werte und gibt die
        Steigung a und y-Achsenverschiebung b mit Fehlern
        sowie das chi^2 und die Korrelation von a und b
        als Liste aus in der Reihenfolge
        [a, ea, b, eb, chiq, cov].
        """

        s = np.sum(1. / ey**2)
        sx = np.sum(x / ey**2)
        sy = np.sum(y / ey**2)
        sxx = np.sum(x**2 / ey**2)
        sxy = np.sum(x * y / ey**2)
        delta = s * sxx - sx * sx
        b = (sxx * sy - sx * sxy) / delta
        a = (s * sxy - sx * sy) / delta
        eb = np.sqrt(sxx / delta)
        ea = np.sqrt(s / delta)
        cov = -sx / delta
        corr = cov / (ea * eb)

        return a, ea, b, eb, corr

    def __linearRegression_xy(self, x, y, ex, ey):
        """
        Lineare Regression mit Fehlern in x und y (approximativ).

        Parameters
        ----------
        x : array_like
            x-Werte der Datenpunkte
        y : array_like
            y-Werte der Datenpunkte
        ex : array_like
            Fehler auf die x-Werte der Datenpunkte
        ey : array_like
            Fehler auf die y-Werte der Datenpunkte

        Diese Funktion benoetigt als Argumente vier Listen:
        x-Werte, y-Werte sowie jeweils eine mit den Fehlern der x-
        und y-Werte.
        Sie fittet eine Gerade an die Werte und gibt die
        Steigung a und y-Achsenverschiebung b mit Fehlern
        sowie das chi^2 und die Korrelation von a und b
        als Liste aus in der Reihenfolge
        [a, ea, b, eb, chiq, cov].
        """

        a = 0.
        for i in range(3):
            exy = np.sqrt(ey**2 + (a * ex)**2)
            a = self.__linearRegression(x, y, exy)[0]
        exy = np.sqrt(ey**2 + (a * ex)**2)

        return self.__linearRegression(x, y, exy)
