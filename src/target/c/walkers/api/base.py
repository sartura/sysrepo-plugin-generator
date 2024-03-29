import os
from libyang.schema import Node as LyNode

from core.utils import to_c_variable
from core.walker import Walker


class APIContext:
    def __init__(self, source_dir, files):
        self.source_dir = source_dir
        self.files = files
        self.extensions = ['c', 'h']

        self.dirs_stack = {
            0: os.path.join(source_dir, "plugin", "api")
        }

        self.prefix_stack = {
            0: ''
        }

        self.types = {
            "unknown": 'unknown',
            "binary": "void *",
            "uint8": "uint8_t",
            "uint16": "uint16_t",
            "uint32": "uint32_t",
            "uint64": "uint64_t",
            "string": "char *",
            "bits": 'uint64_t',
            "boolean": "uint8_t",
            "decimal64": "double",
            "empty": "void",
            "enumeration": 'unknown',
            "identityref": 'unknown',
            "instance-id": 'unknown',
            "leafref": 'unknown',
            "union": 'unknown',
            "int8": "int8_t",
            "int16": "int16_t",
            "int32": "int32_t",
            "int64": "int64_t",
        }

        self.dir_functions = {}

        # iterate tree and create directories
        self.dirs = []


class APIWalker(Walker):
    def __init__(self, prefix, root_nodes, source_dir, files):
        super().__init__(root_nodes)
        self.ctx = APIContext(source_dir, files)

    def walk_node(self, node, depth):
        last_path = self.ctx.dirs_stack[depth]
        last_prefix = self.ctx.prefix_stack[depth]

        if node.nodetype() == LyNode.CONTAINER:
            # update dir stack
            new_dir = os.path.join(last_path, node.name())
            self.ctx.dirs_stack[depth +
                                1] = new_dir
            self.ctx.dirs.append(new_dir)

            # update prefix stack
            new_prefix = last_prefix + to_c_variable(node.name()) + "_"
            self.ctx.prefix_stack[depth + 1] = new_prefix

        if node.nodetype() == LyNode.LEAF or node.nodetype() == LyNode.LEAFLIST or node.nodetype() == LyNode.LIST:
            if last_path not in self.ctx.dir_functions:
                self.ctx.dir_functions[last_path] = (last_prefix[:-1], [])

            self.ctx.dir_functions[last_path][1].append(node)
            return True

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
