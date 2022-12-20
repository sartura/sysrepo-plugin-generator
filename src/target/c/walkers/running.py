
from libyang.schema import Node as LyNode

from core.utils import Callback
from core.utils import to_c_variable
from core.walker import Walker


class RunningContext:
    def __init__(self):
        self.callbacks = []


class RunningWalker(Walker):
    def __init__(self, prefix, root_nodes):
        super().__init__(root_nodes)
        self.ctx = RunningContext()

    def walk_node(self, node, depth):
        # print("\t" * depth, end="")
        # print("{}[{}]".format(node.name(), node.keyword()))

        if (node.nodetype() == LyNode.LEAF or node.nodetype() == LyNode.LEAFLIST or node.nodetype() == LyNode.LIST or node.nodetype() == LyNode.CONTAINER) and depth != 0:
            self.ctx.callbacks.append(Callback(node.data_path(),
                                               to_c_variable(node.name())))

        return depth > 0

    def add_node(self, node):
        return not node.nodetype() == LyNode.RPC and not node.nodetype() == LyNode.ACTION and not node.config_false() and not node.nodetype() == LyNode.NOTIF

    def get_callbacks(self):
        return self.ctx.callbacks
