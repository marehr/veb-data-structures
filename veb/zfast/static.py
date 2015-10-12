# coding=utf8

from word import word
import Trie


class Tree(Trie.Tree):

    def __init__(self, w):
        super(Tree, self).__init__(w)

        self.T = {}

        # use a Static.Node as root
        self.root = Node(word.epsilon, None)

    def _insert_leaf(self, q, root):
        new_node = super(Tree, self)._insert_leaf(q, root)

        # insert / update table
        self.insert_dict(new_node)

        return new_node

    def _insert_node(self, q, parent, child_node):
        branch_node, new_node = super(Tree, self)._insert_node(q, parent, child_node)

        # insert / update table
        self.insert_dict(branch_node)
        self.insert_dict(child_node)
        self.insert_dict(new_node)

        return branch_node, new_node

    def _remove_leaf_of_root(self, branch, leaf):
        self.remove_dict(leaf)

        return super(Tree, self)._remove_leaf_of_root(branch, leaf)

    def _remove_node(self, leaf, parent, branch, sibling):
        self.remove_dict(leaf)
        self.remove_dict(branch)
        self.remove_dict(sibling)

        sibling = super(Tree, self)._remove_node(leaf, parent, branch, sibling)

        self.insert_dict(sibling)
        return sibling

    def search_node(self, q):
        q = word(q, self.w)

        try:
            root = self.T[q]
        except KeyError:
            return None

        # root is the parent of the searched leaf
        q = q.remove_prefix(root.key)[0]
        return root.child(q)

    """
    Finds the lowest common ancestor.
    """
    def lowest_common_ancestor(self, query):
        query = word(query, self.w)

        # child is contained
        child = self.search_node(query)
        if child is not None:
            return [child, None]

        # child is not contained
        lca, child, index = self._lca_phase1(
            query, self.root, self.root.child(query),
            word.epsilon, query, self.w >> 1
        )

        lca, child = self._lca_phase2(query, lca, child)

        return lca, child

    """
    Finds the lowest common ancestor.

    lca = self.root, is the currently found lowest ancestor, root at the start
    child = self.root.left if q starts qith a zero or self.root.right if q
            starts with a one, represents the edge of the currently found lowest
            ancestor
    q = prefix + query, is the original query
    query = q, is the remaining query to search
    prefix = word.epsilon, is the lower bound of the binary search
    w = self.w / 2, is the remaining word size
    """
    def _lca_phase1(self, q, lca, child, prefix, query, w):
        if w == 0:
            return [lca, child, prefix]

        c, i = query
        index = prefix.concat(c)

        # print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        # print "_lca_phase1::"
        # print "\tq: %s" % q
        # print "\tlca: %s" % lca
        # print "\tchild: %s" % child
        # print "\tprefix: %s" % prefix
        # print "\tquery: %s" % query
        # print "\tw: %s\n" % w
        # print "\tc: %s" % c
        # print "\ti: %s" % i
        # print "\tindex: %s" % index

        # either we found a knew edge
        if index in self.T:
            lca = self.T[index]
            child = lca.child_abs(q)

            # print "case 1: new edge"
            return self._lca_phase1(q, lca, child, index, i, w >> 1)

        # or the ``index'' is on an old edge (this is the last found edge)
        if child and child.key.has_prefix(index):
            # print "case 2: on old edge"
            return self._lca_phase1(q, lca, child, index, i, w >> 1)

        # print "case 3: shorter edge"
        # or the searched lca is shorter than ``index''
        return self._lca_phase1(q, lca, child, prefix, c, w >> 1)

    def _lca_phase2(self, query, lca, child):
        # if child is None, lca == self.root and no edge was inserted in the
        # subtree
        if child is None:
            return [lca, child]

        # the query lies between two edges. either it is already the correct one or
        # it is one edge below the current edge
        if not query.has_prefix(child.key):
            return [lca, child]

        q = query.remove_prefix(child.key)[0]

        # its actual on the next edge
        lca = child
        child = lca.child(q)
        return [lca, child]

    def insert_dict(self, node):
        assert not node.is_root()

        index = node.hash_index()
        self.T[index] = node.parent
        node.index = index

    def remove_dict(self, node):
        del self.T[node.index]
        del node.index

    @staticmethod
    def two_fattest_number(left, right):
        """
        Left and right are numbers from an interval.
        """
        diff = left ^ right
        msb = word.epsilon._msb(diff) - 1
        return (right >> msb) << msb

    """
    Left is the node.parent.key and right is the node.key
    """
    @staticmethod
    def hash_index(left, right):
        if left.w == right.w and left == right:
            return left

        # calculate the word size of the prefix, that perfectly aligns to a
        # binary search and that would be hit first in the interval (left.w,
        # right.w]
        w = Tree.two_fattest_number(left.w, right.w)

        index, _ = right.split(w)
        return index


