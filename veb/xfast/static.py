# coding=utf8

from word import word
import Trie


class Tree(Trie.Tree):
    """ The static X-fast trie implementation, which uses the the static trie
    nodes. Those nodes have an pointer to the minimal and maximal leaf of their
    subtree and therefore, take O(1) access time to those leaves. Furthermore,
    are the leaves linked together.

    A special note. The X-fast trie differs from the common presentation, that
    it builds an index into a compact binary trie, and not an index into a
    non-compact trie.
    """

    def __init__(self, w):
        super(Tree, self).__init__(w)

        # use a Static.Node as root
        self.root = Node(word.epsilon, None)

        self.T = {word.epsilon: self.root}

    def replace_node(self, node1, node2):
        super(Tree, self).replace_node(node1, node2)

        lca = node2.parent
        leaf = node2

        # repair hash table
        self._insert_hash_table(lca, leaf, None)

    def _insert_leaf(self, q, value, root):
        new_node = super(Tree, self)._insert_leaf(q, value, root)

        self._insert_hash_table(root, new_node, None)

        return new_node

    def _insert_node(self, q, value, parent, child_node):
        branch_node, new_node = super(Tree, self)._insert_node(q, value, parent, child_node)

        self._insert_hash_table(branch_node, new_node, new_node.sibling())

        return branch_node, new_node

    def _insert_hash_table(self, lca, leaf, sibling_leaf):
        # insert all nodes from below lca and above the leaf
        for w in xrange(lca.key.w+1, leaf.key.w):
            prefix = leaf.key.split_fst(w)
            self.T[prefix] = lca

        # update all nodes up to the sibling
        silb_w = sibling_leaf and sibling_leaf.key.w or 0
        for w in xrange(lca.key.w+1, silb_w):
            prefix = sibling_leaf.key.split_fst(w)
            self.T[prefix] = lca

        self.T[lca.key] = lca
        self.T[leaf.key] = leaf

    def _remove_leaf_of_root(self, branch, leaf):
        assert branch is self.root
        self._remove_hash_table(self.root, branch, leaf, None)

        return super(Tree, self)._remove_leaf_of_root(branch, leaf)

    def _remove_node(self, leaf, parent, branch, sibling):
        self._remove_hash_table(parent, branch, leaf, sibling)

        sibling = super(Tree, self)._remove_node(leaf, parent, branch, sibling)

        return sibling

    def _remove_hash_table(self, parent, lca, leaf, sibling_leaf):
        # remove all nodes strictly below lca and including the leaf
        for w in xrange(lca.key.w+1, leaf.key.w+1):
            prefix = leaf.key.split_fst(w)
            del self.T[prefix]

        # update all nodes up to the sibling
        silb_w = sibling_leaf and sibling_leaf.key.w or 0
        for w in xrange(lca.key.w+1, silb_w):
            prefix = sibling_leaf.key.split_fst(w)
            self.T[prefix] = parent

        self.T[lca.key] = parent

    def search_node(self, q):
        q = word(q, self.w)

        try:
            return self.T[q]
        except KeyError:
            return None

    def lowest_common_ancestor(self, query):
        query = word(query, self.w)

        prefix = word.epsilon
        suffix = query
        w = self.w

        if query in self.T:
            lca = self.T[query]
            return [lca, None]

        while w > 1:
            w = w >> 1
            c, i = suffix
            new_prefix = prefix.concat(c)

            if new_prefix in self.T:
                prefix = new_prefix
                suffix = i
            else:
                suffix = c

        lca = self.T[prefix]
        child = lca.child_abs(query)

        return lca, child


class Node(Trie.Node):

    def __init__(self, edge, parent, value=None):
        super(Node, self).__init__(edge, parent, value)
