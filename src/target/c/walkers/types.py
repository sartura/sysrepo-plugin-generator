from typing import List
from libyang.schema import Node as LyNode

from core.utils import to_c_variable
from core.walker import Walker


class Typedef:
    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.typedef = "{}_t".format(name)


class Def:
    def __init__(self, name):
        self.name = name


class VarDef(Def):
    def __init__(self, type, name, kind):
        super().__init__(name)
        self.type = type
        self.kind = kind


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


class TypesWalker(Walker):
    def __init__(self, prefix, root_nodes):
        super().__init__(root_nodes)
        self.ctx = TypesContext(prefix)

    def walk_node(self, node, depth):
        last_prefix = self.ctx.prefix_stack[depth]
        if len(last_prefix) > 0:
            full_prefix = last_prefix
        else:
            full_prefix = self.ctx.prefix

        # print("\t" * depth, end="")
        if node.nodetype() == LyNode.CONTAINER:
            self.ctx.prefix_stack[depth +
                                  1] = "{}_{}".format(full_prefix, node.name())
            struct_name = to_c_variable(
                "{}_{}".format(full_prefix, node.name()))
            var_name = to_c_variable(node.name())

            # print("struct {}:".format(struct_name))

            td = Typedef("struct", struct_name)
            sd = StructDef(struct_name)

            self.ctx.typedefs.append(td)
            self.ctx.structs.append(sd)

            self.ctx.typedef_map[struct_name] = sd

            parent = to_c_variable(full_prefix)

            if parent in self.ctx.typedef_map:
                # add var def to the parent
                self.ctx.typedef_map[parent].vars.append(
                    VarDef(td.typedef, var_name, "struct"))

        elif node.nodetype() == LyNode.LEAF:
            # print("{} {}".format(node.type().basename(), node.name()))
            struct_name = to_c_variable(full_prefix)

            if node.type().basename() == "enumeration":
                # add enum type
                enum_name = to_c_variable(
                    "{}_{}".format(full_prefix, node.name()))

                enum_ed = EnumDef(enum_name, [to_c_variable("{}_{}".format(
                    enum_name, str(e))) for e in node.type().enums()])
                enum_td = Typedef("enum", enum_name)

                self.ctx.enums.append(enum_ed)
                self.ctx.typedefs.append(enum_td)

                self.ctx.typedef_map[enum_name] = enum_ed

                # previous value has to be a struct of some kind
                self.ctx.typedef_map[struct_name].vars.append(
                    VarDef(enum_td.typedef, to_c_variable(node.name()), "enum"))
            else:
                # previous value has to be a struct of some kind
                self.ctx.typedef_map[struct_name].vars.append(
                    VarDef(node.type().basename(), to_c_variable(node.name()), "var"))
        elif node.nodetype() == LyNode.LEAFLIST:
            struct_name = to_c_variable(
                "{}_{}".format(full_prefix, node.name()))
            var_name = to_c_variable(node.name())

            # element struct
            element_name = to_c_variable("{}_element".format(struct_name))
            element_var_name = var_name

            # print("struct {}:".format(struct_name))

            # element
            element_td = Typedef("struct", element_name)
            element_sd = StructDef(element_name)

            # data
            data_td = Typedef("struct", struct_name)
            data_sd = StructDef(struct_name)

            # add struct variables - data element + pointer to the next node
            element_sd.vars.append(
                VarDef(data_td.typedef, element_var_name, "var"))
            element_sd.vars.append(
                VarDef(element_td.typedef + "*", "next", "var"))

            self.ctx.typedefs.append(element_td)
            self.ctx.structs.append(element_sd)

            # add to typedef map
            self.ctx.typedef_map[element_name] = element_sd

            self.ctx.typedefs.append(data_td)
            self.ctx.structs.append(data_sd)

            self.ctx.typedef_map[struct_name] = data_sd

            # add data variable to the data struct
            if node.type().basename() == "enumeration":
                # add enum type
                enum_name = to_c_variable(
                    "{}_{}".format(full_prefix, node.name()))

                enum_ed = EnumDef(enum_name, [to_c_variable("{}_{}".format(
                    enum_name, str(e))) for e in node.type().enums()])
                enum_td = Typedef("enum", enum_name)

                self.ctx.enums.append(enum_ed)
                self.ctx.typedefs.append(enum_td)

                self.ctx.typedef_map[enum_name] = enum_ed

                # previous value has to be a struct of some kind
                self.ctx.typedef_map[struct_name].vars.append(
                    VarDef(enum_td.typedef, to_c_variable(node.name()), "enum"))
            else:
                # previous value has to be a struct of some kind
                self.ctx.typedef_map[struct_name].vars.append(
                    VarDef(node.type().basename(), to_c_variable(node.name()), "var"))

            # add to parent struct
            parent = to_c_variable(full_prefix)
            if parent in self.ctx.typedef_map:
                self.ctx.typedef_map[parent].vars.append(
                    VarDef(element_td.typedef + "*", var_name, "var"))
        elif node.nodetype() == LyNode.LIST:
            self.ctx.prefix_stack[depth +
                                  1] = "{}_{}".format(full_prefix, node.name())
            struct_name = to_c_variable(
                "{}_{}".format(full_prefix, node.name()))
            var_name = to_c_variable(node.name())

            # element struct
            element_name = to_c_variable("{}_element".format(struct_name))
            element_var_name = to_c_variable(node.name())

            # print("struct {}:".format(struct_name))

            # element
            element_td = Typedef("struct", element_name)
            element_sd = StructDef(element_name)

            # data
            data_td = Typedef("struct", struct_name)
            data_sd = StructDef(struct_name)

            # add struct variables - data element + pointer to the next node
            element_sd.vars.append(
                VarDef(data_td.typedef, element_var_name, "var"))
            element_sd.vars.append(
                VarDef(element_td.typedef + "*", "next", "var"))

            self.ctx.typedefs.append(element_td)
            self.ctx.structs.append(element_sd)

            # add to typedef map
            self.ctx.typedef_map[element_name] = element_sd

            self.ctx.typedefs.append(data_td)
            self.ctx.structs.append(data_sd)

            self.ctx.typedef_map[struct_name] = data_sd

            # add to parent struct
            parent = to_c_variable(full_prefix)
            if parent in self.ctx.typedef_map:
                self.ctx.typedef_map[parent].vars.append(
                    VarDef(element_td.typedef + "*", var_name, "var"))

        return super().walk_node(node, depth)

    def add_node(self, node):
        return not node.nodetype() == LyNode.RPC and not node.nodetype() == LyNode.ACTION and not node.config_false() and not node.nodetype() == LyNode.NOTIF

    def get_types_data(self):
        return self.ctx.types_data
