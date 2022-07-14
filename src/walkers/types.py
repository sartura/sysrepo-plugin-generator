from typing import List
from tree_walker import TreeWalker
from libyang.schema import Node as LyNode

from utils import to_c_variable


class Typedef:
    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.typedef = "{}_t".format(name)


class Def:
    def __init__(self, name):
        self.name = name


class VarDef(Def):
    def __init__(self, type, name):
        super().__init__(name)
        self.type = type


class StructDef(Def):
    def __init__(self, name):
        super().__init__(name)
        self.vars = []


class EnumDef(Def):
    def __init__(self, name, values):
        super().__init__(name)
        self.values = values


class UnionDef(Def):
    def __init__(self, name, vars):
        super().__init__(name)
        self.vars = vars


class TypesContext:
    def __init__(self, prefix):
        self.types_data = {}
        self.prefix = prefix
        self.prefix_stack = {
            0: ""
        }
        self.structs: List[StructDef] = []
        self.unions: List[UnionDef] = []
        self.enums: List[EnumDef] = []
        self.typedefs: List[Typedef] = []
        self.typedef_map = {}


class Walker(TreeWalker):
    def __init__(self, prefix, root_nodes):
        super().__init__(root_nodes)
        self.ctx = TypesContext(prefix)

    def walk_node(self, node, depth):
        last_prefix = self.ctx.prefix_stack[depth]
        if len(last_prefix) > 0:
            full_prefix = last_prefix
        else:
            full_prefix = self.ctx.prefix

        print("\t" * depth, end="")
        if node.nodetype() == LyNode.CONTAINER:
            self.ctx.prefix_stack[depth +
                                  1] = "{}_{}".format(full_prefix, node.name())
            name = to_c_variable("{}_{}".format(full_prefix, node.name()))
            print("struct {}:".format(name))

            td = Typedef("struct", name)
            sd = StructDef(name)

            self.ctx.typedefs.append(td)
            self.ctx.structs.append(sd)

            self.ctx.typedef_map[name] = sd

            parent = to_c_variable(full_prefix)

            if parent in self.ctx.typedef_map:
                # add var def to the parent
                self.ctx.typedef_map[parent].vars.append(
                    VarDef(self.ctx.typedef_map[name].name, to_c_variable(node.name())))

        elif node.nodetype() == LyNode.LEAF:
            print("{} {}".format(node.type().basename(), node.name()))
            vd = VarDef(node.type().basename(), to_c_variable(node.name()))
            name = to_c_variable(full_prefix)

            # previous value has to be a struct of some kind
            self.ctx.typedef_map[name].vars.append(vd)

        elif node.nodetype() == LyNode.LIST:
            self.ctx.prefix_stack[depth +
                                  1] = "{}_{}".format(full_prefix, node.name())
            name = to_c_variable("{}_{}".format(full_prefix, node.name()))
            print("struct {}:".format(name))

            td = Typedef("struct", name)
            sd = StructDef(name)

            self.ctx.typedefs.append(td)
            self.ctx.structs.append(sd)

            self.ctx.typedef_map[name] = sd

            # element struct
            element_name = "{}_element".format(name)
            sd = StructDef(element_name)
            sd.vars.append(VarDef(td.typedef, node.name()))
            sd.vars.append(VarDef(td.typedef + "*", "next"))
            self.ctx.structs.append(sd)
            self.ctx.typedef_map[element_name] = sd

            parent = to_c_variable(full_prefix)

            if parent in self.ctx.typedef_map:
                # add var def to the parent
                self.ctx.typedef_map[parent].vars.append(
                    VarDef(self.ctx.typedef_map[element_name].name + "*", to_c_variable(node.name())))

        return super().walk_node(node, depth)

    def add_node(self, node):
        return not node.nodetype() == LyNode.RPC and not node.config_false() and not node.nodetype() == LyNode.NOTIF

    def get_types_data(self):
        return self.ctx.types_data
