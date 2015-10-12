# coding=utf8

import unittest

import tests.TestCase
import tests.mixins
import veb.zfast.static as Static
from word import word


class NodeTest(
    tests.TestCase.TestCase,
    tests.mixins.NodeTestMixin
):

    def new_trie(self, word_size, elements=[]):
        trie = Static.Tree(word_size)
        trie.extend(elements)
        return trie

    def test_linked_leafes(self):
        veb = self.new_trie(8, [9, 12, 44, 108, 110, 111])

        leaf9 = veb.root.left.left.left.left
        leaf12 = veb.root.left.left.left.right
        leaf44 = veb.root.left.left.right
        leaf108 = veb.root.left.right.left
        leaf110 = veb.root.left.right.right.left
        leaf111 = veb.root.left.right.right.right

        current = veb.search_node(9)
        self.assertEqual(current._previous_leaf, None)
        self.assertEqual(current, leaf9)
        self.assertEqual(current._next_leaf, leaf12)

        current = current._next_leaf
        self.assertEqual(current._previous_leaf, leaf9)
        self.assertEqual(current, leaf12)
        self.assertEqual(current._next_leaf, leaf44)

        current = current._next_leaf
        self.assertEqual(current._previous_leaf, leaf12)
        self.assertEqual(current, leaf44)
        self.assertEqual(current._next_leaf, leaf108)

        current = current._next_leaf
        self.assertEqual(current._previous_leaf, leaf44)
        self.assertEqual(current, leaf108)
        self.assertEqual(current._next_leaf, leaf110)

        current = current._next_leaf
        self.assertEqual(current._previous_leaf, leaf108)
        self.assertEqual(current, leaf110)
        self.assertEqual(current._next_leaf, leaf111)

        current = current._next_leaf
        self.assertEqual(current._previous_leaf, leaf110)
        self.assertEqual(current, leaf111)
        self.assertEqual(current._next_leaf, None)

    def test_random_linked_leafes(self):
        with self.random() as rand:
            size = rand.randint(0, 150)
            samples = rand.sample(xrange(255), size)

            veb = self.new_trie(8, samples)

            samples.sort()

            for value in samples[1:]:
                value = word(value, 8)
                pred = veb.predecessor(value)
                curr = veb.search_node(value)

                self.assertEqual(curr.key, value)
                self.assertEqual(curr._previous_leaf.key, pred)
                self.assertEqual(curr._previous_leaf._next_leaf, curr)

if __name__ == '__main__':
    unittest.main()
