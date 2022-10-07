#!/usr/bin/env python3

import argparse
import sqlite3
import os
import sys
import re

description = 'convert dspf file to sqlite for RC analysis'
args_parser = argparse.ArgumentParser(description=description)
args_parser.add_argument('-dspf', type=str, nargs="?", required=True,
                         help='(REQUIRED) dspf file')
args_parser.add_argument('-f', dest="overwrite", action="store_const", const=True,
                         default=False, help='force to over write existing sql file')

args = args_parser.parse_args()
dspfFile = args.dspf
forceOverwrite = args.overwrite

sqlFile = dspfFile.split(".", -1)[0] + ".sqlite"
DELIMITER = ":"


def cap_value(value: str) -> float:
    if value.endswith("f"):
#        value = float(value[0:-1]) * 1e-12
        value = value.strip("f")
    else:
        value = float(value)*1e12
    return value


def parseNodeName(node: str) -> list:
    nodeSplite = node.split(":")
    if len(nodeSplite) > 1:
        (net, netSeg) = nodeSplite
    else:
        net = nodeSplite[0]
        netSeg = ""
    return (net, netSeg)


netList = []


def parseCap(capLine: str, c) -> list:
    (capInst, nodeA, nodeB, capVal) = capLine.split(None, 4)[0:4]
    (netA, segA) = parseNodeName(nodeA)
    (netB, segB) = parseNodeName(nodeB)
    capVal = cap_value(capVal)
    c.execute(f'INSERT INTO TC (RCTYPE,NETA,SEGA,NETB,SEGB,VALUE) VALUES ("c",?,?,?,?,?)',
              (netA, segA, netB, segB, capVal))
    for net in (netA,netB):
        if net not in netList :
            netList.append(net)
#            print(netList)
#            print(net)
            c.execute(f"INSERT INTO TNETNAME (NETNAME) VALUES ('{net}')")

#   avoide duplicate net by sqlite
#    for net in (netA, netB):
#        c.execute(
#            f"INSERT INTO TNETNAME(NETNAME) SELECT '{net}' WHERE NOT EXISTS(SELECT 1 FROM TNETNAME WHERE NETNAME = '{net}')")
        # if net uniq check in python,run time will improve?
        # c.execute(f"INSERT OR IGNORE INTO TNETNAME (NETNAME) VALUES ('{net}')" )


def parseRes(resLine: str, c) -> list:
    (resInst, nodeA, nodeB, resVal, resVal, resPar) = resLine.split(None, 5)
    (netA, segA) = parseNodeName(nodeA)
    (netB, segB) = parseNodeName(nodeB)
    layer = layerMap[getRCpar(resPar, "lvl")]
    llx = getRCpar(resPar, "llx")
    lly = getRCpar(resPar, "lly")
    urx = getRCpar(resPar, "urx")
    ury = getRCpar(resPar, "ury")
    coor = f'{llx}:{lly} {urx}:{ury}'
    w = getRCpar(resPar, "w")
    l = getRCpar(resPar, "l")
    c.execute(f'INSERT INTO TR (RCTYPE,NETA,SEGA,NETB,SEGB,VALUE,LAYER,COOR,RW,RL) VALUES ("r",?,?,?,?,?,?,?,?,?)',
              (netA, segA, netB, segB, resVal, layer, coor, w, l))


def getRCpar(par: str, parKey: str):
    val = ""
    searchObj = re.search(f'{parKey}=(\S+)', par)
    if searchObj:
        val = searchObj.group(1)
    return (val)


if os.path.isfile(dspfFile):
    dspfFileTime = os.path.getmtime(dspfFile)
else:
    print(f"dspf file {dspfFile} not exist")
    sys.exit(1)

autoOverwrite = False
if os.path.isfile(sqlFile):
    sqlFileTime = os.path.getmtime(sqlFile)
    if dspfFileTime > sqlFileTime:
        autoOverwrite = True
else:
    autoOverwrite = True

