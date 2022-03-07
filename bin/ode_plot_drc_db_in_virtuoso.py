#!/usr/bin/env python3

import argparse
import os
import sys
from odementor.calibre.drc import get_drc_results,run_drc
from odecadence.virtuoso.trans import export_gds
from odemisc.misc import rmandmkdir

# cv = dbOpenCellViewByType("test_lib" "createShape" "layout" "maskLayout" "a")


description = 'generate drc ascii results and plot in virtuoso by ipc'

args_parser = argparse.ArgumentParser( description=description)
args_parser.add_argument('-rule', type=str, nargs="?" , required=True,
                         help='(REQUIRED) calibre drc rule deck')
args_parser.add_argument('-lib', type=str, nargs="?", required=True,
                         help='(REQUIRED) virtuoso library name')
args_parser.add_argument('-cell', type=str, nargs="?", required=True,
                         help='(REQUIRED) virtuoso cell name')
args_parser.add_argument('-view', type=str, nargs="?", required=True,
                         help='(REQUIRED) virtuoso view name')
args_parser.add_argument('-depth', type=int, nargs="?", default=32767,
                         help='(OPTIONAL) gds depth to generate')
args = args_parser.parse_args()

rule_path = args.rule
lib_name = args.lib
cell_name = args.cell
view_name = args.view
# pv_result_dir = os.getenv("PROJ_PV_RESULTS") + "/" +  "os.getenv("USER")"
hier_depth = args.depth


rule_name = os.path.basename(rule_path)
(rule_type,extension) = os.path.splitext(rule_name)
if os.getenv("PROJ_PV_RESULTS_ROOT") :
    proj_pv_results = os.getenv("PROJ_PV_RESULTS_ROOT")
else:
    proj_pv_results = "/tmp"
pv_result_dir = f'{proj_pv_results}/{os.getenv("USER")}/{rule_type}/{cell_name}'

rmandmkdir(pv_result_dir)
export_gds(lib_name,cell_name,view_name,pv_result_dir)
run_drc(cell_name,rule_path,pv_result_dir)

with open(f"{pv_result_dir}/{cell_name}.il","w") as f:
    print(f'cv = dbOpenCellViewByType("{lib_name}" "{cell_name}" "{view_name}" "maskLayout" "a")',file=f)
    drc_db=get_drc_results(f"{pv_result_dir}/{cell_name}.asc",sql=True)
    for rule_check in drc_db["db"]:
        (layer,purpose,gen_or_not) = rule_check.split("_",2)
        if gen_or_not.startswith("color"):
            color = "t"
        if gen_or_not.startswith("gen"):
            color = "nil"
        if gen_or_not.startswith(("gen","color")):
            for shape in drc_db["db"][rule_check]["points"]:
                coor = f'list({drc_db["db"][rule_check]["points"][shape]})'
                print(f'ODECreateShape(cv "{layer}" "{purpose}" {coor} ?color {color})',file=f)
    
    
    print("dbSave(cv)", file = f)
    print("dbClose(cv)",file = f)

print(f'load("{pv_result_dir}/{cell_name}.il")')
