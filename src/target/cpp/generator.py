from typing import Dict, Any

from core.config import GeneratorConfiguration


class CPPGenerator:
    def __init__(self, yang_dir: str, out_dir: str, config: GeneratorConfiguration):
        super().__init__(yang_dir, out_dir, config)

    def generate_directories(self):
        pass

    def copy_files(self):
        pass

    def generate_files(self):
        pass
