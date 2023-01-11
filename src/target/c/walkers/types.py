from typing import List, Dict
from libyang.schema import Node as LyNode

from core.utils import to_c_variable
from core.walker import Walker

from libyang.schema import SNode


class Typedef:
    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.typedef = "{}_t".format(name)

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name

    def get_typedef(self):
        return self.typedef


class Def:
    name: str

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name


class VarDef(Def):
    def __init__(self, type, name, kind):
        super().__init__(name)
        self.type = type
        self.kind = kind

    def get_type(self):
        return self.type

    def get_kind(self):
        return self.kind


class StructDef(Def):
    vars: List[VarDef]

    def __init__(self, name):
        super().__init__(name)
        self.vars = []

    def add_var(self, vd: VarDef):
        self.vars.append(vd)

    def get_vars(self):
        return self.vars

    def __str__(self):
        return "StructDef: {}".format(self.name)

    def __repr__(self):
        return str(self)


class EnumDef(Def):
    values: List[str]

    def __init__(self, name, values):
        super().__init__(name)
        self.values = values

    def get_values(self):
        return self.values


class UnionDef(Def):
    def __init__(self, name, vars):
        super().__init__(name)
        self.vars = vars


class TypesContext:
    """
    Context for types walker.

    Attributes
    ----------
    prefix : str
        Plugin prefix.
    parent_stack : Dict[int, str]
        Parent stack for the current tree.
    structs : List[StructDef]
        List of structure definitions.
    enums : List[EnumDef]
        List of enum definitions.
    typedefs: List[Typedef]
        List of typedefs.
    types_map: Dict[str, Def]
        Map of type names to their definitions.
    """
    prefix: str
    parent_stack: Dict[int, str]
    structs: List[StructDef]
    unions: List[UnionDef]
    enums: List[EnumDef]
    typedefs: List[Typedef]
    types_map: Dict[str, Def]

    def __init__(self, prefix):
        self.types_data = {}
        self.prefix = prefix
        self.parent_stack = {}
        self.structs: List[StructDef] = []
        self.unions: List[UnionDef] = []
        self.enums: List[EnumDef] = []
        self.typedefs: List[Typedef] = []
        self.types_map = {}

    def get_prefix(self):
        return self.prefix

    def add_struct(self, sd: StructDef):
        self.structs.append(sd)

    def add_union(self, ud: UnionDef):
        self.unions.append(ud)

    def add_enum(self, ed: EnumDef):
        self.enums.append(ed)

    def add_typedef(self, d: Def, td: Typedef):
        self.typedefs.append(td)
        self.types_map[d.get_name()] = d

    def parent_exists(self, parent: str) -> bool:
        return parent in self.types_map

    def add_var(self, parent: str, vd: VarDef):
        if self.parent_exists(parent) and type(self.types_map[parent]) == StructDef:
            self.types_map[parent].add_var(vd)
        else:
            raise KeyError("Parent {} not found".format(parent))

    def push_parent(self, depth: int, node_name: str):
        self.parent_stack[depth] = node_name

    def get_parent(self, depth: int) -> str:
        return self.parent_stack[depth-1]


