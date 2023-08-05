from puzzlestream.pslib.fit.general import GeneralFit


class MultiplePeakFit(GeneralFit):

    def __init__(self, x, y, e_x=None, e_y=None, p0=None, kind="gauss"):
        self.__kind = kind
        super().__init__(x, y, e_x=e_x, e_y=e_y, func=None)

    def fitFunction(self, x, *args):
        i = 0
        out = 0
        while i < len(args) - 1:
            if self.__kind == "gauss":
                out += gauss(x, *args[i:i + 3])
            elif self.__kind == "lorentz":
                out += lorentz(x, *args[i:i + 3])
            i += 3
        if len(args) > i:
            out += args[i]
        return out
