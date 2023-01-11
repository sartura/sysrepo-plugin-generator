import argparse
from core.config import GeneratorConfiguration
from target.c.generator import CGenerator
from target.cpp.generator import CPPGenerator

import toml

# setup args
arg_parser = argparse.ArgumentParser(description="Sysrepo plugin generator.")
arg_parser.add_argument("-d", "--dir", type=str, dest="yang_dir", required=True,
                        help="Directory containing all the yang modules.")
arg_parser.add_argument("-o", "--outdir", type=str, dest="out_dir", required=True,
                        help="Output source directory to use.")
arg_parser.add_argument("-c", "--config", type=str, dest="config", required=True,
                        help="Configuration file to use for generation.")
arg_parser.add_argument("-l", "--lang", type=str, dest="lang", required=True,
                        help="Destination language to generate to (C or C++).")
args = arg_parser.parse_args()

data = toml.load(args.config)

generator = None

config = GeneratorConfiguration(data)

# depending on the target language - choose which generator to use
if args.lang == "C":
    generator = CGenerator(args.yang_dir, args.out_dir, config)
elif args.lang == "C++":
    generator = CPPGenerator(args.yang_dir, args.out_dir, config)
else:
    print("Unsupported language: " + args.lang)
    exit(1)

# # generate project directory structure
# generator.generate_directories()

# # copy files which do not need generation
# generator.copy_files()

# # generate all project files
# generator.generate_files()
