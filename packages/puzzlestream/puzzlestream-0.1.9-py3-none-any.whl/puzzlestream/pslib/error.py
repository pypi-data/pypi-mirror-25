import numpy as np


def getValueErrorString(value, error, latex=False):
    if np.isinf(error).any():
        value = 0
        exp = 0
        error = 0
    else:
        exp = -int(round(np.log10(error)))
        if int(error * 10**exp) <= 2:
            exp += 1

        value = np.sign(value) * np.ceil(abs(value) * 10**exp) * 10**(-exp)
        error = np.ceil(error * 10**exp) * 10**(-exp)

        if exp <= 0:
            value = int(value)
            error = int(error)

    out = str(value)
    if latex:
        out += r" \pm "
    else:
        out += " +- "
    out += str(error)
    return out
