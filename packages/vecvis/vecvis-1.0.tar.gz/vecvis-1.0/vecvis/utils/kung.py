# -*- coding: utf-8 -*-
'''
Created on 31.07.2017
https://www.cs.cinvestav.mx/~emoobook/nodom/nondominated.html
@author: Mo
'''
def get_nondominated_vectors(vectors):
    """ Vektoren absteigend sortieren
        [groß,....,klein]
    """
    list = sorted(vectors, reverse=True) # O( n*log(n) * d) <= O( n*log(n)^d-2
    # solve recursive
    kung(list)


def kung(vectors):
    """ vectors = ordered list
    """
    m = len(vectors)
    # if there is only one vector left, return it
    if m == 1:
        return vectors
    #[left,right]
    left = vectors[0: m//2]
    right = vectors[m//2: m]

    nleft = kung(left)
    nright = kung(right)

    # left garanteed undominated
    return merge(nleft, nright)

def merge(left, right):
    """left garanteed undominated"""
    for candidate in right:                 # O(n/2)
        dominated = False
        for vec in left:                    # O(n/2)
            if dominates(vec, candidate):   # O(d - 1)
                dominated = True
                break
        if not dominated:
            left.append(candidate)          # O(1)
    return left

def dominates(vec1, vec2):
    """ if vec1 is nowhere smaller then vec2, it has to be equal
    and in at least one dimension its bigger because there are no duplicates
    """
    for i in range(0, len(vec1)):   # O(d - 1)
        if vec1[i] < vec2[i]:       # O(1)
            return False
    return True

def dominates_not(vec1, vec2):
    """ returns true if not vec1 dominates vec2 """
    for i in range(0, len(vec1)):
        if vec1[i] < vec2[i]:
            return True
    return False
l = [(1,7,9),(2,10,30), (3,5,20), (7,0,10), (7,0,6), (7,0,15)]
l.sort(reverse=True)
print(l)
print(kung(l))
