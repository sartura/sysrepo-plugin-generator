import logging
import os
import shutil
import subprocess

import jinja2

import libyang

from typing import Dict, Any

from core.config import GeneratorConfiguration
from core.generator import Generator

from core.log.filters import DebugLevelFilter, InfoLevelFilter

from .walkers.sub.change import ChangeSubscriptionWalker


class CPPGenerator(Generator):
    # walkers
    change_sub_walker: ChangeSubscriptionWalker

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

    def __setup_libyang_ctx(self, yang_dir: str):
        self.ctx = libyang.Context(yang_dir)

        # access configurations
        yang_cfg = self.config.get_yang_configuration()
        mod_cfg = yang_cfg.get_modules_configuration()

        # load main module
        self.ctx.load_module(mod_cfg.get_main_module())

        # load all needed modules
        for m in yang_cfg.get_modules_configuration().get_other_modules():
            self.ctx.load_module(m)
            self.ctx.get_module(m).feature_enable_all()

        # use main module for plugin generation
        self.ly_mod = self.ctx.get_module(mod_cfg.get_main_module())

        # enable all features
        self.ly_mod.feature_enable_all()

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

    def generate_directories(self):
        cmake_modules_dir = os.path.join(self.out_dir, "CMakeModules")
        plugin_dir = os.path.join(self.source_dir, "core")
        dirs = [
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

    def copy_files(self):
        # copy CMake Find scripts
        modules_input_dir = "templates/common/CMakeModules"
        modules_output_dir = os.path.join(self.out_dir, "CMakeModules")

        for module in os.listdir(modules_input_dir):
            src_path = os.path.join(modules_input_dir, module)
            dst_path = os.path.join(modules_output_dir, module)

            shutil.copyfile(src_path, dst_path)

    def generate_files(self):
        pass

    def apply_formatting(self):
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
