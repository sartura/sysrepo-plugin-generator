from tree_walker import TreeWalker


class Walker(TreeWalker):
    def __init__(self, prefix, root_nodes):
        super().__init__(root_nodes)

    def walk_node(self, node, depth):
        return super().walk_node(node, depth)

    def add_node(self, node):
        return super().add_node(node)
