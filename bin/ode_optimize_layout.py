#!/usr/bin/env python3

"""generate FILL rule from yaml config file
   github : https://github.com/edanote/ODE
   wechat official account(gongzhong hao) : edanote
"""

import yaml
import yamlordereddictloader
import re
from decimal import *
import argparse

args_parser = argparse.ArgumentParser(description="generate DFM FILL file according yaml file")
args_parser.add_argument('-y', type=str, required=True,dest="yaml_file",
                         help='(REQUIRED) yaml file')
args_parser.add_argument('-o', type=str, required=True,dest="output_file",
                         help='(REQUIRED) output file')
args = args_parser.parse_args()
yaml_file = args.yaml_file
output_file = args.output_file

seg_space = " "*4
seg_space2 = seg_space*2

def float_or_exit(upper_key,key,value):
    if not isinstance(value,float):
        print(f"{key} in {upper_key} is not a floating number")
        print(f"program exit")
        exit()

def int_or_exit(upper_key,key,value):
    if not isinstance(value,int):
        print(f"{key} in {upper_key} is not a int number")
        print(f"program exit")
        exit()

def gen_rule_deck_variable(layout_info):
    rule_deck_variable = ""
    if "signal" in layout_info.keys():
        power_ground = ""
        if "power" in layout_info["signal"]:
            power_name = f'"{layout_info["signal"]["power"]}"'
            power_name = re.sub(r"\s+","\" \"",f'{power_name}')
            rule_deck_variable = f'{rule_deck_variable}VARIABLE ODE_POWER {power_name}\n'
        else:
            print("keyword power must be specified in layout_info->signal")
            exit()
        if "ground" in layout_info["signal"]:
            ground_name = f'"{layout_info["signal"]["ground"]}"'
            ground_name = re.sub(r"\s+","\" \"",f'{ground_name}')
            rule_deck_variable = f'{rule_deck_variable}VARIABLE ODE_GROUND {ground_name}\n'
        else:
            print("keyword ground must be specified in layout_info->signal")
            exit()
    rule_deck_variable = f"{rule_deck_variable}VARIABLE ODE_POWER_GROUND {power_name} {ground_name}\n"
    if "rule_var" in layout_info.keys():
         for var in layout_info["rule_var"] :
             rule_deck_variable = f'{rule_deck_variable}VARIABLE {var} {layout_info["rule_var"][var]}\n'
    return(rule_deck_variable)

def gen_lu_layer(fill_name,fill):
    # generate lu layer
    if "lu_layer" not in fill.keys():
        print(f"key lu_layer not define in fills -> {fill_name}")
        exit()
    if "lower_layer" not in fill["lu_layer"].keys() or "upper_layer" not in fill["lu_layer"].keys():
        print(f"key lower_layer/upper_layer not define in fills -> {fill_name} -> lu_layer")
        exit()
    lower_layer = fill["lu_layer"]["lower_layer"]
    upper_layer = fill["lu_layer"]["upper_layer"]
#    print(f"{fill_name}_lu_shape =  AND {lower_layer} {upper_layer}")
    calibre_layer = f"{fill_name}_lu_shape"
    calibre_layer_operation = f"{calibre_layer} =  NET (AND {lower_layer} {upper_layer} CONNECTED) ODE_POWER_GROUND"
    return(calibre_layer,calibre_layer_operation)
    # end of generate lu layer

def gen_dfm_spec_fill_shape(fill_shape_name,fill_shape):
    dfm_spec_fill_shape = f"DFM SPEC FILL SHAPE {fill_shape_name}"
    if "viax" not in fill_shape.keys() or "viay" not in fill_shape.keys():
        print(f"key viax/viay not in {fill_shape_name}")
        exit()
    else:
#        float_or_exit(fill_shape_name,"viax",fill_shape["viax"])
#        float_or_exit(fill_shape_name,"viay",fill_shape["viay"])
#        viax = Decimal(str(fill_shape["viax"]))/Decimal('2')
#        viay = Decimal(str(fill_shape["viay"]))/Decimal('2')
#        viax = float(viax)
#        viay = float(viay)
        viax = fill_shape["viax"]
        viay = fill_shape["viay"]
        dfm_spec_fill_shape = f"{dfm_spec_fill_shape}\n{seg_space}RECTFILL (-{viax}/2) (-{viay}/2) {viax}/2 {viay}/2"
    if "stepx" not in fill_shape.keys() or "stepy" not in fill_shape.keys():
        print(f"key stepx/stepy not in {fill_shape_name}")
        exit()
    else:
#        float_or_exit(fill_shape_name,"stepx",fill_shape["stepx"])
#        float_or_exit(fill_shape_name,"stepy",fill_shape["stepy"])
        stepx = fill_shape["stepx"]
        stepy = fill_shape["stepy"]
        dfm_spec_fill_shape = f"{dfm_spec_fill_shape}\n{seg_space}STEP {stepx} {stepy}"
        if "as_is" in fill_shape.keys():
            for dfm_spec_fill_shape_option in fill_shape["as_is"]:
                for dfm_spec_fill_option_value in fill_shape["as_is"][dfm_spec_fill_shape_option]:
                    dfm_spec_fill_shape = f"{dfm_spec_fill_shape}\n{seg_space}{dfm_spec_fill_shape_option} {dfm_spec_fill_option_value}"
    return(dfm_spec_fill_shape)


