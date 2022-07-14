import argparse
from generator import Generator

# setup args
arg_parser = argparse.ArgumentParser(description="Sysrepo plugin generator.")
arg_parser.add_argument("-p", "--prefix", type=str, dest="prefix",
                        help="Provide prefix that will be used in the plugin generation.")
arg_parser.add_argument("-d", "--dir", type=str, dest="dir", required=True,
                        help="Directory containing all the yang modules.")
arg_parser.add_argument("-m", "--modules", type=str, dest="modules", required=True, nargs="+",
                        help="YANG modules to use for plugin generation.")
arg_parser.add_argument("-M", "--main-module", type=str, dest="main_module", required=True,
                        help="Main YANG module to use for plugin generation.")
arg_parser.add_argument("-o", "--outdir", type=str, dest="outdir", required=True,
                        help="Output source directory to use.")
args = arg_parser.parse_args()

# generate plugin structure
generator = Generator(args.prefix, args.outdir,
                      args.modules, args.main_module, args.dir)

# # generate directory structure
# generator.generate_directories()

# # generate all files
# generator.generate_files()
