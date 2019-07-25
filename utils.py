from time import time
from bitarray import bitarray


def time_func(func):
    """
    Function timing
    :param func:
    :return: result of function
    """
    def wrap(*args,**kwargs):
        t1 = time()
        res = func(*args,**kwargs)
        t2 = time()-t1
        print("Elapsed: ",t2)
        return res
    return wrap


def compress(str:str):
  """ Compress string to binary."""
    d = {'A':0b00,'C':0b01,'G':0b10,'T':0b11}
    return bitarray([d.get(x,0) for x in str.strip().upper()])