if forceOverwrite or autoOverwrite:
    if os.path.isfile(sqlFile):
        os.remove(sqlFile)
    conn = sqlite3.connect(sqlFile)
    print("create database")
    c = conn.cursor()
    c.execute('''CREATE TABLE TNETNAME
           (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
           NETNAME         TEXT
           );''')
    #       UNIQUE(NETNAME));''')
    print("create table net name")
    c.execute('''CREATE TABLE TR
           (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
           RCTYPE     CHAR(1),
           NETA       TEXT,
           SEGA       INT(8),
           NETB       TEXT,
           SEGB       INT(8),
           RW         REAL,
           RL         REAL,
           VALUE      REAL,
           LAYER      TEXT,
           COOR       TEXT);''')
    c.execute('''CREATE TABLE TC
           (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
           RCTYPE     CHAR(1),
           NETA       TEXT,
           SEGA       INT(8),
           NETB       TEXT,
           SEGB       INT(8),
           RW         REAL,
           RL         REAL,
           VALUE      REAL,
           LAYER      TEXT,
           COOR       TEXT);''')
    print("create table rc")

    # c.execute("INSERT OR IGNORE INTO TNETNAME (NETNAME) \
    #      VALUES ('neta')")
    line_cache = ""
    lineFull = ""

    with open(dspfFile, 'r') as dspfFileHandle:
        #        line = dspfFileHandle.readline()
        #        while line:
        layerMap = {}
        for line in dspfFileHandle:
            line = line.rstrip("\n")
            if line.startswith("*"):
                if line.startswith("*|DELIMITER"):
                    DELIMITER = line.split()[1]
                if re.match("\*[0-9]", line):
                    (key, value) = line.lstrip("*").split()[0:2]
                    layerMap[key] = value
            else:
                if line.startswith("+"):
                    line = line.lstrip("+")
                    lineFull = f'{lineFull} {line}'
                else:
                    #                    print(lineFull)
                    if lineFull.startswith(("c", "C")):
                        parseCap(lineFull, c)
                    if lineFull.startswith(("r", "R")):
                        parseRes(lineFull, c)
                    lineFull = line
            #        if not line.startswith("+"):
            #            print(line_cache)
            #            line_cache = line.rstrip()
            #        if line.startswith("+"):
            #            line = line.rstrip()
            #            line = line.lstrip("+")
            #            line_cache = f'{line_cache} {line}'

            #        if line.startswith(("c","C")):
            #            (temp,netASeg,netBSeg,capValue) = line.split()[0:4]
            #            if re.search(DELIMITER,netASeg):
            #                (netA,SegA) = netASeg.split(DELIMITER)
            #            else:
            #                 netA = netASeg
            #                 SegA = ""
            #            if re.search(DELIMITER,netBSeg):
            #                (netB,SegB) = netBSeg.split(DELIMITER)
            #            else:
            #                 netB = netBSeg
            #                 SegB = ""
            #            capValue = cap_value(capValue)
            #            c.execute(f'INSERT INTO TRC (RCTYPE,NETA,SEGA,NETB,SEGB,VALUE) VALUES ("c",?,?,?,?,?)' ,(netA,SegA,netB,SegB,capValue))
            #            for net in (netA,netB):
            #                c.execute(f"INSERT INTO TNETNAME(NETNAME) SELECT '{net}' WHERE NOT EXISTS(SELECT 1 FROM TNETNAME WHERE NETNAME = '{net}')" )
            ##                if net uniq check in python,run time will improve?
            ##                c.execute(f"INSERT OR IGNORE INTO TNETNAME (NETNAME) VALUES ('{net}')" )
            #        if line.startswith(("r","R")):
            #            print(line)
            #            rline = line.replace("\n","")
            #            lastPos = dspfFileHandle.tell()
            #            while( dspfFileHandle.readline )

    #            line = dspfFileHandle.readline()

    conn.commit()
    conn.close()

#print(layerMap)
#print(DELIMITER)