class TypesWalker(Walker):
    def __init__(self, prefix, root_nodes):
        super().__init__(root_nodes)
        self.ctx = TypesContext(prefix)

    def get_parent_name(self, depth: int) -> str:
        return to_c_variable("{}_{}".format(
            self.ctx.get_prefix(), self.ctx.get_parent(depth)))

    def walk_node(self, node: SNode, depth: int):
        if node.nodetype() == LyNode.CONTAINER:
            self.ctx.push_parent(depth, node.name())

            struct_name = to_c_variable(
                "{}_{}".format(self.ctx.get_prefix(), node.name()))
            var_name = to_c_variable(node.name())

            td = Typedef("struct", struct_name)
            sd = StructDef(struct_name)

            self.ctx.add_struct(sd)
            self.ctx.add_typedef(sd, td)

            if depth > 0:
                parent = self.get_parent_name(depth)

                assert (self.ctx.parent_exists(parent))

                # add var def to the parent
                self.ctx.add_var(parent, VarDef(
                    td.get_typedef(), var_name, "struct"))

        elif node.nodetype() == LyNode.LEAF:
            # print("{} {}".format(node.type().basename(), node.name()))

            if node.type().basename() == "enumeration":
                # add enum type
                enum_name = to_c_variable(
                    "{}_{}".format(self.ctx.get_prefix(), node.name()))

                enum_ed = EnumDef(enum_name, [to_c_variable("{}_{}".format(
                    enum_name, str(e))) for e in node.type().enums()])
                enum_td = Typedef("enum", enum_name)

                self.ctx.add_enum(enum_ed)
                self.ctx.add_typedef(enum_ed, enum_td)

                assert (depth > 0)

                parent = self.get_parent_name(depth)

                assert (self.ctx.parent_exists(parent))

                self.ctx.add_var(parent, VarDef(
                    enum_td.typedef, to_c_variable(node.name()), "enum"))
            else:
                # previous value has to be a struct of some kind

                assert (depth > 0)

                parent = self.get_parent_name(depth)

                assert (self.ctx.parent_exists(parent))

                self.ctx.add_var(parent, VarDef(
                    node.type().basename(), to_c_variable(node.name()), "var"))

        elif node.nodetype() == LyNode.LEAFLIST:
            struct_name = to_c_variable(
                "{}_{}".format(self.ctx.get_prefix(), node.name()))
            var_name = to_c_variable(node.name())

            # element struct
            element_name = to_c_variable("{}_element".format(struct_name))
            element_var_name = to_c_variable(node.name())

            # element
            element_td = Typedef("struct", element_name)
            element_sd = StructDef(element_name)

            # data
            data_td = Typedef("struct", struct_name)
            data_sd = StructDef(struct_name)

            # add struct variables - data element + pointer to the next node
            element_sd.add_var(
                VarDef(data_td.typedef, element_var_name, "var"))
            element_sd.add_var(VarDef(element_td.typedef + "*", "next", "var"))

            self.ctx.add_struct(element_sd)
            self.ctx.add_typedef(element_sd, element_td)

            self.ctx.add_struct(data_sd)
            self.ctx.add_typedef(data_sd, data_td)

            self.ctx.typedefs.append(element_td)
            self.ctx.structs.append(element_sd)

            # add data variable to the data struct
            if node.type().basename() == "enumeration":
                # add enum type
                enum_name = to_c_variable(
                    "{}_{}".format(self.ctx.get_prefix(), node.name()))

                enum_ed = EnumDef(enum_name, [to_c_variable("{}_{}".format(
                    enum_name, str(e))) for e in node.type().enums()])
                enum_td = Typedef("enum", enum_name)

                self.ctx.add_enum(enum_ed)
                self.ctx.add_typedef(enum_ed, enum_td)

                assert (depth > 0)

                parent = self.get_parent_name(depth)

                assert (self.ctx.parent_exists(parent))

                self.ctx.add_var(parent, VarDef(
                    enum_td.typedef, to_c_variable(node.name()), "enum"))
            else:
                # previous value has to be a struct of some kind

                assert (depth > 0)

                parent = self.get_parent_name(depth)

                assert (self.ctx.parent_exists(parent))

                self.ctx.add_var(parent, VarDef(
                    node.type().basename(), to_c_variable(node.name()), "var"))

            # add to parent struct
            assert (depth > 0)

            parent = self.get_parent_name(depth)

            assert (self.ctx.parent_exists(parent))

            # add var def to the parent
            self.ctx.add_var(parent, VarDef(
                element_td.get_typedef() + "*", var_name, "var"))

        elif node.nodetype() == LyNode.LIST:
            self.ctx.push_parent(depth, node.name())

            struct_name = to_c_variable(
                "{}_{}".format(self.ctx.get_prefix(), node.name()))
            var_name = to_c_variable(node.name())

            # element struct
            element_name = to_c_variable("{}_element".format(struct_name))
            element_var_name = to_c_variable(node.name())

            # element
            element_td = Typedef("struct", element_name)
            element_sd = StructDef(element_name)

            # data
            data_td = Typedef("struct", struct_name)
            data_sd = StructDef(struct_name)

            # add struct variables - data element + pointer to the next node
            element_sd.add_var(
                VarDef(data_td.typedef, element_var_name, "var"))
            element_sd.add_var(VarDef(element_td.typedef + "*", "next", "var"))

            self.ctx.add_struct(element_sd)
            self.ctx.add_typedef(element_sd, element_td)

            self.ctx.add_struct(data_sd)
            self.ctx.add_typedef(data_sd, data_td)

            self.ctx.typedefs.append(element_td)
            self.ctx.structs.append(element_sd)

            if depth > 0:
                parent = self.get_parent_name(depth)

                assert (self.ctx.parent_exists(parent))

                # add var def to the parent
                self.ctx.add_var(parent, VarDef(
                    element_td.get_typedef() + "*", var_name, "var"))

        return False

    def add_node(self, node):
        return not node.nodetype() == LyNode.RPC and not node.nodetype() == LyNode.ACTION and not node.config_false() and not node.nodetype() == LyNode.NOTIF

    def get_types_data(self):
        return self.ctx.types_data
