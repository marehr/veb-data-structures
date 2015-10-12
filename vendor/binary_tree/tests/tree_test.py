# coding=utf8

import unittest
import test_case
import binary_tree

class BinaryTreeTest(test_case.TestCase):

    def test_readme(self):
        tree = binary_tree.BinaryTree()
        tree.insert(5)
        tree.insert((5,1))
        tree.insert((5,2))

        self.assertEqual(tree.root.key, (5,1))
        self.assertEqual(tree.root.left_child.key, 5)
        self.assertEqual(tree.root.right_child.key, (5,2))

    def test_insert(self):
        bsb = binary_tree.BinaryTree()

        # insert next element
        bsb.insert(100)

        tree1 = bsb.root
        tree2 = self.createTree([100])

        self.assertEqual(len(bsb), 1)
        self.assertAVLTree(tree1)
        self.assertEqualTree(tree1, tree2)

        # insert next element
        bsb.insert(50)

        tree1 = bsb.root
        tree2 = self.createTree([100, 50])

        self.assertEqual(len(bsb), 2)
        self.assertAVLTree(tree1)
        self.assertEqualTree(tree1, tree2)

        # insert next element
        bsb.insert(75)

        tree1 = bsb.root
        tree2 = self.createTree([75, 50, 100])

        self.assertEqual(len(bsb), 3)
        self.assertAVLTree(tree1)
        self.assertEqualTree(tree1, tree2)

        # insert next element
        bsb.insert(250)

        tree1 = bsb.root
        tree2 = self.createTree([75, 50, 100, 250])

        self.assertEqual(len(bsb), 4)
        self.assertAVLTree(tree1)
        self.assertEqualTree(tree1, tree2)

        # insert next element
        bsb.insert(300)

        tree1 = bsb.root
        tree2 = self.createTree([75, 50, 250, 100, 300])

        self.assertEqual(len(bsb), 5)
        self.assertAVLTree(tree1)
        self.assertEqualTree(tree1, tree2)

        # insert next element
        bsb.insert(85)

        tree1 = bsb.root
        tree2 = self.createTree([100, 75, 50, 85, 250, 300])

        self.assertEqual(len(bsb), 6)
        self.assertAVLTree(tree1)
        self.assertEqualTree(tree1, tree2)

    def test_random_insert(self):
        with self.random() as random:
            # draw k values out of the range [0, 50000)
            k = random.randint(0, 20000)
            samples = random.sample(xrange(50000), k)
            bsb = binary_tree.BinaryTree(samples)

            self.assertEqual(len(bsb), k)
            self.assertAVLTree(bsb.root)

            # no element vanished
            self.assertTreeContains(bsb.root, samples)

    def test_remove_leaf(self):
        # remove one element
        tree1 = binary_tree.BinaryTree([100])
        tree2 = self.createTree([])

        tree1.remove(100)

        self.assertEqual(len(tree1), 0)
        self.assertAVLTree(tree1.root)
        self.assertEqualTree(tree1.root, tree2)

        # remove a leaf of two elements
        tree1 = binary_tree.BinaryTree([100, 50])
        tree2 = self.createTree([100])

        tree1.remove(50)

        self.assertEqual(len(tree1), 1)
        self.assertAVLTree(tree1.root)
        self.assertEqualTree(tree1.root, tree2)

        tree1.remove(100)

        self.assertEqual(len(tree1), 0)
        self.assertIs(tree1.root, None)

        # remove a leaf
        tree1 = binary_tree.BinaryTree([100, 75, 250, 50, 85, 300, 25])
        tree2 = self.createTree([75, 50, 25, 100, 85, 250])

        tree1.remove(300)

        self.assertEqual(len(tree1), 6)
        self.assertAVLTree(tree1.root)
        self.assertEqualTree(tree1.root, tree2)

    def test_remove_inner_node_with_one_child(self):
        # remove an inner node of two elements
        tree1 = binary_tree.BinaryTree([50, 100])
        tree2 = self.createTree([100])

        tree1.remove(50)

        self.assertEqual(len(tree1), 1)
        self.assertAVLTree(tree1.root)
        self.assertEqualTree(tree1.root, tree2)

        tree1.remove(100)

        self.assertEqual(len(tree1), 0)
        self.assertIs(tree1.root, None)

        # remove an inner node
        tree1 = binary_tree.BinaryTree([100, 75, 250, 50, 85, 300, 25])
        tree2 = self.createTree([75, 50, 25, 100, 85, 300])

        tree1.remove(250)

        self.assertEqual(len(tree1), 6)
        self.assertAVLTree(tree1.root)
        self.assertEqualTree(tree1.root, tree2)

    def test_remove_branch_node(self):
        # remove an inner node
        tree1 = binary_tree.BinaryTree([100, 75, 250, 50, 85, 300, 25])
        tree2 = self.createTree([100, 50, 25, 85, 250, 300])
        tree1.remove(75)

        self.assertEqual(len(tree1), 6)
        self.assertAVLTree(tree1.root)
        self.assertEqualTree(tree1.root, tree2)

        # remove the root
        tree1 = binary_tree.BinaryTree([100, 75, 250, 50, 85, 300, 25])
        tree2 = self.createTree([75, 50, 25, 250, 85, 300])

        tree1.remove(100)

        self.assertEqual(len(tree1), 6)
        self.assertAVLTree(tree1.root)
        self.assertEqualTree(tree1.root, tree2)

    def test_random_remove(self):
        with self.random() as random:
            # draw k values out of the range [0, 50000)
            k = random.randint(0, 10)
            samples = random.sample(xrange(50000), k)

            # draw l elements and remove them
            l = random.randint(0, k)
            deletes = random.sample(samples, l)

            bsb = binary_tree.BinaryTree(samples)

            for x in deletes:
                samples.remove(x)
                bsb.remove(x)
                self.assertAVLTree(bsb.root)

            self.assertAVLTree(bsb.root)

            # no element vanished
            self.assertTreeContains(bsb.root, samples)

    def test_inorder(self):
        tree = binary_tree.BinaryTree([])
        self.assertEqual(tree.inorder(tree.root), [])

        tree = binary_tree.BinaryTree([100])
        self.assertEqual(tree.inorder(tree.root), [100])

        tree = binary_tree.BinaryTree([100, 75, 250, 50, 85, 300, 25])
        self.assertEqual(tree.inorder(tree.root), [25, 50, 75, 85, 100, 250, 300])

    def test_preorder(self):
        tree = binary_tree.BinaryTree([])
        self.assertEqual(tree.preorder(tree.root), [])

        tree = binary_tree.BinaryTree([100])
        self.assertEqual(tree.preorder(tree.root), [100])

        tree = binary_tree.BinaryTree([100, 75, 250, 50, 85, 300, 25])
        self.assertEqual(tree.preorder(tree.root), [100, 75, 50, 25, 85, 250, 300])

    def test_postorder(self):
        tree = binary_tree.BinaryTree([])
        self.assertEqual(tree.postorder(tree.root), [])

        tree = binary_tree.BinaryTree([100])
        self.assertEqual(tree.postorder(tree.root), [100])

        tree = binary_tree.BinaryTree([100, 75, 250, 50, 85, 300, 25])
        self.assertEqual(tree.postorder(tree.root), [25, 50, 85, 75, 300, 250, 100])

if __name__ == '__main__':
    unittest.main()
