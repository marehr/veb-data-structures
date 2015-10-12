from word import word


class OrderedDictTestMixin(object):

    def new_ordered_dict(self, w, xs=[]):
        raise ValueError("new_ordered_dict must be implemented.")

    def test_ordered_dict_search(self):
        odict = self.new_ordered_dict(4)
        odict.insert(10, 110)
        odict.insert(12, 112)
        odict.insert(15, 115)
        odict.insert(13, 113)
        odict.insert(14, 114)

        # no common edges in a trie
        with self.assertRaises(KeyError):
            odict.search(0)

        # some comon edges in a trie
        with self.assertRaises(KeyError):
            odict.search(11)

        # contained elements
        result = odict.search(10)
        self.assertEqual(result, 110)

        result = odict.search_node(10)
        self.assertEqual(result.key, word(10, 4))
        self.assertEqual(result.value, 110)

        result = odict.search(12)
        self.assertEqual(result, 112)

        result = odict.search_node(12)
        self.assertEqual(result.key, word(12, 4))
        self.assertEqual(result.value, 112)

    def test_ordered_dict_update_value(self):
        odict = self.new_ordered_dict(8)

        self.assertEqual(odict.size(), 0)

        q = word(12, 8)
        node1 = odict.insert(12, 15)
        node2 = odict.insert(q, 18)

        self.assertIs(node1, node2)
        self.assertEqual(node1.value, 18)
        self.assertEqual(odict.size(), 1)

    def test_ordered_dict_insert(self):
        odict = self.new_ordered_dict(8)

        self.assertEqual(odict.size(), 0)

        q = word(12, 8)
        node = odict.insert(q, 112)
        self.assertEqual(node.key, q)
        self.assertEqual(node.value, 112)
        self.assertEqual(odict.size(), 1)

        q = word(14, 8)
        node = odict.insert(q, 114)
        self.assertEqual(node.key, q)
        self.assertEqual(node.value, 114)
        self.assertEqual(odict.size(), 2)

        q = word(13, 8)
        node = odict.insert(q, 113)
        self.assertEqual(node.key, q)
        self.assertEqual(node.value, 113)
        self.assertEqual(odict.size(), 3)

        q = word(77, 8)
        node = odict.insert(q, 177)
        self.assertEqual(node.key, q)
        self.assertEqual(node.value, 177)
        self.assertEqual(odict.size(), 4)

    def test_ordered_dict_remove(self):
        odict = self.new_ordered_dict(8)
        odict.insert(249, 1249)

        with self.assertRaises(KeyError):
            odict.remove(12)

        result = odict.remove(249)
        self.assertEqual(result.key, word(249, 8))
        self.assertEqual(result.value, 1249)
        self.assertEqual(odict.size(), 0)

    def test_ordered_dict_random_remove(self, seed=None):
        with self.random(seed) as rand:
            size = rand.randint(0, 150)
            samples = rand.sample(xrange(255), size)

            while len(samples) > 0:
                odict1 = self.new_ordered_dict(8)
                odict2 = self.new_ordered_dict(8)

                odict1.extend(samples)

                rand.shuffle(samples)
                val = samples.pop()

                result = odict1.remove(val)
                odict2.extend(samples)

                self.assertEqual(result.key, word(val, 8))

                self.assertEqual(odict1.elements(), odict2.elements())
                self.assertEqual(odict1.size(), len(samples))

                min1 = odict1.min_node()
                min2 = odict2.min_node()
                self.assertEqual(min1 and min1.key, min2 and min2.key)

                max1 = odict1.max_node()
                max2 = odict2.max_node()
                self.assertEqual(max1 and max1.key, max2 and max2.key)

    def test_new_node(self):
        odict = self.new_ordered_dict(4)
        result = odict.new_node(15, 215)

        self.assertEqual(result.key, word(15, 4))
        self.assertEqual(result.value, 215)

    def test_replace_node(self):
        odict = self.new_ordered_dict(4)
        odict.insert(13, 113)

        node1 = odict.insert(15, 115)
        node1.special = "A special attribute"

        node2 = odict.new_node(15, 215)
        node2.bar = "A diffferent attribute"

        odict.replace_node(node1, node2)

        # node 2 keeps its special attributes
        result = odict.search_node(15)
        self.assertIs(result, node2)

    def test_ordered_dict_min_and_max_node(self):
        odict = self.new_ordered_dict(4)
        odict.insert(10, 110)
        odict.insert(12, 112)
        odict.insert(15, 115)
        odict.insert(13, 113)
        odict.insert(14, 114)

        min_node = odict.min_node()
        self.assertEqual(min_node.key, word(10, 4))
        self.assertEqual(min_node.value, 110)

        max_node = odict.max_node()
        self.assertEqual(max_node.key, word(15, 4))
        self.assertEqual(max_node.value, 115)

        # min/max stay the same
        odict.remove(14)

        min_node = odict.min_node()
        self.assertEqual(min_node.key, word(10, 4))
        self.assertEqual(min_node.value, 110)

        max_node = odict.max_node()
        self.assertEqual(max_node.key, word(15, 4))
        self.assertEqual(max_node.value, 115)

        # min changes
        odict.remove(10)

        min_node = odict.min_node()
        self.assertEqual(min_node.key, word(12, 4))
        self.assertEqual(min_node.value, 112)

        max_node = odict.max_node()
        self.assertEqual(max_node.key, word(15, 4))
        self.assertEqual(max_node.value, 115)

        # max changes
        odict.remove(15)

        min_node = odict.min_node()
        self.assertEqual(min_node.key, word(12, 4))
        self.assertEqual(min_node.value, 112)

        max_node = odict.max_node()
        self.assertEqual(max_node.key, word(13, 4))
        self.assertEqual(max_node.value, 113)

        # max changes
        odict.remove(13)

        min_node = odict.min_node()
        self.assertEqual(min_node.key, word(12, 4))
        self.assertEqual(min_node.value, 112)

        max_node = odict.max_node()
        self.assertEqual(max_node.key, word(12, 4))
        self.assertEqual(max_node.value, 112)

        # min/max changes
        odict.remove(12)

        min_node = odict.min_node()
        self.assertIsNone(min_node)

        max_node = odict.max_node()
        self.assertIsNone(max_node)

    def test_ordered_dict_predecessor(self):
        # special case odict is empty
        odict = self.new_ordered_dict(8)

        result = odict.predecessor(54)
        self.assertIsNone(result)

        # special case right of root is empty in a trie
        odict = self.new_ordered_dict(8)
        odict.insert(54, 154)

        result = odict.predecessor(53)
        self.assertIsNone(result)

        result = odict.predecessor(54)
        self.assertIsNone(result)

        result = odict.predecessor(112)
        self.assertEqual(result, word(54, 8))

        result = odict.predecessor_node(112)
        self.assertEqual(result.key, word(54, 8))
        self.assertEqual(result.value, 154)

        # special case left of root is empty in a trie
        odict = self.new_ordered_dict(8)
        odict.insert(230, 1230)

        result = odict.predecessor(229)
        self.assertIsNone(result)

        result = odict.predecessor(230)
        self.assertIsNone(result)

        result = odict.predecessor(240)
        self.assertEqual(result, word(230, 8))

        result = odict.predecessor_node(240)
        self.assertEqual(result.key, word(230, 8))
        self.assertEqual(result.value, 1230)

    def test_ordered_dict_random_predecessor(self, seed=None):
        with self.random(seed) as rand:
            size = rand.randint(0, 150)
            samples = rand.sample(xrange(255), size)
            queries = rand.sample(xrange(255), size)
            queries.extend(samples[:size//2])

            odict = self.new_ordered_dict(8)
            odict.extend(samples)

            samples.sort()

            for query in queries:
                result = odict.predecessor(query)
                expect = self.predecessor(samples, query)
                expect = word(expect, 8) if expect is not None else None

                self.assertEqual(result, expect)

    def test_ordered_dict_successor(self):
        # special case odict is empty
        odict = self.new_ordered_dict(8)

        result = odict.successor(54)
        self.assertIsNone(result)

        # special case right of root is empty in a trie
        odict = self.new_ordered_dict(8)
        odict.insert(54, 154)

        result = odict.successor(24)
        self.assertEqual(result, word(54, 8))

        result = odict.successor_node(24)
        self.assertEqual(result.key, word(54, 8))
        self.assertEqual(result.value, 154)

        result = odict.successor(54)
        self.assertIsNone(result)

        result = odict.successor(55)
        self.assertIsNone(result)

        # special case left of root is empty
        odict = self.new_ordered_dict(8)
        odict.insert(230, 1230)

        result = odict.successor(230)
        self.assertIsNone(result)

        result = odict.successor(231)
        self.assertIsNone(result)

        result = odict.successor(125)
        self.assertEqual(result, word(230, 8))

        result = odict.successor_node(125)
        self.assertEqual(result.key, word(230, 8))
        self.assertEqual(result.value, 1230)

    def test_ordered_dict_random_successor(self, seed=None):
        with self.random(seed) as rand:
            size = rand.randint(0, 150)
            samples = rand.sample(xrange(255), size)
            queries = rand.sample(xrange(255), size)
            queries.extend(samples[:size//2])

            odict = self.new_ordered_dict(8)
            odict.extend(samples)

            samples.sort()

            for query in queries:
                result = odict.successor(query)
                expect = self.successor(samples, query)
                expect = word(expect, 8) if expect is not None else None

                self.assertEqual(result, expect)

    def test_ordered_dict_prev_and_next_node(self):
        odict = self.new_ordered_dict(8)
        odict.insert(10, 110)
        odict.insert(12, 112)
        odict.insert(15, 115)
        odict.insert(13, 113)
        odict.insert(14, 114)

        node = odict.min_node()

        node = node.next_node()
        self.assertEqual(node.value, 112)

        node = node.next_node()
        self.assertEqual(node.value, 113)

        node = node.next_node()
        self.assertEqual(node.value, 114)

        node = node.next_node()
        self.assertEqual(node.value, 115)
        self.assertIsNone(node.next_node())

        odict.remove(14)

        self.assertEqual(node.value, 115)

        node = node.previous_node()
        self.assertEqual(node.value, 113)

        node = node.previous_node()
        self.assertEqual(node.value, 112)

        node = node.previous_node()
        self.assertEqual(node.value, 110)
        self.assertIsNone(node.previous_node())
