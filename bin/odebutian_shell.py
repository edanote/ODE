#!/usr/bin/env python3

import argparse
import os
import sys
import subprocess
from decimal import *
from odementor.calibre.drc import get_drc_results,run_calibre_drc,calibredrv_gen_emptyref_gds,calibredrv_merge_gds
from odecadence.virtuoso.trans import export_gds,import_gds
from odemisc.misc import rmandmkdir,getfilerecursive

# cv = dbOpenCellViewByType("test_lib" "createShape" "layout" "maskLayout" "a")


description = 'generate drc ascii results and plot in virtuoso by ipc'

args_parser = argparse.ArgumentParser( description=description)
args_parser.add_argument('-checktype', type=str, nargs="?" , required=True,
                         help='(REQUIRED) run type,can be drc/lvs/xrc/perc/butian')
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
args_parser.add_argument('-core', type=int, nargs="?", default=4,
                         help='(OPTIONAL) core number')
args = args_parser.parse_args()

basic_check_type = args.checktype
rule_path = args.rule
pv_result_dir = args.resultdir
lay_lib_name = args.laylib
lay_cell_name = args.laycell
lay_view_name = args.layview
# pv_result_dir = os.getenv("PROJ_PV_RESULTS") + "/" +  "os.getenv("USER")"
hier_depth = args.laydepth
core_num = args.core


#rule_name = os.path.basename(rule_path)
#(rule_type,extension) = os.path.splitext(rule_name)
#if os.getenv("PROJ_PV_RESULTS_ROOT") :
#    proj_pv_results = os.getenv("PROJ_PV_RESULTS_ROOT")
#else:
#    proj_pv_results = "/tmp"
#pv_result_dir = f'{proj_pv_results}/{os.getenv("USER")}/{rule_type}/{cell_name}'

rmandmkdir(pv_result_dir)
export_gds(lay_lib_name,lay_cell_name,lay_view_name,pv_result_dir)
if basic_check_type == "butian":
    org_gds_path = f'{pv_result_dir}/{lay_cell_name}.gds'
    org_gds_precision = subprocess.getstatusoutput(f'calibredrv -a "puts [layout peek {org_gds_path} -precision]"')[1]
#    print("org_gds_precision is",org_gds_precision)
    drv_units_database = Decimal("1e-6")/Decimal(org_gds_precision)
    drv_units_user = Decimal("1")/Decimal(org_gds_precision)
    rules = list(filter(lambda x:x.endswith(".rule"),os.listdir(rule_path)))
    rules.sort()
#    ode_cell_name = os.path.basename(rule_path.rstrip("/"))
    fix_name = rule_path.rstrip("/").split("/")[-2]
    ode_cell_name = f'{lay_cell_name}_{fix_name}_ode'
    ode_gds_path = f'{pv_result_dir}/{ode_cell_name}.gds'
    for rule in rules:
        rule_name = rule.split(".")[0]
        iter_rundir = f'{pv_result_dir}/{rule_name}'
        iter_cell_name = f'{lay_cell_name}_{rule_name}_ode'
        iter_gds_path = f'{pv_result_dir}/{iter_cell_name}.gds'
        rmandmkdir(iter_rundir)

        # generate empty top gds
        gds_path_list = getfilerecursive(pv_result_dir,".gds",no_top_file=True)
        gds_path_list.append(org_gds_path)
        gds_cellname_list = list(map(lambda x: subprocess.getstatusoutput(f'calibredrv -a puts [layout peek {x} -topcell]')[1],gds_path_list))
        calibredrv_gen_emptyref_gds(pv_result_dir,iter_cell_name," ".join(gds_cellname_list),gds_precision=org_gds_precision)
        # end of generate empty top gds

        gds_path_list.append(iter_gds_path)
        gds_path_list = map(lambda x: f'"{x}"',gds_path_list)
        run_calibre_drc(iter_cell_name,f'{rule_path}/{rule}',iter_rundir," ".join(gds_path_list),core_num=core_num)
#    gds_path_list = getfilerecursive(pv_result_dir,".gds",no_top_file=True)
#    gds_cellname_list = list(map(lambda x: subprocess.getstatusoutput(f'calibredrv -a puts [layout peek {x} -topcell]')[1],gds_path_list))
#    gds_cellname_list.append(f'{lay_cell_name}')
#    calibredrv_gen_emptyref_gds(pv_result_dir,f'{ode_cell_name}_raw'," ".join(gds_cellname_list),gds_precision=org_gds_precision)

    gds_path_list = getfilerecursive(pv_result_dir,".gds",no_top_file=True)
    gds_path_list = " ".join(gds_path_list)
    calibredrv_merge_gds(pv_result_dir,ode_cell_name,gds_path_list,gds_precision=org_gds_precision,flatten_cell="True")
        
    import_gds(lay_lib_name,ode_gds_path,pv_result_dir)
    skill_inst = f'ODEAddInst("{lay_lib_name}" "{lay_cell_name}" "layout" "{lay_lib_name}" "{ode_cell_name}" "layout" ?prompt t)'
    print(skill_inst,file=sys.stdout,flush=True)

##import_gds(lay_lib_name,gds_path,pv_result_dir)
#generated_gds = list(filter(lambda x:x.endswith(".gds"),os.listdir(pv_result_dir)))
#generated_gds = list(filter(lambda x:x != f"{ode_cell_name}.gds",generated_gds))
#for gds in generated_gds:
#    import_gds(lay_lib_name,gds,pv_result_dir)
#    (status,top_cell) = subprocess.getstatusoutput(f"calibredrv -a puts [layout peek {pv_result_dir}/{gds} -topcell]")
#    skill_inst=f'ODEAddInst({lay_lib_name} {ode_cell_name} "layout" {lay_lib_name} top_cell "layout")'
#    print(skill_inst,file=sys.stdout,flush=True)
