from .poly import PolyFit


class CubicalFit(PolyFit):

    def __init__(self, x, y, e_x=None, e_y=None, nameDict={}):
        super().__init__(x, y, e_x, e_y, deg=3, nameDict=nameDict)

    def calculate(self):
        self.fit()
        self._calcChi2()

        title = "$ " + self._dict["function name"] + "("
        title += self._dict["x name"] + ") "
        if self._dict["y unit"] != "":
            title += " / " + self._dict["y unit"]
        title += " = "
        title = "$ " + \
            self._dict["function name"] + "(" + self._dict["x name"] + ") = "
        title += "(" + getValueErrorString(self.opt[0],
                                           sqrt(self.cov[0, 0]),
                                           latex=True) + ") "
        title += self._dict["x name"] + "^3"
        title += " + (" + getValueErrorString(
            self.opt[1], sqrt(self.cov[1, 1]), latex=True) + ") "
        title += self._dict["x name"] + "^2"
        title += " + (" + getValueErrorString(
            self.opt[2], sqrt(self.cov[2, 2]), latex=True) + ") "
        title += self._dict["x name"]
        title += " + (" + getValueErrorString(
            self.opt[3], sqrt(self.cov[3, 3]), latex=True) + ")$"
        self.__title = title

    @property
    def title(self):
        return self.__title
