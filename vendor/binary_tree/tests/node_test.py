# coding=utf8

import unittest
import test_case
import binary_tree

class NodeTest(test_case.TestCase):

    def test_create_tree(self):
        root = self.createTree([10, 5, 2, 4, 6, 8])

        self.assertEqual(root.key, 10)
        self.assertEqual(root.left_child.key, 5)
        self.assertEqual(root.left_child.left_child.key, 2)
        self.assertEqual(root.left_child.right_child.key, 6)
        self.assertEqual(root.left_child.right_child.right_child.key, 8)

        self.assertEqual(root.size, 6)
        self.assertEqual(root.left_child.size, 5)
        self.assertEqual(root.left_child.left_child.size, 2)
        self.assertEqual(root.left_child.left_child.right_child.size, 1)
        self.assertEqual(root.left_child.right_child.size, 2)
        self.assertEqual(root.left_child.right_child.right_child.size, 1)

        bsb = binary_tree.BinaryTree()
        result = bsb.preorder(root)

        self.assertEqual(result, [10, 5, 2, 4, 6, 8])

    def test_iter(self):
        root = self.createTree([10, 5, 2, 4, 6, 8])

        # inorder list of nodes
        expect = [root.find(2), root.find(4), root.find(5), root.find(6), root.find(8), root.find(10)]
        nodes = list(root)

        self.assertEqual(nodes, expect)

        # inorder list of nodes in a subtree
        expect = [root.find(6), root.find(8)]
        nodes = list(root.find(6))

        self.assertEqual(nodes, expect)

    def test_set_child(self):
        root = binary_tree.Node(10)
        left = binary_tree.Node(5)
        left_left = binary_tree.Node(2)
        left_left2 = binary_tree.Node(4)
        left_right = binary_tree.Node(6)
        left_right_right = binary_tree.Node(8)

        result = root.set_child(left)
        self.assertEqual(result, None)

        result = left.set_child(left_left)
        self.assertEqual(result, None)

        result = left.set_child(left_right)
        self.assertEqual(result, None)

        result = left_right.set_child(left_right_right)
        self.assertEqual(result, None)

        self.assertEqual(root.left_child, left)
        self.assertEqual(root.right_child, None)
        self.assertEqual(root.left_child.left_child, left_left)
        self.assertEqual(root.left_child.right_child, left_right)
        self.assertEqual(root.left_child.right_child.right_child, left_right_right)


        # test the replacement of a node
        replaced = left.set_child(left_left2)
        self.assertEqual(replaced, left_left)
        self.assertEqual(root.left_child.left_child, left_left2)

        # replaced won't be fully detached
        self.assertEqual(replaced.parent, left)


        # test set child to None according to the key
        replaced = left.set_child(None, left_left2.key)
        self.assertEqual(replaced, left_left2)
        self.assertEqual(root.left_child.left_child, None)

    def test_swap(self):
        root = self.createTree([10, 5, 2, 4, 6, 8])

        node2 = root.left_child.left_child
        node4 = root.left_child.left_child.right_child
        node5 = root.left_child
        node6 = root.left_child.right_child
        node8 = root.left_child.right_child.right_child
        node10 = root

        node5.swap(node4)

        # node content is the same
        self.assertEqual(node4.key, 4)
        self.assertEqual(node5.key, 5)

        # augmented data is the same
        self.assertEqual(node4.height, 2)
        self.assertEqual(node5.height, 0)

        # tail endpoints adjacent to the node were updated
        self.assertIs(node4.parent, node10)
        self.assertIs(node4.left_child, node2)
        self.assertIs(node4.right_child, node6)

        self.assertIs(node5.parent, node2)
        self.assertIs(node5.left_child, None)
        self.assertIs(node5.right_child, None)

        # head endpoints adjacent to the node were updated
        self.assertIs(node10.left_child, node4)
        self.assertIs(node2.parent, node4)
        self.assertIs(node6.parent, node4)

        self.assertIs(node2.right_child, node5)


        # reswap the nodes
        node4.swap(node5)

        # node content is the same
        self.assertEqual(node4.key, 4)
        self.assertEqual(node5.key, 5)

        # augmented data is the same
        self.assertEqual(node4.height, 0)
        self.assertEqual(node5.height, 2)

        # tail endpoints adjacent to the node were updated
        self.assertIs(node5.parent, node10)
        self.assertIs(node5.left_child, node2)
        self.assertIs(node5.right_child, node6)

        self.assertIs(node4.parent, node2)
        self.assertIs(node4.left_child, None)
        self.assertIs(node4.right_child, None)

        # head endpoints adjacent to the node were updated
        self.assertIs(node10.left_child, node5)
        self.assertIs(node2.parent, node5)
        self.assertIs(node6.parent, node5)

        self.assertIs(node2.right_child, node4)


        # swap with possible cycles
        node6.swap(node5)

        # node content is the same
        self.assertEqual(node5.key, 5)
        self.assertEqual(node6.key, 6)

        # augmented data is the same
        self.assertEqual(node5.height, 1)
        self.assertEqual(node6.height, 2)

        # tail endpoints adjacent to the node were updated
        self.assertIs(node6.parent, node10)
        self.assertIs(node6.left_child, node2)
        self.assertIs(node6.right_child, node5)

        self.assertIs(node5.parent, node6)
        self.assertIs(node5.left_child, None)
        self.assertIs(node5.right_child, node8)

        # head endpoints adjacent to the node were updated
        self.assertIs(node10.left_child, node6)
        self.assertIs(node2.parent, node6)
        self.assertIs(node5.parent, node6)

        self.assertIs(node6.right_child, node5)
        self.assertIs(node8.parent, node5)


        # reswap with possible cycles
        node6.swap(node5)

        # node content is the same
        self.assertEqual(node5.key, 5)
        self.assertEqual(node6.key, 6)

        # augmented data is the same
        self.assertEqual(node5.height, 2)
        self.assertEqual(node6.height, 1)

        # tail endpoints adjacent to the node were updated
        self.assertIs(node5.parent, node10)
        self.assertIs(node5.left_child, node2)
        self.assertIs(node5.right_child, node6)

        self.assertIs(node6.parent, node5)
        self.assertIs(node6.left_child, None)
        self.assertIs(node6.right_child, node8)

        # head endpoints adjacent to the node were updated
        self.assertIs(node10.left_child, node5)
        self.assertIs(node2.parent, node5)
        self.assertIs(node6.parent, node5)

        self.assertIs(node5.right_child, node6)
        self.assertIs(node8.parent, node6)


        # swap with root and possible cycles
        node10.swap(node5)

        # node content is the same
        self.assertEqual(node5.key, 5)
        self.assertEqual(node10.key, 10)

        # augmented data is the same
        self.assertEqual(node5.height, 3)
        self.assertEqual(node10.height, 2)

        # tail endpoints adjacent to the node were updated
        self.assertIs(node5.parent, None)
        self.assertIs(node5.left_child, node10)
        self.assertIs(node5.right_child, None)

        self.assertIs(node10.parent, node5)
        self.assertIs(node10.left_child, node2)
        self.assertIs(node10.right_child, node6)

        # head endpoints adjacent to the node were updated
        self.assertIs(node10.parent, node5)

        self.assertIs(node5.left_child, node10)
        self.assertIs(node2.parent, node10)
        self.assertIs(node6.parent, node10)

    def test_search(self):
        tree = self.createTree([10, 5, 2, 6, 8, 7])

        # find elements
        node = tree.search(2)
        self.assertEqual(node.key, 2)

        node = tree.search(6)
        self.assertEqual(node.key, 6)

        # return the last node of the search path for 3
        # first case: 2 is a leaf
        node = tree.search(3)
        self.assertEqual(node.key, 2)

        # return the last node of the search path for 9
        # second case: 8 is a branch node with only one child
        node = tree.search(9)
        self.assertEqual(node.key, 8)

    def test_random_predecessor(self):
        with self.random() as random:
            # draw k values out of the range [1, 50000)
            k = random.randint(1, 20000)
            samples = random.sample(xrange(50000), k)
            queries = random.sample(samples, k//2) + random.sample(xrange(50000), k)

            tree = self.createAVLTree(samples)
            samples.sort()

            for query in queries:
                result = tree.predecessor(query)
                result = result and result.key
                expect = self.predecessor(samples, query)
                self.assertEqual(expect, result)

    def test_random_successor(self):
        with self.random() as random:
            # draw k values out of the range [1, 50000)
            k = random.randint(1, 20000)
            samples = random.sample(xrange(50000), k)
            queries = random.sample(samples, k//2) + random.sample(xrange(50000), k)

            tree = self.createAVLTree(samples)
            samples.sort()

            for query in queries:
                result = tree.successor(query)
                result = result and result.key
                expect = self.successor(samples, query)
                self.assertEqual(expect, result)

    def test_rotate_left(self):
        tree1 = self.createTree([10, 5, 2, 6, 8])
        tree2 = self.createTree([5, 2, 10, 6, 8])

        new_top = tree1.rotate_left()

        self.assertEqual(new_top.key, 5)
        self.assertEqualTree(tree1.root(), tree2.root())


        tree1 = self.createTree([10, 5, 2, 6, 8])
        tree2 = self.createTree([10, 2, 5, 6, 8])

        new_top = tree1.left_child.rotate_left()

        # update height, s.t. we can compare it with the tree2. rotate will only
        # update the height for all nodes in the subtree
        new_top.parent.update_height()

        self.assertEqual(new_top.key, 2)
        self.assertEqualTree(tree1.root(), tree2.root())

    def test_rotate_right(self):
        tree1 = self.createTree([10, 5, 2, 6, 8])
        tree2 = self.createTree([10, 6, 5, 2, 8])

        new_top = tree1.left_child.rotate_right()

        self.assertEqual(new_top.key, 6)
        self.assertEqualTree(tree1.root(), tree2.root())


        tree1 = self.createTree([10, 6, 5, 2, 8])
        tree2 = self.createTree([10, 8, 6, 5, 2])

        new_top = tree1.left_child.rotate_right()

        # update height, s.t. we can compare it with the tree2. rotate will only
        # update the height for all nodes in the subtree
        new_top.parent.update_height()

        self.assertEqual(new_top.key, 8)
        self.assertEqualTree(tree1.root(), tree2.root())

    def test_remove(self):
        # assert root change on remove
        tree = self.createTree([10, 5, 2, 6, 8])
        expect = self.createTree([5, 2, 6, 8])
        new_root = tree.find(5)

        with self.assertRootChange(tree, new_root) as observer:
            new_tree = tree.remove(observer)

        self.assertIs(new_tree, new_root)
        self.assertIsNone(tree.parent)
        self.assertIsNone(tree.left_child)
        self.assertIsNone(tree.right_child)
        self.assertEqualTree(new_tree, expect)

        # remove root 5
        tree = self.createTree([5, 2, 6, 8])
        expect = self.createTree([6, 2, 8])
        new_root = tree.find(6)

        with self.assertRootChange(tree, new_root) as observer:
            new_tree = tree.remove(observer)

        self.assertIs(new_tree, new_root)
        self.assertIsNone(tree.parent)
        self.assertIsNone(tree.left_child)
        self.assertIsNone(tree.right_child)
        self.assertEqualTree(new_tree, expect)

        # remove root 6
        tree = self.createTree([6, 2, 8])
        expect = self.createTree([8, 2])
        new_root = tree.find(8)

        with self.assertRootChange(tree, new_root) as observer:
            new_tree = tree.remove(observer)

        self.assertIs(new_tree, new_root)
        self.assertIsNone(tree.parent)
        self.assertIsNone(tree.left_child)
        self.assertIsNone(tree.right_child)
        self.assertEqualTree(new_tree, expect)

        # remove root 8
        tree = self.createTree([8, 2])
        expect = self.createTree([2])
        new_root = tree.find(2)

        with self.assertRootChange(tree, new_root) as observer:
            new_tree = tree.remove(observer)

        self.assertIs(new_tree, new_root)
        self.assertIsNone(tree.parent)
        self.assertIsNone(tree.left_child)
        self.assertIsNone(tree.right_child)
        self.assertEqualTree(new_tree, expect)

        # remove root 2
        tree = self.createTree([2])
        expect = self.createTree([])
        new_root = None

        with self.assertRootChange(tree, new_root) as observer:
            new_tree = tree.remove(observer)

        self.assertIs(new_tree, new_root)
        self.assertIsNone(tree.parent)
        self.assertIsNone(tree.left_child)
        self.assertIsNone(tree.right_child)
        self.assertEqualTree(new_tree, expect)

    def test_balance_with_root_change(self):
        tree1 = self.createTree([100, 50, 75])
        tree2 = self.createTree([75, 50, 100])

        new_root = tree1.left_child.right_child

        with self.assertRootChange(tree1, new_root) as observer:
            tree1.balance(observer)

        self.assertEqual(new_root.root(), tree1.root())
        self.assertEqualTree(new_root, tree2)

    def test_balance(self):
        tree1 = self.createTree([100, 50, 25, 12, 40, 30, 75, 60, 200, 150, 125, 110, 175, 250, 225, 210, 240, 230, 300, 350])
        # delete 175 from the tree and balance from parent of 175 (= 150)
        tree2 = self.createTree([100, 50, 25, 12, 40, 30, 75, 60, 200, 150, 125, 110, 250, 225, 210, 240, 230, 300, 350])
        # after balance from the parent of 175 (= 150)
        tree3 = self.createTree([100, 50, 25, 12, 40, 30, 75, 60, 200, 125, 110, 150, 250, 225, 210, 240, 230, 300, 350])
        # after balance from the parent of 150 (= 200)
        tree4 = self.createTree([100, 50, 25, 12, 40, 30, 75, 60, 225, 200, 125, 110, 150, 210, 250, 240, 230, 300, 350])

        node175 = tree1.right_child.left_child.right_child
        node150 = node175.parent
        node200 = node150.parent
        node225 = node200.parent

        # delete node 175
        node175.parent = node150.right_child = None
        node150.update_height()

        self.assertEqualTree(tree1, tree2)

        # rebalance parent (= 150)
        with self.assertNoRootChange(tree1):
            node150.balance()

        # update height, s.t. we can compare it with the tree3. balance will
        # only update the height for all nodes in the subtree
        node200.update_height()

        self.assertEqual(node150.root(), tree1)
        self.assertEqualTree(tree1, tree3)

        # rebalance parent (= 200)
        with self.assertNoRootChange(tree1):
            node200.balance()

        # update height, s.t. we can compare it with the tree3. balance will
        # only update the height for all nodes in the subtree
        node225.update_height()

        self.assertEqual(node150.root(), tree1)
        self.assertEqualTree(tree1, tree4)

    def test_concatenate(self):
        # concatenate with an empty subtree
        tree1 = self.createTree([1, 5, 3, 2, 4, 7, 6])
        tree2 = self.createTree([5, 3, 1, 2, 4, 7, 6])

        height = tree1.height
        new_root = tree1.concatenate()

        # returns new root
        self.assertEqual(new_root, tree1.root())

        # invariant: height reduces at most by 1
        self.assertTrue(height - 1 <= new_root.height <= height)

        self.assertAVLTree(new_root)
        self.assertEqualTree(new_root, tree2)


        # structure above 1 remains unchanged
        tree1 = self.createTree([19, 18, 20, 1, 5, 3, 2, 4, 7, 6])
        tree2 = self.createTree([19, 18, 20, 5, 3, 1, 2, 4, 7, 6])
        node1 = tree1.left_child.left_child

        new_root = node1.concatenate()

        self.assertEqual(new_root, tree1.left_child.left_child)
        self.assertTrue(height - 1 <= new_root.height <= height)
        self.assertAVLTree(new_root)
        self.assertEqualTree(tree1, tree2)

    def test_random_concatenate(self):
        with self.random() as random:
            # draw k values out of the range [1, 50000)
            k = random.randint(1, 20000)
            samples = random.sample(xrange(50000), k)
            samples.sort()

            # randomly split samples into three segments:
            #   [a_0, ..., a_l-1] [a_l] [a_l+1, ..., a_n-1]
            l = random.randint(0, len(samples)-1)

            left   = samples[:l]
            middle = samples[l]
            right  = samples[l+1:]

            # create balanced trees
            left_child = self.createAVLTree(left)
            root = binary_tree.Node(middle)
            right_child = self.createAVLTree(right)

            # construct whole tree
            root.set_child(left_child, middle-1)
            root.set_child(right_child, middle+1)
            root.update_height()
            height = root.height

            # concatenate it
            new_root = root.concatenate()

            # invariant: height reduces at most by 1
            self.assertTrue(height - 1 <= new_root.height <= height)
            self.assertAVLTree(new_root)

            # no element vanished
            self.assertTreeContains(new_root, samples)

    def test_split(self):
        # split node with key 5 (the root, does nothing)
        tree = self.createTree([5, 3, 2, 1, 4, 7, 6])

        with self.assertNoRootChange(tree):
            split = tree.split()

        self.assertIs(split, split.root())
        self.assertEqual(split.key, 5)
        self.assertEqualTree(split, tree)


        # split node with key 1
        tree1 = self.createTree([5, 3, 2, 1, 4, 7, 6])
        tree2 = self.createTree([1, 5, 3, 2, 4, 7, 6])

        new_root = tree1.min()

        with self.assertRootChange(tree1, new_root) as observer:
            split = new_root.split(None, observer)

        self.assertIs(split, split.root())
        self.assertEqual(split.key, 1)
        self.assertEqualTree(split, tree2)


        # split node with key 4
        tree1 = self.createTree([5, 3, 2, 1, 4, 7, 6])
        tree2 = self.createTree([4, 2, 1, 3, 6, 5, 7])

        new_root = tree1.left_child.right_child

        with self.assertRootChange(tree1, new_root) as observer:
            split = new_root.split(None, observer)

        self.assertIs(split, split.root())
        self.assertEqual(split.key, 4)
        self.assertEqualTree(split, tree2)


        # split node with key 4 in the subtree starting at 5
        tree1 = self.createTree([18, 12, 5, 3, 2, 1, 4, 7, 6])
        tree2 = self.createTree([18, 12, 4, 2, 1, 3, 6, 5, 7])

        root = tree1.left_child
        new_root = root.left_child.left_child.right_child

        with self.assertNoRootChange(tree1):
            split = new_root.split(root)

        # update height, s.t. we can compare it with the tree2. split will
        # only update the height for all nodes in the subtree
        new_root.parent.update_height()

        self.assertIs(split.parent, root)
        self.assertEqual(split.key, 4)
        self.assertEqualTree(tree1, tree2)

    def test_random_split(self):
        with self.random() as random:
            # draw k values out of the range [1, 50000)
            k = random.randint(1, 20000)
            samples = random.sample(xrange(50000), k)

            # randomly select the element to split
            splitter = random.choice(samples)

            tree = self.createAVLTree(samples)
            split_node = tree.find(splitter)

            with self.assertRootChange(tree, split_node) as observer:
                # move split_node to root
                new_root = split_node.split(None, observer)

            self.assertIs(new_root, split_node.root())

            self.assertTreeStructure(new_root)
            self.assertAVLTree(new_root.left_child)
            self.assertAVLTree(new_root.right_child)
            self.assertTreeContains(new_root, samples)

    def test_cut(self):
        # empty interval
        tree = self.createTree([4, 2, 1, 3, 6, 5, 7])

        with self.assertNoRootChange(tree):
            root1, root2 = tree.cut(None, None)

        self.assertEqualTree(root1, tree)
        self.assertIsNone(root2)

        # interval [start, end] has all elements
        tree = self.createTree([4, 2, 1, 3, 6, 5, 7])

        start = tree.find(1)
        end = tree.find(7)
        with self.assertNoRootChange(tree):
            root1, root2 = tree.cut(start, end)

        self.assertIsNone(root1)
        self.assertEqualTree(root2, tree)

        # interval (-infty, end]
        tree1 = self.createTree([4, 2, 1, 3, 6, 5, 7])
        tree2 = self.createTree([6, 4, 5, 7])
        tree3 = self.createTree([2, 1, 3])

        end = tree1.find(3)
        with self.assertRootChange(tree1, tree1.find(6)) as observer:
            root1, root2 = tree1.cut(None, end, observer)

        self.assertEqualTree(root1, tree2)
        self.assertEqualTree(root2, tree3)

        # interval [start, +infty)
        tree1 = self.createTree([4, 2, 1, 3, 6, 5, 7])
        tree2 = self.createTree([2, 1, 3])
        tree3 = self.createTree([6, 4, 5, 7])

        start = tree1.find(4)
        with self.assertRootChange(tree1, start.previous()) as observer:
            root1, root2 = tree1.cut(start, None, observer)

        self.assertEqualTree(root1, tree2)
        self.assertEqualTree(root2, tree3)

        # interval [start, end]
        tree1 = self.createTree([4, 2, 1, 3, 6, 5, 7])
        tree2 = self.createTree([6, 1, 5, 7])
        tree3 = self.createTree([3, 2, 4])

        start = tree1.find(2)
        end = tree1.find(4)
        with self.assertRootChange(tree1, tree1.find(1), tree1.find(6)) as observer:
            root1, root2 = tree1.cut(start, end, observer)

        self.assertEqualTree(root1, tree2)
        self.assertEqualTree(root2, tree3)

    def test_random_cut(self):
        with self.random() as random:
            # draw k values out of the range [1, 50000)
            k = random.randint(1, 20000)
            samples = random.sample(xrange(50000), k)
            samples.sort()

            # randomly split samples into three segments:
            #   [a_0, ..., a_i-1] [a_i, ..., a_j] [a_j+1, ..., a_n-1]
            i = random.randint(0, len(samples)-1)
            j = random.randint(0, len(samples)-1)
            i, j = min(i,j), max(i,j)

            left   = samples[:i]
            middle = samples[i:j]
            right  = samples[j:]

            tree = self.createAVLTree(samples)

            # set interval type according to the splitting
            start_node = None
            end_node = None
            if middle != []:
                if left != []:
                    start_node = tree.find(min(middle))
                if right != []:
                    end_node = tree.find(max(middle))

            # cut out interval
            root1, root2 = tree.cut(start_node, end_node)

            # empty interval
            if middle == []:
                self.assertIs(root1, root1.root())
                self.assertIs(root2, None)
                self.assertEqualTree(root1, tree)
            # full interval
            elif left == [] and right == []:
                self.assertIs(root1, None)
                self.assertIs(root2, root2.root())
                self.assertEqualTree(root2, tree)
            else:
                self.assertIs(root1, root1.root())
                self.assertIs(root2, root2.root())

            self.assertEqual(left + right, self.getElements(root1))
            self.assertEqual(middle, self.getElements(root2))

    def test_join(self):
        # join empty tree
        tree1 = self.createTree([4, 2, 1, 3, 6, 5, 7])
        tree2 = self.createTree([])
        expect = self.createTree([4, 2, 1, 3, 6, 5, 7])

        with self.assertNoRootChange(tree1):
            root = tree1.join(tree2)

        self.assertIs(root, tree1.root())
        self.assertEqualTree(root, expect)

        # interval (-infty, end]
        tree1 = self.createTree([6, 4, 5, 7])
        tree2 = self.createTree([2, 1, 3])
        expect = self.createTree([4, 2, 1, 3, 6, 5, 7])

        with self.assertRootChange(tree1, tree1.find(4)) as observer:
            root = tree1.join(tree2, observer)
        self.assertIs(root, tree1.root())
        self.assertIs(root, tree2.root())
        self.assertEqualTree(root, expect)

        # interval [start, +infty)
        tree1 = self.createTree([2, 1, 3])
        tree2 = self.createTree([6, 4, 5, 7])
        expect = self.createTree([3, 2, 1, 6, 4, 5, 7])

        with self.assertRootChange(tree1, tree1.find(3)) as observer:
            root = tree1.join(tree2, observer)

        self.assertIs(root, tree1.root())
        self.assertIs(root, tree2.root())
        self.assertEqualTree(root, expect)

        # interval [start, end]
        tree1 = self.createTree([6, 1, 5, 7])
        tree2 = self.createTree([3, 2, 4])
        expect = self.createTree([5, 3, 1, 2, 4, 6, 7])

        with self.assertRootChange(tree1, tree1.find(1), tree1.find(5)) as observer:
            root = tree1.join(tree2, observer)

        self.assertIs(root, tree1.root())
        self.assertIs(root, tree2.root())
        self.assertEqualTree(root, expect)

    def test_random_join(self):
        with self.random() as random:
            # draw k values out of the range [1, 50000)
            k = random.randint(1, 20000)
            samples = random.sample(xrange(50000), k)
            samples.sort()

            # randomly split samples into three segments:
            #   [a_0, ..., a_i-1] [a_i, ..., a_j] [a_j+1, ..., a_n-1]
            i = random.randint(0, len(samples)-1)
            j = random.randint(0, len(samples)-1)
            i, j = min(i,j), max(i,j)

            left   = samples[:i]
            middle = samples[i:j]
            right  = samples[j:]

            # create balanced trees
            tree1 = self.createAVLTree(left+right)
            tree2 = self.createAVLTree(middle)

            # tree1 is empty
            if tree1 is None:
                return

            # join tree2 into tree1
            root = tree1.join(tree2)

            self.assertIs(root, tree1.root())
            self.assertIs(root, tree2 and tree2.root())
            self.assertAVLTree(root)

            # no element vanished
            self.assertTreeContains(root, samples)

if __name__ == '__main__':
    unittest.main()
