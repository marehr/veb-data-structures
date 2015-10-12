from word import word

import tests.mixins.static


class ReferenceTreeTestMixin(tests.mixins.static.ReferenceTreeTestMixin):

    def test_insert(self):
        veb = self.new_trie(4)
        ref = self.new_reference_trie(4)

        # \
        #  0111
        a = word(0b0111, 4)
        ref.insert(a)
        veb.insert(a)

        self.assertEqualTrie(veb, ref)

        #   0111
        # /
        # \
        #   1000
        b = word(0b1000, 4)
        ref.insert(b)
        veb.insert(b)

        self.assertEqualTrie(veb, ref)

        #   0111
        # /
        # \
        #   1 - 000
        #    \
        #     - 001
        c = word(0b1001, 4)
        ref.insert(c)
        veb.insert(c)

        self.assertEqualTrie(veb, ref)

    def test_insert_order(self):
        # seed: 6897201961525902772
        veb = self.new_trie(8)
        ref = self.new_reference_trie(8)

        a = word(0b00110111, 8)
        ref.insert(a)
        veb.insert(a)

        self.assertEqualTrie(veb, ref)

        # \
        #  00 - 011001
        #    \
        #     - 110111
        b = word(0b00011001, 8)
        ref.insert(b)
        veb.insert(b)

        self.assertEqualTrie(veb, ref)

        # \
        #  00 - 011 - 001
        #    |     \
        #    |      - 100
        #    \
        #     - 110   111

        c = word(0b00011100, 8)
        ref.insert(c)
        veb.insert(c)

        self.assertEqualTrie(veb, ref)

    def test_reference_random_insert(self):
        with self.random() as rand:
            size = rand.randint(0, 150)
            samples = rand.sample(xrange(255), size)

            veb = self.new_trie(8)
            ref = self.new_reference_trie(8)

            for value in samples:
                a = word(value, 8)

                try:
                    ref.insert(a)
                    veb.insert(a)
                except ValueError:
                    continue

                self.assertEqualTrie(veb, ref)

    def test_reference_random_delete(self):
        with self.random() as rand:
            size = rand.randint(0, 150)
            samples = rand.sample(xrange(255), size)

            veb = self.new_trie(8, samples)
            ref = self.new_reference_trie(8, samples)

            while len(samples) > 0:
                rand.shuffle(samples)
                val = samples.pop()

                veb.remove(val)
                ref.remove(val)

                self.assertEqualTrie(veb, ref)

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
