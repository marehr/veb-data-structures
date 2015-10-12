
class VebSlickStaticTestMixin(object):

    def rebuild_structure(self, veb):
        """ Rebuilds hash_table and assigns min/max pointer for each Node and
        chain leaves
        """
        veb.T = self.hash_table(veb=veb)
        self.assign_min_max(veb.root)

    """
    constructs the hash table from vEBSlick for testing purposes
    """
    def hash_table(self, veb):
        T = {}
        self._hash_table(veb, veb.root.left, T)
        self._hash_table(veb, veb.root.right, T)
        return T

    def _hash_table(self, veb, child, table):
        if child is None:
            return

        # insert into hash table
        index = child.hash_index()
        table[index] = child.parent

        self._hash_table(veb, child.left, table)
        self._hash_table(veb, child.right, table)

    def _chain_leaves(self, leaf, leaves):
        # initialize pointers
        leaf._previous_leaf = leaf._next_leaf = None

        # add leaf to the tail of the leaves
        if leaves:
            prev = leaves[-1]

            leaf._previous_leaf = prev
            prev._next_leaf = leaf

        leaves.append(leaf)

    def assign_min_max(self, currentNode, leaves=None):
        if leaves is None:
            leaves = []

        if currentNode is None:
            return

        if currentNode.is_leaf():
            self._chain_leaves(currentNode, leaves)

            # if tree is empty there is no min/max_leaf
            assign = currentNode
            if currentNode.parent is None:
                assign = None

            currentNode._min_leaf = currentNode._max_leaf = assign
            return

        # preorder traversal to garentee, that the min/max values are set
        self.assign_min_max(currentNode.left, leaves)
        self.assign_min_max(currentNode.right, leaves)

        # at least one child is not None
        if currentNode.right is None or currentNode.left is not None and \
            currentNode.left.min_leaf().key < currentNode.right.min_leaf().key:
            currentNode._min_leaf = currentNode.left.min_leaf()
        else:
            currentNode._min_leaf = currentNode.right.min_leaf()

        # at least one child is not None
        if currentNode.right is None or currentNode.left is not None and \
            currentNode.left.max_leaf().key > currentNode.right.max_leaf().key:
            currentNode._max_leaf = currentNode.left.max_leaf()
        else:
            currentNode._max_leaf = currentNode.right.max_leaf()
