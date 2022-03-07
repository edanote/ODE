
import os
import jinja2
from odemisc.odesetting import get_ode_template_path

def export_gds(lib_name,cell_name,view_name,pv_result_dir,hier_depth=32767):
#    virtuoso_template_dir = f'{os.getenv("ODE_HOME")}/python/odecadence/virtuoso/template'
    virtuoso_template_dir = get_ode_template_path("virtuoso")
#    print(virtuoso_template_dir)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(virtuoso_template_dir))
#    print(env)
    template = env.get_template('strmout_gds_template')
    strmout_gds_template_update = template.render(lib_name=lib_name,cell_name=cell_name,view_name=view_name,pv_result_dir=pv_result_dir,hier_depth=hier_depth)
#    print(strmout_gds_template_update)
#    print(pv_result_dir)
    strmout_gds_template_file_path = f"{pv_result_dir}/strmout_template"
    with open(strmout_gds_template_file_path,"w") as f:
        print(strmout_gds_template_update,file=f)
    status = os.system(f"strmout -templateFile {strmout_gds_template_file_path} >& {pv_result_dir}/cmd.log")

def import_gds(lib_name,gds_name,pv_result_dir):
    virtuoso_template_dir = get_ode_template_path("virtuoso")
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(virtuoso_template_dir))
    template = env.get_template('strmin_gds_template')
    strmin_gds_template_update = template.render(lib_name=lib_name,gds_name=gds_name,pv_result_dir=pv_result_dir)
    strmin_gds_template_file_path = f"{pv_result_dir}/strmin_template"
    with open(strmin_gds_template_file_path,"w") as f:
        print(strmin_gds_template_update,file=f)
    status = os.system(f"strmin -templateFile {strmin_gds_template_file_path} >& {pv_result_dir}/cmd.log")
    
