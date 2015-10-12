import unittest

import TestCase
import tests.mixins
import veb.normal as Normal
from word import word


class vEBnormalTest(TestCase.TestCase, tests.mixins.OrderedDictTestMixin):

    def new_ordered_dict(self, word_size, elements=[]):
        odict = Normal.Tree(word_size)
        odict.extend(elements)
        return odict

    def test_insert_3bit(self):
        veb = self.new_ordered_dict(3)
        xs = []

        for x in xrange(8):
            veb.insert(x)
            xs.append(word(x, 3))
            self.assertEqual(veb.elements(), xs)

    def test_insert(self):
        veb = self.new_ordered_dict(4)

        #
        inserted = veb.insert(0b1010, 110)

        self.assertEqual(inserted.short_key, word(0b1010, 4))
        self.assertEqual(inserted.key, word(0b1010, 4))
        self.assertEqual(inserted.value, 110)

        self.assertIs(veb.min, inserted)
        self.assertIs(veb.max, inserted)

        #
        inserted = veb.insert(0b1100, 112)

        self.assertEqual(veb.min.short_key, word(0b1010, 4))
        self.assertEqual(veb.min.key, word(0b1010, 4))
        self.assertEqual(veb.min.value, 110)

        self.assertEqual(inserted.short_key, word(0b1100, 4))
        self.assertEqual(inserted.key, word(0b1100, 4))
        self.assertEqual(inserted.value, 112)
        self.assertIs(veb.max, inserted)

        #
        inserted = veb.insert(0b1111, 115)

        self.assertEqual(veb.min.short_key, word(0b1010, 4))
        self.assertEqual(veb.min.key, word(0b1010, 4))
        self.assertEqual(veb.min.value, 110)

        cluster = veb.clusters[word(0b11, 2)]
        self.assertEqual(cluster.min.short_key, word(0b00, 2))
        self.assertEqual(cluster.min.key, word(0b1100, 4))
        self.assertEqual(cluster.min.value, 112)
        self.assertIs(cluster.max, cluster.min)

        self.assertEqual(inserted.short_key, word(0b1111, 4))
        self.assertEqual(inserted.key, word(15, 4))
        self.assertEqual(inserted.value, 115)
        self.assertIs(veb.max, inserted)

        #
        inserted = veb.insert(0b1101, 113)

        self.assertEqual(veb.min.short_key, word(0b1010, 4))
        self.assertEqual(veb.min.key, word(0b1010, 4))
        self.assertEqual(veb.min.value, 110)

        cluster = veb.clusters[word(0b11, 2)]
        self.assertEqual(cluster.min.short_key, word(0b00, 2))
        self.assertEqual(cluster.min.key, word(0b1100, 4))
        self.assertEqual(cluster.min.value, 112)

        self.assertEqual(cluster.max.short_key, word(0b01, 2))
        self.assertEqual(cluster.max.key, word(0b1101, 4))
        self.assertEqual(cluster.max.value, 113)
        self.assertIs(cluster.max, inserted)

        self.assertEqual(veb.max.short_key, word(0b1111, 4))
        self.assertEqual(veb.max.key, word(15, 4))
        self.assertEqual(veb.max.value, 115)

        #
        inserted = veb.insert(0b1110, 114)

        self.assertEqual(veb.min.short_key, word(0b1010, 4))
        self.assertEqual(veb.min.key, word(0b1010, 4))
        self.assertEqual(veb.min.value, 110)

        cluster = veb.clusters[word(0b11, 2)]
        self.assertEqual(cluster.min.short_key, word(0b00, 2))
        self.assertEqual(cluster.min.key, word(0b1100, 4))
        self.assertEqual(cluster.min.value, 112)

        cluster2 = cluster.clusters[word(0b0, 1)]
        self.assertEqual(cluster2.min.short_key, word(0b1, 1))
        self.assertEqual(cluster2.min.key, word(0b1101, 4))
        self.assertEqual(cluster2.min.value, 113)

        self.assertIs(cluster2.min, cluster2.max)

        self.assertEqual(cluster.max.short_key, word(0b10, 2))
        self.assertEqual(cluster.max.key, word(0b1110, 4))
        self.assertEqual(cluster.max.value, 114)
        self.assertIs(cluster.max, inserted)

        self.assertEqual(veb.max.short_key, word(0b1111, 4))
        self.assertEqual(veb.max.key, word(15, 4))
        self.assertEqual(veb.max.value, 115)

    def test_remove(self):
        veb = self.new_ordered_dict(4)

        veb.insert(0b1010, 110)
        veb.insert(0b1100, 112)
        veb.insert(0b1111, 115)
        veb.insert(0b1101, 113)
        veb.insert(0b1110, 114)

        removed = veb.remove(0b1110)
        self.assertEqual(removed.short_key, word(0b10, 2))
        self.assertEqual(removed.key, word(0b1110, 4))
        self.assertEqual(removed.value, 114)

        self.assertEqual(veb.min.short_key, word(0b1010, 4))
        self.assertEqual(veb.min.key, word(0b1010, 4))
        self.assertEqual(veb.min.value, 110)

        cluster = veb.clusters[word(0b11, 2)]
        self.assertEqual(cluster.min.short_key, word(0b00, 2))
        self.assertEqual(cluster.min.key, word(0b1100, 4))
        self.assertEqual(cluster.min.value, 112)

        self.assertEqual(cluster.max.short_key, word(0b01, 2))
        self.assertEqual(cluster.max.key, word(0b1101, 4))
        self.assertEqual(cluster.max.value, 113)

        self.assertEqual(veb.max.short_key, word(15, 4))
        self.assertEqual(veb.max.key, word(15, 4))
        self.assertEqual(veb.max.value, 115)

        #
        removed = veb.remove(0b1101)
        self.assertEqual(removed.short_key, word(0b01, 2))
        self.assertEqual(removed.key, word(0b1101, 4))
        self.assertEqual(removed.value, 113)

        self.assertEqual(veb.min.short_key, word(0b1010, 4))
        self.assertEqual(veb.min.key, word(0b1010, 4))
        self.assertEqual(veb.min.value, 110)

        cluster = veb.clusters[word(0b11, 2)]
        self.assertEqual(cluster.min.short_key, word(0b00, 2))
        self.assertEqual(cluster.min.key, word(0b1100, 4))
        self.assertEqual(cluster.min.value, 112)
        self.assertIs(cluster.max, cluster.min)

        self.assertEqual(veb.max.short_key, word(15, 4))
        self.assertEqual(veb.max.key, word(15, 4))
        self.assertEqual(veb.max.value, 115)

        #
        # import ipdb;ipdb.set_trace()
        removed = veb.remove(0b1111)
        self.assertEqual(removed.short_key, word(15, 4))
        self.assertEqual(removed.key, word(15, 4))
        self.assertEqual(removed.value, 115)

        self.assertEqual(veb.min.short_key, word(0b1010, 4))
        self.assertEqual(veb.min.key, word(0b1010, 4))
        self.assertEqual(veb.min.value, 110)

        self.assertEqual(veb.max.short_key, word(0b1100, 4))
        self.assertEqual(veb.max.key, word(0b1100, 4))
        self.assertEqual(veb.max.value, 112)

        #
        removed = veb.remove(0b1100)
        self.assertEqual(removed.short_key, word(0b1100, 4))
        self.assertEqual(removed.key, word(0b1100, 4))
        self.assertEqual(removed.value, 112)

        self.assertEqual(veb.min.short_key, word(0b1010, 4))
        self.assertEqual(veb.min.key, word(0b1010, 4))
        self.assertEqual(veb.min.value, 110)

        self.assertIs(veb.min, veb.max)

        #
        removed = veb.remove(0b1010)
        self.assertEqual(removed.short_key, word(0b1010, 4))
        self.assertEqual(removed.key, word(0b1010, 4))
        self.assertEqual(removed.value, 110)

        self.assertIsNone(veb.min)
        self.assertIsNone(veb.summary)
        self.assertIs(veb.min, veb.max)

    def test_delete(self):
        return
        # deleting elements
        veb = Normal.Tree(2)
        veb.insert(1)
        veb.insert(0)

        result = veb.delete(1)
        self.assertTrue(result)

        result = veb.delete(0)
        self.assertTrue(result)

        # reinsert elements
        veb.extend([1, 0])
        result = veb.elements()
        expects = self.data_words([0, 1], 2)
        self.assertEqual(result, expects)

        # test with more elements
        veb = self.new_ordered_dict(8)
        veb.extend([0, 15, 20, word(25, 8), 80, 255])

        result = veb.delete(20)
        self.assertTrue(result)

        result = veb.delete(5)
        self.assertFalse(result)

        result = veb.delete(0)
        self.assertTrue(result)

        result = veb.delete(255)
        self.assertTrue(result)

        result = veb.delete(80)
        self.assertTrue(result)

        result = veb.delete(15)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
