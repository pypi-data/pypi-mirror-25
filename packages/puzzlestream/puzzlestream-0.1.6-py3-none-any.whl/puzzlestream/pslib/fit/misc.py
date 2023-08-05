import numpy as np
from .general import GeneralFit


class GaussFit(GeneralFit):

    def fitFunction(self, x, *args):
        return gauss(x, *args)


class LorentzFit(GeneralFit):

    def fitFunction(self, x, *args):
        return lorentz(x, *args)


class ExponentialFit(GeneralFit):

    def fitFunction(self, x, *args):
        out = args[0] * np.exp(-args[1] * x)
        if len(args) > 2:
            out += args[2]
        return out


class SquareRootFit(GeneralFit):

    def fitFunction(self, x, *args):
        out = []
        for xi in x:
            if xi >= 0:
                out.append(args[0] * sqrt(abs(xi / args[1])))
            else:
                out.append(None)
        return out


class SineFit(GeneralFit):

    def fitFunction(self, x, *args):
        return args[0] * np.sin(args[1] * x + args[2]) + args[3]
