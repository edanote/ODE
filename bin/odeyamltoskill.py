#!/usr/bin/env python3

"""
Author:         Chen Nan (github.com/edanote)
Created:        2022-09-13
Last Modified:  2022-09-13
Description:    A script that conver yaml file to skill format
How to use:     `-f` specifying the yaml file,
"""


import yaml
import copy
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="File.")
args = parser.parse_args()
yaml_file = args.file


def read_yaml(yaml_file):
    try:
        with open(yaml_file,encoding="utf-8") as f:
            data = yaml.load(f,Loader=yaml.FullLoader)
            return data
    except:
        return None

def python_value_to_skill_value(py_value):
    #py_list_temp = " ".join(list(map(lambda x: f'{x}',py_value)))
    if isinstance(py_value,list):
        skill_value = " ".join(map(lambda x:f'"{x}"' if type(x) is str else f'{x}', py_value))
        return f'\'({skill_value})'
    if isinstance(py_value,int):
        skill_value = py_value
        return f'{skill_value}'
    else:
        skill_value = py_value
        return f'\"{skill_value}"'
#    py_list_temp = " ".join(list(map(lambda x: f'"{x}"',py_value)))

yaml_contents = read_yaml(yaml_file)
#yaml_contents_list = " ".join(list(map(lambda x: f'"{x}"',yaml_contents["deniedDev"])))
#yaml_contents_skill = f'\'({yaml_contents_list})'

#yaml_contents_skill = python_list_to_skill_list(yaml_contents["deniedDev"])
#print(f'ODEsetting["schCheck"]["deniedDev"] = {yaml_contents_skill}')

def yaml_to_skill(yaml_contents,hier_level,cur_key):
    if type(yaml_contents) is dict:
        if cur_key:
            hier_level.append(cur_key)
        for key in yaml_contents.keys():
            yaml_to_skill(yaml_contents[key],copy.copy(hier_level),key )
    else:
        print(f'ODEsettingGen({python_value_to_skill_value(hier_level)},"{cur_key}",{python_value_to_skill_value(yaml_contents)})')

yaml_to_skill(yaml_contents,list(),"")
#print(yaml_contents)
#print(type(yaml_contents))
#print(type(yaml_contents) is dict )
#print(type(yaml_contents) == "dict")
