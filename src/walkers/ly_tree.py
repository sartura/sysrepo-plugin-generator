from tree_walker import TreeWalker
from utils import to_c_variable

from libyang.schema import Node as LyNode


class LibyangTreeFunction:
    def __init__(self, prefix, parent_node, node):
        self.prefix = prefix
        self.parent_node = parent_node
        self.node = node
        self.name = to_c_variable(node.name())
        self.parent_name = to_c_variable(
            parent_node.name()) if parent_node else None

    def get_name(self):
        return self.prefix + "_" + self.name

    def __repr__(self):
        parent = self.parent_node.name() if self.parent_node != None else None
        return "[name: {}, parent: {}, function: {}]".format(self.name, parent, self.get_name())


class LibyangTreeContext:
    def __init__(self, prefix):
        self.functions = []
        self.main_prefix = prefix + "_ly_tree_create"
        self.parent_stack = {
            0: (None, self.main_prefix)
        }


class Walker(TreeWalker):
    def __init__(self, prefix, root_nodes):
        super().__init__(root_nodes)
        self.ctx = LibyangTreeContext(prefix)

    def walk_node(self, node, depth):
        parent, parent_prefix = self.ctx.parent_stack[depth]

        if node.nodetype() in [LyNode.CONTAINER, LyNode.LIST]:
            self.ctx.parent_stack[depth +
                                  1] = (node, parent_prefix + "_" + to_c_variable(node.name()))
        # print("\t" * depth, end="")
        # print("{}[{} - {}]".format(
        #     to_c_variable(node.name()), node.keyword(), parent_prefix + "_" + to_c_variable(node.name())))

        self.ctx.functions.append(LibyangTreeFunction(
            parent_prefix, parent, node))

        return False

    def add_node(self, node):
        return not node.nodetype() == LyNode.RPC and not node.nodetype() == LyNode.ACTION

    def get_functions(self):
        return self.ctx.functions
