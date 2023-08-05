from .fit import Fit


class PolyFit(Fit):

    def __init__(self, x, y, e_x=None, e_y=None, nameDict={}):
        self._dict = nameDict
        self.__setDefaultNames()
        self.__deg = deg

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

    def _runFit(self):
        self.opt, self.cov = np.polyfit(self.xc, self.yc, self.__deg, cov=True)

    def fitFunction(self, x, *args):
        return np.polyval(args, x)

    @property
    def xlabel(self):
        return self.__xlabel

    @property
    def ylabel(self):
        return self.__ylabel
