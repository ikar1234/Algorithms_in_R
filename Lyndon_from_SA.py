import numpy as np

# Suffix array
posfast = lambda string: tuple(sorted(range(len(string)), key=lambda x: string[x:]))

# Suffix permutation array
def rank(string):
    p = posfast(string)
    r = np.zeros(len(string),dtype=np.int32)
    for i in range(len(string)):
        r[p[i]] = i
    return r


def lyndon_from_sa(x):
    """
    :param x: input string
    :return: starting positions the factors
    """
    # use suffix permutation array (inverse of SA) for fast comparison of suffixes
    r = rank(x)
    p = posfast(x)
    # first factor
    f = r[0]
    l = [p[f]] # =0
    for i in r:
        if i<f:
            f=i
            l.append(p[f])
    # starting positions of the factors
    return l
