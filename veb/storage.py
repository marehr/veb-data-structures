

class HashArray(dict):

    def __init__(self, w):
        super(HashArray, self).__init__()
        self.w = w

    def __missing__(self, key):
        return None

    def values(self):
        return super(HashArray, self).values()


class Array(list):

    def __init__(self, w):
        w_half = w >> 1
        size = (1 << w_half)
        xs = size * [None]

        super(Array, self).__init__(xs)

    def values(self):
        return filter(None, self)
