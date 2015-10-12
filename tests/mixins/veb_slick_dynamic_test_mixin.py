
class VebSlickDynamicTestMixin(object):

    def assertEqualNode(self, veb_node, ref_node):
        super(VebSlickDynamicTestMixin, self).assertEqualNode(veb_node, ref_node)

        # assert that the aux. is the same
        self.assertEqual(veb_node.min_leaf(), ref_node.min_leaf())
        self.assertEqual(veb_node.max_leaf(), ref_node.max_leaf())
        self.assertEqual(veb_node.previous_leaf(), ref_node.previous_leaf())
        self.assertEqual(veb_node.next_leaf(), ref_node.next_leaf())

    def assertEqualTrie(self, veb, ref):
        super(VebSlickDynamicTestMixin, self).assertEqualTrie(veb, ref)

        self.assertEqualHashTable(veb, ref)

        # assert all min-/max-spines are shared
        self.assertMinMaxStructure(veb.root)

    def is_min_spine_start(self, node):
        # real root does not belong to the min-/max-spines
        if node.parent is None:
            return False

        # node is child of root or node is not left child of the parent node
        return node.parent.is_root() or node is not node.parent.left

    def is_max_spine_start(self, node):
        # real root does not belong to the min-/max-spines
        if node.parent is None:
            return False

        # node is child of root or node is not right child of the parent node
        return node.parent.is_root() or node is not node.parent.right

    def min_spine(self, root):
        """ Get the min-spine (path of only left children)
        """
        nodes = []
        curr = root
        while curr is not None:
            nodes.append(curr)
            curr = curr.left
        return nodes

    def max_spine(self, root):
        """ Get the max-spine (path of only right children)
        """
        nodes = []
        curr = root
        while curr is not None:
            nodes.append(curr)
            curr = curr.right
        return nodes

    def assertSameMinTrees(self, spine_nodes):
        """ Asserts that
            * all the tango nodes are one-to-one with dynamic nodes
            * all the tango nodes are on the spine
            * all the dynamic nodes on the same spine belong to the same tango tree
        """
        if spine_nodes == []:
            return

        nodes = spine_nodes

        # assert bijection between dynamic nodes and tango nodes
        dynamic_nodes = map(lambda node: node._min_node.dynamic_node, nodes)
        self.assertEqual(dynamic_nodes, nodes)

        # assert all nodes in the tango tree are on the spine
        head = nodes[0].min_tree()
        dynamic_nodes = map(lambda tango_node: tango_node.dynamic_node, head)
        self.assertEqual(nodes, dynamic_nodes)

        # assert all nodes on the spine belong to the same tango tree
        tango_roots = map(lambda node: node.min_tree(), nodes)
        min_trees = [head] * len(tango_roots)
        self.assertEqual(min_trees, tango_roots)

    def assertSameMaxTrees(self, spine_nodes):
        """ Asserts that
            * all the tango nodes are one-to-one with dynamic nodes
            * all the tango nodes are on the spine
            * all the dynamic nodes on the same spine belong to the same tango tree
        """
        if spine_nodes == []:
            return

        nodes = spine_nodes

        # assert bijection between dynamic nodes and tango nodes
        dynamic_nodes = map(lambda node: node._max_node.dynamic_node, nodes)
        self.assertEqual(dynamic_nodes, nodes)

        # assert all nodes in the tango tree are on the spine
        head = nodes[0].max_tree()
        dynamic_nodes = map(lambda tango_node: tango_node.dynamic_node, head)
        self.assertEqual(nodes, dynamic_nodes)

        # assert all nodes on the spine belong to the same tango tree
        tango_roots = map(lambda node: node.max_tree(), nodes)
        max_trees = [head] * len(tango_roots)
        self.assertEqual(max_trees, tango_roots)

    def assertSharedMinimum(self, spine_start):
        """ Asserts that all dynamic nodes on a min-spine share the same minimum
        """
        # asserts that all nodes on the spine share the same minimum
        min_spine = self.min_spine(spine_start)
        minimum = min_spine[-1]
        min_tree = minimum.min_tree()

        self.assertIs(min_tree.shared_node, minimum)
        self.assertSameMinTrees(min_spine)

    def assertSharedMaximum(self, spine_start):
        """ Asserts that all dynamic nodes on a max-spine share the same maximum
        """
        # asserts that all nodes on the spine share the same maximum
        max_spine = self.max_spine(spine_start)
        maximum = max_spine[-1]
        max_tree = maximum.max_tree()

        self.assertIs(max_tree.shared_node, maximum)
        self.assertSameMaxTrees(max_spine)

    def assertMinMaxStructure(self, node):
        if node is None:
            return

        # is start of min-spine
        if self.is_min_spine_start(node):
            self.assertSharedMinimum(node)

        # is start of max-spine
        if self.is_max_spine_start(node):
            self.assertSharedMaximum(node)

        self.assertMinMaxStructure(node.left)
        self.assertMinMaxStructure(node.right)
