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

    def __init__(self, prefix, outdir, modules, main_module, yang_dir):
        self.prefix = prefix
        self.outdir = outdir
        self.modules = modules
        self.main_module = main_module
        self.yang_dir = yang_dir

    def generate_directories(self):
        pass

    def copy_files(self):
        pass

    def generate_files(self):
        pass
