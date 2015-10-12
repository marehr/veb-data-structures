# coding=utf8

from word import word
import math
import Trie


class Tree(Trie.Tree):

    def __init__(self, w):
        super(Tree, self).__init__(w)

        self.T_lcas = {}
        self.T = {}
        self.sqrt_log_u = int(math.ceil(math.sqrt(w)))

    def construct(self, items):
        trie = Trie.Tree(self.w)
        trie.extend(items)

        self.root = trie.root

        self._add_branch_node(self.root, self.root)

        # start at next_depth = self.sqrt_log_u, because epsilon was already added
        self._construct_hash_table(self.root, self.root.left, next_depth=self.sqrt_log_u)
        self._construct_hash_table(self.root, self.root.right, next_depth=self.sqrt_log_u)

    def _add_node(self, hash_index, lca):
        # self.T[hash_index] = lca
        diff = hash_index.w - lca.key.w
        self.T[hash_index] = diff

    def _add_branch_node(self, lca, current):
        self.T_lcas[current.key] = current
        self._add_node(current.key, current)

    def _add_nodes_below_lca(self, lca, current):
        # add all nodes below the sqrt(log u) range of the lca

        # exclude the branch node `lca`
        min_length = lca.depth() + 1
        max_length = current.depth()

        end_length = min(max_length, min_length + self.sqrt_log_u)

        current_word = current.key
        for length in xrange(min_length, end_length):
            new_word, _ = current_word.split(length)
            self._add_node(new_word, lca)

    def _add_nodes_at_sqrt_log_u(self, lca, current, next_depth):
        # add all nodes with depth D_i := i \sqrt \log u and
        # lca.depth <= D_i < current.depth for all i
        current_depth = current.depth()

        current_word = current.key
        while next_depth < current_depth:
            new_word, _ = current_word.split(next_depth)
            self._add_node(new_word, lca)

            next_depth += self.sqrt_log_u

        # if the next depth is a branch node, skip it, because it will
        # be added by self._add_branch_node
        if current_depth == next_depth:
            next_depth += self.sqrt_log_u

        return next_depth

    def _construct_hash_table(self, lca, current, next_depth):
        if current is None:
            return

        self._add_branch_node(lca, current)
        self._add_nodes_below_lca(lca, current)
        next_depth = self._add_nodes_at_sqrt_log_u(lca, current, next_depth)

        self._construct_hash_table(current, current.left, next_depth)
        self._construct_hash_table(current, current.right, next_depth)

    def _in_hash(self, q, depth):
        lca, child, u, v = self._get_edge(q, depth)

        # is v really a member of the existing edge (u, w), where w =
        # child.key, it may point to a wrong edge

        if child and child.is_lowest_branch_node(v):
            return [lca, child]

        return None

    def _get_edge(self, q, depth):
        v = q.split(depth)[0]

        try:
            up = self.T[v]
        except KeyError:
            return None

        u, i = q.split(depth - up)
        try:
            lca = self.T_lcas[u]
        except KeyError:
            return None

        # lca is the lower endpoint of the edge (u*, v), where u = v = lca,
        # we need to get the correct u*, which is the parent of v, s.t.
        # u* < v <= w holds, where w = v = u = lca
        if up == 0:
            lca, child = lca.parent, lca
        else:
            child = lca.child(i)

        return lca, child, u, v

    def _lca_search1(self, q, depth, min_, max_):
        if max_ < min_:
            return depth

        mid = (min_ + max_) >> 1

        # WHAT IS THE RUNTIME? BECAUSE OF THE MULTIPLICATION?
        # IF x in w = 2^x is even, the multiplication is only a shift
        new_depth = mid * self.sqrt_log_u
        is_greater = self._get_edge(q, new_depth) is not None

        if is_greater:
            return self._lca_search1(q, new_depth, mid + 1, max_)
        else:
            return self._lca_search1(q, depth, min_, mid - 1)

    def _lca_search2(self, q, depth, min_, max_):
        if max_ < min_:
            assert max_ < min_
            return depth

        mid = (min_ + max_) >> 1

        new_depth = mid
        is_greater = self._get_edge(q, new_depth) is not None

        if is_greater:
            return self._lca_search2(q, new_depth, mid + 1, max_)
        else:
            return self._lca_search2(q, depth, min_, mid - 1)

    def lowest_common_ancestor(self, q):
        q = word(q, self.w)

        if q in self.T_lcas:
            return [self.T_lcas[q], None]

        depth = self._lca_search1(q, 0, 0, self.sqrt_log_u - 1)
        u, v = self._get_edge(q, depth)[0:2]

        # q is below the edge u and v, iff
        #       q = v_0 ... v_|v|-1 q_|v| ... q_|q|-1
        if not q.has_prefix(v.key):
            return [u, v]

        min_ = v.key.w
        max_ = depth + self.sqrt_log_u

        depth = self._lca_search2(q, min_, min_, max_)
        u, v = self._get_edge(q, depth)[0:2]
        return [u, v]
