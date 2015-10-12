# coding=utf8

import unittest
from tango_tree import Node as TangoNode
import binary_tree.tests.test_case as test_case

class TangoNodeTest(test_case.TestCase):

    def createNode(self, key, depth = None):
        return TangoNode(key, depth)

    def assertEqualNode(self, node1, node2):
        super(TangoNodeTest, self).assertEqualNode(node1, node2)

        self.assertEqual(node1.depth, node2.depth)
        self.assertEqual(node1.min_depth, node2.min_depth)
        self.assertEqual(node1.max_depth, node2.max_depth)

    def createTangoTreeBySearchPath(self, elements):
        root = None
        for i, key in enumerate(elements):
            new_node = self.createNode(key, i)
            if root is None:
                root = new_node
            else:
                root.insert(new_node, None)
            root = root.root()

        return root

    def createTangoTree(self, elements_with_depth):
        root = None
        for key, depth in elements_with_depth:
            new_node = self.createNode(key, depth)

            if root is None:
                root = new_node
                continue

            root.search(key).set_child(new_node)
            new_node.update_height()
        return root

    def randomTreePath(self, random, min_depth, max_depth):
        """ Creates a random path-to-leaf subpath in a perfect balanced binary tree
        """
        elements = []

        current = base = 1 << max(0, (max_depth-1))

        for depth in xrange(max_depth):
            if depth >= min_depth:
                elements.append(current)

            base = base // 2

            left = bool(random.randint(0,1))
            if left:
                current = current - base
            else:
                current = current + base

        return elements

    def min_atleast_depth(self, tree, depth):
        """ Reference implementation
        """
        current = tree.root().min()
        while current and current.depth < depth:
            current = current.next()

        if current and current.depth >= depth:
            return current
        return None

    def max_atleast_depth(self, tree, depth):
        """ Reference implementation
        """
        current = tree.root().max()
        while current and current.depth < depth:
            current = current.previous()

        if current and current.depth >= depth:
            return current
        return None

    def test_atleast_max_depth(self):
        node = TangoNode(5, 8)

        self.assertIs(node.node_atleast_max_depth(node, 5), node)
        self.assertIs(node.node_atleast_max_depth(node, 8), node)

        self.assertIsNone(node.node_atleast_max_depth(node, 12))
        self.assertIsNone(node.node_atleast_max_depth(None, 5))

    def test_min_atleast_depth(self):
        # single node
        node = TangoNode(5, 8)

        minimum = node.min_atleast_depth(8)
        self.assertIs(minimum, node)

        minimum = node.min_atleast_depth(9)
        self.assertIsNone(minimum)

        #
        xs = [(15, 1), (7, 2), (8, 3), (10, 4), (23, 5), (22, 6), (24, 7), (37, 8), (30, 10), (28, 0), (29, 9), (38, 11)]
        root = self.createTangoTree(xs)

        minimum = root.min_atleast_depth(12)
        self.assertIsNone(minimum)

        minimum = root.min_atleast_depth(11)
        self.assertEqual(minimum.key, 38)

        minimum = root.min_atleast_depth(10)
        self.assertEqual(minimum.key, 30)

        minimum = root.min_atleast_depth(9)
        self.assertEqual(minimum.key, 29)

        minimum = root.min_atleast_depth(8)
        self.assertEqual(minimum.key, 29)

        minimum = root.min_atleast_depth(7)
        self.assertEqual(minimum.key, 24)

        minimum = root.min_atleast_depth(6)
        self.assertEqual(minimum.key, 22)

        minimum = root.min_atleast_depth(5)
        self.assertEqual(minimum.key, 22)

        minimum = root.min_atleast_depth(4)
        self.assertEqual(minimum.key, 10)

        minimum = root.min_atleast_depth(3)
        self.assertEqual(minimum.key, 8)

        minimum = root.min_atleast_depth(2)
        self.assertEqual(minimum.key, 7)

        minimum = root.min_atleast_depth(1)
        self.assertEqual(minimum.key, 7)

        minimum = root.min_atleast_depth(0)
        self.assertEqual(minimum.key, 7)

    def test_max_atleast_depth(self):
        # single node
        node = TangoNode(5, 8)

        minimum = node.max_atleast_depth(8)
        self.assertIs(minimum, node)

        minimum = node.max_atleast_depth(9)
        self.assertIsNone(minimum)

        #
        xs = [(9, 1), (12, 2), (11, 3), (10, 4), (7, 5), (8, 6), (6, 7), (2, 8), (3, 10), (5, 0), (4, 9), (1, 11)]
        root = self.createTangoTree(xs)

        maximum = root.max_atleast_depth(12)
        self.assertIsNone(maximum)

        maximum = root.max_atleast_depth(11)
        self.assertEqual(maximum.key, 1)

        maximum = root.max_atleast_depth(10)
        self.assertEqual(maximum.key, 3)

        maximum = root.max_atleast_depth(9)
        self.assertEqual(maximum.key, 4)

        maximum = root.max_atleast_depth(8)
        self.assertEqual(maximum.key, 4)

        maximum = root.max_atleast_depth(7)
        self.assertEqual(maximum.key, 6)

        maximum = root.max_atleast_depth(6)
        self.assertEqual(maximum.key, 8)

        maximum = root.max_atleast_depth(5)
        self.assertEqual(maximum.key, 8)

        maximum = root.max_atleast_depth(4)
        self.assertEqual(maximum.key, 10)

        maximum = root.max_atleast_depth(3)
        self.assertEqual(maximum.key, 11)

        maximum = root.max_atleast_depth(2)
        self.assertEqual(maximum.key, 12)

        maximum = root.max_atleast_depth(1)
        self.assertEqual(maximum.key, 12)

        maximum = root.max_atleast_depth(0)
        self.assertEqual(maximum.key, 12)

    def test_random_min_max_atleast_depth(self):
        with self.random() as random:
            # draw k values out of the range [0, 50000)
            k = random.randint(1, 20000)
            samples = random.sample(xrange(50000), k)
            depth = random.randint(0, k+1)

            tree = self.createTangoTreeBySearchPath(samples)

            min_expected = self.min_atleast_depth(tree, depth)
            max_expected = self.max_atleast_depth(tree, depth)

            min_result = tree.min_atleast_depth(depth)
            max_result = tree.max_atleast_depth(depth)

            self.assertIs(min_result, min_expected)
            self.assertIs(max_result, max_expected)

    def test_cut_at_depth(self):
        # left empty path
        lesser_path = []
        greater_path = [500, 400, 300, 200, 0, 100, 150, 175]
        path = lesser_path + greater_path

        tree = self.createTangoTreeBySearchPath(path)

        with self.assertNoRootChange(tree):
            tree1, tree2 = tree.cut_at_depth(0)

        self.assertAVLTree(tree1)
        self.assertAVLTree(tree2)

        lesser_path.sort()
        greater_path.sort()

        self.assertIsNone(tree1)
        self.assertEqual(self.getElements(tree1), lesser_path)
        self.assertEqual(self.getElements(tree2), greater_path)

        # right empty path
        lesser_path = [500, 400, 300, 200, 0, 100, 150, 175]
        greater_path = []
        path = lesser_path + greater_path

        tree = self.createTangoTreeBySearchPath(path)

        with self.assertNoRootChange(tree):
            tree1, tree2 = tree.cut_at_depth(9)

        self.assertAVLTree(tree1)
        self.assertAVLTree(tree2)

        lesser_path.sort()
        greater_path.sort()

        self.assertIsNone(tree2)
        self.assertEqual(self.getElements(tree1), lesser_path)
        self.assertEqual(self.getElements(tree2), greater_path)

        # path >= depth is before 300
        lesser_path = [500, 400, 300]
        greater_path = [200, 0, 100, 150, 175]
        path = lesser_path + greater_path

        tree = self.createTangoTreeBySearchPath(path)

        with self.assertRootChange(tree, tree.find(300), tree.find(400)) as observer:
            tree1, tree2 = tree.cut_at_depth(3, observer)

        self.assertAVLTree(tree1)
        self.assertAVLTree(tree2)

        lesser_path.sort()
        greater_path.sort()

        self.assertEqual(self.getElements(tree1), lesser_path)
        self.assertEqual(self.getElements(tree2), greater_path)

        # path >= depth is after 300
        lesser_path = [100, 200, 300]
        greater_path = [350, 400, 375, 390, 380]
        path = lesser_path + greater_path

        tree = self.createTangoTreeBySearchPath(path)

        with self.assertRootChange(tree, tree.find(300), tree.find(200)) as observer:
            tree1, tree2 = tree.cut_at_depth(3, observer)

        self.assertAVLTree(tree1)
        self.assertAVLTree(tree2)

        lesser_path.sort()
        greater_path.sort()

        self.assertEqual(self.getElements(tree1), lesser_path)
        self.assertEqual(self.getElements(tree2), greater_path)

        # path >= depth is between 200 and 300
        lesser_path = [100, 200, 300]
        greater_path = [225, 250, 260, 280, 270]
        path = lesser_path + greater_path

        tree = self.createTangoTreeBySearchPath(path)

        with self.assertRootChange(tree, tree.find(200)) as observer:
            tree1, tree2 = tree.cut_at_depth(3, observer)

        self.assertAVLTree(tree1)
        self.assertAVLTree(tree2)

        lesser_path.sort()
        greater_path.sort()

        self.assertEqual(self.getElements(tree1), lesser_path)
        self.assertEqual(self.getElements(tree2), greater_path)

    def test_random_cut_at_depth(self):
        with self.random() as random:
            min_depth = random.randint(0, 5000)
            max_depth = random.randint(0, 10000)
            min_depth, max_depth = min(min_depth, max_depth), max(min_depth, max_depth)

            path = self.randomTreePath(random, min_depth, max_depth)
            if path == []:
                return

            # determine depth
            k = random.randint(0, len(path))

            lesser_path = path[:k]
            greater_path = path[k:]

            tree = self.createTangoTreeBySearchPath(path)
            tree1, tree2 = tree.cut_at_depth(k)

            self.assertAVLTree(tree1)
            self.assertAVLTree(tree2)

            lesser_path.sort()
            greater_path.sort()

            self.assertEqual(self.getElements(tree1), lesser_path)
            self.assertEqual(self.getElements(tree2), greater_path)

if __name__ == '__main__':
    unittest.main()
