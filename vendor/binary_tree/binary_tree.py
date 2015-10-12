# coding=utf8

class Node(object):
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.height = 0
        self.size = 1

    def __iter__(self):
        """ Return all nodes that are in the current subtree (sorted by the key)
        """
        curr = self.min()

        if self.parent is None:
            last = None
        elif self.parent.left_child is self:
            last = self.parent
        else:
            last = self.max().next()

        while curr is not last:
            yield curr
            curr = curr.next()

    def keys(self):
        """ Return all keys sorted that are in the current subtree
        """
        for node in self:
            yield node.key

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.key)

    def notify_root_change(self, new_root, observer = None):
        """ Event: Will be called if a root change occured and will call,
        where self is the old_root and new_root is the new root::

            observer.root_changed(self, new_root)

        Returns new_root
        """

        if observer is not None:
            observer.root_changed(self, new_root)

        return new_root

    def min(self):
        """ Returns the Node with the minimum key in the subtree starting at
        the root self

        Runtime: O(log n)

        The returned Node can be self itself, if the left subtree is empty
        """
        node = self
        while node.left_child is not None:
            node = node.left_child
        return node

    def max(self):
        """ Returns the Node with the maximum key in the subtree starting at
        the root self

        Runtime: O(log n)

        The returned Node can be self itself, if the right subtree is empty
        """
        node = self
        while node.right_child is not None:
            node = node.right_child
        return node

    def split(self, root = None, tree = None):
        """ Move self until it becames the root of the subtree (below the node
        root). The left and right subtree of self will be balanced.

        Notice that you may have to update the height of root and all heights of
        the parents of root, because the height invariant will only be restored
        in the subtree.

        Runtime: O(log n)

        Return self
        """

        parent = None
        while self.parent is not root:
            parent = self.parent

            # move self one step further to the root
            self.rotate()

            # one subtree is balanced, but the other may need rebalancing
            parent.concatenate(tree)

        # update height
        self.update_height_locally()

        # update root
        if root is None and parent is not None:
            parent.notify_root_change(self, tree)

        return self

    def concatenate(self, tree = None):
        """ Concatenate the left and right subtree with self, s.t. the whole
        tree is balanced again. This is the "inverse" operation of split (may
        not yield the same tree).

        Assumes that the left and right subtree of self is balanced.

        Notice that:

            * the height of the tree only reduces by at most one.
            * you may have to update the heights of all parents of self, because
              the height invariant will only be restored from self downwards.

        Runtime: O(1 + |left_child.height - right_child.height|)

        Return the root of the subtree
        """
        parent = self.parent

        # only rebalance everything under the parent
        return self.rebalance(tree, parent)

    def detach(self):
        """ Detach the subtree self (cut the Edge between self and self.parent)

        Notice that
            * the tree of self.parent might be unbalanced
            * you may have to update the heights of all parents of root

        Runtime: O(1)

        Return [self, self.parent], where self is the root of the detached tree
        """
        parent = self.parent

        # detach
        if parent is not None:
            parent.replace_child(self, None)
            self.parent = None

            parent.update_height_locally()

        return [self, parent]

    def cut(self, start, end, tree = None):
        """ Cut out all nodes that are in the interval [start, end]

        Assumes start.key < end.key
        Assumes self is the root self.root()

        start is either None or of type Node
        end is either None or of type Node

        Interval types:
            * interval is ∅ iff start is None and end is None
            * (-∞, end] iff start is None and end is not None
            * [start, +∞) iff start is not None and end is None
            * [start, end] iff start is not None and end is not None

        Returns [tree1, tree2], where tree1 has all the nodes that are in the
        interval (-∞, start) ∪ (end, +∞) and tree2 has all the nodes
        that are in the interval [start, end]

        Runtime: O(log n)
        """
        root = self
        if root.parent is not None:
            raise ValueError("cut: self must be root")

        # first interval type (interval is empty)
        if start is None and end is None:
            return [root, None]

        # find predecessor/successor nodes
        min_node = start and start.previous()
        max_node = end and end.next()

        # there are no elements in the interval [-∞, start) or (end, +∞]
        # tree1 is empty
        if min_node is None and max_node is None:
            return [None, root]

        # split at the predecessor and successor node
        min_node = min_node and min_node.split(None, tree)
        max_node = max_node and max_node.split(min_node, tree)

        # all nodes in the interval are between min_node and max_node, the root
        # of this tree is cut
        cut = max_node and max_node.left_child
        cut = cut or min_node and min_node.right_child

        # detach the tree rooted at cut
        cut, parent = cut.detach()

        # restore the balance of the not detached tree
        max_node = max_node and max_node.concatenate(tree)
        min_node = min_node and min_node.concatenate(tree)

        return [parent.root(), cut]

    def join(self, subtree, tree = None):
        """ Re/attach a subtree to the tree. This is the "inverse"
        operation of cut (may not yield the same tree).

        Assumes self is the root self.root()

        The keys in the subtree represent an interval [start, end].

        Assumes that self represents the interval (-∞, start) ∪ (end, +∞), that
        means self has no element in the interval [start, end].

        Runtime: O(log n)
        """
        root = self
        if root.parent is not None:
            raise ValueError("join: self must be root")

        if subtree is None:
            return root

        min_node = subtree.min()
        max_node = subtree.max()

        # find predecessor/successor nodes
        min_node = root.predecessor(min_node.key)
        max_node = root.successor(max_node.key)

        # assert that the tree self has no elements in the key interval
        # [subtree.min(), subtree.max()]
        assert min_node or max_node
        assert not min_node or min_node.next() is max_node
        assert not max_node or max_node.previous() is min_node

        # split at the predecessor and successor node
        min_node = min_node and min_node.split(None, tree)
        max_node = max_node and max_node.split(min_node, tree)

        # reattach the tree
        if max_node is not None:
            replaced = max_node.set_child(subtree)
        else:
            replaced = min_node.set_child(subtree)
        assert replaced is None

        # restore the balance
        max_node = max_node and max_node.concatenate(tree)
        min_node = min_node and min_node.concatenate(tree)

        return root.root()

    def search(self, key):
        """ Perform a binary search and return the last node of the search path

        Runtime: O(log n)
        """
        prev = node = self
        while node is not None:
            if node.key == key:
                return node
            prev, node = node, node.child(key)
        return prev

    def find(self, key):
        """ Find the Node with the same key

        Runtime: O(log n)
        """
        found = self.search(key)
        if found.key == key:
            return found
        return None

    def predecessor(self, key):
        """ Find the node with key max{node.key | node.key < key}
        """
        neighbor = self.search(key)
        # key lies right of the inner node or leaf
        if neighbor.key < key:
            return neighbor
        return neighbor.previous()

    def successor(self, key):
        """ Find the node with key min{node.key | node.key > key}
        """
        neighbor = self.search(key)
        # key lies left of the inner node or leaf
        if neighbor.key > key:
            return neighbor
        return neighbor.next()

    def next(self):
        """ Returns the next Node (next key value larger)

        Runtime: O(log n)
        """
        # If has right child, select, then traverse left all the way down
        if self.right_child is not None:
            return self.right_child.min()

        node = self
        # Try to find an ancestor that is a left child, return parent of that
        while node.parent is not None:
            if node.parent.left_child == node:
                return node.parent
            node = node.parent

        # Nothing greater than this
        return None

    def previous(self):
        """ Returns the previous Node (next key value smaller)

        Runtime: O(log n)
        """
        # If has left child, select, then traverse right all the way down
        if self.left_child is not None:
            return self.left_child.max()

        node = self
        # Try to find an ancestor that is a right child, return parent of that
        while node.parent is not None:
            if node.parent.right_child == node:
                return node.parent
            node = node.parent

        #  Nothing smaller than this
        return None

    def is_leaf(self):
        """ Return True if Leaf, False Otherwise

        Runtime: O(1)
        """
        return self.height == 0

    def left_height(self):
        """ Return height of left child

        Runtime: O(1)
        """
        if self.left_child is None:
            return -1
        return self.left_child.height

    def right_height(self):
        """ Return height of right child

        Runtime: O(1)
        """
        if self.right_child is None:
            return -1
        return self.right_child.height

    def max_child_height(self):
        """ Return Height Of Tallest Child or -1 if No Children
        """
        return max(self.left_height(), self.right_height())

    def weigh(self):
        """ Return How Left or Right Sided the Tree Is
        Positive Number Means Left Side Heavy, Negative Number Means Right Side Heavy

        Runtime: O(1)
        """
        balance = self.left_height() - self.right_height()
        return balance

    def _size(self):
        """ Return sum of children sizes
        """
        size = 1
        size+= self.left_child.size if self.left_child is not None else 0
        size+= self.right_child.size if self.right_child is not None else 0
        return size

    def update_height_locally(self):
        """ Updates Height of This Node

        Runtime: O(1)
        """
        self.height = self.max_child_height() + 1
        self.size = self._size()

    def update_height(self):
        """ Updates Height of This Node and All Ancestor Nodes, As Necessary

        Runtime: O(log n)
        """
        node = self
        while node is not None:
            node.update_height_locally()
            node = node.parent

    def root(self):
        """ Return the root of the tree

        Runtime: O(log n)
        """
        node = self
        while node.parent is not None:
            node = node.parent
        return node

    def rebalance(self, tree = None, root = None):
        """ Rebalances all nodes on the path to the root

        Runtime: O(root.height)

        If root is not None:

            Notice that you may have to update the heights of all parents of
            root, because the height invariant will only be restored from root
            downwards.

        Return the root of the subtree

        If root is not None it must be a Node on the root-path of self
        """
        prev, current = self, self
        while current is not root:
            # update height of current
            current.update_height_locally()

            current.balance(tree)
            prev, current = current, current.parent

        return prev

    def balance(self, tree = None):
        """ Balances node, sets new tree root if appropriate

        Runtime: O(self.height)

        Returns None or a Node, which is the new root of the tree

        Notice that you may have to update the heights of all parents, because
        the height invariant will only be restored from self downwards.

        Note: If balancing does occur, this node will move to a lower position on the tree
        """
        new_root = None
        while abs(self.weigh()) > 1:
            is_root = self.parent is None

            weigh1 = self.weigh()
            child1 = self.left_child if weigh1 > 0 else self.right_child

            weigh2 = child1.weigh()
            child2 = child1.left_child if weigh2 > 0 else child1.right_child

            # double rotation iff one weigh is negative and the other one is positive
            if weigh1 * weigh2 < 0:
                new_top = child2.rotate().rotate()
            else:
                new_top = child1.rotate()

            if is_root:
                # the root can only be changed once
                assert new_root is None

                # update root
                new_root = self.notify_root_change(new_top, tree)

        return new_root

    def out(self):
        """ Return String Representing Tree From Current Node Down
        Only Works for Small Trees
        """
        start_node = self
        space_symbol = "*"
        spaces_count = 250
        out_string = ""
        initial_spaces_string = space_symbol * spaces_count + "\n"
        if start_node is None:
            return "AVLTree is empty"
        else:
            level = [start_node]
            while len([i for i in level if (not i is None)]) > 0:
                level_string = initial_spaces_string
                for i in xrange(len(level)):
                    j = (i + 1) * spaces_count / (len(level) + 1)
                    level_string = level_string[:j] + (str(level[i]) if level[i] else space_symbol) + level_string[j + 1:]
                level_next = []
                for i in level:
                    level_next += ([i.left_child, i.right_child] if i else [None, None])
                level = level_next
                out_string += level_string
        return out_string

    def child(self, key):
        """ Get child according to the key

        Runtime: O(1)
        """
        if key < self.key:
            return self.left_child
        return self.right_child

    def replace_child(self, child, node):
        """ Replace the child of self with the node and set the parent pointer
        of node to self

        Notice that

            * you may have to update the heights of all parents.
            * the parent of the replaced Child will remain the same.
              Set it to None if you really want to detach it from the tree.

        Raises a ValueError if child is None or not a Child of self

        Runtime: O(1)

        Return the replaced Child
        """
        is_left = self.left_child is child
        is_right= self.right_child is child
        is_child= child is not None and (is_left or is_right)

        if not is_child:
            raise ValueError("replace_child: self must be the parent of the child")

        if node is not None:
            node.parent = self

        if is_left:
            self.left_child, node = node, self.left_child
        else:
            self.right_child, node = node, self.right_child

        return node

    def set_child(self, node, key = None):
        """ Replace/Set the Child left or right of self according to the key of
        node and set the parent pointer of node to self

        if key is None set key = node.key

        Notice that

            * you may have to update the heights of all parents.
            * the parent of the replaced Child will remain the same.
              Set it to None if you really want to detach it from the tree.

        Raises a ValueError if node and key is None

        Runtime: O(1)

        Return the replaced Child
        """
        if node is None and key is None:
            raise ValueError("set_child: if node is None you have to give a key")

        key = key or node.key

        if node is not None:
            node.parent = self

        if key < self.key:
            self.left_child, node = node, self.left_child
        else:
            self.right_child, node = node, self.right_child

        return node

    def insert(self, new_node, tree=None):
        """ Insert new_node into subtree starting at self

        If self is not the root, notice that

            * you may have to update the heights of all parents of self.
            * you have to ensure that the key belongs into this subtree, s.t.
              the binary search tree invariant is not violated

        Runtime: O(self.height)

        Raises ValueError if key is already inserted or new_node is not a leaf
        """
        if not new_node.is_leaf():
            raise ValueError("insert: new_node must be a leaf")

        branch_node = self.search(new_node.key)

        # If key/name pair does exist in tree
        if branch_node.key == new_node.key:
            raise ValueError("insert: duplicate key '{0}' found".format(new_node.key))

        # add new_node to the branch_node
        branch_node.set_child(new_node)

        # rebalance parents if needed
        branch_node.rebalance(tree, self.parent)
        return new_node

    def remove(self, tree = None):
        """ Remove this node

        Runtime: O(log n)

        Returns the root
        """

        # Either the node is a leaf or the node has only 1 child.
        if self.left_child is None or self.right_child is None:
            child = self.left_child or self.right_child

            parent = self.parent
            self.parent = None
            self.left_child = None
            self.right_child = None

            # self is root
            if parent is None:
                # we don't have to update the height or rebalance, because
                # the height and the balance of the child was correct before
                # we deleted the root
                if child is not None:
                    child.parent = None

                # root will be replaced, update root
                self.notify_root_change(child, tree)

                return child

            # replace node with the child
            parent.replace_child(self, child)

            # rebalance
            return parent.rebalance(tree)

        # The node has 2 children. Swap items with the successor (the smallest
        # item in its right subtree) and delete the successor from the right
        # subtree of the node.
        next_ = self.next()

        # root changed
        if self.parent is None:
            self.notify_root_change(next_, tree)

        # swap with successor
        self.swap(next_)

        # the next node is either a leaf or an inner node with one child
        assert self.left_child is None or self.right_child is None
        return self.remove(tree)


    def swap(self, other):
        """ Swap both nodes in the tree

        At the end of the swap operation update_height_locally() will be called
        to update the heights

        Note that only the structure changes, that means a reference to a node
        will always have the same key::

            # create a new node
            node1 = Node(key1)
            node2 = root.find(key2)

            node1.swap(node2)

            assert node1.key == key1 and node2.key == key2

            # node 2 is now a loose node
            assert node2.left_child == None
            assert node2.right_child == None
            assert node2.parent == None
        """
        if self is other:
            return

        if other is None:
            raise ValueError("swap: can't swap with None")

        parent1 = self.parent
        parent2 = other.parent

        # update head endpoints adjacent to the node
        if parent1 is not None:
            parent1.replace_child(self, other)
        else:
            other.parent = None

        if parent2 is not None:
            parent2.replace_child(other, self)
        else:
            self.parent = None

        if self.left_child is not None:
            self.left_child.parent = other

        if self.right_child is not None:
            self.right_child.parent = other

        if other.left_child is not None:
            other.left_child.parent = self

        if other.right_child is not None:
            other.right_child.parent = self

        # update tail endpoints adjacent to the node
        self.left_child, other.left_child = other.left_child, self.left_child
        self.right_child, other.right_child = other.right_child, self.right_child

        # fix possible cycles
        if self.left_child is self:
            self.left_child = other
        elif self.right_child is self:
            self.right_child = other
        elif other.left_child is other:
            other.left_child = self
        elif other.right_child is other:
            other.right_child = self

        if other.parent is other:
            other.parent = self
        elif self.parent is self:
            self.parent = other

        # change height update order, if other is directly depended of self
        if other.parent is self:
            self, other = other, self

        # update heights
        self.update_height_locally()
        other.update_height_locally()

    def rotate(self):
        """ Rotate self at the parent of self. If self is a left child of parent
        do a right rotation else do a left rotation.

        Runtime: O(1)

        Notice that you may have to update the heights of all parents, because
        the height invariant will only be restored from self downwards.
        """
        parent = self.parent
        if parent is None:
            return

        if parent.parent is not None:
            parent.parent.replace_child(parent, self)
        else:
            self.parent = None

        # use self.key in case that replaced is None
        replaced = self.set_child(parent)
        parent.set_child(replaced, self.key)

        # update locally the height of parent, self
        parent.update_height_locally()
        self.update_height_locally()

        return self

    def rotate_right(self):
        assert(self.right_child is not None)
        return self.right_child.rotate()

    def rotate_left(self):
        assert(self.left_child is not None)
        return self.left_child.rotate()


