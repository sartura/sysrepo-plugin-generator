import libyang
from libyang.schema import Node as LyNode
import os
import subprocess
import shutil
import jinja2
from .libraries.uthash import UTHashLibrary

from typing import List, Dict, Any, Optional

# add logging
import logging

from core.log.filters import DebugLevelFilter, InfoLevelFilter, WarningLevelFilter, ErrorLevelFilter

# core
from core.config import GeneratorConfiguration
from core.generator import Generator
from core.utils import extract_defines, to_c_variable

# import all walkers

# API walkers
from .walkers.api.change import ChangeAPIWalker
from .walkers.api.check import CheckAPIWalker
from .walkers.api.load import LoadAPIWalker
from .walkers.api.store import StoreAPIWalker

# subscription walkers
from .walkers.subscription.change import ChangeSubscriptionWalker
from .walkers.subscription.operational import OperationalSubscriptionWalker
from .walkers.subscription.rpc import RPCSubscriptionWalker
from .walkers.api.base import APIWalker

# datastore walkers
from .walkers.running import RunningWalker
from .walkers.startup import StartupWalker

# other walkers
from .walkers.ly_tree import LyTreeWalker
from .walkers.types import TypesWalker


class CGenerator(Generator):
    """
    C sysrepo plugin generator.

    Attributes
    ----------
    ly_tree_walker : LyTreeWalker
        Libyang tree walker.
    types_walker : TypesWalker
        Used for generating types for the plugin.
    startup_walker : StartupWalker
        Used for generating startup datastore load/store functionality.
    running_walker : RunningWalker
        Used for generating running datastore load/store functionality.
    change_walker : ChangeSubscriptionWalker
        Used for generating change subscription functionality.
    operational_walker : OperationalSubscriptionWalker
        Used for generating operational subscription functionality.
    rpc_walker : RPCSubscriptionWalker
        Used for generating RPC subscription functionality.
    change_api_walker : ChangeAPIWalker
        Used for generating change API functionality.
    check_api_walker : CheckAPIWalker
        Used for generating check API functionality.
    load_api_walker : LoadAPIWalker
        Used for generating load API functionality.
    store_api_walker : StoreAPIWalker
        Used for generating store API functionality.
    api_walker : APIWalker
        Used for generating whole API functionality.
    logger : logging.Logger
        Logger for the generator.

    Methods
    -------
    generate_directories()
        Generate project directory structure.
    copy_files()
        Copy files which do not need generation.
    generate_files()
        Generate plugin files.
    """

    # walkers
    ly_tree_walker: LyTreeWalker
    types_walker: TypesWalker
    startup_walker: StartupWalker
    running_walker: RunningWalker
    change_walker: ChangeSubscriptionWalker
    operational_walker: OperationalSubscriptionWalker
    rpc_walker: RPCSubscriptionWalker
    change_api_walker: ChangeAPIWalker
    check_api_walker: CheckAPIWalker
    load_api_walker: LoadAPIWalker
    store_api_walker: StoreAPIWalker
    api_walker: APIWalker

    # logger
    logger: logging.Logger

    def __init__(self, yang_dir: str, out_dir: str, config: GeneratorConfiguration):
        """
        Parameters
        ----------
        yang_dir : str
            Path to the directory with YANG modules.
        out_dir : str
            Output directory for the plugin.
        config : Dict[str, Any]
            TOML parsed configuration for the generator.
        """

        super().__init__(yang_dir, out_dir, config)

        # setup logger for the generator
        self.logger = logging.getLogger("CGenerator")
        self.logger.setLevel(logging.DEBUG)

        # Debug level handler
        debug_handler = logging.StreamHandler()
        debug_handler.setLevel(logging.DEBUG)
        debug_formatter = logging.Formatter(
            '[%(levelname)s][%(name)s][%(pathname)s:%(lineno)s]: %(message)s')
        debug_handler.setFormatter(debug_formatter)
        debug_handler.addFilter(DebugLevelFilter())
        self.logger.addHandler(debug_handler)

        # Info level handler
        info_handler = logging.StreamHandler()
        info_handler.setLevel(logging.INFO)
        info_formatter = logging.Formatter(
            '[%(levelname)s][%(name)s]: %(message)s')
        info_handler.setFormatter(info_formatter)
        info_handler.addFilter(InfoLevelFilter())
        self.logger.addHandler(info_handler)

        self.logger.info("Starting generator")

        self.source_dir = os.path.join(out_dir, "src")
        self.ctx = libyang.Context(yang_dir)

        yang_cfg = self.config.get_yang_configuration()
        mod_cfg = yang_cfg.get_modules_configuration()

        # load main module
        self.ctx.load_module(mod_cfg.get_main_module())

        # load features (optional, if None then all are enabled)
        features = mod_cfg.get_features()

        # load all needed modules
        for m in yang_cfg.get_modules_configuration().get_other_modules():
            self.ctx.load_module(m)
            # only enable the configured features
            self.__enable_configured_features(self.ctx.get_module(m), features)

        # use main module for plugin generation
        self.module = self.ctx.get_module(mod_cfg.get_main_module())

        # setup jinja2 environment
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader("templates/c/"),
            autoescape=jinja2.select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True
        )

        # extract defines from module
        self.defines, self.defines_map = extract_defines(
            self.config.get_prefix(), self.module)

        # append the path to the file once generated - at the end used with CMakeLists.txt
        self.generated_files = []
        self.include_dirs = ["src"]

        # only enable the configured features
        self.__enable_configured_features(self.module, features)

        self.logger.info("Loaded module {}".format((self.module.name())))
        self.logger.info(
            "Other modules loaded into the libyang context: {}".format(mod_cfg.get_other_modules()))

        # setup walkers
        self.ly_tree_walker = LyTreeWalker(
            self.config.get_prefix(), self.module.children())
        self.types_walker = TypesWalker(
            self.config.get_prefix(), self.module.children(), self.config.get_yang_configuration().get_prefix_configuration())

        # datastore walkers
        self.startup_walker = StartupWalker(
            self.config.get_prefix(), self.module.children())
        self.running_walker = RunningWalker(
            self.config.get_prefix(), self.module.children())

        # subscription walkers
        self.change_walker = ChangeSubscriptionWalker(
            self.config.get_prefix(), self.module.children())
        self.operational_walker = OperationalSubscriptionWalker(
            self.config.get_prefix(), self.module.children())
        self.rpc_walker = RPCSubscriptionWalker(
            self.config.get_prefix(), self.module.children())

        # API walkers
        self.change_api_walker = ChangeAPIWalker(
            self.config.get_prefix(), self.module.children(), self.source_dir)
        self.load_api_walker = LoadAPIWalker(
            self.config.get_prefix(), self.module.children(), self.source_dir)
        self.store_api_walker = StoreAPIWalker(
            self.config.get_prefix(), self.module.children(), self.source_dir)
        self.check_api_walker = CheckAPIWalker(
            self.config.get_prefix(), self.module.children(), self.source_dir)

        # full API walker
        self.api_walker = APIWalker(self.config.get_prefix(), self.module.children(
        ), self.source_dir, ['check', 'load', 'store', 'change'])

        # setup libraries
        self.libraries = [
            UTHashLibrary(self.out_dir),
        ]

        # add all walkers to the list for easier extraction
        all_walkers = [
            # base
            self.ly_tree_walker,
            self.types_walker,

            # datastore
            self.startup_walker,
            self.running_walker,

            # subscription
            self.change_walker,
            self.operational_walker,
            self.rpc_walker,

            # API
            self.change_api_walker,
            self.load_api_walker,
            self.store_api_walker,
            self.check_api_walker,
            self.api_walker
        ]

        # extract all data
        for walker in all_walkers:
            walker.walk()

        for sd in self.types_walker.ctx.structs:
            print("struct {}".format(sd.get_name()))
            for vd in sd.get_vars():
                print("  {} {};".format(vd.get_type(), vd.get_name()))

        # print(self.types_walker.ctx.structs)

    def __enable_configured_features(self, module, features: Optional[List[str]]):
        self.logger.info("Features in module {}:".format(module.name()))
        module.feature_disable_all()
        for feature in module.features():
            if features == None or feature.name() in features:
                module.feature_enable(feature.name())
                self.logger.info("\tEnabled feature {} in module {}".format(feature, module.name()))
            else:
                self.logger.info("\tDisabled feature {} in module {}".format(feature, module.name()))

    def generate_directories(self):
        deps_dir = os.path.join(self.out_dir, "deps")
        plugin_dir = os.path.join(self.source_dir, "plugin")
        cmake_modules_dir = os.path.join(self.out_dir, "CMakeModules")
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
        # load
        load_dirs = self.load_api_walker.get_directories()
        for dir in load_dirs:
            if not os.path.exists(dir):
                os.mkdir(dir)

        # store
        store_dirs = self.store_api_walker.get_directories()
        for dir in store_dirs:
            if not os.path.exists(dir):
                os.mkdir(dir)

        # check
        check_dirs = self.check_api_walker.get_directories()
        for dir in check_dirs:
            if not os.path.exists(dir):
                os.mkdir(dir)

        # change
        change_dirs = self.change_api_walker.get_directories()
        for dir in change_dirs:
            if not os.path.exists(dir):
                os.mkdir(dir)

    def __generate_data_dirs(self):
        pass

    def generate_files(self):
        # copy cmake modules
        self.__generate_cmake_files()

        # plugin.h, plugin.c and main.c
        self.__generate_plugin_files()

        # common plugin files - common, ly_tree, types, context
        self.__generate_common_files()

        # running and startup DS files
        self.__generate_datastore_files()

        # subscription - change, operational, rpc
        self.__generate_subscription_files()

        # API - load, store, check, change
        self.__generate_api_files()

        # plugin internal data structure functions headers and sources
        self.__generate_data_files()

        # generate library files
        for lib in self.libraries:
            lib.generate_files()

        # get include directories from the library
        for lib in self.libraries:
            paths = lib.get_include_dirs()
            for path in paths:
                self.include_dirs.append(path.replace(self.out_dir, "")[1:])

        # cmake with all files to compile
        self.__generate_cmake_lists()

        # apply style
        self.__apply_clang_format()

    def __generate_plugin_files(self):

        self.__generate_file("src/plugin.h", plugin_prefix=self.config.get_prefix(), module=self.module.name(),
                             defines=self.defines)

        self.__generate_file("src/plugin.c", plugin_prefix=self.config.get_prefix(), module=self.module.name(),
                             rpc_callbacks=self.rpc_walker.get_callbacks(),
                             oper_callbacks=self.operational_walker.get_callbacks(),
                             change_callbacks=self.change_walker.get_callbacks(),
                             defines_map=self.defines_map
                             )

        self.__generate_file(
            "src/main.c", plugin_prefix=self.config.get_prefix(), module=self.module.name())

    def __generate_common_files(self):
        # common.h
        self.__generate_file("src/plugin/common.h", plugin_prefix=self.config.get_prefix(), module=self.module.name(),
                             defines=self.defines)

        # context.h
        self.__generate_file("src/plugin/context.h",
                             plugin_prefix=self.config.get_prefix())

        # types.h
        self.__generate_file("src/plugin/types.h", plugin_prefix=self.config.get_prefix(),
                             structs=self.types_walker.ctx.structs,
                             enums=self.types_walker.ctx.enums,
                             unions=self.types_walker.ctx.unions,
                             typedefs=self.types_walker.ctx.typedefs,
                             types=self.api_walker.get_types())

        # ly_tree
        self.__generate_file("src/plugin/ly_tree.h",  plugin_prefix=self.config.get_prefix(),
                             ly_tree_functions=self.ly_tree_walker.get_functions(), LyNode=LyNode)
        self.__generate_file("src/plugin/ly_tree.c",  plugin_prefix=self.config.get_prefix(),
                             ly_tree_functions=self.ly_tree_walker.get_functions(), LyNode=LyNode)
        # for fn in self.ly_tree_walker.get_functions():
        #     if fn.node.nodetype() == LyNode.LIST:
        #         print(fn.node.keys())
        # self.include_dirs.append(fn.get_include_dir())

    def __generate_datastore_files(self):
        self.__generate_file("src/plugin/startup/load.h",
                             plugin_prefix=self.config.get_prefix())
        self.__generate_file("src/plugin/startup/load.c", plugin_prefix=self.config.get_prefix(),
                             load_callbacks=self.startup_walker.get_callbacks())
        self.__generate_file("src/plugin/startup/store.h",
                             plugin_prefix=self.config.get_prefix())
        self.__generate_file("src/plugin/startup/store.c", plugin_prefix=self.config.get_prefix(),
                             store_callbacks=self.startup_walker.get_callbacks())

    def __generate_subscription_files(self):
        self.__generate_file("src/plugin/subscription/change.h", plugin_prefix=self.config.get_prefix(),
                             change_callbacks=self.change_walker.get_callbacks())
        self.__generate_file("src/plugin/subscription/change.c",
                             plugin_prefix=self.config.get_prefix(),
                             change_callbacks=self.change_walker.get_callbacks(),
                             change_path_map=self.change_api_walker.get_path_map(),
                             to_c_variable=to_c_variable,
                             dir_functions=self.change_api_walker.get_directory_functions())

        self.__generate_file("src/plugin/subscription/operational.h", plugin_prefix=self.config.get_prefix(),
                             oper_callbacks=self.operational_walker.get_callbacks())
        self.__generate_file("src/plugin/subscription/operational.c", plugin_prefix=self.config.get_prefix(),
                             oper_callbacks=self.operational_walker.get_callbacks())

        self.__generate_file("src/plugin/subscription/rpc.h", plugin_prefix=self.config.get_prefix(),
                             rpc_callbacks=self.rpc_walker.get_callbacks())
        self.__generate_file("src/plugin/subscription/rpc.c", plugin_prefix=self.config.get_prefix(),
                             rpc_callbacks=self.rpc_walker.get_callbacks())

    def __generate_api_files(self):
        self.logger.info("Generating API files:")
        dirs = self.api_walker.get_directories()
        dir_functions = self.api_walker.get_directory_functions()
        files = self.api_walker.get_api_filenames()
        types = self.api_walker.get_types()

        for dir in dirs:
            # generate all files in this directory
            prefix, node_list = dir_functions[dir]

            for file in files:
                path = os.path.join(dir, file)
                self.logger.info("\tGenerating {}".format(path))
                template = self.jinja_env.get_template(
                    "src/plugin/api/{}.jinja".format(file))
                with open(path, "w") as api_file:
                    api_file.write(template.render(
                        plugin_prefix=self.config.get_prefix(), prefix=prefix, node_list=node_list, LyNode=LyNode, to_c_variable=to_c_variable, types=types))
                    self.generated_files.append(
                        path.replace(self.out_dir, "")[1:])

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
                    self.logger.info("\tGenerating {}".format(path))
                    template = self.jinja_env.get_template(
                        "src/plugin/api/{}.jinja".format(file))
                    with open(path, "w") as api_file:
                        api_file.write(template.render(
                            plugin_prefix=self.config.get_prefix(), prefix=prefix, node_list=node_list, LyNode=LyNode, to_c_variable=to_c_variable, types=types))
                        self.generated_files.append(
                            path.replace(self.out_dir, "")[1:])

    def __generate_data_files(self):
        pass

    def __generate_file(self, file, **kwargs):
        template = self.jinja_env.get_template("{}.jinja".format(file))

        # generate #def's
        self.defines, self.defines_map = extract_defines(
            self.config.get_prefix(), self.module)

        path = os.path.join(self.out_dir, file)
        self.generated_files.append(file)
        self.logger.info("Generating {}".format(path))

        with open(path, "w") as file:
            file.write(template.render(kwargs))

    def __generate_cmake_files(self):
        modules_input_dir = "templates/common/CMakeModules"
        modules_output_dir = os.path.join(self.out_dir, "CMakeModules")

        for module in os.listdir(modules_input_dir):
            src_path = os.path.join(modules_input_dir, module)
            dst_path = os.path.join(modules_output_dir, module)

            shutil.copyfile(src_path, dst_path)

    def __generate_cmake_lists(self):
        self.__generate_file(
            "CMakeLists.txt", plugin_prefix=self.config.get_prefix(), source_files=[file for file in self.generated_files if file[-2:] == ".c"], include_dirs=self.include_dirs)
        self.__generate_file(
            "CompileOptions.cmake")

    def __apply_clang_format(self):
        self.logger.info("Applying .clang-format style")
        if shutil.which("clang-format") is not None:
            # copy the used clang-format file into the source directory and apply it to all generated files
            src_path = "templates/common/.clang-format"
            dst_path = os.path.join(self.out_dir, ".clang-format")

            shutil.copyfile(src_path, dst_path)

            for gen in self.generated_files:
                # run clang-format command
                if gen[-1:] == "c" or gen[-1:] == "h":
                    self.logger.info("Applying style to {}".format(gen))
                    params = ["clang-format", "-style=file",
                              os.path.join(self.out_dir, gen)]
                    output = subprocess.check_output(params)
                    with open(os.path.join(self.out_dir, gen), "wb") as out_file:
                        out_file.write(output)
