#!/usr/bin/env python3

import argparse
import sqlite3
import os
import sys
import re
import xlwt
from odementor.calibre.odePercRpt import odePercRptAnalysis

description = 'convert perc report to xls report'
args_parser = argparse.ArgumentParser(description=description)
args_parser.add_argument('-perc', type=str, nargs="?", required=True,
                         help='(REQUIRED) perc report file')

args = args_parser.parse_args()
percReportFile = args.perc

xlsFilePath = percReportFile.split(".", -1)[0] + ".xls"


odeCheckResult = odePercRptAnalysis(percReportFile)            



xlsFile = xlwt.Workbook(encoding='utf-8')
sheet_voltage_mark_full = xlsFile.add_sheet("voltage_mark")
# sheet_voltage_mark_max_min = xlsFile.add_sheet("voltage_mark_max_min")

green_back_ground = xlwt.Pattern()
green_back_ground.pattern = xlwt.Pattern.SOLID_PATTERN
green_back_ground.pattern_fore_colour = 5
green_style = xlwt.XFStyle()
green_style.pattern = green_back_ground

styleRedBkg = xlwt.easyxf('font: color-index red, bold on')
styleBlueBkg = xlwt.easyxf('font: color-index blue, bold on')

full_row = 0
full_col = 0
for netName in odeCheckResult["voltage_mark"].keys():
    for voltageType in odeCheckResult["voltage_mark"][netName].keys():
        oneNet = sorted(odeCheckResult["voltage_mark"][netName][voltageType].items(),key=lambda s:s[1])
        for mark in oneNet:
            instName = mark[0]
            voltage = mark[1]
            sheet_voltage_mark_full.write(full_row,full_col,netName)
            sheet_voltage_mark_full.write(full_row,full_col+1,voltageType)
            sheet_voltage_mark_full.write(full_row,full_col+2,instName)
            if voltageType == "vh" and voltage == oneNet[-1][1]:
                sheet_voltage_mark_full.write(full_row,full_col+3,voltage,styleRedBkg)
            elif voltageType == "vl" and voltage == oneNet[0][1]:
                sheet_voltage_mark_full.write(full_row,full_col+3,voltage,styleBlueBkg)
            else:
                sheet_voltage_mark_full.write(full_row,full_col+3,voltage)
            full_row = full_row + 1

    full_row = full_row + 1
xlsFile.save(xlsFilePath)
