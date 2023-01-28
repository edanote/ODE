set Lnew [layout create]
$Lnew create cell {{top_cell}}

set gdslist [list {{gds_list}}]

foreach gds_path $gdslist {
    set gds_path_split [split $gds_path "/"]
    set gds_name [lindex $gds_path_split end]
    set gds_split [split $gds_name "."]
    set cell_name [lindex $gds_split 0]
    set Lone [layout create $gds_path -dt_expand]
    if {[$Lone topcell] != ""} {
        $Lone flatten cell [$Lone topcell]
        $Lnew create cell $cell_name $Lone [$Lone topcell]
        $Lnew create ref {{top_cell}} $cell_name 0 0 0 0 1
        $Lnew flatten cell {{top_cell}}
        $Lnew delete cell $cell_name
    }
}

if { {{flatten_cell}} } {
    $Lnew flatten cell {{top_cell}}
}

$Lnew units user {{drv_units_user}}
$Lnew units database {{drv_units_database}}

$Lnew gdsout {{top_cell}}.gds {{top_cell}}
