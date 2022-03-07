
import os

def get_ode_template_path(tool):
    template_path = "/tmp"
    if tool == "virtuoso":
        template_path = f'{os.getenv("ODE_HOME")}/python/odecadence/virtuoso/template'
    if tool == "calibre":
        template_path = f'{os.getenv("ODE_HOME")}/python/odementor/calibre/template'
    return(template_path)
