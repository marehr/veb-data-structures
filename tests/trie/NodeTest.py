# coding=utf8

import unittest

import tests.mixins
import tests.TestCase
import Trie
from word import word


class NodeTest(tests.TestCase.TestCase, tests.mixins.NodeTestMixin):

    def new_trie(self, word_size, elements=[]):
        trie = Trie.Tree(word_size)
        trie.extend(elements)
        return trie

    def test_is_on_edge(self):
        #  \
        #   0001 - 1001
        #       \
        #        - 0011
        root = Trie.Node(word.epsilon, None)

        branch = Trie.Node(word(0b0001, 4), root)
        root.set_child(branch)

        child1 = Trie.Node(word(0b1001, 4), branch)
        branch.set_child(child1)

        child2 = Trie.Node(word(0b0011, 4), branch)
        branch.set_child(child2)

        # edge cases
        q = word(0b1, 1)
        res = root.is_on_edge(q)
        self.assertFalse(res)

        q = word.epsilon
        res = root.is_on_edge(q)
        self.assertTrue(res)

        # on edge
        q = word(0b0, 1)
        res = branch.is_on_edge(q)
        self.assertTrue(res)

        q = word(0b0001, 4)
        res = branch.is_on_edge(q)
        self.assertTrue(res)

        q = word(0b0000, 4)
        res = branch.is_on_edge(q)
        self.assertFalse(res)

        q = word(0b000110, 6)
        res = child1.is_on_edge(q)
        self.assertTrue(res)

        q = word(0b00011001, 8)
        res = child1.is_on_edge(q)
        self.assertTrue(res)

        q = word(0b000100, 6)
        res = child1.is_on_edge(q)
        self.assertFalse(res)

        q = word(0b00010000, 8)
        res = child1.is_on_edge(q)
        self.assertFalse(res)

        # to long
        q = word(0b00011, 5)
        res = branch.is_on_edge(q)
        self.assertFalse(res)

        q = word(0b000010, 6)
        res = branch.is_on_edge(q)
        self.assertFalse(res)

        # to short
        q = word.epsilon
        res = branch.is_on_edge(q)
        self.assertFalse(res)

        q = word(0b000, 3)
        res = child1.is_on_edge(q)
        self.assertFalse(res)

        # no matching prefix
        q = word(0b01001, 5)
        res = child1.is_on_edge(q)
        self.assertFalse(res)

    def test_is_left_of_edge(self):
        trie = Trie.Tree(8)
        trie.extend([9, 12, 44, 108, 110, 111])

        #
        ## test edge 44
        current = trie.root.left.left.right
        self.assertEqual(current.edge, word(0b101100, 6))
        self.assertEqual(current.key, word(0b00101100, 8))

        # 00000000 is left of 00101100
        q = word(0b00000000, 8)
        result = current.is_left_of_edge(q)
        self.assertTrue(result)

        # 00101011 is left of 00101100
        q = word(0b00101011, 8)
        result = current.is_left_of_edge(q)
        self.assertTrue(result)

        # 00101100 is left of 00101100
        q = word(0b0000101100, 8)
        result = current.is_left_of_edge(q)
        self.assertFalse(result)

        # 00101111 is left of 00101100
        q = word(0b00101111, 8)
        result = current.is_left_of_edge(q)
        self.assertFalse(result)

        #
        ## test edge 0-11011-00 of 108
        current = trie.root.left.right
        self.assertEqual(current.edge, word(0b11011, 5))
        self.assertEqual(current.key, word(0b011011, 6))

        # 00000000 is left of 011011
        q = word(0b00000000, 8)
        result = current.is_left_of_edge(q)
        self.assertTrue(result)

        # 01101000 is left of 011011
        q = word(0b01101000, 8)
        result = current.is_left_of_edge(q)
        self.assertTrue(result)

        # 01101100 is not left of 011011
        q = word(0b01101100, 8)
        result = current.is_left_of_edge(q)
        self.assertFalse(result)

        # 01110111 is not left of 011011
        q = word(0b01110111, 8)
        result = current.is_left_of_edge(q)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
