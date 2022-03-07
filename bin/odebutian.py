#!/usr/bin/env python3

import sys
import argparse
import json
from collections import OrderedDict
from odemisc.odepvgui import Pvgui
from PySide2.QtWidgets import (QWidget,QApplication,QVBoxLayout)


description = 'run calibre drc and stream gds to virtuoso'

args_parser = argparse.ArgumentParser( description=description)
#args_parser.add_argument('-json', type=str, nargs="?" , required=True,
#                         help='(REQUIRED) json file')
args_parser.add_argument('-laylib', type=str, nargs="?", required=True,
                         help='(REQUIRED) virtuoso library name')
args_parser.add_argument('-laycell', type=str, nargs="?", required=True,
                         help='(REQUIRED) virtuoso cell name')
args_parser.add_argument('-layview', type=str, nargs="?", required=True,
                         help='(REQUIRED) virtuoso view name')
args_parser.add_argument('-rule_dir', type=str, nargs="?", required=True,
                         help='(REQUIRED) rule path')
args_parser.add_argument('-result_dir', type=str, nargs="?", required=True,
                         help='(REQUIRED) result path')
args_parser.add_argument('-depth', type=int, nargs="?", default=32767,
                         help='(OPTIONAL) gds depth to generate')
args = args_parser.parse_args()

#json_file = args.json
lay_lib_name = args.laylib
lay_cell_name = args.laycell
lay_view_name = args.layview
rule_dir = args.rule_dir
result_dir = args.result_dir
# pv_result_dir = os.getenv("PROJ_PV_RESULTS") + "/" +  "os.getenv("USER")"
hier_depth = args.depth



app = QApplication(sys.argv)
#pvSource = "/home/study/foundry/process/metaloption/"
#pvDest = "/home/study/butianresults"
pvSource = rule_dir
pvDest = result_dir
gui = Pvgui(pvSource, pvDest,lay_lib_name,lay_cell_name,lay_view_name)
app.exec_()

