# coding=utf8

import unittest

import tests.mixins
import tests.TestCase
import veb.zfast.dynamic as Dynamic


class NodeTest(
    tests.TestCase.TestCase,
    tests.mixins.NodeTestMixin,
    tests.mixins.VebSlickDynamicTestMixin
):

    def new_trie(self, word_size, elements=[]):
        trie = Dynamic.Tree(word_size)
        trie.extend(elements)
        return trie

if __name__ == '__main__':
    unittest.main()
