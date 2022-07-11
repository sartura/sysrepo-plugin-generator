from tree_walker import TreeWalker
import os
from libyang.schema import Node as LyNode

from utils import to_c_variable


class ChangeAPIContext:
    def __init__(self, source_dir):
        self.source_dir = source_dir
        self.files = ['change']
        self.extensions = ['c', 'h']

        self.dirs_stack = {
            0: os.path.join(source_dir, "plugin", "api")
        }

        self.prefix_stack = {
            0: ''
        }

        self.types = {
            "unknown": None,
            "binary": "void *",
            "uint8": "uint8_t",
            "uint16": "uint16_t",
            "uint32": "uint32_t",
            "uint64": "uint64_t",
            "string": "char *",
            "bits": None,
            "boolean": "uint8_t",
            "decimal64": "double",
            "empty": "void",
            "enumeration": None,
            "identityref": None,
            "instance-id": None,
            "leafref": None,
            "union": None,
            "int8": "int8_t",
            "int16": "int16_t",
            "int32": "int32_t",
            "int64": "int64_t",
        }

        self.dir_functions = {}

        # iterate tree and create directories
        self.dirs = []


class Walker(TreeWalker):
    def __init__(self, prefix, root_nodes, source_dir):
        super().__init__(root_nodes)
        self.ctx = ChangeAPIContext(source_dir)

    def walk_node(self, node, depth):
        # print("\t" * depth, end="")
        # print("{}[{}]".format(node.name(),
        #       node.keyword()))

        last_path = self.ctx.dirs_stack[depth]
        last_prefix = self.ctx.prefix_stack[depth]

        if node.nodetype() == LyNode.CONTAINER or node.nodetype() == LyNode.LIST:
            # update dir stack
            new_dir = os.path.join(last_path, node.name())
            self.ctx.dirs_stack[depth +
                                1] = new_dir
            self.ctx.dirs.append(new_dir)

            # update prefix stack
            new_prefix = last_prefix + to_c_variable(node.name()) + "_"
            self.ctx.prefix_stack[depth + 1] = new_prefix

        if node.nodetype() == LyNode.LEAF or node.nodetype() == LyNode.LEAFLIST:
            if last_path not in self.ctx.dir_functions:
                self.ctx.dir_functions[last_path] = (last_prefix[:-1], [])

            self.ctx.dir_functions[last_path][1].append(node)

        return False

    def add_node(self, node):
        return not node.config_false() and not node.nodetype() in [LyNode.RPC, LyNode.NOTIF]

    def get_directories(self):
        return self.ctx.dirs

    def get_directory_functions(self):
        return self.ctx.dir_functions

    def get_api_filenames(self):
        files = []

        for fn in self.ctx.files:
            for ext in self.ctx.extensions:
                files.append("{}.{}".format(fn, ext))
        return files

    def get_types(self):
        return self.ctx.types
