# -*- coding: utf-8 -*-
__author__ = "yangtao"


import os
import configparser




config_path = os.path.dirname(__file__).replace('\\', '/') + '/config.ini'
config_dict = {"SG": {"url":"",
                      "script_name":"",
                      "api_key":""}}

config = configparser.ConfigParser()


def generate_config(config_dict):
    # 创建 config 文件
    for sect in config_dict:
        config[sect] = config_dict[sect]
    with open(config_path, 'w') as configfile:
        config.write(configfile)


def read(section=None, value=None) -> dict:
    if not os.path.exists(config_path):
        generate_config(config_dict)

    config.read(config_path)
    if section and not value:
        value_dict = {}
        for v in config[section]:
            value_dict[v] = config[section][v]
        return value_dict
    elif section and value:
        return config[section][value]
    elif not section and value:
        raise ValueError("section is %s"%section)
    else:
        result = {}
        for sect in config:
            result[sect] = {}
            for v in config[sect]:
                result[sect][v] = config[sect][v]
        return result


def write(section, value):
    if not section:
        raise ValueError("section is %s" % section)

    config_dict = read()
    if section not in config_dict:
        config_dict[section] = {}

    if value:
        value_map = config_dict[section]
        for v in value:
            value_map[v.lower()] = value[v]

        config_dict[section] = value_map

    generate_config(config_dict)