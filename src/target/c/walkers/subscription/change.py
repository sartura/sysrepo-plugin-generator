from libyang.schema import Node as LyNode

from core.utils import Callback
from core.utils import to_c_variable
from core.walker import Walker


class ChangeSubscriptionContext:
    def __init__(self):
        self.callbacks = []
        self.prefix_stack = {0: ""}


class ChangeSubscriptionWalker(Walker):
    def __init__(self, prefix, root_nodes):
        super().__init__(root_nodes)
        self.ctx = ChangeSubscriptionContext()

    def walk_node(self, node, depth):
        # print("\t" * depth, end="")
        # print(self.ctx.prefix_stack)
        # print("\t" * depth, end="")
        # print("{}[{}]".format(node.name(), node.keyword()))

        last_prefix = self.ctx.prefix_stack[depth]

        if node.nodetype() == LyNode.LEAF or node.nodetype() == LyNode.LEAFLIST or node.nodetype() == LyNode.LIST:
            self.ctx.callbacks.append(Callback(node.data_path(),
                                               to_c_variable(last_prefix + "_" + node.name())[1:]))

            return True
        else:
            self.ctx.prefix_stack[depth+1] = last_prefix + \
                "_" + to_c_variable(node.name())

        return False

    def add_node(self, node):
        return not node.nodetype() == LyNode.RPC and not node.nodetype() == LyNode.ACTION and not node.nodetype() == LyNode.NOTIF and not node.config_false()

    def get_callbacks(self):
        return list(reversed(self.ctx.callbacks))
