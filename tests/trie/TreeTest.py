# coding=utf8

import unittest

import tests.mixins
import tests.TestCase
import Trie


class TreeTest(
    tests.TestCase.TestCase,
    tests.mixins.TreeTestMixin
):

    def new_trie(self, word_size, elements=[]):
        trie = Trie.Tree(word_size)
        trie.extend(elements)
        return trie

    def test_elements(self):
        with self.random() as rand:
            trie = Trie.Tree(8)

            xs = rand.sample(range(30), 20)
            xs = self.data_words(xs, 8)
            expect = []

            for x in xs:
                trie.insert(x)
                expect.append(x)

                expect.sort()
                result = trie.elements()

                self.assertEqual(expect, result)

    def test_preoder(self):
        trie = self.new_trie(4, [3, 5, 8, 10, 15])
        nodes = list(trie)

        root = trie.root
        node0011 = root.left.left
        node0 = root.left
        node0101 = root.left.right

        node1000 = root.right.left.left
        node10 = root.right.left
        node1010 = root.right.left.right
        node1 = root.right
        node1111 = root.right.right

        result = [node0011, node0, node0101, root, node1000, node10, node1010, node1, node1111]
        self.assertEqual(nodes, result)

if __name__ == '__main__':
    unittest.main()
