from core.utils import has_children


class Walker:
    def __init__(self, root_nodes):
        self.root_nodes = root_nodes

    def walk_node(self, node, depth):
        pass

    def add_node(self, node):
        pass

    def walk(self):
        node_stack = []

        for n in self.root_nodes:
            if self.add_node(n):
                node_stack.append((n, 0))

        while node_stack:
            node, depth = node_stack.pop()

            if self.walk_node(node, depth):
                continue

            if has_children(node):
                for n in node.children():
                    if self.add_node(n):
                        node_stack.append((n, depth + 1))
