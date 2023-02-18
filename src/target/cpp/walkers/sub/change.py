from typing import List, Dict

from libyang.schema import Node as LyNode
from libyang.schema import SNode

from typing import Iterator

from core.utils import Callback
from core.utils import to_c_variable
from core.walker import Walker

from core.config import YangPrefixConfiguration


class ChangeSubscriptionContext:
    callbacks: List[Callback]
    prefix_stack: Dict[int, str]

    def __init__(self):
        self.callbacks = []
        self.prefix_stack = {0: None}

    def check_prefix_depth(self, depth: int) -> bool:
        return depth in self.prefix_stack

    def add_prefix(self, depth: int, prefix: str):
        self.prefix_stack[depth] = prefix


class ChangeSubscriptionWalker(Walker):
    def __init__(self, prefix: str, root_nodes: Iterator[SNode], prefix_cfg: YangPrefixConfiguration):
        super().__init__(root_nodes)
        self.ctx = ChangeSubscriptionContext()
        self.prefix_cfg = prefix_cfg

    def walk_node(self, node, depth):
        last_prefix = None

        if depth in self.ctx.prefix_stack:
            last_prefix = self.ctx.prefix_stack[depth]

        if node.nodetype() == LyNode.LEAF or node.nodetype() == LyNode.LEAFLIST or node.nodetype() == LyNode.LIST:
            if last_prefix is not None:
                self.ctx.callbacks.append(
                    Callback(node.data_path(), to_c_variable(last_prefix + "_" + node.name())))
            else:
                self.ctx.callbacks.append(
                    Callback(node.data_path(), to_c_variable(node.name())))
            return True
        else:
            c_var = to_c_variable(node.name())
            if self.prefix_cfg.check_prefix(c_var):
                self.ctx.prefix_stack[depth +
                                      1] = self.prefix_cfg.get_prefix_value(c_var)
            elif last_prefix is not None:
                self.ctx.prefix_stack[depth +
                                      1] = last_prefix
            else:
                self.ctx.prefix_stack[depth + 1] = None

        return False

    def add_node(self, node):
        return not node.nodetype() == LyNode.RPC and not node.nodetype() == LyNode.ACTION and not node.nodetype() == LyNode.NOTIF and not node.config_false() and not node.deprecated() and not node.obsolete()

    def get_callbacks(self):
        return list(reversed(self.ctx.callbacks))
