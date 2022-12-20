from core.utils import CLibrary
import os
import shutil


class UTHashLibrary(CLibrary):
    def __init__(self, outdir):
        super().__init__(outdir, "uthash")

    def generate_directories(self):
        if not os.path.exists(self.lib_dir):
            os.mkdir(self.lib_dir)

    def generate_files(self):
        # copy files from deps/uthash/src
        uthash_source = "deps/uthash/src"

        for file in os.listdir(uthash_source):
            src_path = os.path.join(uthash_source, file)
            dst_path = os.path.join(self.lib_dir, file)

            shutil.copyfile(src_path, dst_path)

    def get_include_dirs(self):
        return [self.lib_dir]
