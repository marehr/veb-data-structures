# coding=utf8

import config
import binary_tree

class Node(binary_tree.Node):

    def __init__(self, key, depth = None):
        super(Node, self).__init__(key)

        self.depth = depth
        self.min_depth = depth
        self.max_depth = depth

    def node_atleast_max_depth(self, node, depth):
        if node and node.max_depth >= depth:
            return node
        return None

    def min_atleast_depth(self, depth):
        minimum = None

        # this tree has no node with >= depth
        if not self.max_depth >= depth:
            return minimum

        current = self
        while current is not None:
            left = self.node_atleast_max_depth(current.left_child, depth)

            if current.depth >= depth:
                minimum = current
                current = left
                continue

            if left is not None:
                current = left
                continue

            current = self.node_atleast_max_depth(current.right_child, depth)

        return minimum

    def max_atleast_depth(self, depth):
        maximum = None

        # this tree has no node with >= depth
        if not self.max_depth >= depth:
            return maximum

        current = self
        while current is not None:
            right = self.node_atleast_max_depth(current.right_child, depth)

            if current.depth >= depth:
                maximum = current
                current = right
                continue

            if right is not None:
                current = right
                continue

            current = self.node_atleast_max_depth(current.left_child, depth)

        return maximum

    def cut_at_depth(self, depth, tree = None):
        """ Returns [tree1, tree2], where tree1 is the tree with the nodes that
        have a depth < depth and tree2 have a depth >= depth
        """
        root = self
        assert root is root.root()

        # find minimum node with node.depth >= depth
        min_node = root.min_atleast_depth(depth)
        max_node = root.max_atleast_depth(depth)

        return root.cut(min_node, max_node, tree)

    def _min_depth(self):
        depth = self.depth

        if self.left_child is not None and self.left_child.min_depth < depth:
            depth = self.left_child.min_depth

        if self.right_child is not None and self.right_child.min_depth < depth:
            depth = self.right_child.min_depth

        return depth

    def _max_depth(self):
        depth = self.depth

        if self.left_child is not None and self.left_child.max_depth > depth:
            depth = self.left_child.max_depth

        if self.right_child is not None and self.right_child.max_depth > depth:
            depth = self.right_child.max_depth

        return depth

    def update_height_locally(self):
        super(Node, self).update_height_locally()

        self.min_depth = self._min_depth()
        self.max_depth = self._max_depth()
