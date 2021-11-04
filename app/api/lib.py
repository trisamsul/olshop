# Libraries


def pagination(data, n, page):
    start = (page * n)
    end = start + n

    return data[start: end]
