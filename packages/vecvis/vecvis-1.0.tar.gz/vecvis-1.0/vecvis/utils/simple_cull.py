""" doc
"""


def simple_cull(vectors, minimize):
    non_dominated_points = []
    dominated_points = []
    vectors = vectors.copy()
    m = len(vectors)
    orderfactor = []
    for b in minimize:
        if b:
            orderfactor.append(-1)
        else:
            orderfactor.append(1)
    vectors.sort(reverse=True, key = lambda x:[orderfactor[i]*x[i] for i in range(len(x))])
    for i in range(m):
        if vectors[i] is not None:
            vec = vectors[i]
            non_dominated_points.append(vec)
            vectors[i] = None
            for j in range(i + 1, len(vectors)):
                if vectors[j] is None:
                    continue
                if dominates(vec, vectors[j], minimize):
                    dominated_points.append(vectors[j])
                    vectors[j] = None
    return non_dominated_points, dominated_points

def dominates(vec1, vec2, minimize):
    """ if vec1 is nowhere smaller then vec2, it has to be equal
    and in at least one dimension its bigger because there are no duplicates
    """
    for i in range(0, len(vec1)):   # O(d - 1)
        if not minimize[i]:
            if vec1[i] < vec2[i]:       # O(1)
                return False
        else:
            if vec1[i] > vec2[i]:
                return False
    return True
