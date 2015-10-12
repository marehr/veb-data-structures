from word import word
import ordered_dict_test


class TreeTestMixin(ordered_dict_test.OrderedDictTestMixin):

    def new_ordered_dict(self, word_size, elements=[]):
        return self.new_trie(word_size, elements)

    def test_insert(self):
        trie = self.new_trie(8)

        # 12 = 0000 1100 = 12
        a = word(12, 8)
        trie.insert(a)

        root = trie.root
        child = root.left
        self.assertEqual(child.key, a)
        self.assertEqual(child.edge, a)

        self.assertEqual(child.left, None)
        self.assertEqual(child.right, None)
        self.assertEqual(child.parent, root)

        ##
        # 14 = 0000 1110 = 14
        b = word(14, 8)
        trie.insert(b)

        root = trie.root.left
        left = root.left
        right = root.right

        # prefix: 3 = 0000 11xx
        self.assertEqual(root.key, word(3, 6))
        self.assertEqual(root.edge, word(3, 6))

        # left is 0000 1100, that means 00 is the edge
        self.assertEqual(left.key, a)
        self.assertEqual(left.edge, word(0, 2))
        self.assertEqual(left.left, None)
        self.assertEqual(left.right, None)
        self.assertEqual(left.parent, root)

        # right is 0000 1110, that means 10 is the edge
        self.assertEqual(right.key, b)
        self.assertEqual(right.edge, word(2, 2))
        self.assertEqual(right.left, None)
        self.assertEqual(right.right, None)
        self.assertEqual(right.parent, root)

        ##
        # 13 = 0000 1101 = 13
        c = word(13, 8)
        trie.insert(c)

        root = trie.root.left
        # prefix: 3 = 0000 11xx
        self.assertEqual(root.key, word(3, 6))
        self.assertEqual(root.edge, word(3, 6))

        root = root.left
        # prefix: 0 = (0000 11)0x
        self.assertEqual(root.edge, word(0, 1))
        self.assertEqual(root.key, word(6, 7))

        left = root.left
        right = root.right

        # left is 0000 1100, that means (0000 110)0 is the edge
        self.assertEqual(left.key, a)
        self.assertEqual(left.edge, word(0, 1))
        self.assertEqual(left.left, None)
        self.assertEqual(left.right, None)
        self.assertEqual(left.parent, root)

        # right is 0000 1101, that means (0000 110)1 is the edge
        self.assertEqual(right.key, c)
        self.assertEqual(right.edge, word(1, 1))
        self.assertEqual(right.left, None)
        self.assertEqual(right.right, None)
        self.assertEqual(right.parent, root)

        # 77 = 0100 1101 = 77
        d = word(77, 8)
        trie.insert(d)

        root = trie.root.left
        left = root.left
        right = root.right

        # prefix: 0 = 0xxx xxxx
        self.assertEqual(root.key, word(0, 1))
        self.assertEqual(root.edge, word(0, 1))

        # left is 0000 11xx, that means (0)000 11(xx) is the edge
        self.assertEqual(left.key, word(3, 6))
        self.assertEqual(left.edge, word(3, 5))
        self.assertNotEqual(left.left, None)
        self.assertNotEqual(left.right, None)
        self.assertEqual(left.parent, root)

        # right is 0100 1101, that means (0)100 1101 is the edge
        self.assertEqual(right.key, d)
        self.assertEqual(right.edge, word(77, 7))
        self.assertEqual(right.left, None)
        self.assertEqual(right.right, None)
        self.assertEqual(right.parent, root)

    def test_lowest_common_ancestor(self):
        trie = self.new_trie(8)

        a = word(12, 8)
        trie.insert(a)

        ##
        #
        q = word(0b00001001, 8)
        lca, child = trie.lowest_common_ancestor(q)

        self.assertEqual(lca, trie.root)
        self.assertEqual(lca.edge, word.epsilon)
        self.assertEqual(lca.key, word.epsilon)

        self.assertEqual(child, trie.root.left)
        self.assertEqual(child.edge, a)
        self.assertEqual(child.key, a)

        b = word(9, 8)
        trie.insert(b)

        ##
        #
        q = word(0b00101100, 8)
        lca, child = trie.lowest_common_ancestor(q)

        self.assertEqual(lca, trie.root)

        self.assertEqual(child, trie.root.left)
        self.assertEqual(child.edge, word(0b00001, 5))
        self.assertEqual(child.key, word(0b00001, 5))

        c = word(44, 8)
        trie.insert(c)

        d = word(108, 8)
        trie.insert(d)

        ##
        # empty root.right
        q = word(0b10101100, 8)
        lca, child = trie.lowest_common_ancestor(q)

        self.assertEqual(lca, trie.root)
        self.assertEqual(child, None)

        # hash map
        #  9 = 0 - 0 - 00 - 1001
        #       |   |    \
        # 12 =  |   |     - 1100
        #       |   \
        # 44 =  |    - 10   1100
        #       \
        #108 =   - 1   10   1100

        # actual tree
        #  9 = 0 - 0 - 001 - 001
        #       |   |     \
        # 12 =  |   |      - 100
        #       |   \
        # 44 =  |    - 101   100
        #       \
        #108 =   - 1   101   100

        # contained element 44
        q = word(44, 8)
        lca, child = trie.lowest_common_ancestor(q)

        self.assertEqual(lca, trie.root.left.left.right)
        self.assertEqual(lca.edge, word(0b101100, 6))
        self.assertEqual(lca.key, q)

        self.assertIsNone(child)

        #
        # contained element 108
        q = word(108, 8)
        lca, child = trie.lowest_common_ancestor(q)

        self.assertEqual(lca, trie.root.left.right)
        self.assertEqual(lca.edge, word(0b1101100, 7))
        self.assertEqual(lca.key, q)

        self.assertIsNone(child)

        #
        # before the element 9
        q = word(0b00000010, 8)
        lca, child = trie.lowest_common_ancestor(q)

        self.assertEqual(lca, trie.root.left.left)
        self.assertEqual(lca.edge, word(0b0, 1))
        self.assertEqual(lca.key, word(0b00, 2))

        self.assertEqual(child, trie.root.left.left.left)
        self.assertEqual(child.edge, word(0b001, 3))
        self.assertEqual(child.key, word(0b00001, 5))

        #
        # between the element 9 and 12
        q = word(0b00001010, 8)
        lca, child = trie.lowest_common_ancestor(q)

        self.assertEqual(lca, trie.root.left.left.left)
        self.assertEqual(lca.edge, word(0b001, 3))
        self.assertEqual(lca.key, word(0b00001, 5))

        self.assertEqual(child, trie.root.left.left.left.left)
        self.assertEqual(child.edge, word(0b001, 3))
        self.assertEqual(child.key, word(0b00001001, 8))

        #
        # between the element 12 and 14
        q = word(0b00011010, 8)
        lca, child = trie.lowest_common_ancestor(q)

        self.assertEqual(lca, trie.root.left.left)
        self.assertEqual(lca.edge, word(0b0, 1))
        self.assertEqual(lca.key, word(0b00, 2))

        self.assertEqual(child, trie.root.left.left.left)
        self.assertEqual(child.edge, word(0b001, 3))
        self.assertEqual(child.key, word(0b00001, 5))

        #
        # after the element 108
        q = word(0b01111111, 8)
        lca, child = trie.lowest_common_ancestor(q)

        self.assertEqual(lca, trie.root.left)
        self.assertEqual(lca.edge, word(0b0, 1))
        self.assertEqual(lca.key, word(0b0, 1))

        self.assertEqual(child, trie.root.left.right)
        self.assertEqual(child.edge, word(0b1101100, 7))
        self.assertEqual(child.key, word(0b01101100, 8))

    def test_random_remove(self, seed=None):
        with self.random(seed) as rand:
            size = rand.randint(0, 150)
            samples = rand.sample(xrange(255), size)

            while len(samples) > 0:
                trie1 = self.new_trie(8)
                trie2 = self.new_trie(8)

                trie1.extend(samples)

                rand.shuffle(samples)
                val = samples.pop()

                result = trie1.remove(val)
                trie2.extend(samples)
                self.assertTrue(result)

                self.assertEqualTrie(trie1, trie2)

    def test_predecessor_with_lca(self):
        # special case trie is empty
        trie = self.new_trie(8)

        q = word(54, 8)
        result = trie.predecessor_with_lca(q, trie.root, None)
        self.assertIsNone(result)

    def test_successor_with_lca(self):
        # special case trie is empty
        trie = self.new_trie(8)

        q = word(54, 8)
        result = trie.successor_with_lca(q, trie.root, None)
        self.assertIsNone(result)
