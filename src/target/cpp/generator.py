import logging
import os
import shutil
import subprocess

import jinja2

import libyang

from typing import List, Dict, Any, Optional

from core.config import GeneratorConfiguration
from core.generator import Generator

from core.log.filters import DebugLevelFilter, InfoLevelFilter

from .walkers.sub.change import ChangeSubscriptionWalker
from .walkers.sub.oper import OperSubscriptionWalker
from .walkers.sub.rpc import RPCSubscriptionWalker
from .walkers.yang.tree import YangTreeWalker

from core.utils import to_camel_case, to_c_variable

from libyang.schema import Node as LyNode


class CPPGenerator(Generator):
    # walkers
    change_sub_walker: ChangeSubscriptionWalker
    oper_sub_walker: OperSubscriptionWalker
    rpc_sub_walker: RPCSubscriptionWalker
    yang_tree_walker: YangTreeWalker

    # libyang
    ly_mod: libyang.Module

    # logger
    logger: logging.Logger

    def __init__(self, yang_dir: str, out_dir: str, config: GeneratorConfiguration):
        super().__init__(yang_dir, out_dir, config)

        # setup logger for the generator
        self.logger = logging.getLogger("CPPGenerator")
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

        self.logger.info("Starting C++ generator")

        # setup jinja2 environment
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader("templates/c/"),
            autoescape=jinja2.select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True
        )

        # initialize libyang and jinja2
        self.__setup_libyang_ctx(yang_dir)
        self.__setup_jinja2_env()

        # setup and run walkers
        self.source_dir = os.path.join(out_dir, "src")
        self.generated_files = []

        self.change_sub_walker = ChangeSubscriptionWalker(
            self.config.get_prefix(), self.ly_mod.children(), self.config.get_yang_configuration().get_prefix_configuration())
        self.oper_sub_walker = OperSubscriptionWalker(
            self.config.get_prefix(), self.ly_mod.children(), self.config.get_yang_configuration().get_prefix_configuration())
        self.rpc_sub_walker = RPCSubscriptionWalker(
            self.config.get_prefix(), self.ly_mod.children(), self.config.get_yang_configuration().get_prefix_configuration())
        self.yang_tree_walker = YangTreeWalker(
            self.config.get_prefix(), self.ly_mod.children(), self.config.get_yang_configuration().get_prefix_configuration())

        # run walkers
        walkers = [
            # sub walkers
            self.change_sub_walker,
            self.oper_sub_walker,
            self.rpc_sub_walker,
            # yang walkers
            self.yang_tree_walker,
        ]

        for walker in walkers:
            walker.walk()

        [self.logger.info("oper callbacks: {}".format(
            self.oper_sub_walker.get_callbacks()))]

    def __setup_libyang_ctx(self, yang_dir: str):
        self.ctx = libyang.Context(yang_dir)

        # access configurations
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
        self.ly_mod = self.ctx.get_module(mod_cfg.get_main_module())

        # only enable the configured features
        self.__enable_configured_features(self.ly_mod, features)

        self.logger.info("Loaded module {}".format((self.ly_mod.name())))
        self.logger.info(
            "Other modules loaded into the libyang context: {}".format(mod_cfg.get_other_modules()))

    def __setup_jinja2_env(self):
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader("templates/cpp/"),
            autoescape=jinja2.select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True
        )

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
        cmake_modules_dir = os.path.join(self.out_dir, "CMakeModules")
        plugin_dir = os.path.join(self.source_dir, "core")
        dirs = [
            self.source_dir,
            plugin_dir,
            cmake_modules_dir,
            os.path.join(plugin_dir, "sub"),
            os.path.join(plugin_dir, "yang"),
            os.path.join(plugin_dir, "api"),
            os.path.join(plugin_dir, "data"),
        ]

        for dir in dirs:
            if not os.path.exists(dir):
                os.mkdir(dir)

    def copy_files(self):
        # copy CMake Find scripts
        modules_input_dir = "templates/common/CMakeModules"
        modules_output_dir = os.path.join(self.out_dir, "CMakeModules")

        for module in os.listdir(modules_input_dir):
            src_path = os.path.join(modules_input_dir, module)
            dst_path = os.path.join(modules_output_dir, module)

            shutil.copyfile(src_path, dst_path)

    def __generate_file(self, file, **kwargs):
        template = self.jinja_env.get_template("{}.jinja2".format(file))

        path = os.path.join(self.out_dir, file)
        self.generated_files.append(file)
        self.logger.info("Generating {}".format(path))

        with open(path, "w") as file:
            file.write(template.render(kwargs))

    def __generate_core_files(self):
        self.__generate_file(
            "src/core/context.hpp", root_namespace=self.config.get_prefix().replace("_", "::"))
        self.__generate_file(
            "src/core/context.cpp", root_namespace=self.config.get_prefix().replace("_", "::"))

    def __generate_sub_files(self):
        # module change subscriptions
        self.__generate_file("src/core/sub/change.hpp", root_namespace=self.config.get_prefix().replace("_", "::"),
                             change_callbacks=self.change_sub_walker.get_callbacks(), to_camel_case=to_camel_case)
        self.__generate_file("src/core/sub/change.cpp", root_namespace=self.config.get_prefix().replace("_", "::"),
                             change_callbacks=self.change_sub_walker.get_callbacks(), to_camel_case=to_camel_case)

        # operational subscriptions
        self.__generate_file("src/core/sub/oper.hpp", root_namespace=self.config.get_prefix().replace("_", "::"),
                             oper_callbacks=self.oper_sub_walker.get_callbacks(), to_camel_case=to_camel_case)
        self.__generate_file("src/core/sub/oper.cpp", root_namespace=self.config.get_prefix().replace("_", "::"),
                             oper_callbacks=self.oper_sub_walker.get_callbacks(), to_camel_case=to_camel_case)

        # rpc/action subscriptions
        self.__generate_file("src/core/sub/rpc.hpp", root_namespace=self.config.get_prefix().replace("_", "::"),
                             rpc_callbacks=self.rpc_sub_walker.get_callbacks(), to_camel_case=to_camel_case)
        self.__generate_file("src/core/sub/rpc.cpp", root_namespace=self.config.get_prefix().replace("_", "::"),
                             rpc_callbacks=self.rpc_sub_walker.get_callbacks(), to_camel_case=to_camel_case)

    def __generate_yang_files(self):
        # yang tree API
        self.__generate_file("src/core/yang/tree.hpp", root_namespace=self.config.get_prefix().replace("_", "::"),
                             yang_tree_functions=self.yang_tree_walker.get_functions(), to_camel_case=to_camel_case, LyNode=LyNode, to_c_variable=to_c_variable)
        self.__generate_file("src/core/yang/tree.cpp", root_namespace=self.config.get_prefix().replace("_", "::"),
                             yang_tree_functions=self.yang_tree_walker.get_functions(), to_camel_case=to_camel_case, LyNode=LyNode, to_c_variable=to_c_variable)

        # yang paths variables

    def __generate_plugin_files(self):
        self.__generate_file(
            "src/plugin.hpp", root_namespace=self.config.get_prefix().replace("_", "::"))
        self.__generate_file(
            "src/plugin.cpp", root_namespace=self.config.get_prefix().replace("_", "::"))

    def __generate_cmake_files(self):
        # CMakeLists.txt
        print(self.generated_files)
        self.__generate_file("CMakeLists.txt", project_name="{}-plugin".format(self.config.get_yang_configuration().get_modules_configuration().get_main_module()),
                             sources=[
                                 f for f in self.generated_files if f[-3:] == "cpp"],
                             headers=[
                                 f for f in self.generated_files if f[-3:] == "cpp"],
                             source_dir="src",
                             to_camel_case=to_camel_case
                             )
        pass

    def generate_files(self):
        self.__generate_core_files()
        self.__generate_sub_files()
        self.__generate_yang_files()
        self.__generate_plugin_files()
        self.__generate_cmake_files()

    def apply_formatting(self):
        self.logger.info("Applying .clang-format style")

        if shutil.which("clang-format") is not None:
            self.logger.info("clang-format found!")
            # copy the used clang-format file into the source directory and apply it to all generated files
            src_path = "templates/common/.clang-format"
            dst_path = os.path.join(self.out_dir, ".clang-format")

            shutil.copyfile(src_path, dst_path)

            for gen in self.generated_files:
                # run clang-format command
                if gen[-3:] == "cpp" or gen[-3:] == "hpp":
                    self.logger.info("Running clang-format on {}".format(gen))
                    params = ["clang-format", "-style=file",
                              os.path.join(self.out_dir, gen)]
                    output = subprocess.check_output(params)
                    with open(os.path.join(self.out_dir, gen), "wb") as out_file:
                        out_file.write(output)
