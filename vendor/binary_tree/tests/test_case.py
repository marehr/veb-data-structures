# coding=utf8

import unittest
import binary_tree
from mock import MagicMock

import sys
import random
import bisect

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

        def __init__(self, seed = None):
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

    class EmptyTestCase(unittest.TestCase):
        def runTest():
            pass

    class assertRootChange(object):
        """ Asserts that root#notify_root_change will be called with the right
        parameters. Also ensures that the observer will be called, therefore
        you have to give the observer as argument::

            with self.assertRootChange(old_root, new_root) as observer:
                cut, parent = node.cut(observer)

        You can also assert multiple root changes::

            with self.assertRootChange(old_root, node1, node2) as observer:
                node1.split(None, observer)
                node2.split(None, observer)

        Means that old_root changed to node1 and after that node1 changed to node2

        Note::

            If new_root is the same as the current root it will be asserted that
            notify_root_change WASN'T called
        """
        def __init__(self, old_root, new_root, *new_roots):
            self.old_root = old_root
            self.new_roots = [new_root] + list(new_roots)

            # mock roots
            for root in [old_root] + self.new_roots[:-1]:
                root.notify_root_change = MagicMock()

        def root_changed(self, old_root, new_root):
            pass

        def __enter__(self):
            return self

        def __exit__(self, type, value, traceback):
            method = self.old_root.notify_root_change

            if len(self.new_roots) == 1 and self.old_root is self.new_roots[0]:
                test = TestCase.EmptyTestCase('runTest')
                test.assertFalse(method.called)
                return

            # assert that all root changes where called
            for new_root in self.new_roots:
                method.assert_called_with(new_root, self)
                method = new_root and new_root.notify_root_change

    class assertNoRootChange(assertRootChange):
        def __init__(self, root):
            super(TestCase.assertNoRootChange, self).__init__(root, root)

    def createNode(self, key):
        return binary_tree.Node(key)

    def createTree(self, elements, root = None):
        """ Construct a binary tree using the elements given by preorder traversal

        That means
        ```self.createTree(tree.preorder())``` creates the same tree
        """
        if elements == []:
            return root

        head, tail = elements[0], elements[1:]

        if root is None:
            root = self.createNode(head)

            self.createTree(tail, root)
            return root

        insert = self.createNode(head)

        # binary search the correct place to insert the node `insert`
        current = root
        while current is not None:
            current, prev = current.child(head), current

        prev.set_child(insert)
        insert.update_height()
        return self.createTree(tail, root)

    def createAVLTree(self, elements):
        bsb = binary_tree.BinaryTree(elements)
        return bsb.root

    def assertEqualNode(self, node1, node2):
        self.assertEqual(node1.key, node2.key)
        self.assertEqual(node1.size, node2.size)
        self.assertEqual(node1.height, node2.height)

    def assertEqualTree(self, tree1, tree2):
        if tree1 is None or tree2 is None:
            self.assertEqual(tree1, None)
            self.assertEqual(tree2, None)
            return

        # assert same properties
        self.assertEqualNode(tree1, tree2)

        # assert same parent value
        if tree1.parent is None or tree2.parent is None:
            self.assertEqual(tree1.parent, None)
            self.assertEqual(tree2.parent, None)
        else:
            self.assertEqual(tree1.parent.key, tree2.parent.key)

        # assert same subtrees
        self.assertEqualTree(tree1.left_child, tree2.left_child)
        self.assertEqualTree(tree1.right_child, tree2.right_child)

    def _in_range(self, value, min_, max_):
        """ Check min_ <= value <= max_, where
        min_ = -infty if min_ is None
        max_ = +infty if max_ is None
        """
        result = True
        if min_ is not None:
            result = result and min_ <= value
        if max_ is not None:
            result = result and value <= max_
        return result

    def assertTreeStructure(self, tree, min_ = None, max_ = None):
        if tree is None:
            return

        # assert that the key is in the right order
        self.assertTrue(self._in_range(tree.key, min_, max_))

        # assert height
        expect = tree.height
        result = tree.max_child_height() + 1
        self.assertEqual(expect, result)

        # assert size
        result = tree._size()
        self.assertEqual(tree.size, result)

        # assert no cycles
        self.assertIsNot(tree.left_child, tree)
        self.assertIsNot(tree.right_child, tree)

        if tree.left_child is not None:
            self.assertIs(tree, tree.left_child.parent)
            self.assertTreeStructure(tree.left_child, min_, tree.key)

        if tree.right_child is not None:
            self.assertIs(tree, tree.right_child.parent)
            self.assertTreeStructure(tree.right_child, tree.key, max_)

    def assertBalanced(self, tree):
        if tree is None:
            return

        # assert height
        result = tree.max_child_height() + 1
        self.assertEqual(tree.height, result)

        # assert balance
        self.assertTrue(-1 <= tree.weigh() <= 1)

        self.assertBalanced(tree.left_child)
        self.assertBalanced(tree.right_child)

    def assertAVLTree(self, tree):
        self.assertTreeStructure(tree)
        self.assertBalanced(tree)

    def getElements(self, tree):
        bsb = binary_tree.BinaryTree()
        bsb.root = tree
        return bsb.as_list(1)

    def assertTreeContains(self, tree, elements):
        ys = list(elements)
        ys.sort()

        xs = self.getElements(tree)
        self.assertEqual(xs, ys)

    def predecessor(self, xs, q):
        """ Find rightmost value less than x
        """
        i = bisect.bisect_left(xs, q)
        if i:
            return xs[i-1]

        return None

    def successor(self, xs, q):
        """ Find leftmost value greater than q
        """
        i = bisect.bisect_right(xs, q)
        if i != len(xs):
            return xs[i]

        return None
