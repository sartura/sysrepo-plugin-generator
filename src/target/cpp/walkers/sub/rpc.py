from typing import List, Dict

from libyang.schema import Node as LyNode
from libyang.schema import SNode

from typing import Iterator

from core.utils import Callback
from core.utils import to_c_variable
from core.walker import Walker

from core.config import YangPrefixConfiguration


class RPCSubscriptionContext:
    callbacks: List[Callback]
    prefix_stack: Dict[int, str]

    def __init__(self):
        self.callbacks = []
        self.prefix_stack = {0: None}

    def check_prefix_depth(self, depth: int) -> bool:
        return depth in self.prefix_stack

    def add_prefix(self, depth: int, prefix: str):
        self.prefix_stack[depth] = prefix


class RPCSubscriptionWalker(Walker):
    def __init__(self, prefix: str, root_nodes: Iterator[SNode], prefix_cfg: YangPrefixConfiguration):
        super().__init__(root_nodes)
        self.ctx = RPCSubscriptionContext()
        self.prefix_cfg = prefix_cfg

    def walk_node(self, node, depth):
        self.ctx.callbacks.append(
            Callback(node.data_path(), to_c_variable(node.name())))

        return False

    def add_node(self, node):
        return node.nodetype() == LyNode.RPC or node.nodetype() == LyNode.ACTION

    def get_callbacks(self):
        return list(reversed(self.ctx.callbacks))
