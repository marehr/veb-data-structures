# coding=utf8

import unittest

import tests.mixins.static
import tests.TestCase
import veb.deltafast.static as Static
import Trie
from word import word


class TreeTest(
    tests.TestCase.TestCase,
    tests.mixins.static.ReferenceTreeTestMixin,
    tests.mixins.TreeTestMixin
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

    def test_depth(self):
        trie = self.new_trie(16)
        self.assertEqual(14, trie._depth(0))
        self.assertEqual(12, trie._depth(1))
        self.assertEqual(0, trie._depth(2))

        trie = self.new_trie(8)
        self.assertEqual(6, trie._depth(0))
        self.assertEqual(4, trie._depth(1))
        self.assertEqual(0, trie._depth(2))

    def test_depths(self):
        trie = self.new_trie(16)

        q = word(0b0011111011101110, 16)
        depths = list(trie._depths(q))
        expect = [q.split_fst(14), q.split_fst(12), word.epsilon]

        self.assertEqual(depths, expect)

        q = word(0b0011010111010001, 16)
        depths = list(trie._depths(q))
        expect = [q.split_fst(14), q.split_fst(12), word.epsilon]

        self.assertEqual(depths, expect)

        #
        trie = self.new_trie(8)

        q = word(0b00111110, 8)
        depths = list(trie._depths(q))
        expect = [q.split_fst(6), q.split_fst(4), word.epsilon]

        self.assertEqual(depths, expect)

        q = word(0b00110101, 8)
        depths = list(trie._depths(q))
        expect = [q.split_fst(6), q.split_fst(4), word.epsilon]

        self.assertEqual(depths, expect)

    def test_insert(self):

        xs = [0b0011111011101110]
        trie = self.new_trie(16, xs)
        T = trie.T_d

        self.assertHash(T, word(0b00111110111011, 14), trie.root)
        self.assertHash(T, word(0b001111101110, 12), trie.root)
        self.assertHash(T, word.epsilon, trie.root)
        self.assertEqual(len(T), 0)

        #
        # #
        # # #
        xs = [0b0011111011101110, 0b0011110111001110]
        trie = self.new_trie(16, xs)
        T = trie.T_d

        self.assertHash(T, word.epsilon, trie.root)

        self.assertHash(T, word(0b00111110111011, 14), trie.root.left)
        self.assertHash(T, word(0b001111101110, 12), trie.root.left)

        self.assertHash(T, word(0b00111101110011, 14), trie.root.left)
        self.assertHash(T, word(0b001111011100, 12), trie.root.left)

        self.assertEqual(len(T), 0)

        #
        # #
        # # #
        xs = [
            0b0000011110101100, 0b0000101001001101, 0b0000101100001000,
            0b0001010010110101, 0b0001101011100100, 0b0010001001100001,
            0b0010011101100011, 0b0011101101101101, 0b0100000010000111,
            0b0100010000000101, 0b0101010100000001, 0b0101010100110111,
            0b0101101000111011, 0b0110000011111000, 0b0110100011010001,
            0b0110100100101001, 0b0111100011011101, 0b0111101010010111,
            0b0111111000000010, 0b1000001010000011, 0b1000100100010011,
            0b1000111001111010, 0b1000111001111101, 0b1010101101011110,
            0b1010110101110010, 0b1010110101110100, 0b1010110101110111,
            0b1011000111100100, 0b1100101010101110, 0b1100110011100000,
            0b1110001101101010, 0b1110110010010001, 0b1111100110110010
        ]

        trie = self.new_trie(16, xs)
        T = trie.T_d

        self.assertHash(T, word.epsilon, trie.root)

        self.assertHash(T, word(0b00000111101011, 14), trie.root.left.left.left.left)
        self.assertHash(T, word(0b000001111010, 12), trie.root.left.left.left.left)

        self.assertHash(T, word(0b00001010010011, 14), trie.root.left.left.left.left.right)
        self.assertHash(T, word(0b000010100100, 12), trie.root.left.left.left.left.right)

        self.assertHash(T, word(0b00001011000010, 14), trie.root.left.left.left.left.right)
        self.assertHash(T, word(0b000010110000, 12), trie.root.left.left.left.left.right)

        self.assertHash(T, word(0b00010100101101, 14), trie.root.left.left.left.right)
        self.assertHash(T, word(0b000101001011, 12), trie.root.left.left.left.right)

        self.assertHash(T, word(0b00011010111001, 14), trie.root.left.left.left.right)
        self.assertHash(T, word(0b000110101110, 12), trie.root.left.left.left.right)

        self.assertHash(T, word(0b00100010011000, 14), trie.root.left.left.right.left)
        self.assertHash(T, word(0b001000100110, 12), trie.root.left.left.right.left)

        self.assertHash(T, word(0b00100111011000, 14), trie.root.left.left.right.left)
        self.assertHash(T, word(0b001001110110, 12), trie.root.left.left.right.left)

        self.assertHash(T, word(0b00111011011011, 14), trie.root.left.left.right)
        self.assertHash(T, word(0b001110110110, 12), trie.root.left.left.right)

        self.assertHash(T, word(0b01000000100001, 14), trie.root.left.right.left.left)
        self.assertHash(T, word(0b010000001000, 12), trie.root.left.right.left.left)

        self.assertHash(T, word(0b01000100000001, 14), trie.root.left.right.left.left)
        self.assertHash(T, word(0b010001000000, 12), trie.root.left.right.left.left)

        self.assertHash(T, word(0b01010101000000, 14), trie.root.left.right.left.right.left)
        self.assertHash(T, word(0b010101010000, 12), trie.root.left.right.left.right.left)

        self.assertHash(T, word(0b01010101001101, 14), trie.root.left.right.left.right.left)
        self.assertHash(T, word(0b010101010011, 12), trie.root.left.right.left.right.left)

        self.assertHash(T, word(0b01011010001110, 14), trie.root.left.right.left.right)
        self.assertHash(T, word(0b010110100011, 12), trie.root.left.right.left.right)

        self.assertHash(T, word(0b01100000111110, 14), trie.root.left.right.right.left)
        self.assertHash(T, word(0b011000001111, 12), trie.root.left.right.right.left)

        self.assertHash(T, word(0b01101000110100, 14), trie.root.left.right.right.left.right)
        self.assertHash(T, word(0b011010001101, 12), trie.root.left.right.right.left.right)

        self.assertHash(T, word(0b01101001001010, 14), trie.root.left.right.right.left.right)
        self.assertHash(T, word(0b011010010010, 12), trie.root.left.right.right.left.right)

        self.assertHash(T, word(0b01111000110111, 14), trie.root.left.right.right.right.left)
        self.assertHash(T, word(0b011110001101, 12), trie.root.left.right.right.right.left)

        self.assertHash(T, word(0b01111010100101, 14), trie.root.left.right.right.right.left)
        self.assertHash(T, word(0b011110101001, 12), trie.root.left.right.right.right.left)

        self.assertHash(T, word(0b01111110000000, 14), trie.root.left.right.right.right)
        self.assertHash(T, word(0b011111100000, 12), trie.root.left.right.right.right)

        self.assertHash(T, word(0b10000010100000, 14), trie.root.right.left.left)
        self.assertHash(T, word(0b100000101000, 12), trie.root.right.left.left)

        self.assertHash(T, word(0b10001001000100, 14), trie.root.right.left.left.right)
        self.assertHash(T, word(0b100010010001, 12), trie.root.right.left.left.right)

        self.assertHash(T, word(0b10001110011110, 14), trie.root.right.left.left.right.right)
        self.assertHash(T, word(0b100011100111, 12), trie.root.right.left.left.right)

        self.assertHash(T, word(0b10001110011111, 14), trie.root.right.left.left.right.right)
        # self.assertHash(T, word(0b100011100111, 12), trie.root.right.left.left.right) duplcate

        self.assertHash(T, word(0b10101011010111, 14), trie.root.right.left.right.left)
        self.assertHash(T, word(0b101010110101, 12), trie.root.right.left.right.left)

        self.assertHash(T, word(0b10101101011100, 14), trie.root.right.left.right.left.right)
        self.assertHash(T, word(0b101011010111, 12), trie.root.right.left.right.left)

        self.assertHash(T, word(0b10101101011101, 14), trie.root.right.left.right.left.right)
        # self.assertHash(T, word(0b101011010111, 12), trie.root.right.left.right.left) duplicate

        # self.assertHash(T, word(0b10101101011101, 14), trie.root.right.left.right.left.right) duplicate
        # self.assertHash(T, word(0b101011010111, 12), trie.root.right.left.right.left) duplicate

        self.assertHash(T, word(0b10110001111001, 14), trie.root.right.left.right)
        self.assertHash(T, word(0b101100011110, 12), trie.root.right.left.right)

        self.assertHash(T, word(0b11001010101011, 14), trie.root.right.right.left)
        self.assertHash(T, word(0b110010101010, 12), trie.root.right.right.left)

        self.assertHash(T, word(0b11001100111000, 14), trie.root.right.right.left)
        self.assertHash(T, word(0b110011001110, 12), trie.root.right.right.left)

        self.assertHash(T, word(0b11100011011010, 14), trie.root.right.right.right.left)
        self.assertHash(T, word(0b111000110110, 12), trie.root.right.right.right.left)

        self.assertHash(T, word(0b11101100100100, 14), trie.root.right.right.right.left)
        self.assertHash(T, word(0b111011001001, 12), trie.root.right.right.right.left)

        self.assertHash(T, word(0b11111001101100, 14), trie.root.right.right.right)
        self.assertHash(T, word(0b111110011011, 12), trie.root.right.right.right)

        self.assertEqual(len(T), 0)

    def test_search_parameters(self):

        xs = [
            0b0111111000000010, 0b1000100100010011, 0b1010101101011110,
            0b1110110010010001, 0b1111100110110010, 0b0110000011111000,
            0b0000011110101100, 0b0101101000111011, 0b0111101010010111,
            0b0001010010110101, 0b0110100011010001, 0b0101010100000001,
            0b1100101010101110, 0b1110001101101010, 0b0010001001100001,
            0b0001101011100100, 0b0111100011011101, 0b0100000010000111,
            0b1100110011100000, 0b0101010100110111, 0b1000111001111010,
            0b0000101100001000, 0b1000001010000011, 0b0010011101100011,
            0b1010110101110111, 0b0110100100101001, 0b0011101101101101,
            0b0100010000000101, 0b0000101001001101, 0b1011000111100100,
            0b1010110101110100, 0b1010110101110010, 0b1000111001111101
        ]

        trie = self.new_trie(16, xs)
        q = word(0b1010110101110101, 16)

        # the same as a normal search start
        c = q.split_fst(0)
        lca, child, prefix, query, w = trie._search_parameters(q, c)

        self.assertEqual(lca, trie.root)
        self.assertEqual(child, trie.root.right)
        self.assertEqual(prefix, word.epsilon)
        self.assertEqual(query, q)
        self.assertEqual(w, 8)

        c = q.split_fst(12)
        lca, child, prefix, query, w = trie._search_parameters(q, c)

        self.assertEqual(lca, trie.root.right.left.right.left)
        self.assertEqual(prefix, q.split_fst(12))
        self.assertEqual(query, q.split_snd(12))
        self.assertEqual(w, 2)

        c = q.split_fst(14)
        lca, child, prefix, query, w = trie._search_parameters(q, c)

        self.assertEqual(lca, trie.root.right.left.right.left.right)
        self.assertEqual(prefix, q.split_fst(14))
        self.assertEqual(query, q.split_snd(14))
        self.assertEqual(w, 1)

        # different q
        q = word(0b1000111001111110, 16)

        c = q.split_fst(0)
        lca, child, prefix, query, w = trie._search_parameters(q, c)

        self.assertEqual(lca, trie.root)
        self.assertEqual(prefix, word.epsilon)
        self.assertEqual(query, q)
        self.assertEqual(w, 8)

        c = q.split_fst(12)
        lca, child, prefix, query, w = trie._search_parameters(q, c)

        self.assertEqual(lca, trie.root.right.left.left.right)
        self.assertEqual(prefix, q.split_fst(12))
        self.assertEqual(query, q.split_snd(12))
        self.assertEqual(w, 2)

        # an edge with a leaf assigns the key of the leaf
        c = q.split_fst(14)
        lca, child, prefix, query, w = trie._search_parameters(q, c)

        self.assertEqual(lca, trie.root.right.left.left.right.right)
        self.assertEqual(prefix, q.split_fst(14))
        self.assertEqual(query, q.split_snd(14))
        self.assertEqual(w, 1)

    def test_lowest_common_ancestor_start(self):

        xs = [
            0b0111111000000010, 0b1000100100010011, 0b1010101101011110,
            0b1110110010010001, 0b1111100110110010, 0b0110000011111000,
            0b0000011110101100, 0b0101101000111011, 0b0111101010010111,
            0b0001010010110101, 0b0110100011010001, 0b0101010100000001,
            0b1100101010101110, 0b1110001101101010, 0b0010001001100001,
            0b0001101011100100, 0b0111100011011101, 0b0100000010000111,
            0b1100110011100000, 0b0101010100110111, 0b1000111001111010,
            0b0000101100001000, 0b1000001010000011, 0b0010011101100011,
            0b1010110101110111, 0b0110100100101001, 0b0011101101101101,
            0b0100010000000101, 0b0000101001001101, 0b1011000111100100,
            0b1010110101110100, 0b1010110101110010, 0b1000111001111101
        ]

        trie = self.new_trie(16, xs)
        q = word(0b1010110101110101, 16)

        lca, child = trie.lowest_common_ancestor(q)
        expected_lca = trie.root.right.left.right.left.right.right
        expected_child = trie.root.right.left.right.left.right.right.left

        self.assertEqual(lca, expected_lca)
        self.assertEqual(child, expected_child)

        # the same as a normal search start
        c = q.split_fst(0)
        lca, child = trie.lowest_common_ancestor_start(q, c)

        self.assertEqual(lca, expected_lca)
        self.assertEqual(child, expected_child)

        c = q.split_fst(12)
        lca, child = trie.lowest_common_ancestor_start(q, c)

        self.assertEqual(lca, expected_lca)
        self.assertEqual(child, expected_child)

        c = q.split_fst(14)
        lca, child = trie.lowest_common_ancestor_start(q, c)

        self.assertEqual(lca, expected_lca)
        self.assertEqual(child, expected_child)

        #
        # different q
        #
        q = word(0b1000111001111110, 16)

        lca, child = trie.lowest_common_ancestor(q)
        expected_lca = trie.root.right.left.left.right.right
        expected_child = trie.root.right.left.left.right.right.right

        self.assertEqual(lca, expected_lca)
        self.assertEqual(child, expected_child)

        c = q.split_fst(0)
        lca, child = trie.lowest_common_ancestor_start(q, c)

        self.assertEqual(lca, expected_lca)
        self.assertEqual(child, expected_child)

        c = q.split_fst(12)
        lca, child = trie.lowest_common_ancestor_start(q, c)

        self.assertEqual(lca, expected_lca)
        self.assertEqual(child, expected_child)

        c = q.split_fst(14)
        lca, child = trie.lowest_common_ancestor_start(q, c)

        self.assertEqual(lca, expected_lca)
        self.assertEqual(child, expected_child)

    def test_predecessor_query_is_in_successor_tree(self):
        items = [41, 72, 110, 150, 210]

        trie = self.new_trie(8, items)

        result = trie.predecessor(90)
        expect = word(72, 8)
        self.assertEqual(result, expect)

if __name__ == '__main__':
    unittest.main()
