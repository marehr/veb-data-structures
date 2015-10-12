

class ReferenceTreeTestMixin(object):

    # DUPLICATE from static reference tree test??!?!
    def test_reference_random_search(self, seed=None):
        # Fixed seeds: 260471632980128674

        with self.random(seed) as rand:
            size = rand.randint(0, 150)
            samples = rand.sample(xrange(255), size)

            veb = self.new_trie(8, samples)
            ref = self.new_reference_trie(8, samples)

            self.assertEqualTrie(veb, ref)

            rand.shuffle(samples)
            for value in samples:
                a = veb.search_node(value)
                b = ref.search_node(value)

                self.assertEqualTree(a, b)

    def test_reference_random_predecessors(self, seed=None):
        with self.random(seed) as rand:
            size = rand.randint(0, 150)
            samples = rand.sample(xrange(255), size)

            veb = self.new_trie(8, samples)
            ref = self.new_reference_trie(8, samples)

            self.assertEqualTrie(veb, ref)

            rand.shuffle(samples)
            for value in samples:
                a = veb.predecessor(value)
                b = ref.predecessor(value)

                self.assertEqual(a, b)

    def test_reference_random_successor(self, seed=None):
        # Fixed Errors with seeds:
        # ======================================================================
        # 601513756194754376
        with self.random(seed) as rand:
            size = rand.randint(0, 150)
            samples = rand.sample(xrange(255), size)

            veb = self.new_trie(8, samples)
            ref = self.new_reference_trie(8, samples)

            self.assertEqualTrie(veb, ref)

            rand.shuffle(samples)
            for value in samples:
                a = veb.successor(value)
                b = ref.successor(value)

                self.assertEqual(a, b)

    def test_reference_random_lowest_common_ancestor(self, seed=None):
        # Fixed Errors with seeds:
        # ======================================================================
        # 6654739386600373571, 1082299352670606736, 4980390892282488568,
        # 3922406464876612439

        with self.random(seed) as rand:
            size = rand.randint(0, 150)

            # have random and contained elements as queries
            samples = rand.sample(xrange(255), size)
            queries = rand.sample(xrange(255), size)
            queries.extend(samples[:size//2])

            veb = self.new_trie(8, samples)
            ref = self.new_reference_trie(8, samples)

            self.assertEqualTrie(veb, ref)

            for q in queries:
                veb_lca, veb_child = veb.lowest_common_ancestor(q)
                ref_lca, ref_child = ref.lowest_common_ancestor(q)

                self.assertEqualTree(veb_lca, ref_lca)
                self.assertEqualTree(veb_child, ref_child)
