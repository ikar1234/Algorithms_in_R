from typing import List
from utils import time_func
from collections import deque


@time_func
def pos(x:str) -> List:
    """
    Naive O(n^2*logn) suffix array algorithm
    Problem: memory error for large strings (>100000 chars)
    """
    return sorted([i for i in range(len(x))], key=lambda l: x[l:])



@time_func
def skew(string:str) -> List[int]:
    """
    Skew algorithm, which constructs the suffix array in O(n) time.
    This implementation is better than the naive algorithm for big string(>10000 chars), but still
    lacks performance. Consider converting some parts of the code to C/C++.
    :param string:
    :return:
    """
    n = len(string)
    # append dollar signs such that we can build triples
    string += "$$$$"
    s0 = range(0,n+1,3)
    s1 = list(range(1,n,3))
    s2 = list(range(2,n,3))
    s12 = s1+s2

    # sort all triples
    # TODO: instead of comparing who suffixes, use radix/bucket sort
    # TODO: the result is for example 4223156, which is your new string
    # TODO  iterate until the string contains no duplicate digits
    s12_rank = sorted([l for l in s12],key = lambda l: string[l:])

    # use this to sort make a permutation
    s12_rank = [s12_rank.index(l) for l in s12]
    z = dict(zip(s12,s12_rank))
    # sort S0
    # dollar sign is always smaller, so we put -1
    s0 = sorted([l for l in s0], key=lambda l: (string[l],z.get(l+1,-1)))

    # merge

    c1_s0 = [(string[i],z.get(i+1,-1),i) for i in s0]
    c2_s0 = [(string[i:i+2],z.get(i+2,-1),i) for i in s0]
    s12_sorted = sorted([x for x in s12],key=lambda l: z.get(l))
    c12_s12 = [(string[i:i+2],z.get(i+2,-1),i) if i%3==2 else (string[i],z.get(i+1,-1),i) for i in s12_sorted]

    result = deque()

    dc1_s0 = deque(c1_s0)
    dc2_s0 = deque(c2_s0)
    right = deque(c12_s12)

    # merge both lists
    while dc1_s0 and right:
        if right[0][2]%3==1:
            if dc1_s0[0] > right[0]:
                result.append(right.popleft())
            else:
                result.append(dc1_s0.popleft())
                dc2_s0.popleft()
        elif right[0][2]%3==2:
            if dc2_s0[0] > right[0]:
                result.append(right.popleft())
            else:
                result.append(dc2_s0.popleft())
                dc1_s0.popleft()
    return [x[2] for x in result+dc1_s0+right]


x= 'abababab'
print(skew(x))
