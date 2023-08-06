# -*- coding: utf-8 -*-
import os
try:
    import ConfigParser as configparser
except:
    import configparser

# Check configuration files
Config = configparser.ConfigParser()
if len(Config.read(".airbridgerc")) == 0 and \
    len(Config.read(os.path.expanduser("~/.airbridgerc"))) == 0:
    raise Exception("No .airbridgerc file.")


def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

# TODO 필수 설정값들 받아서 없으면 raise Exception
engine_configs = ConfigSectionMap('ENGINE')

if 'USE_AIRBRIDGE_LOCAL_DB' in os.environ:
    engine_configs = ConfigSectionMap('ENGINE_LOCAL')
