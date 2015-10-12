from word import word


class OrderedDictMixin(object):

    def search(self, q):
        """ Return the value of the element q, otherwise None.
            Raise KeyError, if q is not contained.
        """
        leaf = self.search_node(q)
        if leaf is None:
            q = q.x if isinstance(q, word) else q
            raise KeyError(q)

        return leaf.value

    def predecessor(self, q):
        """ Find max{ s \in S | s < q }
        """
        pred = self.predecessor_node(q)
        return pred and pred.key

    def successor(self, q):
        """ Find min{ s \in S | s > q }
        """
        succ = self.successor_node(q)
        return succ and succ.key

    def min(self, q):
        """ Find min S
        """
        min_ = self.min_node(q)
        return min_ and min_.key

    def max(self, q):
        """ Find max S
        """
        max_ = self.max_node(q)
        return max_ and max_.key

    def size(self):
        """ Return |S|
        """
        pass

    def search_node(self, q):
        """ Return the node, which stores q, otherwise None.
        """
        pass

    def predecessor_node(self, q):
        """ Return the node, which stores the predecessor of q, otherwise None.
        """
        pass

    def successor_node(self, q):
        """ Return the node, which stores the successor of q, otherwise None.
        """
        pass

    def min_node(self):
        """ Return the node, which stores the minimal element, otherwise None.
        """
        pass

    def max_node(self):
        """ Return the node, which stores the maximal element, otherwise None.
        """
        pass

    def insert(self, q, value=None):
        """ Insert q into the data structure and return the inserted leaf.
            Update value of search_node(q), if q is already contained.
        """
        pass

    def delete(self, q):
        """ Delete q from the data structure and return the removed leaf.
            Raise KeyError, if q is not contained.
        """
        pass

    def elements(self):
        """ Return the elements in a sorted list.
        """
        pass

    def extend(self, xs):
        """ Insert all elements in a batch.
        """
        for x in xs:
            self.insert(x)

    def new_node(self, key, value=None):
        """ Create a new node
        """
        pass

    def replace_node(self, node1, node2):
        """ Replace node1 with node2. The subclasses need to ensure, that their
        added additional information get transfered from node1 to node2.

        Raises ValueError, if both nodes does not represent the same key
        """
        if node1 is None or node2 is None:
            raise ValueError("can't swap with None")

        if node1.key != node2.key:
            raise ValueError("keys mismatch")


class Node(object):

    def __init__(self, key, value=None):
        self.key = key
        self.value = value

    def previous_node(self):
        """ Return the previous element in the ordered set S.
            Might be implemented by ```Predecessor.predecessor_node(self.key)```.
            May raise RuntimeError, if Node was deleted.
        """
        pass

    def next_node(self):
        """ Return the next element in the ordered set S.
            Might be implemented by ```Predecessor.successor_node(self.key)```.
            May raise RuntimeError, if Node was deleted.
        """
        pass
