from typing import List, Dict

from libyang.schema import Node as LyNode
from libyang.schema import SNode

from typing import Iterator

from core.utils import Callback
from core.utils import to_c_variable
from core.walker import Walker

from core.config import YangPrefixConfiguration
from core.utils import LibyangTreeFunction


class YangTreeContext:
    functions: List[LibyangTreeFunction]
    prefix_stack: Dict[int, str]
    parent_stack: Dict[int, SNode]

    def __init__(self):
        self.functions = []
        self.prefix_stack = {0: None}
        self.parent_stack = {0: None}

    def check_prefix_depth(self, depth: int) -> bool:
        return depth in self.prefix_stack

    def add_prefix(self, depth: int, prefix: str):
        self.prefix_stack[depth + 1] = prefix

    def add_parent(self, depth: int, parent: SNode):
        self.parent_stack[depth + 1] = parent

    def get_functions(self):
        return self.functions

    def add_function(self, fn: LibyangTreeFunction):
        self.functions.append(fn)

    def get_parent(self, depth: int):
        return self.parent_stack[depth]


class YangTreeWalker(Walker):
    def __init__(self, prefix: str, root_nodes: Iterator[SNode], prefix_cfg: YangPrefixConfiguration):
        super().__init__(root_nodes)
        self.ctx = YangTreeContext()
        self.prefix_cfg = prefix_cfg

    def walk_node(self, node, depth):
        last_prefix = None

        if depth in self.ctx.prefix_stack:
            last_prefix = self.ctx.prefix_stack[depth]

        if node.nodetype() == LyNode.LEAF or node.nodetype() == LyNode.LEAFLIST or node.nodetype() == LyNode.LIST:
            if last_prefix is not None:
                # self.ctx.callbacks.append(
                #     Callback(node.data_path(), to_c_variable(last_prefix + "_" + node.name())))
                self.ctx.add_function(LibyangTreeFunction(to_c_variable(
                    last_prefix + "_" + node.name()), self.ctx.get_parent(depth), node))
            else:
                self.ctx.add_function(LibyangTreeFunction(to_c_variable(
                    node.name()), self.ctx.get_parent(depth), node))
            return True
        else:
            c_var = to_c_variable(node.name())
            if self.prefix_cfg.check_prefix(c_var):
                self.ctx.add_prefix(
                    depth, self.prefix_cfg.get_prefix_value(c_var))
            elif last_prefix is not None:
                self.ctx.add_prefix(
                    depth, last_prefix)
            else:
                self.ctx.add_prefix(depth, None)
            # also add containers to the tree
            self.ctx.add_parent(depth, node)
            self.ctx.add_function(LibyangTreeFunction(to_c_variable(
                node.name()), self.ctx.get_parent(depth), node))

        return False

    def add_node(self, node):
        return not node.nodetype() == LyNode.RPC and not node.nodetype() == LyNode.ACTION and not node.nodetype() == LyNode.NOTIF and not node.deprecated() and not node.obsolete()

    def get_functions(self):
        return self.ctx.get_functions()