class Node(Trie.Node):

    def __init__(self, edge, parent):
        super(Node, self).__init__(edge, parent)

    def hash_index(self):
        assert not self.is_root()
        return Tree.hash_index(self.parent.key, self.key)

    """
    Returns the minimum of this subtree starting by self.

    If self is a leaf it will return itself.
    """
    def min_leaf(self):
        if self.is_root():
            self = self.left or self.right

        return self and getattr(self, '_min_leaf', self)

    """
    Returns the maximum of this subtree starting by self.

    If self is a leaf it will return itself.
    """
    def max_leaf(self):
        if self.is_root():
            self = self.left or self.right

        return self and getattr(self, '_max_leaf', self)

    """
    Find the previous leaf assuming that the searched leaf is not in the
    left subtree of the node self

    This handles the cases, that self is a leaf or a query diverges left of
    the edge (self, self.parent)
    """
    def previous_leaf(self):
        leaf = self.min_leaf()
        if leaf is None:
            return None
        return leaf._previous_leaf

    """
    Find the successor leaf assuming that the searched leaf is not in the
    right subtree of the node self

    This handles the cases, that self is a leaf or a query diverges right of
    the edge (self, self.parent)
    """
    def next_leaf(self):
        leaf = self.max_leaf()
        if leaf is None:
            return None
        return leaf._next_leaf

    def _update_min_max_insert(self, new_node, branch_node):
        curr = branch_node

        # we dont update the root
        while curr.parent is not None:

            # at least one child is not None
            if curr.right is None or curr.left is not None and \
                curr.left.min_leaf().key < curr.right.min_leaf().key:
                curr._min_leaf = curr.left.min_leaf()
            else:
                curr._min_leaf = curr.right.min_leaf()

            # at least one child is not None
            if curr.right is None or curr.left is not None and \
                curr.left.max_leaf().key > curr.right.max_leaf().key:
                curr._max_leaf = curr.left.max_leaf()
            else:
                curr._max_leaf = curr.right.max_leaf()

            curr = curr.parent

    def _update_linked_leaves_insert(self, new_node, branch_node):
        assert self is new_node.sibling()

        # put new_node in the list of leaves
        sibling_node = self
        if new_node is branch_node.left:
            next_leaf = sibling_node.min_leaf()
            prev_leaf = next_leaf.previous_leaf()
        else:
            prev_leaf = sibling_node.max_leaf()
            next_leaf = prev_leaf.next_leaf()

        assert prev_leaf is None or prev_leaf.key < new_node.key
        assert next_leaf is None or next_leaf.key > new_node.key

        if prev_leaf is not None:
            prev_leaf._next_leaf = new_node

        if next_leaf is not None:
            next_leaf._previous_leaf = new_node

        new_node._previous_leaf = prev_leaf
        new_node._next_leaf = next_leaf

    def _update_min_max_remove(self, parent_node, branch_node, sibling_node):
        branch_node._min_leaf = sibling_node.min_leaf()
        branch_node._max_leaf = sibling_node.max_leaf()

        self._update_min_max_insert(branch_node, parent_node)

    def _update_linked_leaves_remove(self):
        # remove self from the list of leaves
        prev_leaf = self._previous_leaf
        next_leaf = self._next_leaf

        if prev_leaf is not None:
            prev_leaf._next_leaf = next_leaf

        if next_leaf is not None:
            next_leaf._previous_leaf = prev_leaf

        assert prev_leaf is None or next_leaf is None or prev_leaf.key < next_leaf.key

    def insert_leaf(self, q):
        new_node = super(Node, self).insert_leaf(q)

        root = self
        sibling = new_node.sibling()

        if sibling is None:
            # first leaf has to be initialized
            new_node._previous_leaf = new_node._next_leaf = None
        else:
            sibling._update_linked_leaves_insert(new_node, root)

        return new_node

    def insert_node(self, q):
        branch_node, new_node = super(Node, self).insert_node(q)

        self._update_min_max_insert(new_node, branch_node)
        self._update_linked_leaves_insert(new_node, branch_node)

        return branch_node, new_node

    def remove_leaf_of_root(self, root):
        self._update_linked_leaves_remove()

        return super(Node, self).remove_leaf_of_root(root)

    def remove_node(self, parent, branch, sibling):
        self._update_linked_leaves_remove()
        self._update_min_max_remove(parent, branch, sibling)

        return super(Node, self).remove_node(parent, branch, sibling)
