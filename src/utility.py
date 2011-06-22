"""
A set of unrelated functions for performing various usful tasks
"""


def tuple_to_list(intuple):
    tmp = list()
    for x in intuple:
        y = None
        if isinstance(x, tuple):
            y = tuple_to_list(x)
        else:
            y = x
        tmp.append(y)

    print 'tuple_to_list', tmp

    return tmp
