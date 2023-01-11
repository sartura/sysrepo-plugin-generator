from typing import Dict, Any

from core.config import GeneratorConfiguration


class Generator:
    """
    Base class for all generators.

    Methods
    -------
    generate_directories()
        Creates the directories needed by the generator.
    copy_files()
        Copies the files which do not need generation.
    generate_files()
        Generates plugin files.
    """

    def __init__(self, yang_dir: str, out_dir: str, config: GeneratorConfiguration):
        self.out_dir = out_dir
        self.yang_dir = yang_dir
        self.config = config

    def generate_directories(self):
        pass

    def copy_files(self):
        pass

    def generate_files(self):
        pass
