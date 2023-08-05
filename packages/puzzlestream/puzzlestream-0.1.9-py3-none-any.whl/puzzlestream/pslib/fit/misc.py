import numpy as np
from puzzlestream.pslib.fit.general import GeneralFit


class GaussFit(GeneralFit):

    def fitFunction(self, x, *args):
        out = args[0] * np.exp(-0.5 * ((x - args[2]) / args[1])**2)
        if len(args) > 3:
            out += args[3]
        return out


class LorentzFit(GeneralFit):

    def fitFunction(self, x, *args):
        out = args[0] / (1 + ((x - args[2]) / args[1])**2)

        if len(args) > 3:
            out += args[3]
        return out


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
