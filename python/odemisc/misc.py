
import os
import shutil
import gdspy

def rmandmkdir(dir_path):
    if os.path.exists(dir_path) & os.path.isfile(dir_path):
        os.remove(dir_path)
    if os.path.exists(dir_path) & os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except :
            print(f"Error: directory {dir_path} create failed")
            exit()


def getfilerecursive(dir_path,suffix,no_top_file=True):
    """no_top_file False will not get files under dir_path
    But lower level files will get
    """
    full_path_files = []
    for root,dirs,files in os.walk(dir_path):
        for file_single in files:
            if (no_top_file and  os.path.samefile(root,dir_path)):
                pass
            else:
                full_path_files.append(os.path.join(root,file_single))
    return(list(filter(lambda x:x.endswith(suffix),full_path_files)))

def genrefgds(top_cell,cells_name,gds_related_path = "."):
#    lib = gdspy.GdsLibrary()
#    cell = lib.new_cell(top_cell)
##    for cell_name in cells_name:
##        cell1 = lib.new_cell(cell_name)
##        inst = gdspy.CellReference(cell1)
##        cell.add(inst,include_dependencies=True,overwrite_duplicate=True)
##        lib.remove(cell_name,remove_references=False)
#    cells = map(lambda x: lib.new_cell(x),cells_name)
#    cells_ref = map(lambda x: gdspy.CellReference(x),cells)
#    cell.add(cells_ref)
#    lib.write_gds(f'{gds_related_path}/{top_cell}.gds')
#    lib.remove(cells)
    lib = gdspy.GdsLibrary()
    print("lib name is :",lib)
    cell = gdspy.Cell(top_cell)   
    print("cell name is:",cell)
    cells = map(lambda x: lib.new_cell(x),cells_name)
    print("cells name is:",cells)
    print("cells name is:",list(cells))
    cells_ref = map(lambda x: gdspy.CellReference(x),cells)
    print("cells_ref name is:",cells_ref)
    print("cells_ref name is:",type(cells_ref))
    cell.add(cells_ref)
    lib.write_gds(f'{gds_related_path}/{top_cell}.gds')
