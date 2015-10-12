# coding=utf8

import unittest

import tests.mixins.static
import tests.TestCase
import veb.mufast.static as Mihai
import Trie
from mock import MagicMock
from word import word


class TreeTest(
    tests.TestCase.TestCase,
    tests.mixins.TreeTestMixin,
    tests.mixins.static.ReferenceTreeTestMixin,
):

    def new_trie(self, word_size, elements=[]):
        trie = Mihai.Tree(word_size)
        trie.construct(elements)
        return trie

    def new_reference_trie(self, word_size, elements=[]):
        trie = Trie.Tree(word_size)
        trie.extend(elements)
        return trie

    def assertHash(self, T, hash_index, expect):
        self.assertEqual(T[hash_index], expect)
        del T[hash_index]

    def test_hash_table_at_depth_sqrt_log_u(self):
        trie = Mihai.Tree(16)
        trie._add_nodes_below_lca = MagicMock()
        trie._add_branch_node = MagicMock()
        trie.construct([
            0b0111111000000010, 0b1000100100010011, 0b1010101101011110,
            0b1110110010010001, 0b1111100110110010, 0b0110000011111000,
            0b0000011110101100, 0b0101101000111011, 0b0111101010010111,
            0b0001010010110101, 0b0110100011010001, 0b0101010100000001,
            0b1100101010101110, 0b1110001101101010, 0b0010001001100001,
            0b0001101011100100, 0b0111100011011101, 0b0100000010000111,
            0b1100110011100000, 0b0101010100110111, 0b1000111001111010,
            0b0000101100001000, 0b1000001010000011, 0b0010011101100011,
            0b1010110101110111, 0b0110100100101001, 0b0011101101101101,
            0b0100010000000101, 0b0000101001001101, 0b1011000111100100
        ])

        T = trie.T

        # is a branch node
        # self.assertHash(T, word.epsilon,             root)

        # is a branch node
        # self.assertHash(T, word(0b0000, 4),          root.left.left.left.left)
        self.assertHash(T, word(0b00000111, 8),      4)
        self.assertHash(T, word(0b000001111010, 12), 8)

        self.assertHash(T, word(0b00001010, 8),      1)
        self.assertHash(T, word(0b000010100100, 12), 5)

        self.assertHash(T, word(0b00001011, 8),      1)
        self.assertHash(T, word(0b000010110000, 12), 5)

        # is a branch node
        #self.assertHash(T, word(0b0001, 4),          root.left.left.left.right)
        self.assertHash(T, word(0b00010100, 8),      4)
        self.assertHash(T, word(0b000101001011, 12), 8)

        self.assertHash(T, word(0b00011010, 8),      4)
        self.assertHash(T, word(0b000110101110, 12), 8)

        self.assertHash(T, word(0b0010, 4),          1)
        self.assertHash(T, word(0b00100010, 8),      3)
        self.assertHash(T, word(0b001000100110, 12), 7)

        self.assertHash(T, word(0b00100111, 8),      3)
        self.assertHash(T, word(0b001001110110, 12), 7)

        self.assertHash(T, word(0b0011, 4),          1)
        self.assertHash(T, word(0b00111011, 8),      5)
        self.assertHash(T, word(0b001110110110, 12), 9)

        self.assertHash(T, word(0b0100, 4),          1)
        self.assertHash(T, word(0b01000000, 8),      3)
        self.assertHash(T, word(0b010000001000, 12), 7)

        self.assertHash(T, word(0b01000100, 8),      3)
        self.assertHash(T, word(0b010001000000, 12), 7)

        # is a branch node
        # self.assertHash(T, word(0b0101, 4),          root.left.right.left.right)
        self.assertHash(T, word(0b01010101, 8),      4)
        self.assertHash(T, word(0b010101010000, 12), 2)

        self.assertHash(T, word(0b010101010011, 12), 2)

        self.assertHash(T, word(0b01011010, 8),      4)
        self.assertHash(T, word(0b010110100011, 12), 8)

        # is a branch node
        #self.assertHash(T, word(0b0110, 4),          root.left.right.right.left)
        self.assertHash(T, word(0b01100000, 8),      4)
        self.assertHash(T, word(0b011000001111, 12), 8)

        self.assertHash(T, word(0b01101000, 8),      1)
        self.assertHash(T, word(0b011010001101, 12), 5)

        self.assertHash(T, word(0b01101001, 8),      1)
        self.assertHash(T, word(0b011010010010, 12), 5)

        self.assertHash(T, word(0b0111, 4),          1)
        self.assertHash(T, word(0b01111000, 8),      2)
        self.assertHash(T, word(0b011110001101, 12), 6)

        self.assertHash(T, word(0b01111010, 8),      2)
        self.assertHash(T, word(0b011110101001, 12), 6)

        self.assertHash(T, word(0b01111110, 8),      3)
        self.assertHash(T, word(0b011111100000, 12), 7)

        # is a branch node
        # self.assertHash(T, word(0b1000, 4),          root.right.left.left)
        self.assertHash(T, word(0b10000010, 8),      4)
        self.assertHash(T, word(0b100000101000, 12), 8)

        self.assertHash(T, word(0b10001001, 8),      3)
        self.assertHash(T, word(0b100010010001, 12), 7)

        self.assertHash(T, word(0b10001110, 8),      3)
        self.assertHash(T, word(0b100011100111, 12), 7)

        self.assertHash(T, word(0b1010, 4),          1)
        self.assertHash(T, word(0b10101011, 8),      3)
        self.assertHash(T, word(0b101010110101, 12), 7)

        self.assertHash(T, word(0b10101101, 8),      3)
        self.assertHash(T, word(0b101011010111, 12), 7)

        self.assertHash(T, word(0b1011, 4),          1)
        self.assertHash(T, word(0b10110001, 8),      5)
        self.assertHash(T, word(0b101100011110, 12), 9)

        self.assertHash(T, word(0b1100, 4),          2)
        self.assertHash(T, word(0b11001010, 8),      3)
        self.assertHash(T, word(0b110010101010, 12), 7)

        self.assertHash(T, word(0b11001100, 8),      3)
        self.assertHash(T, word(0b110011001110, 12), 7)

        # is a branch node
        # self.assertHash(T, word(0b1110, 4),          root.right.right.right.left)

        self.assertHash(T, word(0b11100011, 8),      4)
        self.assertHash(T, word(0b111000110110, 12), 8)

        self.assertHash(T, word(0b11101100, 8),      4)
        self.assertHash(T, word(0b111011001001, 12), 8)

        self.assertHash(T, word(0b1111, 4),          1)
        self.assertHash(T, word(0b11111001, 8),      5)
        self.assertHash(T, word(0b111110011011, 12), 9)

        self.assertEqual(len(T), 0)

    def test_hash_table_below_lca_sqrt_log_u(self):
        trie = Mihai.Tree(16)
        trie._add_nodes_at_sqrt_log_u = MagicMock()
        trie._add_branch_node = MagicMock()
        trie.construct([
            0b0111111000000010, 0b1000100100010011, 0b1010101101011110,
            0b1110110010010001, 0b1111100110110010, 0b0110000011111000,
            0b0000011110101100, 0b0101101000111011, 0b0111101010010111,
            0b0001010010110101, 0b0110100011010001, 0b0101010100000001,
            0b1100101010101110, 0b1110001101101010, 0b0010001001100001,
            0b0001101011100100, 0b0111100011011101, 0b0100000010000111,
            0b1100110011100000, 0b0101010100110111, 0b1000111001111010,
            0b0000101100001000, 0b1000001010000011, 0b0010011101100011,
            0b1010110101110111, 0b0110100100101001, 0b0011101101101101,
            0b0100010000000101, 0b0000101001001101, 0b1011000111100100
        ])

        T = trie.T
        root = trie.root

        self.assertHash(T, word(0b00000, 5), 1)
        self.assertHash(T, word(0b000001, 6), 2)
        self.assertHash(T, word(0b0000011, 7), 3)
        self.assertHash(T, word(0b00000111, 8), 4)

        self.assertHash(T, word(0b00001, 5), 1)
        self.assertHash(T, word(0b000010, 6), 2)

        self.assertHash(T, word(0b00001010, 8), 1)
        self.assertHash(T, word(0b000010100, 9), 2)
        self.assertHash(T, word(0b0000101001, 10), 3)
        self.assertHash(T, word(0b00001010010, 11), 4)

        self.assertHash(T, word(0b00001011, 8), 1)
        self.assertHash(T, word(0b000010110, 9), 2)
        self.assertHash(T, word(0b0000101100, 10), 3)
        self.assertHash(T, word(0b00001011000, 11), 4)

        self.assertHash(T, word(0b00010, 5), 1)
        self.assertHash(T, word(0b000101, 6), 2)
        self.assertHash(T, word(0b0001010, 7), 3)
        self.assertHash(T, word(0b00010100, 8), 4)

        self.assertHash(T, word(0b00011, 5), 1)
        self.assertHash(T, word(0b000110, 6), 2)
        self.assertHash(T, word(0b0001101, 7), 3)
        self.assertHash(T, word(0b00011010, 8), 4)

        self.assertHash(T, word(0b0010, 4), 1)

        self.assertHash(T, word(0b001000, 6), 1)
        self.assertHash(T, word(0b0010001, 7), 2)
        self.assertHash(T, word(0b00100010, 8), 3)
        self.assertHash(T, word(0b001000100, 9), 4)

        self.assertHash(T, word(0b001001, 6), 1)
        self.assertHash(T, word(0b0010011, 7), 2)
        self.assertHash(T, word(0b00100111, 8), 3)
        self.assertHash(T, word(0b001001110, 9), 4)

        self.assertHash(T, word(0b0011, 4), 1)
        self.assertHash(T, word(0b00111, 5), 2)
        self.assertHash(T, word(0b001110, 6), 3)
        self.assertHash(T, word(0b0011101, 7), 4)

        self.assertHash(T, word(0b0100, 4), 1)

        self.assertHash(T, word(0b010000, 6), 1)
        self.assertHash(T, word(0b0100000, 7), 2)
        self.assertHash(T, word(0b01000000, 8), 3)
        self.assertHash(T, word(0b010000001, 9), 4)

        self.assertHash(T, word(0b010001, 6), 1)
        self.assertHash(T, word(0b0100010, 7), 2)
        self.assertHash(T, word(0b01000100, 8), 3)
        self.assertHash(T, word(0b010001000, 9), 4)

        self.assertHash(T, word(0b01010, 5), 1)
        self.assertHash(T, word(0b010101, 6), 2)
        self.assertHash(T, word(0b0101010, 7), 3)
        self.assertHash(T, word(0b01010101, 8), 4)

        self.assertHash(T, word(0b01010101000, 11), 1)
        self.assertHash(T, word(0b010101010000, 12), 2)
        self.assertHash(T, word(0b0101010100000, 13), 3)
        self.assertHash(T, word(0b01010101000000, 14), 4)

        self.assertHash(T, word(0b01010101001, 11), 1)
        self.assertHash(T, word(0b010101010011, 12), 2)
        self.assertHash(T, word(0b0101010100110, 13), 3)
        self.assertHash(T, word(0b01010101001101, 14), 4)

        self.assertHash(T, word(0b01011, 5), 1)
        self.assertHash(T, word(0b010110, 6), 2)
        self.assertHash(T, word(0b0101101, 7), 3)
        self.assertHash(T, word(0b01011010, 8), 4)

        self.assertHash(T, word(0b01100, 5), 1)
        self.assertHash(T, word(0b011000, 6), 2)
        self.assertHash(T, word(0b0110000, 7), 3)
        self.assertHash(T, word(0b01100000, 8), 4)

        self.assertHash(T, word(0b01101, 5), 1)
        self.assertHash(T, word(0b011010, 6), 2)

        self.assertHash(T, word(0b01101000, 8), 1)
        self.assertHash(T, word(0b011010001, 9), 2)
        self.assertHash(T, word(0b0110100011, 10), 3)
        self.assertHash(T, word(0b01101000110, 11), 4)

        self.assertHash(T, word(0b01101001, 8), 1)
        self.assertHash(T, word(0b011010010, 9), 2)
        self.assertHash(T, word(0b0110100100, 10), 3)
        self.assertHash(T, word(0b01101001001, 11), 4)

        self.assertHash(T, word(0b0111, 4), 1)

        self.assertHash(T, word(0b0111100, 7), 1)
        self.assertHash(T, word(0b01111000, 8), 2)
        self.assertHash(T, word(0b011110001, 9), 3)
        self.assertHash(T, word(0b0111100011, 10), 4)

        self.assertHash(T, word(0b0111101, 7), 1)
        self.assertHash(T, word(0b01111010, 8), 2)
        self.assertHash(T, word(0b011110101, 9), 3)
        self.assertHash(T, word(0b0111101010, 10), 4)

        self.assertHash(T, word(0b011111, 6), 1)
        self.assertHash(T, word(0b0111111, 7), 2)
        self.assertHash(T, word(0b01111110, 8), 3)
        self.assertHash(T, word(0b011111100, 9), 4)

        self.assertHash(T, word(0b100, 3), 1)

        self.assertHash(T, word(0b10000, 5), 1)
        self.assertHash(T, word(0b100000, 6), 2)
        self.assertHash(T, word(0b1000001, 7), 3)
        self.assertHash(T, word(0b10000010, 8), 4)

        self.assertHash(T, word(0b100010, 6), 1)
        self.assertHash(T, word(0b1000100, 7), 2)
        self.assertHash(T, word(0b10001001, 8), 3)
        self.assertHash(T, word(0b100010010, 9), 4)

        self.assertHash(T, word(0b100011, 6), 1)
        self.assertHash(T, word(0b1000111, 7), 2)
        self.assertHash(T, word(0b10001110, 8), 3)
        self.assertHash(T, word(0b100011100, 9), 4)

        self.assertHash(T, word(0b1010, 4), 1)

        self.assertHash(T, word(0b101010, 6), 1)
        self.assertHash(T, word(0b1010101, 7), 2)
        self.assertHash(T, word(0b10101011, 8), 3)
        self.assertHash(T, word(0b101010110, 9), 4)

        self.assertHash(T, word(0b101011, 6), 1)
        self.assertHash(T, word(0b1010110, 7), 2)
        self.assertHash(T, word(0b10101101, 8), 3)
        self.assertHash(T, word(0b101011010, 9), 4)

        self.assertHash(T, word(0b1011, 4), 1)
        self.assertHash(T, word(0b10110, 5), 2)
        self.assertHash(T, word(0b101100, 6), 3)
        self.assertHash(T, word(0b1011000, 7), 4)

        self.assertHash(T, word(0b110, 3), 1)
        self.assertHash(T, word(0b1100, 4), 2)

        self.assertHash(T, word(0b110010, 6), 1)
        self.assertHash(T, word(0b1100101, 7), 2)
        self.assertHash(T, word(0b11001010, 8), 3)
        self.assertHash(T, word(0b110010101, 9), 4)

        self.assertHash(T, word(0b110011, 6), 1)
        self.assertHash(T, word(0b1100110, 7), 2)
        self.assertHash(T, word(0b11001100, 8), 3)
        self.assertHash(T, word(0b110011001, 9), 4)

        self.assertHash(T, word(0b11100, 5), 1)
        self.assertHash(T, word(0b111000, 6), 2)
        self.assertHash(T, word(0b1110001, 7), 3)
        self.assertHash(T, word(0b11100011, 8), 4)

        self.assertHash(T, word(0b11101, 5), 1)
        self.assertHash(T, word(0b111011, 6), 2)
        self.assertHash(T, word(0b1110110, 7), 3)
        self.assertHash(T, word(0b11101100, 8), 4)

        self.assertHash(T, word(0b1111, 4), 1)
        self.assertHash(T, word(0b11111, 5), 2)
        self.assertHash(T, word(0b111110, 6), 3)
        self.assertHash(T, word(0b1111100, 7), 4)

        self.assertEqual(len(T), 0)

    def test_hash_table_add_branch_nodes(self):
        trie = Mihai.Tree(16)
        trie._add_nodes_at_sqrt_log_u = MagicMock()
        trie._add_nodes_below_lca = MagicMock()
        trie.construct([
            0b0111111000000010, 0b1000100100010011, 0b1010101101011110,
            0b1110110010010001, 0b1111100110110010, 0b0110000011111000,
            0b0000011110101100, 0b0101101000111011, 0b0111101010010111,
            0b0001010010110101, 0b0110100011010001, 0b0101010100000001,
            0b1100101010101110, 0b1110001101101010, 0b0010001001100001,
            0b0001101011100100, 0b0111100011011101, 0b0100000010000111,
            0b1100110011100000, 0b0101010100110111, 0b1000111001111010,
            0b0000101100001000, 0b1000001010000011, 0b0010011101100011,
            0b1010110101110111, 0b0110100100101001, 0b0011101101101101,
            0b0100010000000101, 0b0000101001001101, 0b1011000111100100
        ])

        T = trie.T_lcas
        root = trie.root

        self.assertHash(T, word.epsilon, root)
        self.assertHash(T, word(0b0, 1), root.left)
        self.assertHash(T, word(0b00, 2), root.left.left)
        self.assertHash(T, word(0b000, 3), root.left.left.left)
        self.assertHash(T, word(0b0000, 4), root.left.left.left.left)
        self.assertHash(T, word(0b0000011110101100, 16), root.left.left.left.left.left)
        self.assertHash(T, word(0b0000101, 7), root.left.left.left.left.right)
        self.assertHash(T, word(0b0000101001001101, 16), root.left.left.left.left.right.left)
        self.assertHash(T, word(0b0000101100001000, 16), root.left.left.left.left.right.right)
        self.assertHash(T, word(0b0001, 4), root.left.left.left.right)
        self.assertHash(T, word(0b0001010010110101, 16), root.left.left.left.right.left)
        self.assertHash(T, word(0b0001101011100100, 16), root.left.left.left.right.right)
        self.assertHash(T, word(0b001, 3), root.left.left.right)
        self.assertHash(T, word(0b00100, 5), root.left.left.right.left)
        self.assertHash(T, word(0b0010001001100001, 16), root.left.left.right.left.left)
        self.assertHash(T, word(0b0010011101100011, 16), root.left.left.right.left.right)
        self.assertHash(T, word(0b0011101101101101, 16), root.left.left.right.right)
        self.assertHash(T, word(0b01, 2), root.left.right)
        self.assertHash(T, word(0b010, 3), root.left.right.left)
        self.assertHash(T, word(0b01000, 5), root.left.right.left.left)
        self.assertHash(T, word(0b0100000010000111, 16), root.left.right.left.left.left)
        self.assertHash(T, word(0b0100010000000101, 16), root.left.right.left.left.right)
        self.assertHash(T, word(0b0101, 4), root.left.right.left.right)
        self.assertHash(T, word(0b0101010100, 10), root.left.right.left.right.left)
        self.assertHash(T, word(0b0101010100000001, 16), root.left.right.left.right.left.left)
        self.assertHash(T, word(0b0101010100110111, 16), root.left.right.left.right.left.right)
        self.assertHash(T, word(0b0101101000111011, 16), root.left.right.left.right.right)
        self.assertHash(T, word(0b011, 3), root.left.right.right)
        self.assertHash(T, word(0b0110, 4), root.left.right.right.left)
        self.assertHash(T, word(0b0110000011111000, 16), root.left.right.right.left.left)
        self.assertHash(T, word(0b0110100, 7), root.left.right.right.left.right)
        self.assertHash(T, word(0b0110100011010001, 16), root.left.right.right.left.right.left)
        self.assertHash(T, word(0b0110100100101001, 16), root.left.right.right.left.right.right)
        self.assertHash(T, word(0b01111, 5), root.left.right.right.right)
        self.assertHash(T, word(0b011110, 6), root.left.right.right.right.left)
        self.assertHash(T, word(0b0111100011011101, 16), root.left.right.right.right.left.left)
        self.assertHash(T, word(0b0111101010010111, 16), root.left.right.right.right.left.right)
        self.assertHash(T, word(0b0111111000000010, 16), root.left.right.right.right.right)
        self.assertHash(T, word(0b1, 1), root.right)
        self.assertHash(T, word(0b10, 2), root.right.left)
        self.assertHash(T, word(0b1000, 4), root.right.left.left)
        self.assertHash(T, word(0b1000001010000011, 16), root.right.left.left.left)
        self.assertHash(T, word(0b10001, 5), root.right.left.left.right)
        self.assertHash(T, word(0b1000100100010011, 16), root.right.left.left.right.left)
        self.assertHash(T, word(0b1000111001111010, 16), root.right.left.left.right.right)
        self.assertHash(T, word(0b101, 3), root.right.left.right)
        self.assertHash(T, word(0b10101, 5), root.right.left.right.left)
        self.assertHash(T, word(0b1010101101011110, 16), root.right.left.right.left.left)
        self.assertHash(T, word(0b1010110101110111, 16), root.right.left.right.left.right)
        self.assertHash(T, word(0b1011000111100100, 16), root.right.left.right.right)
        self.assertHash(T, word(0b11, 2), root.right.right)
        self.assertHash(T, word(0b11001, 5), root.right.right.left)
        self.assertHash(T, word(0b1100101010101110, 16), root.right.right.left.left)
        self.assertHash(T, word(0b1100110011100000, 16), root.right.right.left.right)
        self.assertHash(T, word(0b111, 3), root.right.right.right)
        self.assertHash(T, word(0b1110, 4), root.right.right.right.left)
        self.assertHash(T, word(0b1110001101101010, 16), root.right.right.right.left.left)
        self.assertHash(T, word(0b1110110010010001, 16), root.right.right.right.left.right)
        self.assertHash(T, word(0b1111100110110010, 16), root.right.right.right.right)

        self.assertEqual(len(T), 0)

    def test_search_phase_one(self):
        trie = Mihai.Tree(16)
        trie.construct([
            0b0111111000000010, 0b1000100100010011, 0b1010101101011110,
            0b1110110010010001, 0b1111100110110010, 0b0110000011111000,
            0b0000011110101100, 0b0101101000111011, 0b0111101010010111,
            0b0001010010110101, 0b0110100011010001, 0b0101010100000001,
            0b1100101010101110, 0b1110001101101010, 0b0010001001100001,
            0b0001101011100100, 0b0111100011011101, 0b0100000010000111,
            0b1100110011100000, 0b0101010100110111, 0b1000111001111010,
            0b0000101100001000, 0b1000001010000011, 0b0010011101100011,
            0b1010110101110111, 0b0110100100101001, 0b0011101101101101,
            0b0100010000000101, 0b0000101001001101, 0b1011000111100100
        ])

        q = word(0b1101110101100101, 16)
        index = trie._lca_search1(q, 0, 0, trie.sqrt_log_u - 1)
        self.assertEqual(index, 0)

        q = word(0b1001011010001001, 16)
        index = trie._lca_search1(q, 0, 0, trie.sqrt_log_u - 1)
        self.assertEqual(index, 0)

        q = word(0b1010100101111010, 16)
        index = trie._lca_search1(q, 0, 0, trie.sqrt_log_u - 1)
        self.assertEqual(index, 4)

        q = word(0b1010000010100001, 16)
        index = trie._lca_search1(q, 0, 0, trie.sqrt_log_u - 1)
        self.assertEqual(index, 4)

        q = word(0b1100101111111111, 16)
        index = trie._lca_search1(q, 0, 0, trie.sqrt_log_u - 1)
        self.assertEqual(index, 4)

        q = word(0b0110100011110001, 16)
        index = trie._lca_search1(q, 0, 0, trie.sqrt_log_u - 1)
        self.assertEqual(index, 8)

        q = word(0b0101010100000000, 16)
        index = trie._lca_search1(q, 0, 0, trie.sqrt_log_u - 1)
        self.assertEqual(index, 12)

        q = word(0b0000011110100101, 16)
        index = trie._lca_search1(q, 0, 0, trie.sqrt_log_u - 1)
        self.assertEqual(index, 12)

        q = word(0b0111111000000010, 16)
        index = trie._lca_search1(q, 0, 0, trie.sqrt_log_u)
        self.assertEqual(index, 16)

    def test_search_phase_two(self):
        trie = Mihai.Tree(16)
        trie.construct([
            0b0111111000000010, 0b1000100100010011, 0b1010101101011110,
            0b1110110010010001, 0b1111100110110010, 0b0110000011111000,
            0b0000011110101100, 0b0101101000111011, 0b0111101010010111,
            0b0001010010110101, 0b0110100011010001, 0b0101010100000001,
            0b1100101010101110, 0b1110001101101010, 0b0010001001100001,
            0b0001101011100100, 0b0111100011011101, 0b0100000010000111,
            0b1100110011100000, 0b0101010100110111, 0b1000111001111010,
            0b0000101100001000, 0b1000001010000011, 0b0010011101100011,
            0b1010110101110111, 0b0110100100101001, 0b0011101101101101,
            0b0100010000000101, 0b0000101001001101, 0b1011000111100100
        ])

        # q is below (u,v)
        q = word(0b1101110101100101, 16)
        index = trie._lca_search2(q, 2, 2, 4)
        self.assertEqual(index, 3)

        # q is in between (u,v)
        q = word(0b1000011010001001, 16)
        index = trie._lca_search2(q, 4, 4, 8)
        self.assertEqual(index, 5)

        # q is below (u,v)
        q = word(0b1010100101111010, 16)
        index = trie._lca_search2(q, 5, 5, 8)
        self.assertEqual(index, 6)

        # q is below (u,v)
        q = word(0b1100101111111111, 16)
        index = trie._lca_search2(q, 5, 5, 8)
        self.assertEqual(index, 7)

        # q is in between (u,v)
        q = word(0b1010000010100001, 16)
        index = trie._lca_search2(q, 4, 4, 8)
        self.assertEqual(index, 4)

        # q is in between (u,v)
        q = word(0b0110100011110001, 16)
        index = trie._lca_search2(q, 8, 8, 12)
        self.assertEqual(index, 10)

        # q is in between (u,v)
        q = word(0b0101010100000000, 16)
        index = trie._lca_search2(q, 12, 12, 16)
        self.assertEqual(index, 14)

        # q is in between (u,v)
        q = word(0b0000011110100101, 16)
        index = trie._lca_search2(q, 12, 12, 16)
        self.assertEqual(index, 12)

        # q is contained
        q = word(0b0111111000000010, 16)
        index = trie._lca_search2(q, 16, 16, 16)
        self.assertEqual(index, 16)

    def test_lowest_common_ancestor(self):
        trie = Mihai.Tree(16)
        trie.construct([
            0b0111111000000010, 0b1000100100010011, 0b1010101101011110,
            0b1110110010010001, 0b1111100110110010, 0b0110000011111000,
            0b0000011110101100, 0b0101101000111011, 0b0111101010010111,
            0b0001010010110101, 0b0110100011010001, 0b0101010100000001,
            0b1100101010101110, 0b1110001101101010, 0b0010001001100001,
            0b0001101011100100, 0b0111100011011101, 0b0100000010000111,
            0b1100110011100000, 0b0101010100110111, 0b1000111001111010,
            0b0000101100001000, 0b1000001010000011, 0b0010011101100011,
            0b1010110101110111, 0b0110100100101001, 0b0011101101101101,
            0b0100010000000101, 0b0000101001001101, 0b1011000111100100
        ])

        root = trie.root

        # q is below (u,v)
        q = word(0b1101110101100101, 16)
        lca, child = trie.lowest_common_ancestor(q)
        self.assertEqual(lca, root.right.right)
        self.assertEqual(child, root.right.right.left)

        # q is in between (u,v)
        q = word(0b1000011010001001, 16)
        lca, child = trie.lowest_common_ancestor(q)
        self.assertEqual(lca, root.right.left.left)
        self.assertEqual(child, root.right.left.left.left)

        # q is below (u,v)
        q = word(0b1010100101111010, 16)
        lca, child = trie.lowest_common_ancestor(q)
        self.assertEqual(lca, root.right.left.right.left)
        self.assertEqual(child, root.right.left.right.left.left)

        # q is below (u,v)
        q = word(0b1100101111111111, 16)
        lca, child = trie.lowest_common_ancestor(q)
        self.assertEqual(lca, root.right.right.left)
        self.assertEqual(child, root.right.right.left.left)

        # q is in between (u,v)
        q = word(0b1010000010100001, 16)
        lca, child = trie.lowest_common_ancestor(q)
        self.assertEqual(lca, root.right.left.right)
        self.assertEqual(child, root.right.left.right.left)

        # q is in between (u,v)
        q = word(0b0110100011110001, 16)
        lca, child = trie.lowest_common_ancestor(q)
        self.assertEqual(lca, root.left.right.right.left.right)
        self.assertEqual(child, root.left.right.right.left.right.left)

        # q is in between (u,v)
        q = word(0b0101010100000000, 16)
        lca, child = trie.lowest_common_ancestor(q)
        self.assertEqual(lca, root.left.right.left.right.left)
        self.assertEqual(child, root.left.right.left.right.left.left)

        # q is in between (u,v)
        q = word(0b0000011110100101, 16)
        lca, child = trie.lowest_common_ancestor(q)
        self.assertEqual(lca, root.left.left.left.left)
        self.assertEqual(child, root.left.left.left.left.left)

        # q is contained
        q = word(0b0111111000000010, 16)
        lca, child = trie.lowest_common_ancestor(q)
        self.assertEqual(lca, root.left.right.right.right.right)
        self.assertEqual(child, None)

    def test_lca_4159569830323394869(self):
        # with size = rand.randint(5, 15) and seed 4159569830323394869
        xs = [77, 180, 9, 102, 185, 249, 63, 158, 210, 89, 224, 240, 174, 236, 78]
        ref = self.new_reference_trie(8, xs)
        trie = self.new_trie(8, xs)

        q = word(79, 8)

        lca, child = ref.lowest_common_ancestor(q)
        self.assertEqual(lca, ref.root.left.right.left.left)
        self.assertEqual(child, ref.root.left.right.left.left.right)

        lca, child = trie.lowest_common_ancestor(q)
        self.assertEqual(lca, trie.root.left.right.left.left)
        self.assertEqual(child, trie.root.left.right.left.left.right)

if __name__ == '__main__':
    unittest.main()
