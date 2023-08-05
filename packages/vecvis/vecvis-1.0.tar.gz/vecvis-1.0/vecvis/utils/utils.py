""" doc
"""


def add_items(to_list, from_list):
    """ doc
    """
    new_list = []
    items_added = []
    i, j = 0, 0
    len_to = len(to_list)
    len_from = len(from_list)
    while i < len_to and j < len_from:
        if to_list[i] > from_list[j]:
            new_list.append(to_list[i])
            i = i + 1
        elif to_list[i] == from_list[j]:
            new_list.append(from_list[j])
            i = i + 1
            j = j + 1
        else:
            new_list.append(from_list[j])
            items_added.append(from_list[j])
            j = j + 1
    while i < len_to:
        new_list.append(to_list[i])
        i = i + 1
    while j < len_from:
        new_list.append(from_list[j])
        items_added.append(from_list[j])
        j = j + 1
    return new_list, items_added


def remove_from_list(from_list, remove_list):
    """ doc
    """
    len_from = len(from_list)
    len_remove = len(remove_list)
    new_list = []
    removed = []
    i, j = 0, 0
    while i < len_from and j < len_remove:
        itema = from_list[i]
        itemb = remove_list[j]
        if from_list[i] < remove_list[j]:
            j = j + 1
        elif from_list[i] == remove_list[j]:
            removed.append(remove_list[j])
            j = j + 1
            i = i + 1
        else:  # they are not equal and the next item in remove_list is greater than the nex item in from_list
            new_list.append(from_list[i])
            i = i + 1
    while i < len_from:
        new_list.append(from_list[i])
        i = i + 1
    return new_list, removed


def calculate_vectors_min_max(vectors):
    """ Calculates the min an max value per dimensions """
    if not vectors:
        return None
    dimensions = len(next(iter(vectors)))
    ret = []
    for i in range(dimensions):
        min_value = next(iter(vectors))[i]
        max_value = min_value
        for vector in vectors:
            min_value = min(min_value, vector[i])
            max_value = max(max_value, vector[i])
        ret.append((min_value, max_value))
    return ret
