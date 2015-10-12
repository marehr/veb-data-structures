# coding=utf8

import unittest

import tests.mixins.static
import tests.TestCase
import veb.xfast.static as Static
import Trie
from word import word


class TreeTest(
    tests.TestCase.TestCase,
    tests.mixins.TreeTestMixin,
    tests.mixins.static.ReferenceTreeTestMixin,
):

    def new_trie(self, word_size, elements=[]):
        trie = Static.Tree(word_size)
        trie.extend(elements)
        return trie

    def new_reference_trie(self, word_size, elements=[]):
        trie = Trie.Tree(word_size)
        trie.extend(elements)
        return trie

    def assertHash(self, T, hash_index, expect):
        self.assertEqual(T[hash_index], expect)
        del T[hash_index]

    def assertHashTable(self, xfast):
        T = dict(xfast.T)
        root = xfast.root

        self.assertHash(T, word.epsilon, root)

        for node in Trie.Iterators.preorder(root):
            if node.is_root():
                continue

            # print "~~~~~~~~~~~~~`"
            # print "word: %s" % node.key
            self.assertHash(T, node.key, node)

            lca = node.parent
            for w in xrange(lca.key.w + 1, node.key.w):
                p = node.key.split_fst(w)
                # print "word: %s" % p
                self.assertHash(T, p, lca)

        # print T
        self.assertEqual(len(T), 0)

    def test_insert(self):

        xs = [0b00000111]
        xfast = self.new_trie(8, xs)
        T = dict(xfast.T)

        self.assertHash(T, word(0b00000111, 8), xfast.root.left)
        self.assertHash(T, word(0b0000011, 7), xfast.root)
        self.assertHash(T, word(0b000001, 6), xfast.root)
        self.assertHash(T, word(0b00000, 5), xfast.root)
        self.assertHash(T, word(0b0000, 4), xfast.root)
        self.assertHash(T, word(0b000, 3), xfast.root)
        self.assertHash(T, word(0b00, 2), xfast.root)
        self.assertHash(T, word(0b0, 1), xfast.root)
        self.assertHash(T, word(0, 0), xfast.root)

        self.assertEqual(len(T), 0)
        self.assertHashTable(xfast)

        #
        # #
        # # #
        xs = [0b00000111, 0b000101110]
        xfast = self.new_trie(8, xs)
        T = dict(xfast.T)

        self.assertHash(T, word(0b00000111, 8), xfast.root.left.left)
        self.assertHash(T, word(0b0000011, 7), xfast.root.left)
        self.assertHash(T, word(0b000001, 6), xfast.root.left)
        self.assertHash(T, word(0b00000, 5), xfast.root.left)
        self.assertHash(T, word(0b0000, 4), xfast.root.left)
        self.assertHash(T, word(0b000, 3), xfast.root.left)
        self.assertHash(T, word(0b00, 2), xfast.root.left)

        self.assertHash(T, word(0b0, 1), xfast.root)
        self.assertHash(T, word(0, 0), xfast.root)

        self.assertHash(T, word(0b000101110, 8), xfast.root.left.right)
        self.assertHash(T, word(0b00010111, 7), xfast.root.left)
        self.assertHash(T, word(0b0001011, 6), xfast.root.left)
        self.assertHash(T, word(0b000101, 5), xfast.root.left)
        self.assertHash(T, word(0b00010, 4), xfast.root.left)
        self.assertHash(T, word(0b0001, 3), xfast.root.left)

        self.assertEqual(len(T), 0)
        self.assertHashTable(xfast)

        #
        # #
        # # #
        xs = [0b00000111, 0b000101110, 0b10101100]
        xfast = self.new_trie(8, xs)
        T = dict(xfast.T)

        self.assertHash(T, word(0b00000111, 8), xfast.root.left.left)
        self.assertHash(T, word(0b0000011, 7), xfast.root.left)
        self.assertHash(T, word(0b000001, 6), xfast.root.left)
        self.assertHash(T, word(0b00000, 5), xfast.root.left)
        self.assertHash(T, word(0b0000, 4), xfast.root.left)
        self.assertHash(T, word(0b000, 3), xfast.root.left)
        self.assertHash(T, word(0b00, 2), xfast.root.left)

        self.assertHash(T, word(0b0, 1), xfast.root)
        self.assertHash(T, word(0, 0), xfast.root)

        self.assertHash(T, word(0b000101110, 8), xfast.root.left.right)
        self.assertHash(T, word(0b00010111, 7), xfast.root.left)
        self.assertHash(T, word(0b0001011, 6), xfast.root.left)
        self.assertHash(T, word(0b000101, 5), xfast.root.left)
        self.assertHash(T, word(0b00010, 4), xfast.root.left)
        self.assertHash(T, word(0b0001, 3), xfast.root.left)

        self.assertHash(T, word(0b10101100, 8), xfast.root.right)
        self.assertHash(T, word(0b1010110, 7), xfast.root)
        self.assertHash(T, word(0b101011, 6), xfast.root)
        self.assertHash(T, word(0b10101, 5), xfast.root)
        self.assertHash(T, word(0b1010, 4), xfast.root)
        self.assertHash(T, word(0b101, 3), xfast.root)
        self.assertHash(T, word(0b10, 2), xfast.root)
        self.assertHash(T, word(0b1, 1), xfast.root)

        self.assertEqual(len(T), 0)
        self.assertHashTable(xfast)

    def test_remove(self):

        xs = [0b00000111]
        xfast = self.new_trie(8, xs)
        xfast.remove(0b00000111)

        T = dict(xfast.T)

        self.assertHash(T, word(0, 0), xfast.root)
        self.assertEqual(len(T), 0)

        self.assertHashTable(xfast)

        #
        # #
        # # #
        xs = [0b00000111, 0b000101110]
        xfast = self.new_trie(8, xs)
        xfast.remove(0b000101110)

        T = dict(xfast.T)

        self.assertHash(T, word(0b00000111, 8), xfast.root.left)
        self.assertHash(T, word(0b0000011, 7), xfast.root)
        self.assertHash(T, word(0b000001, 6), xfast.root)
        self.assertHash(T, word(0b00000, 5), xfast.root)
        self.assertHash(T, word(0b0000, 4), xfast.root)
        self.assertHash(T, word(0b000, 3), xfast.root)
        self.assertHash(T, word(0b00, 2), xfast.root)
        self.assertHash(T, word(0b0, 1), xfast.root)
        self.assertHash(T, word(0, 0), xfast.root)

        self.assertEqual(len(T), 0)
        self.assertHashTable(xfast)

        #
        # #
        # # #
        xs = [0b00000111, 0b000101110, 0b10101100]
        xfast = self.new_trie(8, xs)
        xfast.remove(0b10101100)

        T = dict(xfast.T)

        self.assertHash(T, word(0b00000111, 8), xfast.root.left.left)
        self.assertHash(T, word(0b0000011, 7), xfast.root.left)
        self.assertHash(T, word(0b000001, 6), xfast.root.left)
        self.assertHash(T, word(0b00000, 5), xfast.root.left)
        self.assertHash(T, word(0b0000, 4), xfast.root.left)
        self.assertHash(T, word(0b000, 3), xfast.root.left)
        self.assertHash(T, word(0b00, 2), xfast.root.left)

        self.assertHash(T, word(0b0, 1), xfast.root)
        self.assertHash(T, word(0, 0), xfast.root)

        self.assertHash(T, word(0b000101110, 8), xfast.root.left.right)
        self.assertHash(T, word(0b00010111, 7), xfast.root.left)
        self.assertHash(T, word(0b0001011, 6), xfast.root.left)
        self.assertHash(T, word(0b000101, 5), xfast.root.left)
        self.assertHash(T, word(0b00010, 4), xfast.root.left)
        self.assertHash(T, word(0b0001, 3), xfast.root.left)

        self.assertEqual(len(T), 0)
        self.assertHashTable(xfast)

if __name__ == '__main__':
    unittest.main()
