import logging
import os
import shutil
import subprocess

from typing import Dict, Any

from core.config import GeneratorConfiguration
from core.generator import Generator

from core.log.filters import DebugLevelFilter, InfoLevelFilter

from .walkers.sub.change import ChangeSubscriptionWalker


class CPPGenerator(Generator):
    # walkers
    change_sub_walker: ChangeSubscriptionWalker

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

        self.source_dir = os.path.join(out_dir, "src")
        self.generated_files = []

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
