# coding=utf8

import unittest
import bisect
from word import word

import sys
import random


class TestCase(unittest.TestCase):

    class random(random.Random):
        """ Custom random, that will print the seed of random if any Exception
        occurs during a test.

        Usage::

            class Test(TestCase):
                def test_random(self):
                    with self.random() as random:
                        coin = random.randint(0, 1)

                        # this will eventually fail
                        self.assertTrue(bool(coin))

        Reproduce a testcase with a given seed::

            class Test(TestCase):
                def test_random(self):
                    seed = 8232198159120460518
                    with self.random(seed) as random:
                        coin = random.randint(0, 1)

                        # this will fail
                        self.assertTrue(bool(coin))

        will return::

            FAIL: test_random (__main__.Test)
            ----------------------------------------------------------------------
            Traceback (most recent call last):
                File "test.py", line 14, in test_random
                self.assertTrue(bool(coin))
            AssertionError: ('False is not true', 'random seed: 8232198159120460518')
        """

        def __init__(self, seed=None):
            if seed is None:
                self.__seed = random.randint(0, sys.maxint)
            else:
                self.__seed = seed
            super(TestCase.random, self).__init__(self.__seed)

        def __enter__(self):
            return self

        def __exit__(self, type, value, traceback):
            if isinstance(value, Exception):
                value.args += ("random seed: %s" % self.__seed,)

            return False

    def random_integers(self, low, high, size, random):
        return [random.randint(low, high) for x in xrange(size)]

    def data(self):
        return []

    def data_words(self, data=None, w=8):
        data = data if data is not None else self.data()

        return map(lambda x: word(x, w), data)

    def predecessor(self, xs, q):
        'Find rightmost value less than x'
        i = bisect.bisect_left(xs, q)
        if i:
            return xs[i-1]

        return None

    def successor(self, xs, q):
        'Find leftmost value greater than q'
        i = bisect.bisect_right(xs, q)
        if i != len(xs):
            return xs[i]

        return None

    def assertEqualNode(self, veb_node, ref_node):
        self.assertEqual(veb_node.key, ref_node.key)
        self.assertEqual(veb_node.edge, ref_node.edge)

    def assertEqualTree(self, veb_node, ref_node):
        if veb_node is None and ref_node is None:
            return
        elif veb_node is None or ref_node is None:
            self.fail("One Node is None but the other not")

        self.assertEqualNode(veb_node, ref_node)

        if veb_node.parent is None or ref_node.parent is None:
            self.assertIsNone(veb_node.parent)
            self.assertIsNone(ref_node.parent)

        # left node structure equals
        if veb_node.left is None or ref_node.left is None:
            self.assertIsNone(veb_node.left)
            self.assertIsNone(ref_node.left)
        else:
            self.assertEqual(veb_node, veb_node.left.parent)
            self.assertEqual(ref_node, ref_node.left.parent)

        # right node structure equals
        if veb_node.right is None or ref_node.right is None:
            self.assertIsNone(veb_node.right)
            self.assertIsNone(ref_node.right)
        else:
            self.assertEqual(veb_node, veb_node.right.parent)
            self.assertEqual(ref_node, ref_node.right.parent)

        self.assertEqualTree(veb_node.left, ref_node.left)
        self.assertEqualTree(veb_node.right, ref_node.right)

    def assertEqualHashTable(self, veb, ref):
        expected_table = ref.T
        result_table = veb.T

        for k in expected_table.keys():
            self.assertTrue(k in result_table, "%s should be contained in results" % k)
            self.assertEqual(expected_table[k], result_table[k])

        for k in result_table.keys():
            self.assertTrue(k in expected_table, "%s should be contained in expected" % k)
            self.assertEqual(result_table[k], expected_table[k])

    def assertEqualTrie(self, veb, ref):
        self.assertEqualTree(veb.root, ref.root)
