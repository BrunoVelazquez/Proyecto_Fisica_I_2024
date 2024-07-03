import numpy as np

def fill(arr, maxlength):
    return np.append(arr, [arr[-1]] * (maxlength - len(arr)))