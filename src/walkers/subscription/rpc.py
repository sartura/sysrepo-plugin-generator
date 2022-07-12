from tree_walker import TreeWalker
from libyang.schema import Node as LyNode
from callback import Callback
from utils import to_c_variable


class RPCContext:
    def __init__(self):
        self.callbacks = []


class Walker(TreeWalker):
    def __init__(self, prefix, root_nodes):
        super().__init__(root_nodes)
        self.ctx = RPCContext()

    def walk_node(self, node, depth):
        # print("\t" * depth, end="")
        # print("{}[{}]".format(node.name(), node.keyword()))

        self.ctx.callbacks.append(Callback(node.data_path(),
                                           to_c_variable(node.name())))

        return depth > -1

    def add_node(self, node):
        return node.nodetype() == LyNode.RPC

    def get_callbacks(self):
        return list(reversed(self.ctx.callbacks))
