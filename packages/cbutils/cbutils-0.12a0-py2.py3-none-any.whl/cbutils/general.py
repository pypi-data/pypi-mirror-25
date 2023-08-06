

def split(it, sz):
    """
    Split a iterable in N parts each of len = sz. Last chunk maybe will have len < sz.

    Parameters
    ----------
    it: iterable
    sz: int

    Returns
    -------
    list of iterable

    """

    out = []
    last = 0.0

    while last < len(it):
        out.append(it[int(last):int(last + sz)])
        last += sz

    return out