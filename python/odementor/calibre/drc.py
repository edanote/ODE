
import os
import sys
import re
import sqlite3
import jinja2
from decimal import *
from odemisc.odesetting import get_ode_template_path

def calibredrv_gen_emptyref_gds(pv_result_dir,top_cell,ref_cells,gds_precision="1000"):
    drv_units_database = Decimal("1e-6")/Decimal(gds_precision)
    drv_units_user = Decimal("1")/Decimal(gds_precision)
    calibre_template_dir = get_ode_template_path("calibre")
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(calibre_template_dir))
    template = env.get_template('calibredrv_refcell_template.tcl')
    calibredrv_template = template.render(top_cell = top_cell,cell_list = ref_cells,drv_units_user=drv_units_user,drv_units_database=drv_units_database)
    with open(f"{pv_result_dir}/{top_cell}_drv.tcl","w") as f:
        print(calibredrv_template,file=f)
    status = os.system(f"cd {pv_result_dir};calibredrv {top_cell}_drv.tcl >& {top_cell}_drv.log")

def calibredrv_merge_gds(pv_result_dir,top_cell,gds_path_list,gds_precision="1000",flatten_cell="False"):
    drv_units_database = Decimal("1e-6")/Decimal(gds_precision)
    drv_units_user = Decimal("1")/Decimal(gds_precision)
    calibre_template_dir = get_ode_template_path("calibre")
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(calibre_template_dir))
    template = env.get_template('calibredrv_combile_gds.tcl')
    calibredrv_template = template.render(top_cell = top_cell,gds_list = gds_path_list,drv_units_user=drv_units_user,drv_units_database=drv_units_database,flatten_cell=flatten_cell)
    with open(f"{pv_result_dir}/{top_cell}_drv.tcl","w") as f:
        print(calibredrv_template,file=f)
    status = os.system(f"cd {pv_result_dir};calibredrv {top_cell}_drv.tcl >& {top_cell}_drv.log")

def run_calibre_drc(cell_name,rule_path,pv_result_dir,gds_path,core_num=4):
    calibre_template_dir = get_ode_template_path("calibre")
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(calibre_template_dir))
    template = env.get_template('drc_template')
    drc_template_update = template.render(cell_name=cell_name,rule_path=rule_path,gds_path=gds_path)
    with open(f"{pv_result_dir}/{cell_name}.drc","w") as f:
        print(drc_template_update,file=f)
    status = os.system(f"cd {pv_result_dir};calibre -drc -hier -turbo {core_num} {cell_name}.drc >& {cell_name}.log")

def get_drc_results(drc_db_file,var = True,sql = False):
    """ parse drc results
    return drc db coordinate or generate sql database
    if var is set, will return as dictionary variable
    if sql is set, will generate sql database
    """
    sql_file = drc_db_file + ".sql"
    if sql:
        if os.path.exists(sql_file):
            os.remove(sql_file)  
        conn = sqlite3.connect(sql_file)
        c = conn.cursor()
        c.execute('''CREATE TABLE TCOOR
               (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
               RULECHECK            TEXT,
               COORDINATE         TEXT
               );''')
        c.execute('''CREATE TABLE TRULECOMMENT
               (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
               RULECHECK            TEXT,
               COMMENT         TEXT
               );''')
        c.execute('''CREATE TABLE TMISC
               (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
               TOP            TEXT,
               PRECISION         TEXT
               );''')
    drcDict = {}
    with open(drc_db_file, "r") as fDB:
        (topName,precision) = fDB.readline().replace("\n","").split()
        if sql:
            c.execute(f'INSERT INTO TMISC (TOP,PRECISION) VALUES (?,?)' ,(topName,precision))
        if var:
            drcDict["misc"] = {}
            drcDict["misc"]["top"] = topName
            drcDict["misc"]["precision"] = precision
            drcDict["db"] = {}
        line = fDB.readline()
        while(line):
            # match rule check name
            # AA
            matchObj = re.match("^(\S+)$",line)
            if matchObj:
                ruleCheck = matchObj.group(1)
                drcDict["db"][ruleCheck] = {}
            # match rule check comments
            # 0 0 2 Jan 26 20:03:36 2022
            matchObj = re.match("^(\d+)\s+(\d+)\s+(\d+)\s+(\S+)\s+(\d+)\s+(\S+)\s+(\d+)\s*$",line)
            if matchObj:
                drcItemCount = matchObj.group(1)
                text_line_count = int(matchObj.group(3))
                drcDict["db"][ruleCheck]["text"] = ""
                drcDict["db"][ruleCheck]["points"] = {}
                tmp = ""
                while(text_line_count > 0):
#                    drcDict["db"][ruleCheck]["text"] = drcDict["db"][ruleCheck]["text"] + fDB.readline()
                    tmp = f"{tmp} {fDB.readline()}"
                    text_line_count = text_line_count - 1
                if sql:
#                    c.execute(f'INSERT INTO TRULECOMMENT (RULECHECK,COMMENT) VALUES (?,?)' ,(ruleCheck,drcDict["db"][ruleCheck]["text"]))
                    c.execute(f'INSERT INTO TRULECOMMENT (RULECHECK,COMMENT) VALUES (?,?)' ,(ruleCheck,tmp))
                if var:
                   drcDict["db"][ruleCheck]["text"] = tmp
            # match drc results
            # p 1 4
            matchObj = re.match("^(\S)\s+(\d+)\s+(\d+)$",line)
            if matchObj:
                drcOrgNum = str(matchObj.group(2))
                text_line_count = int(matchObj.group(3))
                tmp = ""
                while(text_line_count > 0):
                    next_line = fDB.readline().replace("\n","")
                    coor_list = []
                    for coor in next_line.split():
                        coor_list.append(str(int(coor)/int(precision)))
                    tmp = f'{tmp} {":".join(coor_list)}'
                    text_line_count = text_line_count - 1
                tmp = tmp.lstrip()
                if sql:
#                    c.execute(f'INSERT INTO TCOOR (RULECHECK,COORDINATE) VALUES (?,?)' ,(ruleCheck,drcDict[ruleCheck]["points"][drcOrgNum]))
                    c.execute(f'INSERT INTO TCOOR (RULECHECK,COORDINATE) VALUES (?,?)' ,(ruleCheck,tmp))
                if var:
                    drcDict["db"][ruleCheck]["points"][drcOrgNum] = tmp
                
    
            line = fDB.readline()
    if sql:
        conn.commit()
        conn.close()

    return(drcDict)
