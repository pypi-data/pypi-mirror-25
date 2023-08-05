
def unpack(d, *keys):
    return tuple(d[k] for k in keys)


if __name__ == '__main__':
    c = {
        'a': 11,
        'b': 22
    }
    a, b = unpack(c, 'a', 'b')
    print(a, b)
