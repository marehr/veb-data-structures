# coding=utf8


class word(object):

    """docstring for Word"""

    epsilon = None

    def __init__(self, x, w):
        if isinstance(x, word):
            if w != x.w:
                raise TypeError("word: wordsize of %d (%d) does not match with the given wordsize %d" % (x.x, x.w, w))

            x = x.x

        if x < 0:
            raise TypeError("word: The word must be positive, but a negative number (%d) was given" % (x))

        if x.bit_length() > w:
            raise TypeError("word: The wordsize of %d is %d, but the wordsize can be atmost %d" % (x, x.bit_length(), w))

        self.x = x
        self.w = w

    def __index__(self):
        return self.x

    def __repr__(self):
        w = self.w
        x = self.x
        if self.is_epsilon():
            return "0: ɛ"

        c, i = self.split(w>>1)
        return ('%d: {0:0%db} = <{1:0%db}, {2:0%db}>' % (x, w,c.w,i.w)).format(x,c.x,i.x)

    def __iter__(self):
        yield self.c
        yield self.i

    def __hash__(self):
        return hash((self.x, self.w))

    def __check_wordsize(a,b):
        if(a.w != b.w):
            raise TypeError("word: %s with wordsize %d does not match with %s and a wordsize of %d" % (a, a.w, b, b.w))

    def __lt__(self, other):
        self.__check_wordsize(other)
        return self.x < other.x

    def __eq__(self, other):
        self.__check_wordsize(other)
        return self.x == other.x

    def __gt__(self, other):
        self.__check_wordsize(other)
        return self.x > other.x

    def __le__(self, other):
        self.__check_wordsize(other)
        return self.x <= other.x

    def __ge__(self, other):
        self.__check_wordsize(other)
        return self.x >= other.x

    def __ne__(self, other):
        self.__check_wordsize(other)
        return not self.x == other.x

    def is_epsilon(self):
        return self.w == 0

    def max(self):
        """ Return 2^w - 1, the maximal possible number.
        """
        return (1 << self.w) - 1

    def succ(self):
        """ Return self + 1.
        Will throw an TypeError, if self+1 exceeds self.w bits.
        """
        s = self.x + 1
        return word(s, self.w)

    def pred(self):
        """ Return self + 1.
        Will throw an TypeError, if self-1 is less than zero.
        """
        s = self.x - 1
        return word(s, self.w)

    """ Concats two binary string to one binary string """
    def concat(self, other):
        w = self.w + other.w
        y = (self.x << other.w) + other.x
        return word(y, w)

    def split(self, w):
        wa = w
        wb = self.w-w

        if wa < 0 or wb < 0:
            raise ValueError('word: split %d exceeds wordsize or is less than zero' % w)

        a = self.x >> wb
        b = self.x & ((1 << wb) - 1)
        return [word(a, wa), word(b, wb)]

    def split_fst(self, w):
        return self.split(w)[0]

    def split_snd(self, w):
        return self.split(w)[1]

    def first_bit(self):
        """ Return the first bit of the bit sequence.
        """
        if self.w == 0:
            raise ValueError("word is ɛ")

        msb = self.x >> (self.w-1)
        return msb

    """ Returns the most significant bit """
    def msb(self):
        return self._msb(self.x)

    def _msb(self, diff):
        bits = diff.bit_length()
        return bits

    """
    Is ``other'' a prefix of ``self''?

    self  = s1 s2 s3 ... sN
    other = o1 o2 o3 ... oM

    return True, iff s = o1 ... o_M s_M+1 ... s_N
    """
    def has_prefix(self, other):
        if self.w < other.w:
            return False

        c, i = self.split(other.w)
        return c == other

    """
    Find the longest common prefix of self and other

    self  = s1 s2 s3 ... sN
    other = o1 o2 o3 ... oN

    prefix = s1 s2 ... sK, where o1 = s1, ... oK = sK and oK+1 != sK+1

    Note: self and other must have the same length
    """
    def common_prefix(self, other):
        diff = other.x ^ self.x
        msb = self._msb(diff)
        w = max(other.w - msb, 0)

        p1, s1 = self.split(w)
        return p1


    """
    Find the longest common prefix of self and other

    self  = s1 s2 s3 ... sN
    other = o1 o2 o3 ... oN

    prefix = s1 s2 ... sK, where o1 = s1, ... oK = sK and oK+1 != sK+1
    suffix1 = sK+1 ... sN
    suffix2 = oK+1 ... oN

    return [prefix, suffix1, suffix2]

    Note: self and other must have the same length
    """
    def common_prefix_split(self, other):
        diff = other.x ^ self.x
        msb = self._msb(diff)
        w = max(other.w - msb, 0)

        p1, s1 = self.split(w)
        p2, s2 = other.split(w)

        return [p1, s1, s2]

    """
    Remove the longest common prefix of self and other

    self  = s1 s2 s3 ... sN
    other = o1 o2 o3 ... oM

    prefix = s1 s2 ... sK, where o1 = s1, ... oK = sK and oK+1 != sK+1
                                                 (oK+1 or sK+1 could also be epsilon)
    suffix1 = sK+1 ... sN
    suffix2 = oK+1 ... oM

    return [suffix1, suffix2, prefix]

    Note: self and other can have different lengths
    """
    def remove_prefix(self, other):
        if self.w < other.w:
            suffix1, suffix2, prefix = other.remove_prefix(self)
            return suffix2, suffix1, prefix

        # 00000  10
        # 00100
        c, i = self.split(other.w)

        if c == other:
            return i, word.epsilon, c

        # find in c common prefix
        # 00  000  10
        # 00  100
        prefix, suffix1, suffix2 = c.common_prefix_split(other)
        return suffix1.concat(i), suffix2, prefix

    @property
    def c(self):
        c, i = self.split(self.w>>1)
        return c

    @property
    def i(self):
        c, i = self.split(self.w>>1)
        return i

word.epsilon = word(0, 0)


class compare_word(word):

    def _cmp_split(self, other):
        w = min(self.w, other.w)
        q1, i1 = self.split(w)
        q2, i2 = other.split(w)
        return q1, q2

    def __lt__(self, other):
        q1, q2 = self._cmp_split(other)
        return q1.x < q2.x or (q1.x == q2.x and self.w < other.w)

    def __eq__(self, other):
        return self.x == other.x and self.w == other.w

    def __le__(self, other):
        q1, q2 = self._cmp_split(other)
        return q1.x < q2.x or q1.x == q2.x and self.w <= other.w

    def __gt__(self, other):
        q1, q2 = self._cmp_split(other)
        return q1.x > q2.x or (q1.x == q2.x and self.w > other.w)

    def __ge__(self, other):
        q1, q2 = self._cmp_split(other)
        return q1.x > q2.x or q1.x == q2.x and self.w >= other.w

    def __ne__(self, other):
        return self.x != other.x or self.w != other.w
