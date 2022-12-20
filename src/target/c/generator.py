import libyang
from libyang.schema import Node as LyNode
import os
import subprocess
import shutil
import jinja2
from libraries.uthash import UTHashLibrary

# import all walkers

# API walkers
from .walkers.api.change import ChangeApiWalker
from .walkers.api.check import CheckApiWalker
from .walkers.api.load import LoadApiWalker
from .walkers.api.store import StoreApiWalker

# subscription walkers
from .walkers.subscription.change import ChangeSubscriptionWalker

# datastore walkers
from .walkers.running import RunningWalker
from .walkers.startup import StartupWalker

# other walkers
from .walkers.ly_tree import LyTreeWalker
from .walkers.types import TypesWalker

from .walkers import startup, ly_tree, api, types
from .walkers.subscription import rpc, change, operational
from .walkers import change_api
from core.generator import Generator

from core.utils import extract_defines, to_c_variable


class CGenerator(Generator):
    def __init__(self, prefix, outdir, modules, main_module, yang_dir):
        super.__init__(prefix, outdir, modules, main_module, yang_dir)

        print("Started generator")

        self.source_dir = os.path.join(outdir, "src")
        self.ctx = libyang.Context(yang_dir)

        # load all needed modules
        for m in modules:
            self.ctx.load_module(m)
            self.ctx.get_module(m).feature_enable_all()

        # use main module for plugin generation
        self.module = self.ctx.get_module(main_module)
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader("templates/C/"),
            autoescape=jinja2.select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True
        )

        # append the path to the file once generated - at the end used with CMakeLists.txt
        self.generated_files = []
        self.include_dirs = ["src"]

        # assume all features enabled for full module generation
        self.module.feature_enable_all()

        print("Loaded module %s:" % (self.module.name()))
        print("All loaded modules: ", modules)

        if prefix is not None:
            self.prefix = prefix
        else:
            self.prefix = self.module.prefix()

        # setup walkers
        self.ly_tree_walker = ly_tree.Walker(
            self.prefix, self.module.children())
        self.startup_walker = startup.Walker(
            self.prefix, self.module.children())
        self.rpc_walker = rpc.Walker(
            self.prefix, self.module.children())
        self.change_walker = change.Walker(self.prefix, self.module.children())
        self.operational_walker = operational.Walker(
            self.prefix, self.module.children())
        self.api_walker = api.Walker(
            self.prefix, self.module.children(), self.source_dir)
        self.change_api_walker = change_api.Walker(
            self.prefix, self.module.children(), self.source_dir)

        self.types_walker = types.Walker(
            self.prefix, self.module.children())

        self.libraries = [
            UTHashLibrary(self.outdir),
        ]

        # add all walkers to the list for easier extraction
        all_walkers = [
            # base
            self.ly_tree_walker,
            self.startup_walker,
            self.types_walker,

            # subscription
            self.rpc_walker,
            self.change_walker,
            self.operational_walker,

            # API
            self.api_walker,
            self.change_api_walker,
        ]

        # extract all data
        for walker in all_walkers:
            walker.walk()

        self.types_walker.ctx.structs.reverse()

        for s in self.types_walker.ctx.structs:
            # print("struct {}".format(s.name))
            s.vars.reverse()
            # for v in s.vars:
            #     # print("\t {} {}".format(v.type, v.name))
            # # print()

        self.types_walker.ctx.typedefs.reverse()

        for e in self.types_walker.ctx.enums:
            # print("enum {}:".format(e.name))
            e.values.reverse()
            # for v in e.values:
            #     print("\t {}".format(v))
            # print()

        # for t in self.types_walker.ctx.typedefs:
        #     print("typedef {} {} {}".format(t.type, t.name, t.typedef))

    def generate_directories(self):
        deps_dir = os.path.join(self.outdir, "deps")
        plugin_dir = os.path.join(self.source_dir, "plugin")
        cmake_modules_dir = os.path.join(self.outdir, "CMakeModules")
        dirs = [
            deps_dir,
            self.source_dir,
            plugin_dir,
            cmake_modules_dir,
            os.path.join(plugin_dir, "subscription"),
            os.path.join(plugin_dir, "startup"),
            os.path.join(plugin_dir, "api"),
            os.path.join(plugin_dir, "data"),
        ]

        for dir in dirs:
            if not os.path.exists(dir):
                os.mkdir(dir)

        self.__generate_api_dirs()
        self.__generate_data_dirs()

        # generate library directories
        for lib in self.libraries:
            lib.generate_directories()

    def __generate_api_dirs(self):
        dirs = self.api_walker.get_directories()

        for dir in dirs:
            if not os.path.exists(dir):
                os.mkdir(dir)

        dirs = self.change_api_walker.get_directories()

        for dir in dirs:
            if not os.path.exists(dir):
                os.mkdir(dir)

    def __generate_data_dirs(self):
        pass

    def generate_files(self):
        # copy cmake modules
        self.__generate_cmake_files()

        # generate files
        self.__generate_common_h()
        self.__generate_context_h()
        self.__generate_types_h()

        # startup
        self.__generate_startup_load_h()
        self.__generate_startup_load_c()
        self.__generate_startup_store_h()
        self.__generate_startup_store_c()

        # subscription
        self.__generate_subscription_change_h()
        self.__generate_subscription_change_c()
        self.__generate_subscription_operational_h()
        self.__generate_subscription_operational_c()
        self.__generate_subscription_rpc_h()
        self.__generate_subscription_rpc_c()

        # ly_tree
        self.__generate_ly_tree_h()
        self.__generate_ly_tree_c()

        # API and data files
        self.__generate_api_files()
        self.__generate_data_files()

        # main files
        self.__generate_plugin_h()
        self.__generate_plugin_c()
        self.__generate_main_c()

        # generate library files
        for lib in self.libraries:
            lib.generate_files()

        # get include directories from the library
        for lib in self.libraries:
            paths = lib.get_include_dirs()
            for path in paths:
                self.include_dirs.append(path.replace(self.outdir, "")[1:])

        # cmake with all files to compile
        self.__generate_cmake_lists()

        # apply style
        self.__apply_clang_format()

    def __generate_file(self, file, **kwargs):
        template = self.jinja_env.get_template("{}.jinja".format(file))

        # generate #def's
        self.defines, self.defines_map = extract_defines(
            self.prefix, self.module)

        path = os.path.join(self.outdir, file)
        self.generated_files.append(file)
        print("Generating {}".format(path))

        with open(path, "w") as file:
            file.write(template.render(kwargs))

    def __generate_cmake_files(self):
        modules_input_dir = "src/CMakeModules"
        modules_output_dir = os.path.join(self.outdir, "CMakeModules")

        for module in os.listdir(modules_input_dir):
            src_path = os.path.join(modules_input_dir, module)
            dst_path = os.path.join(modules_output_dir, module)

            shutil.copyfile(src_path, dst_path)

    def __generate_common_h(self):
        self.defines, self.defines_map = extract_defines(
            self.prefix, self.module)
        self.__generate_file("src/plugin/common.h", plugin_prefix=self.prefix, module=self.module.name(),
                             defines=self.defines)

    def __generate_context_h(self):
        self.__generate_file("src/plugin/context.h", plugin_prefix=self.prefix)

    def __generate_types_h(self):
        self.__generate_file("src/plugin/types.h", plugin_prefix=self.prefix,
                             structs=self.types_walker.ctx.structs,
                             enums=self.types_walker.ctx.enums,
                             unions=self.types_walker.ctx.unions,
                             typedefs=self.types_walker.ctx.typedefs,
                             types=self.api_walker.get_types())

    def __generate_startup_load_h(self):
        self.__generate_file("src/plugin/startup/load.h",
                             plugin_prefix=self.prefix)

    def __generate_startup_load_c(self):
        self.__generate_file("src/plugin/startup/load.c", plugin_prefix=self.prefix,
                             load_callbacks=self.startup_walker.get_callbacks())

    def __generate_startup_store_h(self):
        self.__generate_file("src/plugin/startup/store.h",
                             plugin_prefix=self.prefix)

    def __generate_startup_store_c(self):
        self.__generate_file("src/plugin/startup/store.c", plugin_prefix=self.prefix,
                             store_callbacks=self.startup_walker.get_callbacks())

    def __generate_subscription_change_h(self):
        self.__generate_file("src/plugin/subscription/change.h", plugin_prefix=self.prefix,
                             change_callbacks=self.change_walker.get_callbacks())

    def __generate_subscription_change_c(self):
        self.__generate_file("src/plugin/subscription/change.c",
                             plugin_prefix=self.prefix,
                             change_callbacks=self.change_walker.get_callbacks(),
                             change_path_map=self.change_api_walker.get_path_map(),
                             to_c_variable=to_c_variable,
                             dir_functions=self.change_api_walker.get_directory_functions())

    def __generate_subscription_operational_h(self):
        self.__generate_file("src/plugin/subscription/operational.h", plugin_prefix=self.prefix,
                             oper_callbacks=self.operational_walker.get_callbacks())

    def __generate_subscription_operational_c(self):
        self.__generate_file("src/plugin/subscription/operational.c", plugin_prefix=self.prefix,
                             oper_callbacks=self.operational_walker.get_callbacks())

    def __generate_subscription_rpc_h(self):
        self.__generate_file("src/plugin/subscription/rpc.h", plugin_prefix=self.prefix,
                             rpc_callbacks=self.rpc_walker.get_callbacks())

    def __generate_subscription_rpc_c(self):
        self.__generate_file("src/plugin/subscription/rpc.c", plugin_prefix=self.prefix,
                             rpc_callbacks=self.rpc_walker.get_callbacks())

    def __generate_ly_tree_h(self):
        self.__generate_file("src/plugin/ly_tree.h",  plugin_prefix=self.prefix,
                             ly_tree_functions=self.ly_tree_walker.get_functions(), LyNode=LyNode)

    def __generate_ly_tree_c(self):
        self.__generate_file("src/plugin/ly_tree.c",  plugin_prefix=self.prefix,
                             ly_tree_functions=self.ly_tree_walker.get_functions(), LyNode=LyNode)

    def __generate_api_files(self):
        print("Generating API files:")
        dirs = self.api_walker.get_directories()
        dir_functions = self.api_walker.get_directory_functions()
        files = self.api_walker.get_api_filenames()
        types = self.api_walker.get_types()
        for dir in dirs:
            # generate all files in this directory
            prefix, node_list = dir_functions[dir]
            for file in files:
                path = os.path.join(dir, file)
                print("\tGenerating {}".format(path))
                template = self.jinja_env.get_template(
                    "src/plugin/api/{}.jinja".format(file))
                with open(path, "w") as api_file:
                    api_file.write(template.render(
                        plugin_prefix=self.prefix, prefix=prefix, node_list=node_list, LyNode=LyNode, to_c_variable=to_c_variable, types=types))
                    self.generated_files.append(
                        path.replace(self.outdir, "")[1:])

        dirs = self.change_api_walker.get_directories()
        dir_functions = self.change_api_walker.get_directory_functions()
        files = self.change_api_walker.get_api_filenames()
        types = self.change_api_walker.get_types()
        for dir in dirs:
            # generate all files in this directory
            if dir in dir_functions:
                prefix, node_list = dir_functions[dir]
                for file in files:
                    path = os.path.join(dir, file)
                    print("\tGenerating {}".format(path))
                    template = self.jinja_env.get_template(
                        "src/plugin/api/{}.jinja".format(file))
                    with open(path, "w") as api_file:
                        api_file.write(template.render(
                            plugin_prefix=self.prefix, prefix=prefix, node_list=node_list, LyNode=LyNode, to_c_variable=to_c_variable, types=types))
                        self.generated_files.append(
                            path.replace(self.outdir, "")[1:])

    def __generate_data_files(self):
        pass

    def __generate_plugin_h(self):
        self.__generate_file("src/plugin.h", plugin_prefix=self.prefix, module=self.module.name(),
                             defines=self.defines)

    def __generate_plugin_c(self):
        self.__generate_file("src/plugin.c", plugin_prefix=self.prefix, module=self.module.name(),
                             rpc_callbacks=self.rpc_walker.get_callbacks(),
                             oper_callbacks=self.operational_walker.get_callbacks(),
                             change_callbacks=self.change_walker.get_callbacks(),
                             defines_map=self.defines_map
                             )

    def __generate_main_c(self):
        self.__generate_file(
            "src/main.c", plugin_prefix=self.prefix, module=self.module.name())

    def __generate_cmake_lists(self):
        self.__generate_file(
            "CMakeLists.txt", plugin_prefix=self.prefix, source_files=[file for file in self.generated_files if file[-2:] == ".c"], include_dirs=self.include_dirs)
        self.__generate_file(
            "CompileOptions.cmake")

    def __apply_clang_format(self):
        print("Applying .clang-format style")
        if shutil.which("clang-format") is not None:
            # copy the used clang-format file into the source directory and apply it to all generated files
            src_path = "src/.clang-format"
            dst_path = os.path.join(self.outdir, ".clang-format")

            shutil.copyfile(src_path, dst_path)

            for gen in self.generated_files:
                # run clang-format command
                if gen[-1:] == "c" or gen[-1:] == "h":
                    print("Applying style to {}".format(gen))
                    params = ["clang-format", "-style=file",
                              os.path.join(self.outdir, gen)]
                    output = subprocess.check_output(params)
                    with open(os.path.join(self.outdir, gen), "wb") as out_file:
                        out_file.write(output)
