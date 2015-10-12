import unittest
from word import word, compare_word

class compareWordTest(unittest.TestCase):

    def test_create(self):
        # test normal creation
        a = compare_word(0b1111, 4)
        self.assertIsInstance(a, compare_word)

        # test normal creation with a compare_word as argument
        a = compare_word(a, 4)

        # test normal creation with a word as argument
        a = word(a, 4)
        a = compare_word(a, 4)
        self.assertIsInstance(a, compare_word)

        # 4095 needs 12 bits, but it can only hold 8 bits
        with self.assertRaises(TypeError):
            a = compare_word(4095, 8)

        # you can't create a compare_word with a compare_word, which does not matches the
        # compare_wordsize
        with self.assertRaises(TypeError):
            a = compare_word(0b1111, 4)
            a = compare_word(a, 8)

    def test_eq(self):
        a = compare_word(0b00001100, 8)
        b = compare_word(0b00001100, 8)
        self.assertTrue(a == b, "0b00001100 == 0b00001100 == True")

        a = compare_word(0b00001100, 8)
        b = compare_word(0b00001101, 8)
        self.assertFalse(a == b, "0b00001100 == 0b00001101 == False")

        a = compare_word(0b1100, 4)
        b = compare_word(0b00001100, 8)
        self.assertFalse(a == b, "0b1100 == 0b00001100 == False")

    def test_neq(self):
        a = compare_word(0b00001100, 8)
        b = compare_word(0b00001100, 8)
        self.assertFalse(a != b, "0b00001100 != 0b00001100 == False")

        a = compare_word(0b00001100, 8)
        b = compare_word(0b00001101, 8)
        self.assertTrue(a != b, "0b00001100 != 0b00001101 == True")

        a = compare_word(0b1100, 4)
        b = compare_word(0b00001100, 8)
        self.assertTrue(a != b, "0b1100 != 0b00001100 == True")

    def test_lt(self):
        a = compare_word(0b00001100, 8)
        b = compare_word(0b00001111, 8)
        self.assertTrue(a < b, "0b00001100 < 0b00001111 == True")

        a = compare_word(0b00010101, 8)
        b = compare_word(0b00000001, 8)
        self.assertFalse(a < b, "0b00010101 < 0b00000001 == False")

        a = compare_word(0b000001, 6)
        b = compare_word(0b00010101, 8)
        self.assertTrue(a < b, "0b000001 < 0b00010101 == True")

        a = compare_word(0b00010101, 8)
        b = compare_word(0b000001, 6)
        self.assertFalse(a < b, "0b00010101 < 0b000001 == False")

        a = compare_word(0b000101, 6)
        b = compare_word(0b00010101, 8)
        self.assertTrue(a < b, "0b000101 < 0b00010101 == True")

        a = compare_word(0b00010101, 8)
        b = compare_word(0b000101, 6)
        self.assertFalse(a < b, "0b00010101 < 0b000101 == False")

    def test_le(self):
        a = compare_word(0b00001100, 8)
        b = compare_word(0b00001111, 8)
        self.assertTrue(a <= b, "0b00001100 <= 0b00001111 == True")

        a = compare_word(0b00010101, 8)
        b = compare_word(0b00000001, 8)
        self.assertFalse(a <= b, "0b00010101 <= 0b00000001== False")

        a = compare_word(0b00001100, 8)
        b = compare_word(0b00001100, 8)
        self.assertTrue(a <= b, "0b00001100 <= 0b00001100 == True")

        a = compare_word(0b000001, 6)
        b = compare_word(0b00010101, 8)
        self.assertTrue(a <= b, "0b000001 <= 0b00010101 == True")

        a = compare_word(0b00010101, 8)
        b = compare_word(0b000001, 6)
        self.assertFalse(a <= b, "0b00010101 <= 0b000001 == False")

        a = compare_word(0b000101, 6)
        b = compare_word(0b00010101, 8)
        self.assertTrue(a <= b, "0b000101 <= 0b00010101 == True")

        a = compare_word(0b00010101, 8)
        b = compare_word(0b000101, 6)
        self.assertFalse(a <= b, "0b00010101 <= 0b000101 == False")

    def test_gt(self):
        a = compare_word(0b00001100, 8)
        b = compare_word(0b00001111, 8)
        self.assertTrue(b > a, "0b00001111 > 0b00001100 == True")

        a = compare_word(0b00010101, 8)
        b = compare_word(0b00000001, 8)
        self.assertFalse(b > a, "0b00000001 > 0b00010101 == False")

        a = compare_word(0b00010101, 8)
        b = compare_word(0b000001, 6)
        self.assertTrue(a > b, "0b00010101 > 0b000001 == True")

        a = compare_word(0b000001, 6)
        b = compare_word(0b00010101, 8)
        self.assertFalse(a > b, "0b000001 > 0b00010101 == False")

        a = compare_word(0b00010101, 8)
        b = compare_word(0b000101, 6)
        self.assertTrue(a > b, "0b00010101 > 0b000101 == True")

        a = compare_word(0b000101, 6)
        b = compare_word(0b00010101, 8)
        self.assertFalse(a > b, "0b000101 > 0b00010101 == False")

    def test_ge(self):
        a = compare_word(0b00001100, 8)
        b = compare_word(0b00001111, 8)
        self.assertTrue(b >= a, "0b00001111 >= 0b00001100 == True")

        a = compare_word(0b00010101, 8)
        b = compare_word(0b00000001, 8)
        self.assertFalse(b >= a, "0b00000001 >= 0b00010101 == False")

        a = compare_word(0b00001100, 8)
        b = compare_word(0b00001100, 8)
        self.assertTrue(b >= a, "0b00001100 >= 0b00001100 == True")

        a = compare_word(0b00010101, 8)
        b = compare_word(0b000001, 6)
        self.assertTrue(a >= b, "0b00010101 >= 0b000001 == True")

        a = compare_word(0b000001, 6)
        b = compare_word(0b00010101, 8)
        self.assertFalse(a >= b, "0b000001 >= 0b00010101 == False")

        a = compare_word(0b00010101, 8)
        b = compare_word(0b000101, 6)
        self.assertTrue(a >= b, "0b00010101 >= 0b000101 == True")

        a = compare_word(0b000101, 6)
        b = compare_word(0b00010101, 8)
        self.assertFalse(a >= b, "0b000101 >= 0b00010101 == False")

if __name__ == '__main__':
    unittest.main()
