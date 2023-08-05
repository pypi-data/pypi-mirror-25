from puzzlestream.pslib.fit.poly import PolyFit


class ParabolaFit(PolyFit):

    def __init__(self, x, y, e_x=None, e_y=None, nameDict={}):
        super().__init__(x, y, e_x, e_y, deg=2,
                         usetex=usetex, nameDict=nameDict)

    def calculate(self):
        self.fit()
        self._calcChi2()

        title = "$ " + \
            self._dict["function name"] + "(" + self._dict["x name"] + ") = "
        title += "(" + getValueErrorString(self.opt[0],
                                           sqrt(self.cov[0, 0]),
                                           latex=True) + ") x^2"
        title += " + (" + getValueErrorString(
            self.opt[1], sqrt(self.cov[1, 1]), latex=True) + ") x"
        title += " + (" + getValueErrorString(
            self.opt[2], sqrt(self.cov[2, 2]), latex=True) + ")$"
        self.__title = title

    @property
    def title(self):
        return self.__title
