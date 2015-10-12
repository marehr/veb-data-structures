# coding=utf8

import unittest

import tests.mixins
import tests.mixins.static
import tests.TestCase
import Trie
import veb.zfast.static as Static
from word import word


class TreeTest(
    tests.TestCase.TestCase,
    tests.mixins.VebSlickStaticTestMixin,
    tests.mixins.static.ReferenceTreeTestMixin,
    tests.mixins.TreeTestMixin
):

    def new_trie(self, word_size, elements=[]):
        trie = Static.Tree(word_size)
        trie.extend(elements)
        return trie

    def construct_zfast(self, word_size, elements=[]):
        """
        Utility method, for the case, that the z-fast trie can't be constructed
        with zfast.insert().
        """
        trie = Trie.Tree(word_size)

        # use trie methods to create the trie, but use zfast nodes instead
        trie.root = Static.Node(word.epsilon, None)
        trie.extend(elements)

        # reinject zfast root and rebuild index
        zfast = Static.Tree(word_size)
        zfast.root = trie.root
        self.rebuild_structure(zfast)
        return zfast

    def new_reference_trie(self, word_size, elements=[]):
        trie = Trie.Tree(word_size)
        trie.extend(elements)
        return trie

    def test_hash_index(self):
        low = word(0, 0)
        high = word(0b0, 1)
        result = Static.Tree.hash_index(low, high)
        self.assertEqual(result, word(0b0, 1))

        low = word(0b0, 1)
        high = word(0b00, 2)
        result = Static.Tree.hash_index(low, high)
        self.assertEqual(result, word(0b00, 2))

        low = word(0b00, 2)
        high = word(0b0000, 4)
        result = Static.Tree.hash_index(low, high)
        self.assertEqual(result, word(0b0000, 4))

        low = word(0b0000, 4)
        high = word(0b00001001, 8)
        result = Static.Tree.hash_index(low, high)
        self.assertEqual(result, word(0b00001001, 8))

        low = word(0b0000, 4)
        high = word(0b00001100, 8)
        result = Static.Tree.hash_index(low, high)
        self.assertEqual(result, word(0b00001100, 8))

        low = word(0b00, 2)
        high = word(0b00101100, 8)
        result = Static.Tree.hash_index(low, high)
        self.assertEqual(result, word(0b00101100, 8))

        low = word(0b0, 1)
        high = word(0b011011, 6)
        result = Static.Tree.hash_index(low, high)
        self.assertEqual(result, word(0b0110, 4))

        low = word(0b011011, 6)
        high = word(0b01101100, 8)
        result = Static.Tree.hash_index(low, high)
        self.assertEqual(result, word(0b01101100, 8))

        low = word(0b011011, 6)
        high = word(0b0110111, 7)
        result = Static.Tree.hash_index(low, high)
        self.assertEqual(result, word(0b0110111, 7))

        low = word(0b0110111, 7)
        high = word(0b01101110, 8)
        result = Static.Tree.hash_index(low, high)
        self.assertEqual(result, word(0b01101110, 8))

        low = word(0b0110111, 7)
        high = word(0b01101111, 8)
        result = Static.Tree.hash_index(low, high)
        self.assertEqual(result, word(0b01101111, 8))

        low = word(0, 0)
        high = word(0b00001100, 8)
        result = Static.Tree.hash_index(low, high)
        self.assertEqual(result, word(0b00001100, 8))

    def test_hash_table(self):
        veb = self.new_trie(8)

        # 12 = 0000 1100
        a = word(12, 8)
        veb.insert(a)

        result = self.hash_table(veb)
        expects = {a: veb.root}
        self.assertEqual(expects, result)

        # 9  = 0000 - 1001
        #          \
        # 12 =      - 1100
        b = word(9, 8)
        veb.insert(b)

        root = veb.root
        result = self.hash_table(veb)
        self.assertEqual(result[word(0b0000, 4)], root)
        self.assertEqual(result[word(0b00001001, 8)], root.left)
        self.assertEqual(result[word(0b00001100, 8)], root.left)

        # 9  = 00 - 00 - 1001
        #             \
        # 12 =         - 1100
        #        \
        # 44 =    - 10   1100
        c = word(44, 8)
        veb.insert(c)

        root = veb.root
        result = self.hash_table(veb)
        self.assertEqual(result[word(0b00, 2)], root)
        self.assertEqual(result[word(0b0000, 4)], root.left)
        self.assertEqual(result[word(0b00001001, 8)], root.left.left)
        self.assertEqual(result[word(0b00001100, 8)], root.left.left)
        self.assertEqual(result[word(0b00101100, 8)], root.left)

        #  9 = 0 - 0 - 00 - 1001
        #                \
        # 12 =            - 1100
        #           \
        # 44 =       - 10   1100
        #       \
        #108 =   - 1   10   1100
        d = word(108, 8)
        veb.insert(d)

        root = veb.root
        result = self.hash_table(veb)
        self.assertEqual(result[word(0b0, 1)], root)
        self.assertEqual(result[word(0b00, 2)], root.left)
        self.assertEqual(result[word(0b0000, 4)], root.left.left)
        self.assertEqual(result[word(0b00001001, 8)], root.left.left.left)
        self.assertEqual(result[word(0b00001100, 8)], root.left.left.left)
        self.assertEqual(result[word(0b00101100, 8)], root.left.left)
        self.assertEqual(result[word(0b01101100, 8)], root.left)

        #  9 = 0 - 0 - 00 - 10   0   1
        #       |   |    \
        # 12 =  |   |     - 11   0   0
        #       |   \
        # 44 =  |    - 10   11   0   0
        #       \
        #108 =   - 1   10   11 - 0   0
        #                     \
        #110 =                 - 1 - 0
        #                         \
        #111 =                     - 1
        e = word(110, 8)
        veb.insert(e)

        f = word(111, 8)
        veb.insert(f)

        root = veb.root
        result = self.hash_table(veb)
        self.assertEqual(result[word(0b0, 1)], root)
        self.assertEqual(result[word(0b00, 2)], root.left)
        self.assertEqual(result[word(0b0000, 4)], root.left.left)
        self.assertEqual(result[word(0b00001001, 8)], root.left.left.left)
        self.assertEqual(result[word(0b00001100, 8)], root.left.left.left)
        self.assertEqual(result[word(0b00101100, 8)], root.left.left)
        self.assertEqual(result[word(0b0110, 4)], root.left)
        self.assertEqual(result[word(0b01101100, 8)], root.left.right)
        self.assertEqual(result[word(0b0110111, 7)], root.left.right)
        self.assertEqual(result[word(0b01101110, 8)], root.left.right.right)
        self.assertEqual(result[word(0b01101111, 8)], root.left.right.right)

if __name__ == '__main__':
    unittest.main()
