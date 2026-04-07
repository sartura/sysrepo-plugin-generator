# sysrepo-plugin-generator
Sysrepo plugin generator based on main YANG modules used for the specific plugin.

## Dependencies
- libyang
- Jinja2

## Usage
Provide needed arguments for the script and run it to generate plugin directory code and structure.

```
$ python3 sysrepo-plugin-generator.py -h
usage: sysrepo-plugin-generator.py [-h] -d YANG_DIR -o OUT_DIR -c CONFIG -l LANG

Sysrepo plugin generator.

options:
  -h, --help            show this help message and exit
  -d YANG_DIR, --dir YANG_DIR
                        Directory containing all the yang modules.
  -o OUT_DIR, --outdir OUT_DIR
                        Output source directory to use.
  -c CONFIG, --config CONFIG
                        Configuration file to use for generation.
  -l LANG, --lang LANG  Destination language to generate to (C or C++).
```

## Example

Generate the ietf-system plugin using the provided YANG modules and configuration:

```
$ python3 src/sysrepo-plugin-generator.py -d yang -o generated/ietf-system -l C -c config/ietf-system.toml
```

Build the generated plugin:

```
$ cd generated/ietf-system
$ mkdir build && cd build
$ cmake ..
$ make -j
```

## Available plugins

The following plugin configurations are available in the `config/` folder:

| Config | YANG module |
|--------|-------------|
| `ietf-access-control.toml` | ietf-access-control-list |
| `ietf-dhcpv6-client.toml` | ietf-dhcpv6-client |
| `ietf-interfaces.toml` | ietf-interfaces |
| `ietf-routing.toml` | ietf-routing |
| `ietf-system.toml` | ietf-system |

Generate and build a specific plugin:

```
$ python3 src/sysrepo-plugin-generator.py -d yang -o generated/ietf-access-control -l C -c config/ietf-access-control.toml
$ python3 src/sysrepo-plugin-generator.py -d yang -o generated/ietf-dhcpv6-client -l C -c config/ietf-dhcpv6-client.toml
$ python3 src/sysrepo-plugin-generator.py -d yang -o generated/ietf-interfaces -l C -c config/ietf-interfaces.toml
$ python3 src/sysrepo-plugin-generator.py -d yang -o generated/ietf-routing -l C -c config/ietf-routing.toml
$ python3 src/sysrepo-plugin-generator.py -d yang -o generated/ietf-system -l C -c config/ietf-system.toml
```

Then build the generated plugin:

```
$ cd generated/<plugin-name>
$ mkdir build && cd build
$ cmake ..
$ make -j
```

Generate and build all plugins at once:

```
$ for cfg in config/*.toml; do
    name=$(basename "$cfg" .toml)
    mkdir -p "generated/$name"
    python3 src/sysrepo-plugin-generator.py -d yang -o "generated/$name" -l C -c "$cfg"
    cd "generated/$name" && mkdir -p build && cd build && cmake .. && make -j
    cd ../../..
  done
```

## Enabling YANG features in sysrepo

The generator enables all YANG features when generating plugin code. For the plugin to work correctly at runtime, the same features must be enabled in sysrepo. Otherwise, subscriptions to feature-gated paths (e.g. `/ietf-system:system/radius/server`) will fail with "not found" errors.

Enable all features for a module:

```
$ sudo sysrepoctl --change ietf-system --enable-feature '*'
```

Or enable specific features:

```
$ sudo sysrepoctl --change ietf-system --enable-feature radius --enable-feature authentication --enable-feature ntp
```

Check which features are currently enabled:

```
$ sysrepoctl -l | grep ietf-system
```

## Directory structure

The generator will produce the following source directory structure (the example is taken for the ietf-system plugin):

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
|   |-- types.h
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
  - `context.h` - context used throughout the plugin callbacks
  - `types.h` - types used in the plugin (common structures, enums and unions)
  - `ly_tree.(h|c)` - API for creating libyang tree nodes based on the main YANG module, here `ietf-system`

Other parts of the plugin include:
  - `plugin/api/` - the API for loading, storing and changing data on the system
  - `plugin/data/` - helper functions for types defined in `types.h` - example would be implementing `init()` and `free()` functionalities for a list of types - TODO
  - `plugin/startup/` - load and store functionalities for the startup datastore - initial load for startup when the plugin is first started, and constant store API for when the plugin starts up again so that the state is left unchanged
  - `plugin/subscription/` - change, operational and RPC/action callbacks, used in `plugin.c` file which subscribes all callbacks to their respective paths

`plugin/data/` and `plugin/api/` folders use separation based on the YANG containers - for each container one folder is used which enables easier navigation. In these folders, files can be separated based on more containers or lists etc.
