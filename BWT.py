from time import time
import re
import numpy as np
from collections import Counter


def bwt(s):
    """Apply Burrows-Wheeler transform to input string. Not indicated by a unique byte but use index list"""
    # Table of rotations of string
    table = [s[i:] + s[:i] for i in range(len(s))]
    # Sorted table
    table_sorted = table.copy()
    table_sorted.sort()
    # Get index list of ((every string in sorted table)'s next string in unsorted table)'s index in sorted table
    indexlist = []
    for t in table_sorted:
        index1 = table.index(t)
        index1 = index1+1 if index1 < len(s)-1 else 0
        index2 = table_sorted.index(table[index1])
        indexlist.append(index2)
    r = ''.join([row[-1] for row in table_sorted])
    return r, indexlist


def ibwt(r,indexlist):
    """Inverse Burrows-Wheeler transform. Not indicated by a unique byte but use index list"""
    s = ''
    x = indexlist[0]
    for _ in r:
        s = s + r[x]
        x = indexlist[x]
    return s


def rle(string):
    """ Is actually very good!"""
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


def search_in_bwt(p,t):
    p_rev= p[::-1]
    last = bwt(t)[0]
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


# Suffix array


def maximal_prefix(a,b):
    if len(a)==0 or len(b)==0:
        return 0
    c = 0
    while c<len(a) and c<len(b) and a[c]==b[c]:
        c+=1
    return c


posfast = lambda string: tuple(sorted(range(len(string)), key=lambda x: string[x:]))


# Kasai O(n) algorithm
def build_lcp_array(string, suffix_array):
    inverse_suffix_array = np.full(len(suffix_array),-1)
    for i, suffix in enumerate(suffix_array):
        inverse_suffix_array[suffix] = i
    lcp_array = np.full(len(suffix_array),-1)
    lcp = 0
    for i in inverse_suffix_array:
        if i > 0:
            i0, i1 = suffix_array[i], suffix_array[i-1]
            while max(i0,i1)+lcp < len(string) and string[i0+lcp] == string[i1+lcp]:
                lcp += 1
            lcp_array[i] = lcp
            lcp = max(0, lcp - 1)
        else:
            lcp = 0
    return tuple(lcp_array)


# t1 = time()
# print(posfast("acgttgtacgtt"*1000))
# print("Time 2: ",time()-t1)

# t1 = time()
# x = "attqwweattyuiooattdfghjattklnmattzxcvattqlvpatt"*400
# x = "CABACBCBACABCABCACBC$"
# print(build_lcp_array(x,posfast(x)))
# print(posfast("GCATAAATAAA$"))

if __name__ == '__main__':
    print(search_in_bwt("SS", "MISSISSIPPI$"))
