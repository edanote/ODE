#!/usr/bin/env python3

import os
import re



def odePercRptAnalysis(percReportFile):
    """ Analysis the perc report file generate by ODE script
    return dict"""

    if not os.path.isfile(percReportFile):
        print(f"perc report file {percReportFile} not exist")
        sys.exit(1)

    odeCheckResult = {}
    odeCheckResult["voltage_mark"] = {}
#    odeCheckResult["voltage_mark"]["vh"] = {}
#    odeCheckResult["voltage_mark"]["vl"] = {}

    with open(percReportFile, 'r') as percFileHandle:
        for line in percFileHandle:


            # ODE voltage mark vl XX1 on net net8 voltage is 0.0
            vlMatchObj = re.match(r"\s*ODE voltage mark (\S+) (\S+) on net (\S+) voltage is (\S+)", line)
            if vlMatchObj :
                voltageType = vlMatchObj.group(1)
                instName = vlMatchObj.group(2)
                netName = vlMatchObj.group(3)
                voltage = vlMatchObj.group(4)
                if netName not in odeCheckResult["voltage_mark"].keys():
                    odeCheckResult["voltage_mark"][netName] = {}
                if voltageType not in odeCheckResult["voltage_mark"][netName].keys():
                    odeCheckResult["voltage_mark"][netName][voltageType] = {}
                odeCheckResult["voltage_mark"][netName][voltageType][instName] = voltage

#                if voltageType not in odeCheckResult["voltage_mark"].keys():
#                    odeCheckResult["voltage_mark"][voltageType] = {}
#                if netName not in odeCheckResult["voltage_mark"][voltageType].keys():
#                    odeCheckResult["voltage_mark"][voltageType][netName] = {}
#                odeCheckResult["voltage_mark"][voltageType][netName][instName] = voltage

#            # ODE voltage mark vl XX1 on net net8 voltage is 0.0
#            vlMatchObj = re.match(r"\s*ODE voltage mark vl (\S+) on net (\S+) voltage is (\S+)", line)
#            if vlMatchObj :
#                instName = vlMatchObj.group(1)
#                netName = vlMatchObj.group(2)
#                voltage = vlMatchObj.group(3)
#                if netName not in odeCheckResult["voltage_mark"]["vl"].keys():
#                    odeCheckResult["voltage_mark"]["vl"][netName] = {}
#                odeCheckResult["voltage_mark"]["vl"][netName][instName] = voltage
#            # ODE voltage mark vh XX0 on net net8 voltage is 1.2
#            vhMatchObj = re.match(r"\s*ODE voltage mark vh (\S+) on net (\S+) voltage is (\S+)", line)
#            if vhMatchObj :
#                instName = vhMatchObj.group(1)
#                netName = vhMatchObj.group(2)
#                voltage = vhMatchObj.group(3)
#                if netName not in odeCheckResult["voltage_mark"]["vh"].keys():
#                    odeCheckResult["voltage_mark"]["vh"][netName] = {}
#                odeCheckResult["voltage_mark"]["vh"][netName][instName] = voltage

    return(odeCheckResult)
