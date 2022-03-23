layout create -type gds -handle L
L create cell {{top_cell}}

set cells { {{cell_list}} }
foreach cell $cells {
    L create ref {{top_cell}} $cell 0 0 0 0 1 -force
}

#L units user 0.0005
#L units database 5E-10

L units user {{drv_units_user}}
L units database {{drv_units_database}}

L gdsout {{top_cell}}.gds -depth 0
