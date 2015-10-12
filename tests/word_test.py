import unittest
from word import word

class wordTest(unittest.TestCase):

    def test_create(self):
        # test normal creation
        a = word(15, 4)
        self.assertIsInstance(a, word)

        # test normal creation with a word as argument
        a = word(a, 4)
        self.assertIsInstance(a, word)

        # 4095 needs 12 bits, but it can only hold 8 bits
        with self.assertRaises(TypeError):
            a = word(4095, 8)

        # you can't create a word with a word, which does not matches the
        # wordsize
        with self.assertRaises(TypeError):
            a = word(15, 4)
            a = word(a, 8)

    def test_hash(self):
        a = word(12, 8)
        b = word(12, 8)
        hashmap = {}

        hashmap[a] = False
        hashmap[b] = True

        self.assertEqual(hash(a), hash(b))
        self.assertTrue(hashmap[a], 'a should hash to the same as b location')
        self.assertTrue(hashmap[b], 'b should hash to the same as a location')

    def test_eq(self):
        a = word(12, 8)
        b = word(12, 8)
        self.assertTrue(a == b, "12 == 12 == true")

        a = word(12, 8)
        b = word(13, 8)
        self.assertFalse(a == b, "12 == 13 == false")

        with self.assertRaises(TypeError):
            a = word(12, 4)
            b = word(12, 8)
            a == b

    def test_neq(self):
        a = word(12, 8)
        b = word(12, 8)
        self.assertFalse(a != b, "12 != 12 == false")

        a = word(12, 8)
        b = word(13, 8)
        self.assertTrue(a != b, "12 != 13 == true")

        with self.assertRaises(TypeError):
            a = word(12, 4)
            b = word(12, 8)
            a != b

    def test_lt(self):
        a = word(12, 8)
        b = word(15, 8)
        self.assertTrue(a < b, "12 < 15 == true")

        a = word(21, 8)
        b = word(1, 8)
        self.assertFalse(a < b, "21 < 1 == False")

        with self.assertRaises(TypeError):
            a = word(12, 4)
            b = word(15, 8)
            a < b

    def test_le(self):
        a = word(12, 8)
        b = word(15, 8)
        self.assertTrue(a <= b, "12 <= 15 == true")

        a = word(21, 8)
        b = word(1, 8)
        self.assertFalse(a <= b, "21 <= 1 == False")

        a = word(12, 8)
        b = word(12, 8)
        self.assertTrue(a <= b, "12 <= 12 == true")

        with self.assertRaises(TypeError):
            a = word(12, 4)
            b = word(12, 8)
            a <= b

    def test_gt(self):
        a = word(12, 8)
        b = word(15, 8)
        self.assertTrue(b > a, "15 > 12 == true")

        a = word(21, 8)
        b = word(1, 8)
        self.assertFalse(b > a, "1 > 21 == False")

        with self.assertRaises(TypeError):
            a = word(12, 4)
            b = word(15, 8)
            b > a

    def test_ge(self):
        a = word(12, 8)
        b = word(15, 8)
        self.assertTrue(b >= a, "15 >= 12 == true")

        a = word(21, 8)
        b = word(1, 8)
        self.assertFalse(b >= a, "1 >= 21 == False")

        a = word(12, 8)
        b = word(12, 8)
        self.assertTrue(b >= a, "12 >= 12 == true")

        with self.assertRaises(TypeError):
            a = word(12, 4)
            b = word(12, 8)
            b >= a

    def test_concat(self):
        a = word(12, 6)
        b = word(15, 4)
        c = a.concat(b)
        d = b.concat(a)

        self.assertEqual("0b1100", bin(a.x))
        self.assertEqual("0b1111", bin(b.x))

        self.assertEqual("0b11001111", bin(c.x))
        self.assertEqual("0b1111001100", bin(d.x))

        a = word(12, 6)
        b = word(0, 0)
        c = a.concat(b)
        d = b.concat(a)

        self.assertEqual("0b1100", bin(a.x))
        self.assertEqual("0b0", bin(b.x))

        self.assertEqual("0b1100", bin(c.x))
        self.assertEqual("0b1100", bin(d.x))

    def test_succ(self):
        self.assertEqual(word(0, 2).succ(), word(1, 2))
        self.assertEqual(word(1, 2).succ(), word(2, 2))
        self.assertEqual(word(2, 2).succ(), word(3, 2))

        with self.assertRaises(TypeError):
            word(3, 2).succ()

    def test_pred(self):
        self.assertEqual(word(3, 2).pred(), word(2, 2))
        self.assertEqual(word(2, 2).pred(), word(1, 2))
        self.assertEqual(word(1, 2).pred(), word(0, 2))

        with self.assertRaises(TypeError):
            word(0, 2).pred()

    def test_split(self):
        # a = 1011
        a = word(11, 4)
        b,c = a.split(2)
        self.assertEqual("0b1011", bin(a.x))
        self.assertEqual("0b10", bin(b.x))
        self.assertEqual("0b11", bin(c.x))

        self.assertEqual(4, a.w)
        self.assertEqual(2, b.w)
        self.assertEqual(2, c.w)

        # a = 101
        a = word(5, 3)
        b,c = a.split(2)
        self.assertEqual("0b101", bin(a.x))
        self.assertEqual("0b10", bin(b.x))
        self.assertEqual("0b1", bin(c.x))

        self.assertEqual(3, a.w)
        self.assertEqual(2, b.w)
        self.assertEqual(1, c.w)

        # a = 010
        a = word(2, 3)
        b,c = a.split(1)

        self.assertEqual("0b10", bin(a.x))
        self.assertEqual("0b0", bin(b.x))
        self.assertEqual("0b10", bin(c.x))

        self.assertEqual(3, a.w)
        self.assertEqual(1, b.w)
        self.assertEqual(2, c.w)

        # edge case, split = 0
        a = word(2, 3)
        b,c = a.split(0)

        self.assertEqual("0b10", bin(a.x))
        self.assertEqual("0b0", bin(b.x))
        self.assertEqual("0b10", bin(c.x))

        self.assertEqual(3, a.w)
        self.assertEqual(0, b.w)
        self.assertEqual(3, c.w)

        # edge case, split = 3
        a = word(2, 3)
        b,c = a.split(3)

        self.assertEqual("0b10", bin(a.x))
        self.assertEqual("0b10", bin(b.x))
        self.assertEqual("0b0", bin(c.x))

        self.assertEqual(3, a.w)
        self.assertEqual(3, b.w)
        self.assertEqual(0, c.w)

        # edge case, split > 3
        a = word(2, 3)
        with self.assertRaises(ValueError):
            a.split(4)

        # edge case, split < 0
        a = word(2, 3)
        with self.assertRaises(ValueError):
            a.split(-17)

    "Tests that splitting and concatenating is idempotent"
    def test_split_concat(self):
        xs = [(w, x) for w in range(4) for x in range(8)]

        for w, x in xs:
            a = word(x, 3)
            c, i = a.split(w)
            b = c.concat(i)

            self.assertEqual(a, b)

    def msb(self):
        # a = 0000 1100 = 12
        a = word(12, 8)
        result = a.msb()

        self.assertEqual(result, 4)

        # a = 0000 0001 = 1
        a = word(1, 8)
        result = a.msb()

        self.assertEqual(result, 1)

        # a = 0000 0000 = 0
        a = word(0, 8)
        result = a.msb()

        self.assertEqual(result, 0)

        # a = 1111 1111 = 255
        a = word(255, 8)
        result = a.msb()

        self.assertEqual(result, 8)

    def test_has_prefix(self):
        # word itself is prefix
        a = word(0b1100, 4)
        p = word(0b1100, 4)

        result = a.has_prefix(p)
        self.assertTrue(result)

        # epsilon is a prefix
        a = word(0b1100, 4)
        p = word.epsilon

        result = a.has_prefix(p)
        self.assertTrue(result)

        # prefix is a prefix
        a = word(0b1100, 4)
        p = word(0b110, 3)

        result = a.has_prefix(p)
        self.assertTrue(result)

        # word which is shorter, but is no prefix
        a = word(0b1100, 4)
        p = word(0b010, 3)

        result = a.has_prefix(p)
        self.assertFalse(result)

        # word which is longer can't be a prefix
        a = word(0b1100, 4)
        p = word(0b11001, 5)

        result = a.has_prefix(p)
        self.assertFalse(result)

    def test_common_prefix(self):
        # a = 1100 = 12
        # b = 1100 = 12
        # p = 1100 = 12
        a = word(12, 8)
        b = word(12, 8)
        p = word(12, 8)

        result = a.common_prefix(b)
        self.assertEqual(result, p)

        result = b.common_prefix(a)
        self.assertEqual(result, p)

        # a = 1111 0001 0001 1100 = 61724
        # b = 1111 0010 1001 0100 = 62100
        # p = 1111 00 = 60
        a = word(61724, 16)
        b = word(62100, 16)
        p = word(60, 6)

        result = a.common_prefix(b)
        self.assertEqual(result, p)

        result = b.common_prefix(a)
        self.assertEqual(result, p)

        # a = 1100 1101 0001 1100 = 52508
        # b = 0100 1100 1001 0100 = 19604
        # p = empty = 0 with word size 0
        a = word(52508, 16)
        b = word(19604, 16)
        p = word(0, 0)

        result = a.common_prefix(b)
        self.assertEqual(result, p)

        result = b.common_prefix(a)
        self.assertEqual(result, p)

        # a = 0010 1101 0001 1100 = 52508
        # b =      1100 1100 1001 = 3273
        # p = 0 with word size 0
        a = word(52508, 16)
        b = word(3273, 12)
        p = word(0, 0)

        result = a.common_prefix(b)
        self.assertEqual(result, p)

        result = b.common_prefix(a)
        self.assertEqual(result, p)

    def test_common_prefix_split(self):
        # a = 1100 = 12
        # b = 1100 = 12
        # p = 1100 = 12
        # suffix1 = 0 with word size 0
        # suffix2 = 0 with word size 0
        a = b = p = word(12, 8)
        s1 = s2 = word(0, 0)

        pre, suf1, suf2 = a.common_prefix_split(b)
        self.assertEqual(pre, p)
        self.assertEqual(suf1, s1)
        self.assertEqual(suf2, s2)

        # a = 1111 0001 0001 1100 = 61724
        # b = 1111 0010 1001 0100 = 62100
        # p = 1111 00 = 60
        # suffix1 = 0 with word size 0
        # suffix2 = 0 with word size 0
        a = word(61724, 16)
        b = word(62100, 16)
        p = word(60, 6)
        s1 = word(284, 10)
        s2 = word(660, 10)

        pre, suf1, suf2 = a.common_prefix_split(b)
        self.assertEqual(pre, p)
        self.assertEqual(suf1, s1)
        self.assertEqual(suf2, s2)

        # a = 1100 1101 0001 1100 = 52508
        # b = 0100 1100 1001 0100 = 19604
        # p = empty = 0 with word size 0
        # suffix1 = 1100 1101 0001 1100 = 52508
        # suffix2 = 0100 1100 1001 0100 = 19604
        a = word(52508, 16)
        b = word(19604, 16)
        p = word(0, 0)
        s1, s2 = a, b

        pre, suf1, suf2 = a.common_prefix_split(b)
        self.assertEqual(pre, p)
        self.assertEqual(suf1, s1)
        self.assertEqual(suf2, s2)

    def test_remove_prefix_equal_size(self):
        a = word(0b1100, 8)
        b = word(0b1100, 8)
        p = word(0b1100, 8)
        s1 = word(0, 0)
        s2 = word(0, 0)

        suf1, suf2, pre = a.remove_prefix(b)
        self.assertEqual(pre, p)
        self.assertEqual(suf1, s1)
        self.assertEqual(suf2, s2)


        a = word(0b1111000100011100, 16)
        b = word(0b1111001010010100, 16)
        p = word(0b111100, 6)
        s1 = word(0b0000000100011100, 10)
        s2 = word(0b0000001010010100, 10)

        suf1, suf2, pre = a.remove_prefix(b)
        self.assertEqual(pre, p)
        self.assertEqual(suf1, s1)
        self.assertEqual(suf2, s2)


        a = word(0b1100110100011100, 16)
        b = word(0b0100110010010100, 16)
        p = word(0, 0)
        s1 = a
        s2 = b

        suf1, suf2, pre = a.remove_prefix(b)
        self.assertEqual(pre, p)
        self.assertEqual(suf1, s1)
        self.assertEqual(suf2, s2)

    def test_remove_prefix_unequal_size(self):
        a = word(0b00110001, 8)
        b = word(0b001100, 6)
        p = word(0b001100, 6)
        s1 = word(0b01, 2)
        s2 = word(0b0, 0)

        suf1, suf2, pre = a.remove_prefix(b)
        self.assertEqual(pre, p)
        self.assertEqual(suf1, s1)
        self.assertEqual(suf2, s2)

        # same test as before, but with swapped arguments
        suf2, suf1, pre = b.remove_prefix(a)
        self.assertEqual(pre, p)
        self.assertEqual(suf1, s1)
        self.assertEqual(suf2, s2)

        #
        a = word(0b1111000100011100101010, 22)
        b = word(0b1111001010010100, 16)
        p = word(0b111100, 6)
        s1 = word(0b000000100011100101010, 16)
        s2 = word(0b0000001010010100, 10)

        suf1, suf2, pre = a.remove_prefix(b)
        self.assertEqual(pre, p)
        self.assertEqual(suf1, s1)
        self.assertEqual(suf2, s2)

        # same test as before, but with swapped arguments
        suf2, suf1, pre = b.remove_prefix(a)
        self.assertEqual(pre, p)
        self.assertEqual(suf1, s1)
        self.assertEqual(suf2, s2)

        #
        a = word(0b110011010001110010100101, 24)
        b = word(0b0100110010010100, 16)
        p = word(0, 0)
        s1 = a
        s2 = b

        suf1, suf2, pre = a.remove_prefix(b)
        self.assertEqual(pre, p)
        self.assertEqual(suf1, s1)
        self.assertEqual(suf2, s2)

        # same test as before, but with swapped arguments
        suf2, suf1, pre = b.remove_prefix(a)
        self.assertEqual(pre, p)
        self.assertEqual(suf1, s1)
        self.assertEqual(suf2, s2)

if __name__ == '__main__':
    unittest.main()
