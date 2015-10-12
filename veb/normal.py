# coding=utf8

from word import word
import storage
import mixin.OrderedDict


class Tree(mixin.OrderedDict.OrderedDictMixin):

    def __init__(self, w, Storage=storage.HashArray, veb=None, name=None):
        self.w = w

        if name is None:
            name = word.epsilon

        self.name = name
        self.veb = veb or self
        self.storage = Storage
        self.clusters = Storage(w)
        self.summary = None
        self.min = self.max = None
        self._size = 0

    def __repr_array__(self, prefix=word.epsilon):
        if self.min is None:
            return []

        xs = self.clusters.values()
        xss = []

        min_ = prefix.concat(self.min.short_key)
        max_ = prefix.concat(self.max.short_key)

        xss.append(min_)

        for cluster in xs:
            newprefix = prefix.concat(cluster.name)
            elements = cluster.__repr_array__(newprefix)
            xss.append(elements)

        if min_ < max_:
            xss.append(max_)

        return xss

    def __repr__(self):
        xs = self.__repr_array__()
        return str(xs)

    def __flatten_array(self, lst):
        newlst = []
        for x in lst:
            if isinstance(x, list):
                x = self.__flatten_array(x)
            else:
                x = [x]

            newlst.extend(x)
        return newlst

    def size(self):
        return self._size

    def elements(self):
        xs = self.__repr_array__()
        xs = self.__flatten_array(xs)
        xs.sort()
        return xs

    def __create_or_use_cluster(self, c):
        cluster = self.clusters[c]

        if cluster is not None:
            return cluster

        cluster = Tree(self.w-c.w, self.storage, self.veb, c)
        self.clusters[c] = cluster

        if self.summary is None:
            self.summary = Tree(c.w, self.storage, self.veb, None)

        return cluster

    def search_node(self, q):
        q = word(q, self.w)
        try:
            return self._search(q)
        except KeyError:
            raise KeyError(q.x)

    def _search(self, q):
        c, i = q

        if self.min == q:
            return self.min

        if self.max == q:
            return self.max

        cluster = self.clusters[c]
        if cluster is None:
            raise KeyError(q)

        return cluster._search(i)

    def min_node(self):
        return self.min

    def max_node(self):
        return self.max

    def insert(self, q, value=None):
        q = word(q, self.w)
        try:
            new_node = self._insert(q, q, value)
            self._size += 1
            return new_node
        except ValueError as err:
            return err.args[0]

    def _insert(self, q, key, value):
        if self.min is None:
            self.min = self.max = Item(self.veb, q, key, value)
            return self.min

        if self.min == q:
            self.min.value = value
            raise ValueError(self.min)

        if self.max == q:
            self.max.value = value
            raise ValueError(self.max)

        one_element = self.min == self.max.short_key
        new_item = None

        if self.min > q:
            item = self.min
            self.min = new_item = Item(self.veb, q, key, value)
            q, key, value = item.short_key, item.key, item.value

        if self.max < q:
            item = self.max
            self.max = new_item = Item(self.veb, q, key, value)
            q, key, value = item.short_key, item.key, item.value

        if one_element:
            return new_item

        c, i = q
        cluster = self.__create_or_use_cluster(c)

        if cluster.min is None:
            self.summary._insert(c, None, None)

        inserted = cluster._insert(i, key, value)
        return new_item or inserted

    def successor_node(self, q):
        q = word(q, self.w)
        _, item = self._successor(q)
        return item

    def _successor(self, q):
        c, i = q

        if self.min is None:
            return None, None

        if self.max <= q:
            return None, None

        if self.min > q:
            return self.min.short_key, self.min

        if self.summary is None:
            return self.max.short_key, self.max

        cluster = self.clusters[c]
        assert cluster is None or cluster.max is not None

        if cluster is not None and cluster.max > i:
            succ, item = cluster._successor(i)
            assert succ is not None
            r = c.concat(succ)
            return r, item

        succ, _ = self.summary._successor(c)

        if succ is None:
            return self.max.short_key, self.max

        i = self.clusters[succ].min
        r = succ.concat(i.short_key)
        return r, i

    def predecessor_node(self, q):
        q = word(q, self.w)
        _, item = self._predecessor(q)
        return item

    def _predecessor(self, q):
        c, i = q

        if self.min is None:
            return None, None

        if self.min >= q:
            return None, None

        if self.max < q:
            return self.max.short_key, self.max

        if self.summary is None:
            return self.min.short_key, self.min

        cluster = self.clusters[c]
        assert cluster is None or cluster.min is not None

        if cluster is not None and cluster.min < i:
            pred, item = cluster._predecessor(i)
            assert pred is not None
            r = c.concat(pred)
            return r, item

        pred, _ = self.summary._predecessor(c)

        if pred is None:
            return self.min.short_key, self.min

        i = self.clusters[pred].max
        r = pred.concat(i.short_key)
        return r, i

    def remove(self, q):
        q = word(q, self.w)
        try:
            removed = self._remove(q)
            self._size -= 1
            return removed
        except KeyError:
            raise KeyError(q.x)

    def _remove_one(self, q):
        # at most two elements:
        # that means their is no summary, because nothing was inserted in
        # the clusters yet and we have to remove the two extra elements by hand

        # only one element in the set
        if self.min == self.max.short_key and self.max == q:
            removed = self.min
            self.min = self.max = None
            return removed

        # two elements in the set and the first will be removed
        if self.min == q:
            removed = self.min
            self.min = self.max
            return removed

        # two elements in the set and the second will be removed
        if self.max == q:
            removed = self.max
            self.max = self.min
            return removed

        # one or two elements in the set, but q is neither one of the elements
        raise KeyError()

    def _remove(self, q):
        assert self.summary is None or self.summary.min is not None
        if self.summary is None:
            return self._remove_one(q)

        removed = None
        c, i = q

        # the minimum will be removed, swap it with the successor
        if self.min == q:
            removed = self.min
            c = self.summary.min.short_key
            item = self.clusters[c].min
            i = item.short_key
            q = c.concat(i)
            self.min = Item(self.veb, q, item.key, item.value)

        # the maximum will be removed, swap it with the predecessor
        if self.max == q:
            removed = self.max
            c = self.summary.max.short_key
            item = self.clusters[c].max
            i = item.short_key
            q = c.concat(i)
            self.max = Item(self.veb, q, item.key, item.value)

        cluster = self.clusters[c]

        # no element found in the cluster, abort the deletion
        if cluster is None:
            raise KeyError()

        removed2 = cluster._remove(i)

        # cluster is empty after the deletion, remove it from the summary
        if cluster.min is None:
            del self.clusters[c]
            self.summary._remove(c)

        # no elements in the summary, remove it
        if self.summary.min is None:
            self.summary = None

        return removed or removed2


class Item(mixin.OrderedDict.Node):
    def __init__(self, veb, q, key, value):
        super(Item, self).__init__(key, value)
        self.short_key = q
        self.veb = veb

    def __repr__(self):
        t = (self.short_key, self.key, self.value)
        return repr(t)

    def previous_node(self):
        return self.veb.predecessor_node(self.key)

    def next_node(self):
        return self.veb.successor_node(self.key)

    """ All comparision operator assume on the left side the item and on the
    right side a word, i.e. a <= word(b, w)
    """
    def __lt__(self, other):
        return self.short_key < other

    def __le__(self, other):
        return self.short_key <= other

    def __eq__(self, other):
        return self.short_key == other

    def __ne__(self, other):
        return self.short_key != other

    def __gt__(self, other):
        return self.short_key > other

    def __ge__(self, other):
        return self.short_key >= other
