from typing import Dict, Any, List, Optional


class YangModulesConfiguration:
    main_module: str
    other_modules: List[str] = []
    features: Optional[List[str]] = None

    def __init__(self, config: Dict[str, Any]) -> None:
        assert ("main" in config)

        self.main_module = config["main"]

        if "other" in config:
            self.other_modules = config["other"]

        if "features" in config:
            self.features = config["features"]

    def get_main_module(self) -> str:
        return self.main_module

    def get_other_modules(self) -> List[str]:
        return self.other_modules

    def get_features(self) -> Optional[List[str]]:
        return self.features


class YangPrefixConfiguration:
    cfg: Dict[str, str]

    def __init__(self, config: Dict[str, Any]) -> None:
        self.cfg = config

    def check_prefix(self, prefix: str) -> bool:
        if prefix in self.cfg:
            return True
        return False

    def get_prefix_value(self, prefix: str) -> str:
        return self.cfg[prefix]


class YangTypesConfiguration:
    types_map: Dict[str, str]

    def __init__(self, config: Dict[str, Any]) -> None:
        self.types_map = config

    def get_types_map(self) -> Dict[str, str]:
        return self.types_map


class YangConfiguration:
    mod_cfg: YangModulesConfiguration
    types_cfg: YangTypesConfiguration
    prefix_cfg: YangPrefixConfiguration

    def __init__(self, config: Dict[str, Any]):
        self.mod_cfg = YangModulesConfiguration(config["modules"])
        self.types_cfg = YangTypesConfiguration(config["types"])
        self.prefix_cfg = YangPrefixConfiguration(config["prefix"])

    def get_modules_configuration(self) -> YangModulesConfiguration:
        return self.mod_cfg

    def get_types_configuration(self) -> YangTypesConfiguration:
        return self.types_cfg

    def get_prefix_configuration(self) -> YangPrefixConfiguration:
        return self.prefix_cfg


class GeneratorConfiguration:
    prefix: str
    yang_cfg: YangConfiguration

    def __init__(self, config: Dict[str, Any]):
        self.prefix = config["generator"]["prefix"]
        self.yang_cfg = YangConfiguration(config["yang"])

    def get_prefix(self) -> str:
        return self.prefix

    def get_yang_configuration(self) -> YangConfiguration:
        return self.yang_cfg
