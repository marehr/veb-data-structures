# coding=utf8

from word import word
import mixin.OrderedDict


class Tree(mixin.OrderedDict.OrderedDictMixin):

    def __init__(self, w):
        self.w = w
        self._size = 0

        # use a Trie.Node as root
        self.root = Node(word.epsilon, None)

    def __iter__(self):
        return Iterators.preorder(self.root)

    def insert(self, q, value=None):
        """
        Insert q into the trie
        """
        q = word(q, self.w)

        start_node = self.root.child(q)

        if start_node is None:
            node = self._insert_leaf(q, value, self.root)
            self._size += 1
            return node

        assert \
            start_node.is_leaf() or (
                start_node.left is not None and
                start_node.right is not None
            ), "start_node is either a leaf or a strict branch node"

        lca, child = self.lowest_common_ancestor(q)

        if lca.is_leaf_of(q):
            lca.value = value
            return lca

        assert \
            child is not None, \
            "the subtree in which q belongs is not empty"

        _, new_node = self._insert_node(q, value, lca, child)
        self._size += 1
        return new_node

    def remove(self, q):
        """
        Remove q from the trie
        """
        leaf = self.search_node(q)

        # element is not in the set
        if leaf is None:
            q = word(q, self.w)
            raise KeyError(repr(q.x))

        self._size -= 1

        branch = leaf.parent
        if branch.is_root():
            self._remove_leaf_of_root(branch, leaf)
        else:
            parent = branch.parent
            sibling = leaf.sibling()
            self._remove_node(leaf, parent, branch, sibling)

        return leaf

    def _remove_leaf_of_root(self, branch, leaf):
        return leaf.remove_leaf_of_root(branch)

    def _remove_node(self, leaf, parent, branch, sibling):
        return leaf.remove_node(parent, branch, sibling)

    def _insert_leaf(self, q, value, root):
        return root.insert_leaf(q, value)

    def _insert_node(self, q, value, parent, child):
        return child.insert_node(q, value)

    def elements(self):
        xs = []
        prefix = word.epsilon

        return self._elements(self.root, prefix, xs)

    def _elements(self, root, prefix, xs):
        prefix = prefix.concat(root.edge)

        if root.is_leaf():
            assert prefix == root.key
            xs.append(prefix)
            return xs

        if root.left is not None:
            self._elements(root.left, prefix, xs)

        if root.right is not None:
            self._elements(root.right, prefix, xs)

        return xs

    def new_node(self, q, value=None):
        q = word(q, self.w)
        node = self.root.new_node(q, value)

        # create a new loose node
        node.parent = None
        return node

    def replace_node(self, node1, node2):
        super(Tree, self).replace_node(node1, node2)
        node1.swap_node(node2)

    def search_node(self, q):
        q = word(q, self.w)

        lca, child = self.lowest_common_ancestor(q)

        if lca.is_leaf_of(q):
            return lca

        return None

    def lowest_common_ancestor(self, q):
        """
        lca - lowest common ancestor
        child - child of lowest common ancestor in the direction of q

        return [lca, child]
        """
        q = word(q, self.w)
        start_node = self.root.child(q)

        # q navigates into an empty subtree of the root
        if start_node is None:
            return [self.root, None]

        curr = start_node
        c, i = q.split(curr.edge.w)

        # c == curr.edge iff q.has_prefix(curr.key)
        while not curr.is_leaf() and c == curr.edge:
            curr = curr.child(i)
            c, i = i.split(curr.edge.w)

        if c == curr.edge:
            return [curr, None]

        return [curr.parent, curr]

    def size(self):
        return self._size

    def min_node(self):
        return self.root.min_leaf()

    def max_node(self):
        return self.root.max_leaf()

    def predecessor_node(self, q):
        q = word(q, self.w)

        # tree is empty
        if self.root.is_leaf():
            return None

        lca, child = self.lowest_common_ancestor(q)
        return self.predecessor_with_lca(q, lca, child)

    def successor_node(self, q):
        q = word(q, self.w)

        # tree is empty
        if self.root.is_leaf():
            return None

        lca, child = self.lowest_common_ancestor(q)
        return self.successor_with_lca(q, lca, child)

    def predecessor_with_lca(self, q, lca, child):
        """
        Search the predecessor starting from the lca of q
        """
        # q is in the set and therefore is the lca a leaf
        if lca.is_leaf_of(q):
            return lca.previous_leaf()

        # a special case if the subtree, where q goes into, of the root is empty
        if child is None:
            return lca.left and lca.left.max_leaf()

        _, suffix_lcp, lcp = q.remove_prefix(child.key)
        lcp_has_left_child = suffix_lcp.first_bit() == 0

        if lcp_has_left_child:
            v_p = child.max_leaf()
            return v_p

        v_s = child.min_leaf()
        return v_s.previous_leaf()

    def successor_with_lca(self, q, lca, child):
        """
        Search the successor starting from the lca of q
        """
        # q is in the set and therefore is the lca a leaf
        if lca.is_leaf_of(q):
            return lca.next_leaf()

        # a special case if the subtree, where q goes into, of the root is empty
        if child is None:
            return lca.right and lca.right.min_leaf()

        _, suffix_lcp, lcp = q.remove_prefix(child.key)
        lcp_has_right_child = suffix_lcp.first_bit() == 1

        if lcp_has_right_child:
            v_s = child.min_leaf()
            return v_s

        v_p = child.max_leaf()
        return v_p.next_leaf()


