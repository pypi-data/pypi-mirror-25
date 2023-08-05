# Author: Michal Ciesielczyk
# Licence: MIT


def range_without(start, stop, without, step=1, reverse=False):
    """Return evenly spaced values within a given interval (from start to stop)
    omitting the specified value or list of values.

    :param start: the value of the start parameter
    :type start: int
    :param stop: the value of the stop parameter
    :type stop: int
    :param without: values to be omitted
    :type without: int or list of ints
    :param step: the value of the step parameter
    :type step: int
    :param reverse: indicates wheter the resulting range should be in reversed
        order
    :type reverse: boolean
    :return: range without the specified values
    :rtype: generator object
    """
    skip = 1
    if reverse:
        start, stop = (stop - 1), (start - 1)
        step *= -1
        skip *= -1
    if isinstance(without, list):
        without = sorted(without)
        if reverse:
            without = without[::-1]
        arange = []
        for w in without:
            arange.append(range(start, w, step))
            start = w + skip
        arange.append(range(start, stop, step))
        return (i for j in arange for i in j)
    else:
        a = range(start, without, step)
        b = range(without + skip, stop, step)
        return (i for j in (a, b) for i in j)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def check_type(var_name, var, expected_types):
    if isinstance(expected_types, type):
        if not isinstance(var, expected_types):
            raise TypeError("{} variable must be type of {}, not {}.".format(
                var_name, expected_types.__name__, type(var)))
    elif isinstance(expected_types, tuple):
        if not isinstance(var, expected_types):
            types_str = ', '.join(et.__name__ for et in expected_types)
            types_str = ' or '.join(types_str.rsplit(', ', maxsplit=1))
            raise TypeError("{} variable must be type of {}, not {}."
                            .format(var_name, types_str, type(var)))
    else:
        raise TypeError("expected_types argument must be "
                        "a type or tuple of types")


def is_sequence(seq, expected_element_type=None):
    import collections
    if not isinstance(seq, collections.Sequence):
        return False
    if isinstance(expected_element_type, (type, tuple)):
        return all(isinstance(e, expected_element_type) for e in seq)
    else:
        raise TypeError("element_type argument must be "
                        "a type or tuple of types")
