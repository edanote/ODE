#!/usr/bin/env python3

import argparse
import os
import sys
import subprocess
from odementor.calibre.drc import get_drc_results,run_drc
from odecadence.virtuoso.trans import export_gds,import_gds
from odemisc.misc import rmandmkdir

# cv = dbOpenCellViewByType("test_lib" "createShape" "layout" "maskLayout" "a")


description = 'generate drc ascii results and plot in virtuoso by ipc'

args_parser = argparse.ArgumentParser( description=description)
args_parser.add_argument('-rule', type=str, nargs="?" , required=True,
                         help='(REQUIRED) calibre drc rule deck')
args_parser.add_argument('-resultdir', type=str, nargs="?" , required=True,
                         help='(REQUIRED) result dir')
args_parser.add_argument('-laylib', type=str, nargs="?", required=True,
                         help='(REQUIRED) virtuoso library name')
args_parser.add_argument('-laycell', type=str, nargs="?", required=True,
                         help='(REQUIRED) virtuoso cell name')
args_parser.add_argument('-layview', type=str, nargs="?", required=True,
                         help='(REQUIRED) virtuoso view name')
args_parser.add_argument('-laydepth', type=int, nargs="?", default=32767,
                         help='(OPTIONAL) gds depth to generate')
args = args_parser.parse_args()

rule_path = args.rule
pv_result_dir = args.resultdir
lay_lib_name = args.laylib
lay_cell_name = args.laycell
lay_view_name = args.layview
# pv_result_dir = os.getenv("PROJ_PV_RESULTS") + "/" +  "os.getenv("USER")"
hier_depth = args.laydepth


#rule_name = os.path.basename(rule_path)
#(rule_type,extension) = os.path.splitext(rule_name)
#if os.getenv("PROJ_PV_RESULTS_ROOT") :
#    proj_pv_results = os.getenv("PROJ_PV_RESULTS_ROOT")
#else:
#    proj_pv_results = "/tmp"
#pv_result_dir = f'{proj_pv_results}/{os.getenv("USER")}/{rule_type}/{cell_name}'

rmandmkdir(pv_result_dir)
export_gds(lay_lib_name,lay_cell_name,lay_view_name,pv_result_dir)
run_drc(lay_cell_name,rule_path,pv_result_dir)
#import_gds(lay_lib_name,gds_path,pv_result_dir)
generated_gds = list(filter(lambda x:x.endswith(".gds"),os.listdir(pv_result_dir)))
generated_gds = list(filter(lambda x:x != f"{lay_cell_name}.gds",generated_gds))
for gds in generated_gds:
    import_gds(lay_lib_name,gds,pv_result_dir)
    (status,top_cell) = subprocess.getstatusoutput(f"calibredrv -a puts [layout peek {pv_result_dir}/{gds} -topcell]")
    skill_inst=f'let((cv inst instAdd) cv=dbOpenCellViewByType("{lay_lib_name}" "{lay_cell_name}" "{lay_view_name}" "" "a") foreach(inst dbInstQuery(cv list(0:0 0:0) 0 0) if(inst~>cellName == "{top_cell}" dbDeleteObject(inst)))  instAdd=dbOpenCellViewByType("{lay_lib_name}" "{top_cell}" "layout") dbCreateInst(cv instAdd "IODE_{top_cell}" 0.0:0.0 "R0") dbSave(cv))'
    print(skill_inst,file=sys.stdout,flush=True)
