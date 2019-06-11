from time import time
import re
import numpy as np
from collections import Counter


def bwt(s):
    table = [s[i:] + s[:i] for i in range(len(s))]
    # Sorted table
    table_sorted = table.copy()
    table_sorted.sort()
    indexlist = []
    for t in table_sorted:
        index1 = table.index(t)
        index1 = index1+1 if index1 < len(s)-1 else 0
        index2 = table_sorted.index(table[index1])
        indexlist.append(index2)
    r = ''.join([row[-1] for row in table_sorted])
    return r, indexlist


def ibwt(r,indexlist):
    """Inverse BWT"""
    s = ''
    x = indexlist[0]
    for _ in r:
        s = s + r[x]
        x = indexlist[x]
    return s


def rle(string):
    new = string[0]+''.join([string[x] if string[x-1]==string[x] else '_'+string[x] for x in range(1,len(string)) ])
    new1 = new.split('_')
    new2 = ''.join([str(len(x))+x[0] if len(x)>2 else ''.join(x) for x in new1])
    print(new2)


x="TGATGCATCATGCAT$"
# print(rle(bwt(x)[0]))


def rank(string):
    p = posfast(string)
    r = np.zeros(6,dtype=np.int32)
    for i in range(len(string)+1):
        r[p[i]] = i
    return r

# Much faster and shorter version
bwt_from_pos = lambda string: [string[x-1] for x in posfast(string)]

def search_in_bwt(p,t):
    """Exact search in BWT"""
    p_rev= p[::-1]
    last = bwt_from_pos(t)
    pos = posfast(t)
    count = Counter(last)
    c_array = {x:0 for x in count.keys()}
    for x in count.keys():
        for y in count.keys():
            if y<x:
                c_array[x] += count.get(y,0)
    occ_array = {x:[0] for x in count.keys()}
    # first letter in last-array has occ. of 1 in the first position
    occ_array.get(last[0])[0] +=1
    for x in range(1,len(last)):
        for y in occ_array.keys():
            if last[x]==y:
                occ_array[y].append(occ_array[y][max(0,x-1)]+1)
            else:
                occ_array[y].append(occ_array[y][max(0,x - 1)])
    l = 0
    r = len(last)-1
    c = 0
    while c<len(p):
        try:
            if l==0:
                l = c_array[p_rev[c]]
            else:
                l = c_array[p_rev[c]] + occ_array.get(p_rev[c])[l-1]
            r = c_array[p_rev[c]] + occ_array.get(p_rev[c])[r] -1

        except KeyError:
            return "Pattern not found"
        if l>r:
            return "Pattern not found"
        c+=1
    return [pos[i] for i in range(l,r+1)]


# Naive suffix array - needed for finding positions in original text
posfast = lambda string: tuple(sorted(range(len(string)), key=lambda x: string[x:]))

if __name__ == '__main__':
    t1 = time()
    print(search_in_bwt("SS", "MISSISSIPPI$"*3000))
    t2 = time()
    print("Time 2",t2-t1)

