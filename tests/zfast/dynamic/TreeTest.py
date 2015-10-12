# coding=utf8

import unittest

import tests.mixins
import tests.mixins.dynamic
import tests.TestCase
import veb.zfast.static as Static
import veb.zfast.dynamic as Dynamic
from word import word


class TreeTest(
    tests.TestCase.TestCase,
    tests.mixins.TreeTestMixin,
    tests.mixins.dynamic.ReferenceTreeTestMixin,
    tests.mixins.VebSlickDynamicTestMixin
):

    def new_trie(self, word_size, elements=[]):
        trie = Dynamic.Tree(word_size)
        trie.extend(elements)
        return trie

    def new_reference_trie(self, word_size, elements=[]):
        trie = Static.Tree(word_size)
        trie.extend(elements)
        return trie

    def test_min_max_tree_insert(self):
        veb = self.new_trie(4)

        #  0001
        a = word(0b0001, 4)
        veb.insert(a)

        # shared minimum/maximum of 0001
        self.assertSharedMinimum(veb.root.left)
        self.assertSharedMaximum(veb.root.left)

        # assert all min-/max-spines are shared
        self.assertMinMaxStructure(veb.root)

        #  0 - 001
        #   \
        #    - 111
        b = word(0b0111, 4)
        veb.insert(b)

        # shared minimum of 0 and 0001
        self.assertSharedMinimum(veb.root.left)

        # shared minimum of 0111
        self.assertSharedMinimum(veb.root.left.right)

        # shared maximum of 0 and 0111
        self.assertSharedMaximum(veb.root.left)

        # shared maximum of 0001
        self.assertSharedMaximum(veb.root.left.left)

        # assert all min-/max-spines are shared
        self.assertMinMaxStructure(veb.root)

        #  0 - 0 - 01
        #   |   \
        #   \    - 10
        #    - 1   11
        c = word(0b0010, 4)
        veb.insert(c)

        # shared minimum of 0, 00 and 0001
        self.assertSharedMinimum(veb.root.left)

        # shared minimum of 0010
        self.assertSharedMinimum(veb.root.left.left.right)

        # shared minimum of 0111
        self.assertSharedMinimum(veb.root.left.right)

        # shared maximum of 0 and 0111
        self.assertSharedMaximum(veb.root.left)

        # shared maximum of 00 and 0010
        self.assertSharedMaximum(veb.root.left.left)

        # shared maximum of 0001
        self.assertSharedMaximum(veb.root.left.left.left)

        # assert all min-/max-spines are shared
        self.assertMinMaxStructure(veb.root)

        #  0 - 0 - 0 - 0
        #   |   |   \
        #   |   \    - 1
        #   \    - 1   0
        #    - 1   1   1
        c = word(0b0000, 4)
        veb.insert(c)

        # shared minimum of 0, 00, 000 and 0000
        self.assertSharedMinimum(veb.root.left)

        # shared minimum of 0001
        self.assertSharedMinimum(veb.root.left.left.left.right)

        # shared minimum of 0010
        self.assertSharedMinimum(veb.root.left.left.right)

        # shared minimum of 0111
        self.assertSharedMinimum(veb.root.left.right)

        # shared maximum of 0 and 0111
        self.assertSharedMaximum(veb.root.left)

        # shared maximum of 00 and 0010
        self.assertSharedMaximum(veb.root.left.left)

        # shared maximum of 000 and 0001
        self.assertSharedMaximum(veb.root.left.left.left)

        # shared maximum of 0000
        self.assertSharedMaximum(veb.root.left.left.left.left)

        # assert all min-/max-spines are shared
        self.assertMinMaxStructure(veb.root)

    def test_min_max_tree_remove(self):
        veb = self.new_trie(8)
        veb.insert(0b10110100)
        veb.insert(0b11100110)
        veb.insert(0b10000000)

        result = veb.remove(0b11100110)
        self.assertTrue(result)

        # 1 - 000 0000
        #  \
        #   - 011 0100

        # shared minimum of 1 and 1000 0000; 1011 0100
        self.assertSharedMinimum(veb.root.right)
        self.assertSharedMinimum(veb.root.right.right)

        # shared maximum of 1 and 1011 0100; 1000 0000
        self.assertSharedMaximum(veb.root.right)
        self.assertSharedMaximum(veb.root.right.left)

        # assert all min-/max-spines are shared
        self.assertMinMaxStructure(veb.root)

        result = veb.remove(0b10110100)
        self.assertTrue(result)

        # shared minimum/maximum of 1000 0000
        self.assertSharedMinimum(veb.root.right)
        self.assertSharedMaximum(veb.root.right)

        # assert all min-/max-spines are shared
        self.assertMinMaxStructure(veb.root)

if __name__ == '__main__':
    unittest.main()
