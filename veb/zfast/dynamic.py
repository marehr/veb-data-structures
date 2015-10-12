# coding=utf8

from word import word

import static as Static
import tango_tree

class Tree(Static.Tree):

    def __init__(self, w):
        super(Tree, self).__init__(w)

        # use a Dynamic.Node as root
        self.root = Node(word.epsilon, None)

class TangoNode(tango_tree.Node):

    def __init__(self, key, depth, dynamic_node):
        super(TangoNode, self).__init__(key, depth)

        self.dynamic_node = dynamic_node
        self.shared_node = dynamic_node

    def notify_root_change(self, new_root, observer = None):
        super(TangoNode, self).notify_root_change(new_root, observer)

        # update shared node on root change
        if new_root is not None:
            new_root.shared_node = self.shared_node

        return new_root

class Node(Static.Node):

    def __init__(self, edge, parent):
        super(Node, self).__init__(edge, parent)

        key = self.depth()
        self._min_node = TangoNode(key, key, self)
        self._max_node = TangoNode(key, key, self)

    """
    Returns the minimum of this subtree starting by self.

    If self is a leaf it will return itself.
    """
    def min_leaf(self):
        if self.is_root():
            self = self.left or self.right

        return self and self.min_tree().shared_node

    """
    Returns the maximum of this subtree starting by self.

    If self is a leaf it will return itself.
    """
    def max_leaf(self):
        if self.is_root():
            self = self.left or self.right

        return self and self.max_tree().shared_node

    def min_tree(self):
        """ Returns the tango tree, that manages the minimas
        """
        return self._min_node.root()

    def max_tree(self):
        """ Returns the tango tree, that manages the maximas
        """
        return self._max_node.root()

    def depth(self):
        """ Returns for the tango tree, which depth this node has
        """
        return self.key.w

    def _update_min_max_insert(self, new_node, branch_node):
        self._update_min_insert(new_node, branch_node)
        self._update_max_insert(new_node, branch_node)

    def _update_min_insert(self, new_node, branch_node):
        min_tree = self.min_tree()

        assert branch_node is self.parent
        # branch_node = self.parent
        # root_node = self.parent.parent
        # child_node = self

        if branch_node.right is new_node:
            min_tree.insert(branch_node._min_node)

            # assert shared_node stayed the same
            assert min_tree.shared_node is min_tree.root().shared_node
            assert branch_node.min_tree() is min_tree.root()
            return

        depth = branch_node.depth()
        tree1, tree2 = min_tree.cut_at_depth(depth)

        # all nodes in tree2 have >= branch_node.depth and the smallest depth
        # has self
        assert tree2 is not None
        assert tree2.min().dynamic_node is self
        assert tree2 is self.min_tree()
        assert min_tree.depth < depth or tree2 is min_tree.root()

        # all nodes in tree2 have < branch_node.depth and the smallest depth
        # has the root_node (= self.parent.parent)
        assert tree1 is None or tree1.max().dynamic_node is self.parent.parent
        assert tree1 is None or tree1.shared_node is min_tree.shared_node
        assert min_tree.depth >= depth or tree1 is min_tree.root()

        # set the global minimum of tree2 to the old global minimum
        tree2.shared_node = min_tree.shared_node

        # insert new_node and branch_node and set the global minimum to that of the
        # new_node
        if tree1 is not None:
            tree1.shared_node = new_node

            tree1.insert(new_node._min_node)
            tree1.insert(branch_node._min_node)
        else:
            # there is no global minimum, make the new_node the new global minimum
            tree1 = new_node._min_node
            tree1.insert(branch_node._min_node)

        # assert shared_node stayed the same
        assert tree1.shared_node is tree1.root().shared_node
        assert tree1.root() is new_node.min_tree()
        assert tree1.root() is branch_node.min_tree()

    def _update_max_insert(self, new_node, branch_node):
        max_tree = self.max_tree()

        assert branch_node is self.parent
        # branch_node = self.parent
        # root_node = self.parent.parent
        # child_node = self

        if branch_node.left is new_node:
            max_tree.insert(branch_node._max_node)

            # assert shared_node stayed the same
            assert max_tree.shared_node is max_tree.root().shared_node
            assert branch_node.max_tree() is max_tree.root()
            return

        depth = branch_node.depth()
        tree1, tree2 = max_tree.cut_at_depth(depth)

        # all nodes in tree2 have >= branch_node.depth and the smallest depth
        # has self
        assert tree2 is not None
        assert tree2.min().dynamic_node is self
        assert tree2 is self.max_tree()
        assert max_tree.depth < depth or tree2 is max_tree.root()

        # all nodes in tree2 have < branch_node.depth and the smallest depth
        # has the root_node (= self.parent.parent)
        assert tree1 is None or tree1.max().dynamic_node is self.parent.parent
        assert tree1 is None or tree1.shared_node is max_tree.shared_node
        assert max_tree.depth >= depth or tree1 is max_tree.root()

        # set the global maximum of tree2 to the old global maximum
        tree2.shared_node = max_tree.shared_node

        # insert new_node and branch_node and set the global maximum to that of the
        # new_node
        if tree1 is not None:
            tree1.shared_node = new_node

            tree1.insert(new_node._max_node)
            tree1.insert(branch_node._max_node)
        else:
            # there is no global maximum, make the new_node the new global maximum
            tree1 = new_node._max_node
            tree1.insert(branch_node._max_node)

        # assert shared_node stayed the same
        assert tree1.shared_node is tree1.root().shared_node
        assert tree1.root() is new_node.max_tree()
        assert tree1.root() is branch_node.max_tree()

    def _update_min_max_remove(self, parent_node, branch_node, sibling_node):
        self._update_min_remove(parent_node, branch_node, sibling_node)
        self._update_max_remove(parent_node, branch_node, sibling_node)

    def _update_min_remove(self, parent_node, branch_node, sibling_node):
        assert parent_node is not None
        assert branch_node.left is self or branch_node.right is self
        assert branch_node.left is sibling_node or branch_node.right is sibling_node
        assert sibling_node is not None

        # remove self node and branch node from the min-spine
        self._min_node.remove()
        min_tree1 = branch_node._min_node.remove()

        # min-spine is up-to-date
        if self is branch_node.right or min_tree1 is None:
            return

        assert min_tree1 is min_tree1.root()

        # update min-spine
        min_tree2 = sibling_node.min_tree()
        min_tree2.join(min_tree1)

        assert min_tree2.shared_node is min_tree1.root().shared_node
        assert min_tree2.shared_node is min_tree2.root().shared_node

    def _update_max_remove(self, parent_node, branch_node, sibling_node):
        assert parent_node is not None
        assert branch_node.left is self or branch_node.right is self
        assert branch_node.left is sibling_node or branch_node.right is sibling_node
        assert sibling_node is not None

        # remove self node and branch node from the max-spine
        self._max_node.remove()
        max_tree1 = branch_node._max_node.remove()

        # max-spine is up-to-date
        if self is branch_node.left or max_tree1 is None:
            return

        assert max_tree1 is max_tree1.root()

        # update max-spine
        max_tree2 = sibling_node.max_tree()
        max_tree2.join(max_tree1)

        assert max_tree2.shared_node is max_tree1.root().shared_node
        assert max_tree2.shared_node is max_tree2.root().shared_node
