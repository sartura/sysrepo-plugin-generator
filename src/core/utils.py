from libyang.schema import Node as LyNode
import os


class LibyangTreeFunction:
    def __init__(self, prefix, parent_node, node, path=None):
        self.prefix = prefix
        self.parent_node = parent_node
        self.node = node
        self.path = path
        self.name = to_c_variable(node.name())
        self.parent_name = to_c_variable(
            parent_node.name()) if parent_node else None

    def get_name(self):
        if self.prefix is None:
            return self.name
        return self.prefix + "_" + self.name

    def __repr__(self):
        parent = self.parent_node.name() if self.parent_node != None else None
        return "[name: {}, parent: {}, function: {}]".format(self.name, parent, self.get_name())


class CLibrary:
    def __init__(self, outdir, name):
        deps_dir = os.path.join(outdir, "deps")
        self.lib_dir = os.path.join(deps_dir, name)

    def generate_directories(self):
        pass

    def generate_files(self):
        pass

    def get_include_dirs(self):
        pass


class Callback:
    def __init__(self, path, sufix):
        self.path = path
        self.sufix = sufix

    def __repr__(self):
        return self.path + "=" + self.sufix


class CDefine:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return self.name + " " + self.value


def print_tree(children, depth=0):

    for ch in children:
        print(" " * depth, end="")
        print("%s -> %s %d" % (ch.name(), ch.keyword(), ch.config_false()))

        if hasattr(ch, "children"):
            print_tree(ch.children(), depth + 1)


def to_c_variable(s):
    return s.replace('-', '_')


def to_camel_case(snake_case, first_upper: bool = False):
    components = snake_case.split('_')
    if first_upper:
        return components[0].title() + "".join(x.title() for x in components[1:])
    return components[0] + "".join(x.title() for x in components[1:])


def has_children(node):
    return hasattr(node, "children")


def extract_defines(prefix, module):
    defines = []
    defines_map = {}

    module_name = module.name()

    for root_node in module.children():
        current_prefix = "%s_%s" % (
            prefix.upper(), to_c_variable(root_node.name()).upper())
        define = CDefine("%s_YANG_PATH" % (current_prefix),
                         "\"/%s:%s\"" % (module_name, root_node.name()))
        defines.append(define)

        defines_map[root_node.data_path()] = define.name

        node_stack = []

        # use stack and prefix to generate other #def's
        if has_children(root_node):
            for n in root_node.children():
                node_stack.append(
                    (n, current_prefix, define))

        while node_stack:
            node, last_prefix, prev_def = node_stack.pop()

            new_prefix = "%s_%s" % (
                last_prefix, to_c_variable(node.name()).upper())
            define = CDefine("%s_YANG_PATH" % (new_prefix),
                             "%s \"/%s\"" % (prev_def.name, node.name()))

            # append to list
            defines.append(define)

            defines_map[node.data_path()] = define.name

            if has_children(node):
                for n in node.children():
                    node_stack.append((n, new_prefix, define))

    defines.reverse()

    return defines, defines_map
