import argparse
from target.c.generator import CGenerator
from target.cpp.generator import CPPGenerator

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
arg_parser.add_argument("-l", "--lang", type=str, dest="lang", required=True,
                        help="Destination language to generate to (C or C++).")
args = arg_parser.parse_args()

generator = None

# depending on the target language - choose which generator to use
if args.lang == "C":
    generator = CGenerator(args.prefix, args.outdir,
                           args.modules, args.main_module, args.dir)
elif args.lang == "C++":
    generator = CPPGenerator(args.prefix, args.outdir,
                             args.modules, args.main_module, args.dir)
else:
    print("Unsupported language: " + args.lang)
    exit(1)

# # generate project directory structure
# generator.generate_directories()

# # copy files which do not need generation
# generator.copy_files()

# # generate all project files
# generator.generate_files()