class Iterators(object):

    @staticmethod
    def preorder(root):
        """ Traverses all nodes in the trie in preorder.
        """
        current = root.min_leaf()

        while current is not None:
            yield current
            current = current.next_inner_node()


class Node(mixin.OrderedDict.Node):

    def __init__(self, edge, parent, value=None):
        key = parent.key.concat(edge) if parent is not None else word.epsilon
        super(Node, self).__init__(key, value)

        self.edge = edge
        self.left = None
        self.right = None
        self.parent = parent

    def __eq__(self, other):
        if other is None:
            return False

        has_parent1 = self.parent is not None
        has_parent2 = other.parent is not None
        has_left1 = self.left is not None
        has_left2 = other.left is not None
        has_right1 = self.right is not None
        has_right2 = other.right is not None

        return \
            self.key == other.key and self.value == other.value and \
            self.edge == other.edge and has_parent1 == has_parent2 and \
            has_left1 == has_left2 and has_right1 == has_right2

    def __repr__(self):
        return "(%s; %s)" % (self.key, self.edge)

    def depth(self):
        return self.key.w

    def child(self, query):
        """
        If q's first bit is zero it returns the left child. Otherwise the right
        child.

        query is relative to the node self
        """
        if query.is_epsilon():
            return None

        if self.is_left(query):
            return self.left
        else:
            return self.right

    def child_abs(self, q):
        """
        Return the child, where q is contained.

        q is absolute
        """
        edge = q.remove_prefix(self.key)[0]
        return self.child(edge)

    def set_child(self, child):
        if self.is_left(child.edge):
            self.left = child
        else:
            self.right = child

    def destroy(self):
        self.left = None
        self.right = None
        self.parent = None

    def is_left(self, q):
        """
        True, if q first bit is zero. That means that q should navigate further
        into the tree rooted at the left child.

        q is relative to the node self
        """
        return q.first_bit() == 0

    def is_left_of_edge(self, q):
        """
        Branches q on the edge (self, self.parent) to the left?

        q is the whole w-bit number
        """
        c, i = q.split(self.key.w)
        return c < self.key

    def is_right_of_edge(self, q):
        """
        Branches q on the edge (self, self.parent) to the right?

        q is the whole w-bit number
        """
        c, i = q.split(self.key.w)
        return c > self.key

    def root(self):
        curr = self
        while curr.parent is not None:
            curr = curr.parent
        return curr

    def sibling(self):
        parent = self.parent

        if parent.left is self:
            return parent.right
        else:
            return parent.left

    def is_empty(self):
        return self.is_root() and self.is_leaf()

    def is_root(self):
        return self.parent is None

    def is_leaf(self):
        return self.left is None and self.right is None

    def is_leaf_of(self, q):
        """
        q is the whole w-bit number
        """
        # special case:
        # * if the structure is empty, then there are no leaves
        # * if it is not empty, the root is not a leave
        if self.is_root():
            return False

        return self.is_leaf() and self.key == q

    def is_on_edge(self, q):
        """
        Checks if q is on the edge, by determining whether q is in the interval
        of prefices (self.parent, self] or not.

        q is an address of an inner node
        """
        if self.parent is None:
            return q.is_epsilon()

        low = self.parent.key
        high = self.key

        # to short, q should be at least one letter larger or to long
        if not (low.w < q.w <= high.w):
            return False

        # check prefix of q, that it matches with the nodes prefix
        return high.has_prefix(q)

    def is_lowest_branch_node(self, p):
        """
        Checks if the current node is the lowest branch node of p.

        If p is the key of this node, i.e. a branch node, the function will
        return true.

        p is an address of an inner node
        """
        return self.is_on_edge(p)

    def new_node(self, edge, value=None):
        """
        Create a new node, which has the self node as parent. The key will be
        constructed from the parent.key and the edge label.
        """
        parent = self
        return self.__class__(edge, parent, value)

    def insert_leaf(self, q, value):
        """
        q is the whole w-bit number
        """
        root_node = self

        new_node = root_node.new_node(q, value)
        root_node.set_child(new_node)

        return new_node

    def insert_node(self, q, value):
        """
        Insert a branch node between self and self.parent and add a leaf to the
        branch node with q as key

        return branch_node and new_node, which contains q

        precondition: q must be lexicographic between self and self.parent, that
        means q branches of on this edge

        q is the whole w-bit number
        """
        root_node = self.parent
        sibling_node = self

        suffix = q.remove_prefix(root_node.key)[0]
        new_edge, sibling_edge, branch_edge = suffix.remove_prefix(sibling_node.edge)

        #  r
        #  | \
        #  b   \
        #  |\    \
        #  | \     \
        #  s  \      other child
        #      n

        branch_node = root_node.new_node(branch_edge)
        root_node.set_child(branch_node)
        new_node = branch_node.new_node(new_edge, value)

        sibling_node.edge = sibling_edge
        sibling_node.parent = branch_node

        if branch_node.is_left(sibling_node.edge):
            branch_node.left = sibling_node
            branch_node.right = new_node
        else:
            branch_node.left = new_node
            branch_node.right = sibling_node

        return [branch_node, new_node]

    def remove_leaf_of_root(self, root):
        """
        Remove the current node from the trie

        Returns None
        """
        assert root is self.parent
        #  r
        #  |\
        #  | \
        #  s  \
        #      other child
        self.parent = None

        if root.left is self:
            root.left = None
        elif root.right is self:
            root.right = None
        else:
            raise AssertionError("Internal error, tree links are defect")

        return None

    def remove_node(self, parent, branch, sibling):
        """
        Remove the current and branch node from the trie

        Returns sibling
        """
        #  p
        #  |
        #  b
        #  |\
        #  | \
        #  s \
        #      sibling
        sibling_edge = branch.edge.concat(sibling.edge)

        sibling.edge = sibling_edge
        sibling.parent = parent

        if parent.left is branch:
            parent.left = sibling
        elif parent.right is branch:
            parent.right = sibling
        else:
            raise AssertionError("Internal error, tree links are defect")

        branch.destroy()
        self.destroy()

        return sibling

    def previous_leaf(self):
        """
        Find the previous leaf assuming that the searched leaf is not in the
        left subtree of the node self

        That means, if self
            * is a leaf return the predecessor leaf
            * is not a leaf return self.min_leaf().previous_leaf()
        """
        current = self
        # find first parent, where the current subtree is right child of parent
        while current.parent is not None and current.parent.left is current:
            current = current.parent

        # either reached root or the current parent has no left subtree
        if current.parent is None or current.parent.left is None:
            return None

        # left subtree is not the current subtree
        return current.parent.left.max_leaf()

    def previous_node(self):
        return self.previous_leaf()

    def next_leaf(self):
        """
        Find the successor leaf assuming that the searched leaf is not in the
        right subtree of the node self

        That means, if self
            * is a leaf return the successor leaf
            * is not a leaf return self.max_leaf().next_leaf()
        """
        current = self
        # find first parent, where the current subtree is left child of parent
        while current.parent is not None and current.parent.right is current:
            current = current.parent

        # either reached root or the current parent has no right subtree
        if current.parent is None or current.parent.right is None:
            return None

        # right subtree is not the current subtree
        return current.parent.right.min_leaf()

    def next_node(self):
        return self.next_leaf()

    def min_leaf(self):
        """
        Returns the minimum of this subtree starting by self.

        If self is a leaf it will return itself.
        """
        # if root is empty, then there is no min_leaf
        if self.is_empty():
            return None

        curr = self

        while not curr.is_leaf():
            if curr.left is None:
                curr = curr.right
            else:
                curr = curr.left

        return curr

    def max_leaf(self):
        """
        Returns the maximum of this subtree starting by self.

        If self is a leaf it will return itself.
        """
        # if root is empty, then there is no min_leaf
        if self.is_empty():
            return None

        curr = self

        while not curr.is_leaf():
            if curr.right is None:
                curr = curr.left
            else:
                curr = curr.right

        return curr

    def next_inner_node(self):
        """
        Returns the next Node (next key value larger)
        """
        # If has right child, select, then traverse left all the way down
        if self.right is not None:
            return self.right.min_leaf()

        node = self
        # Try to find an ancestor that is a left child, return parent of that
        while node.parent is not None:
            if node.parent.left is node:
                return node.parent
            node = node.parent

        # Nothing greater than this
        return None

    def replace_node(self, child, node):
        """ Replace the ``child'' of ``self'' with the ``node'' and set the
        parent pointer of ``node'' to ``self''

        Notice that the parent of the replaced Child will remain the same. Set
        it to None if you really want to detach it from the tree.

        Raises a ValueError if child is None or not a Child of self

        Runtime: O(1)

        Return the replaced Child
        """
        is_left = self.left is child
        is_right = self.right is child
        is_child = child is not None and (is_left or is_right)

        if not is_child:
            raise ValueError("replace_node: self must be the parent of the child")

        if node is not None:
            node.parent = self

        if is_left:
            self.left, node = node, self.left
        else:
            self.right, node = node, self.right

        return node

    def swap_node(self, other):
        self._swap_node(other)

        other.edge, self.edge = self.edge, other.edge

    def _swap_node(self, other):
        if other is None:
            raise ValueError("can't swap with None")

        if self is other:
            return

        parent1 = self.parent
        parent2 = other.parent

        # update head endpoints adjacent to the node
        if parent1 is not None:
            parent1.replace_node(self, other)
        else:
            other.parent = None

        if parent2 is not None:
            parent2.replace_node(other, self)
        else:
            self.parent = None

        if self.left is not None:
            self.left.parent = other

        if self.right is not None:
            self.right.parent = other

        if other.left is not None:
            other.left.parent = self

        if other.right is not None:
            other.right.parent = self

        # update tail endpoints adjacent to the node
        self.left, other.left = other.left, self.left
        self.right, other.right = other.right, self.right

        # fix possible cycles
        if self.left is self:
            self.left = other
        elif self.right is self:
            self.right = other
        elif other.left is other:
            other.left = self
        elif other.right is other:
            other.right = self

        if other.parent is other:
            other.parent = self
        elif self.parent is self:
            self.parent = other
