; create shape by coordinate number and layer name
; two coordinate is rectangle
; more than two coordinate is polygon

; ------------ example -------------------
; let((cv layer purpose coor)
;     cv = dbOpenCellViewByType("test_lib" "createShape" "layout" "maskLayout" "a")
;     layer = "Metal1"
;     purpose = "drawing"
;     coor = list(0:0 1:0 1:1)
;     ODECreateShape(cv layer purpose coor)
;     dbSave(cv)
;     dbClose(cv)
; )
; ------------ end of example -------------------

procedure( plot_drc_db_in_virtuoso(drc_rule)
let((cv libName cellName viewName pycmd )
    cv = hiGetCurrentWindow()
    libName = cv~>cellView~>libName
    cellName = cv~>cellView~>cellName
    viewName = cv~>cellView~>viewName
    pycmd = strcat("ode_plot_drc_db_in_virtuoso.py -rule " drc_rule " -lib " libName " -cell " cellName " -view " viewName)
;    println(pycmd)
    ipcBeginProcess(pycmd "" 'ODEStdoutHandler 'ODEStderrHandler)
) ; end of leg
) ; end of procedure

