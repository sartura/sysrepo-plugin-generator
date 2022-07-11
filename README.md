# sysrepo-plugin-generator
Sysrepo plugin generator based on main YANG modules used for the specific plugin.

## Dependencies
- libyang
- Jinja2

## Usage
Provide needed arguments for the script and run it to generate plugin directory code and structure.

Example for `ietf-system` YANG module:

```
$ python3 sysrepo-plugin-generator.py -h
usage: sysrepo-plugin-generator.py [-h] -p PREFIX -d DIR -m MODULES [MODULES ...] -M MAIN_MODULE -o OUTDIR

Sysrepo plugin generator.

optional arguments:
  -h, --help            show this help message and exit
  -p PREFIX, --prefix PREFIX
                        Provide prefix that will be used in the plugin generation.
  -d DIR, --dir DIR     Directory containing all the yang modules.
  -m MODULES [MODULES ...], --modules MODULES [MODULES ...]
                        YANG modules to use for plugin generation.
  -M MAIN_MODULE, --main-module MAIN_MODULE
                        Main YANG module to use for plugin generation.
  -o OUTDIR, --outdir OUTDIR
                        Output source directory to use.
```

## Directory structure

The generator will follow the following source directory structure (the example is taken for the ietf-system plugin):

```
|-- main.c
|-- plugin
|   |-- api
|   |   `-- system
|   |       |-- authentication
|   |       |   |-- change.c
|   |       |   |-- change.h
|   |       |   |-- check.c
|   |       |   |-- check.h
|   |       |   |-- load.c
|   |       |   |-- load.h
|   |       |   |-- store.c
|   |       |   `-- store.h
|   |       |-- change.c
|   |       |-- change.h
|   |       |-- check.c
|   |       |-- check.h
|   |       |-- clock
|   |       |   |-- change.c
|   |       |   |-- change.h
|   |       |   |-- check.c
|   |       |   |-- check.h
|   |       |   |-- load.c
|   |       |   |-- load.h
|   |       |   |-- store.c
|   |       |   `-- store.h
|   |       |-- dns-resolver
|   |       |   |-- change.c
|   |       |   |-- change.h
|   |       |   |-- check.c
|   |       |   |-- check.h
|   |       |   |-- load.c
|   |       |   |-- load.h
|   |       |   |-- options
|   |       |   |   |-- change.c
|   |       |   |   |-- change.h
|   |       |   |   |-- check.c
|   |       |   |   |-- check.h
|   |       |   |   |-- load.c
|   |       |   |   |-- load.h
|   |       |   |   |-- store.c
|   |       |   |   `-- store.h
|   |       |   |-- store.c
|   |       |   `-- store.h
|   |       |-- load.c
|   |       |-- load.h
|   |       |-- ntp
|   |       |   |-- change.c
|   |       |   |-- change.h
|   |       |   |-- check.c
|   |       |   |-- check.h
|   |       |   |-- load.c
|   |       |   |-- load.h
|   |       |   |-- store.c
|   |       |   `-- store.h
|   |       |-- radius
|   |       |   |-- change.c
|   |       |   |-- change.h
|   |       |   |-- check.c
|   |       |   |-- check.h
|   |       |   |-- load.c
|   |       |   |-- load.h
|   |       |   |-- options
|   |       |   |   |-- change.c
|   |       |   |   |-- change.h
|   |       |   |   |-- check.c
|   |       |   |   |-- check.h
|   |       |   |   |-- load.c
|   |       |   |   |-- load.h
|   |       |   |   |-- store.c
|   |       |   |   `-- store.h
|   |       |   |-- store.c
|   |       |   `-- store.h
|   |       |-- store.c
|   |       `-- store.h
|   |-- common.h
|   |-- context.h
|   |-- data
|   |-- ly_tree.c
|   |-- ly_tree.h
|   |-- startup
|   |   |-- load.c
|   |   |-- load.h
|   |   |-- store.c
|   |   `-- store.h
|   `-- subscription
|       |-- change.c
|       |-- change.h
|       |-- operational.c
|       |-- operational.h
|       |-- rpc.c
|       `-- rpc.h
|-- plugin.c
`-- plugin.h
```

The main files are:
  - `main.c` - plugin independent of `sysrepo-plugind`
  - `plugin.h` - init and cleanup plugin callbacks
  - `plugin.c` - init and cleanup implementation
  - `common.h` - YANG paths and other commonly used macros
  - `context.h` - used context throughout the plugin callbacks
  - `types.h` - used types in the plugin (common structures, enums and unions)
  - `ly_tree.(h|c)` - API for creating libyang tree nodes based on the main YANG module, here `ietf-system`

Other parts of the plugin include:
  - `plugin/api/` - the API for loading, storing and changing data on the system
  - `plugin/data/` - helper functions for types defined in `types.h` - example would be implementing `init()` and `free()` functionalities for a list of types - TODO
  - `plugin/startup/` - load and store functionalities for the startup datastore - initial load for startup when the plugin is first started and constant store API for when the plugin starts up again so that the state is left unchanged
  - `plugin/subscription/` - change, operational and RPC/action callbacks, used in `plugin.c` file which subscribes all callbacks to their respective paths

`plugin/data/` and `plugin/api/` folders use separation based on the YANG containers - for each container one folder is used which enables easier navigation. In these folders, files can be separated based on more containers or lists etc.

## TODO
- [x] support startup load and store generation
- [x] support subscription callbacks generation
- [x] add `--outdir` parameter support - setting output directory for C source and header generated files
- [x] support `ly_tree` API generation
- [x] support API generation for each node (load, store, check)
- [x] change `--outdir` to point to the root of the project, not the source folder as the current implementation
- [x] include uthash library for every plugin
- [x] generate CMakeLists.txt for the plugin
- [x] use clang-format to apply same code style to files
- [ ] support change API for each node
- [ ] include all store, load and check API files into startup files
- [ ] support types.h generation - generate C types based on libyang nodes
- [ ] support data code generation (optional for now)
- [x] support `augment` YANG nodes