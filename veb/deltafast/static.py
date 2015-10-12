# coding=utf8

import veb.zfast.static
from word import word


class Tree(veb.zfast.static.Tree):

    def __init__(self, w):
        super(Tree, self).__init__(w)

        self.T[word.epsilon] = self.root
        self.T_d = {word.epsilon: self.root}

    # return depth = w - 2^2^i
    def _depth(self, i):
        depth = 1 << (1 << i)
        return max(0, self.w - depth)

    # return all prefixes of q for all possible depths
    def _depths(self, q):
        depth, i = 1, 0
        while depth > 0:
            # depth is >= 0
            depth = self._depth(i)
            c, _ = q.split(depth)
            yield c
            i = i + 1

    def insert(self, q, value=None):
        q = word(q, self.w)

        new_node = super(Tree, self).insert(q, value)
        branch_node = new_node.parent
        sibling = new_node.sibling()

        # print
        # print "`````````````````"
        # print "q: %s" % q

        depths = self._depths(q)

        # update edge of q and the sibling edge of q
        for c in depths:
            # print "c: %s" % c
            # print "branch_node: %s" % branch_node
            # print "sibling: %s" % sibling

            # prefix jumps over the branch_node.key, that means, that c is not on
            # the edge anymore
            if not (branch_node.key.w < c.w):
                break

            assert branch_node.key.w < c.w <= q.w
            assert new_node.is_on_edge(c)

            # update node on sibling edge
            if sibling and branch_node.key.w < c.w <= sibling.key.w:
                d = sibling.key.split_fst(c.w)
                assert sibling.is_on_edge(d)
                self.T_d[d] = branch_node

            # add node on edge of q
            self.T_d[c] = branch_node

        return new_node

    def _search_parameters(self, q, prefix):
        # use the new method
        w = self.w - prefix.w
        w_half = w >> 1

        bs_prefix, bs_suffix = q.split(prefix.w)

        # cautiuos:
        # child = lca.child_abs(prefix), instead use child = lca.child_abs(q)
        #
        # doesn't work, because the lca can be the root and prefix = epsilon,
        # therefore the precondition lca.key.w < prefix.w is not always given
        # and lca.child_abs(prefix) can't infere the correct child.
        lca = self.T_d[prefix]
        child = lca.child_abs(q)

        # print "lca: %s" % lca
        # print "prefix: %s" % prefix
        # print "child: %s" % child

        assert (lca.is_root() and prefix.is_epsilon()) or lca.key.w < prefix.w
        assert not child or (prefix.w <= child.key.w)

        return lca, child, bs_prefix, bs_suffix, w_half

    def lowest_common_ancestor_start(self, q, prefix):
        """
        Finds the lowest common ancestor starting from a given prefix.

        Preconditions:
            * ``prefix'' is a prefix of the lowest common ancestor
            * prefix is in the hash table T_d, that means |prefix| = w - 2^2^i

        The search time is O(log (w - |prefix|)).
        """
        lca, child, bs_prefix, bs_suffix, w_half = self._search_parameters(q, prefix)
        # print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        # print "lowest_common_ancestor_start::"
        # print "\tlca: %s" % lca
        # print "\tchild: %s" % child
        # print "\tedge: %s" % child.edge
        # print "\tprefix: %s" % prefix
        # print "\tquery: %s" % query
        # print "\tw: %s" % w

        lca, child, _ = self._lca_phase1(q, lca, child, bs_prefix, bs_suffix, w_half)

        return self._lca_phase2(q, lca, child)

    def _successor(self, q, prefix):
        try:
            prefix = prefix.succ()
        except TypeError:
            return False

        if prefix not in self.T_d:
            return False

        assert not prefix.is_epsilon()

        # we had to be cautious in _search_parameters of:
        # child = lca.child_abs(prefix)
        #
        # here it works, because the prefix is never empty.
        lca = self.T_d[prefix]
        child = lca.child_abs(prefix)

        assert lca.key.w < prefix.w <= child.key.w

        return child.min_leaf()

    def _predecessor(self, q, prefix):
        try:
            prefix = prefix.pred()
        except TypeError:
            return False

        if prefix not in self.T_d:
            return False

        assert not prefix.is_epsilon()

        # we had to be cautious in _search_parameters of:
        # child = lca.child_abs(prefix)
        #
        # here it works, because the prefix is never empty.
        lca = self.T_d[prefix]
        child = lca.child_abs(prefix)

        assert lca.key.w < prefix.w <= child.key.w

        return child.max_leaf()

    def predecessor_node(self, q):
        q = word(q, self.w)

        # q is in the set
        child = self.search_node(q)
        if child is not None:
            return child.previous_leaf()

        # print
        # print "%s" % self.T_d
        for c in self._depths(q):

            # print "depth: %s (%s)" % (c, c.w)

            if c in self.T_d:
                # print "T_d[c] != None"
                lca, child = self.lowest_common_ancestor_start(q, c)
                return self.predecessor_with_lca(q, lca, child)

            successor = self._successor(q, c)
            if successor:
                return successor.previous_leaf()

            predecessor = self._predecessor(q, c)
            if predecessor:
                return predecessor

        return None

    def successor_node(self, q):
        q = word(q, self.w)

        # q is in the set
        child = self.search_node(q)
        if child is not None:
            return child.next_leaf()

        # print
        # print "%s" % self.T_d
        for c in self._depths(q):

            # print "depth: %s (%s)" % (c, c.w)

            if c in self.T_d:
                # print "T_d[c] != None"
                lca, child = self.lowest_common_ancestor_start(q, c)
                return self.successor_with_lca(q, lca, child)

            successor = self._successor(q, c)
            if successor:
                return successor

            predecessor = self._predecessor(q, c)
            if predecessor:
                return predecessor.next_leaf()

        return None
