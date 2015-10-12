from word import word


class NodeTestMixin(object):

    def test_previous_next_leaf(self):
        # special case empty trie
        trie = self.new_trie(8)

        current = trie.root
        self.assertIsNone(current.previous_leaf())
        self.assertIsNone(current.next_leaf())

    def test_min_max_leaf(self):
        # special case empty trie
        trie = self.new_trie(8)

        current = trie.root
        self.assertIsNone(current.min_leaf())
        self.assertIsNone(current.max_leaf())

        # if right subtree of root is empty, max is from the left subtree
        elements = [9, 12, 44, 108, 110, 111]
        trie = self.new_trie(8, elements)

        #  9 = 0 - 0 - 00 - 10   0   1
        #       |   |    \
        # 12 =  |   |     - 11   0   0
        #       |   \
        # 44 =  |    - 10   11   0   0
        #       \
        #108 =   - 1   10   11 - 0   0
        #                     \
        #110 =                 - 1 - 0
        #                         \
        #111 =                     - 1

        current = trie.root
        self.assertEqual(current.min_leaf().key, word(9, 8))
        self.assertEqual(current.max_leaf().key, word(111, 8))

        current = trie.root.left
        self.assertEqual(current.min_leaf().key, word(9, 8))
        self.assertEqual(current.max_leaf().key, word(111, 8))

        current = trie.root.left.left
        self.assertEqual(current.min_leaf().key, word(9, 8))
        self.assertEqual(current.max_leaf().key, word(44, 8))

        current = trie.root.left.left.left
        self.assertEqual(current.min_leaf().key, word(9, 8))
        self.assertEqual(current.max_leaf().key, word(12, 8))

        current = trie.root.left.left.left.left
        self.assertEqual(current.min_leaf().key, word(9, 8))
        self.assertEqual(current.max_leaf().key, word(9, 8))

        current = trie.root.left.left.left.right
        self.assertEqual(current.min_leaf().key, word(12, 8))
        self.assertEqual(current.max_leaf().key, word(12, 8))

        current = trie.root.left.left.right
        self.assertEqual(current.min_leaf().key, word(44, 8))
        self.assertEqual(current.max_leaf().key, word(44, 8))

        current = trie.root.left.right
        self.assertEqual(current.min_leaf().key, word(108, 8))
        self.assertEqual(current.max_leaf().key, word(111, 8))

        current = trie.root.left.right.left
        self.assertEqual(current.min_leaf().key, word(108, 8))
        self.assertEqual(current.max_leaf().key, word(108, 8))

        current = trie.root.left.right.right
        self.assertEqual(current.min_leaf().key, word(110, 8))
        self.assertEqual(current.max_leaf().key, word(111, 8))

        current = trie.root.left.right.right.left
        self.assertEqual(current.min_leaf().key, word(110, 8))
        self.assertEqual(current.max_leaf().key, word(110, 8))

        current = trie.root.left.right.right.right
        self.assertEqual(current.min_leaf().key, word(111, 8))
        self.assertEqual(current.max_leaf().key, word(111, 8))