with open(yaml_file,"r") as via_file:
    data = yaml.load(via_file, Loader=yamlordereddictloader.Loader)

with open(output_file,"w") as output_file:
    if "fill_definition" not in data.keys():
        print(f"key fill_definition not defined in yaml file")
        exit()

    # generate variable
    if "layout_info" in data.keys():
        rule_deck_variable = gen_rule_deck_variable(data["layout_info"])
        print(rule_deck_variable,file=output_file)
    # end of generage variable

    # generate net area

    # end of generate net area

    # generate DFM SPEC FILL SHAPE
    for via_group in data["fill_definition"].keys():
        if "fill_shapes" not in data["fill_definition"][via_group].keys():
            print(f"key fill_shapes not define in fill_definition -> {via_group}")
            exit()
        else:
            for fill_shape_name in data["fill_definition"][via_group]["fill_shapes"].keys():
                dfm_spec_fill_shape = gen_dfm_spec_fill_shape(fill_shape_name,data["fill_definition"][via_group]["fill_shapes"][fill_shape_name])
                print(dfm_spec_fill_shape,file=output_file)
        print("",file=output_file)
    # end of generate DFM SPEC FILL SHAPE

    print("",file=output_file)

    # generate DFM SPEC FILL
    if "fills" not in data.keys():
        print(f"key fills not defined in yaml file")
        exit()
    else:
        for fill_name in data["fills"]:
            calibre_layer,calibre_layer_operation = gen_lu_layer(fill_name,data["fills"][fill_name])
            print(calibre_layer_operation,file=output_file)
            dfm_spec_fill = f"DFM SPEC FILL {fill_name}"
            dfm_spec_fill = f"{dfm_spec_fill}\n{seg_space}INSIDE OF LAYER {calibre_layer}"
#            print(dfm_spec_fill)
            if "spec_fill" not in data["fills"][fill_name]:
                print(f"spec_fill not defined in fills -> {fill_name}")
                exit()
            else:
                for i in data["fills"][fill_name]["spec_fill"]:
                    dfm_spec_fill = f"{dfm_spec_fill}\n{seg_space}FILLSHAPE"
                    for j in i:
                        if j.startswith("FILLSHAPE_OPTION "):
                            dfm_spec_fill_option = j.replace("FILLSHAPE_OPTION ","")
                            dfm_spec_fill = f"{dfm_spec_fill}\n{seg_space2}{dfm_spec_fill_option}"
                        else:
                            if len(j.split()) != 2:
                                print(f"{j} musti be 2 word")
                                exit()
                            fill_shape_name = j.split()[1]
                            dfm_spec_fill = f"{dfm_spec_fill}\n{seg_space2}OUTPUT {fill_shape_name}_OUTPUT \"{fill_shape_name}\""
            print(dfm_spec_fill,file=output_file)
            print("",file=output_file)
    # end of generate DFM SPEC FILL

    # key is output layer name in rule deck
    # value is layer and purpose

    # generate output
    for fill_name in data["fills"]:
        output_layer_dict = dict()
        fill_group_dict = dict()
        for i in data["fills"][fill_name]["spec_fill"]:
            for j in i:
                fill_group,fill_shape_name = j.split()[0:2:1]
                fill_shape_name = f'{fill_shape_name}_OUTPUT'
                if not fill_group.startswith("FILLSHAPE_OPTION"):
                    if fill_group in fill_group_dict:
                        fill_group_dict[fill_group] = f"{fill_group_dict[fill_group]} {fill_shape_name}"
                    else:
                        fill_group_dict[fill_group] = fill_shape_name
#                print(fill_group)
#                print(fill_shape_name)
        for fill_group in fill_group_dict:
            output_layer = f"{fill_name}_{fill_group}"
            print(f"{output_layer} = DFM FILL {fill_name} {fill_group_dict[fill_group]}",file=output_file)
            output_layer_dict[output_layer] = f"{data['fill_definition'][fill_group]['gds_layer']['layer']} {data['fill_definition'][fill_group]['gds_layer']['purpose']}"
#            output_layer_dict[output_layer] = f"{data['fill_definition'][fill_group]['dfm_spec_fill']['layer']} {data['fill_definition'][fill_group]['gds_layer']['purpose']}"
#        print(output_layer_dict)
        fill_gds = ""
        for output_layer in output_layer_dict:
            fill_gds = f"{fill_gds}\n{seg_space}{output_layer} {output_layer_dict[output_layer]}"
        print(f"{fill_name} {{\n{seg_space}DFM RDB GDS output.gds{fill_gds}\n}}",file=output_file)
        print("",file=output_file)
    # end of generate output