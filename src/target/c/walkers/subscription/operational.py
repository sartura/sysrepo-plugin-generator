from libyang.schema import Node as LyNode
from core.utils import Callback
from core.utils import to_c_variable
from core.walker import Walker


class OperationalSubscriptionContext:
    def __init__(self):
        self.callbacks = []
        self.prefix_stack = {0: ""}


class OperationalSubscriptionWalker(Walker):
    def __init__(self, prefix, root_nodes):
        super().__init__(root_nodes)
        self.ctx = OperationalSubscriptionContext()

    def walk_node(self, node, depth):

        last_prefix = self.ctx.prefix_stack[depth]

        if (node.nodetype() == LyNode.LEAF or node.nodetype() == LyNode.LEAFLIST) and node.config_false():
            self.ctx.callbacks.append(Callback(node.data_path(),
                                               to_c_variable(last_prefix + "_" + node.name())[1:]))

            # return True
        elif node.nodetype() == LyNode.LIST:
            # also add optional list callback
            self.ctx.callbacks.append(Callback(node.data_path(),
                                               to_c_variable(last_prefix + "_" + node.name())[1:]))
            self.ctx.prefix_stack[depth+1] = last_prefix + \
                "_" + to_c_variable(node.name())
        else:
            self.ctx.prefix_stack[depth+1] = last_prefix + \
                "_" + to_c_variable(node.name())

        return False

    def add_node(self, node):
        return not node.nodetype() == LyNode.RPC and not node.nodetype() == LyNode.ACTION and not node.nodetype() == LyNode.NOTIF and node.status() is not 'obsolete' and node.status() is not 'deprecated'

    def get_callbacks(self):
        return list(reversed(self.ctx.callbacks))
