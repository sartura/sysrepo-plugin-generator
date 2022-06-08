from libyang.schema import Node as LyNode


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
