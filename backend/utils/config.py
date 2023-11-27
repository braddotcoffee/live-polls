import os
import yaml


class YAMLConfig:
    CONFIG = dict()
    with open(os.path.join(os.getcwd(), "config.yaml")) as config_file:
        CONFIG = yaml.safe_load(config_file)
