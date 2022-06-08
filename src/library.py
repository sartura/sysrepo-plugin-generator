import os


class CLibrary:
    def __init__(self, outdir, name):
        deps_dir = os.path.join(outdir, "deps")
        self.lib_dir = os.path.join(deps_dir, name)

    def generate_directories(self):
        pass

    def generate_files(self):
        pass

    def get_include_dirs(self):
        pass