class BinaryTree(object):
    """ Binary Search Tree
    Uses AVL Tree
    """
    def __init__(self, *args):
        self.root = None  # root Node
        if len(args) == 1:
            for i in args[0]:
                self.insert(i)

    def __len__(self):
        if self.root is None:
            return 0
        return self.root.size

    def __str__(self):
        return self.out()

    def height(self):
        """ Return Max Height Of Tree
        """
        if self.root:
            return self.root.height
        else:
            return -1

    def size(self):
        """ Return size Of Tree
        """
        if self.root:
            return self.root.size
        else:
            return 0

    def find(self, key):
        # raises KeyError if key doesn't exist
        found = self.root and self.root.find(key)
        if found is None:
            raise KeyError(key)
        return found

    def predecessor(self, key):
        return self.root and self.root.predecessor(key)

    def successor(self, key):
        return self.root and self.root.successor(key)

    def root_changed(self, old_root, new_root):
        self.root = new_root

    def insert(self, key, *args):
        new_node = Node(key, *args)

        if self.root is None:
            # If nothing in tree
            self.root = new_node
            return self.root

        # raises ValueError if key already exists
        return self.root.insert(new_node, self)

    def remove(self, key):
        # raises KeyError if key doesn't exist
        node = self.find(key)
        node.remove(self)

    def preorder(self, node, retlst = None):
        if retlst is None:
            retlst = []

        if node is None:
            return retlst

        retlst.append(node.key)
        retlst = self.preorder(node.left_child, retlst)
        retlst = self.preorder(node.right_child, retlst)
        return retlst

    def inorder(self, node, retlst = None):
        curr = self.root
        retlst = []

        if curr is not None:
            curr = curr.min()

        while curr is not None:
            retlst.append(curr.key)

            curr = curr.next()

        return retlst

    def postorder(self, node, retlst = None):
        if retlst is None:
            retlst = []

        if node is None:
            return retlst

        retlst = self.postorder(node.left_child, retlst)
        retlst = self.postorder(node.right_child, retlst)
        retlst.append(node.key)
        return retlst

    def as_list(self, pre_in_post = 1):
        if not self.root:
            return []
        if pre_in_post == 0:
            return self.preorder(self.root)
        elif pre_in_post == 1:
            return self.inorder(self.root)
        elif pre_in_post == 2:
            return self.postorder(self.root)

    # use for debug only and only with small trees
    def out(self, start_node=None):
        if start_node is None:
            start_node = self.root

        if start_node is None:
            return None
        else:
            return start_node.out()
