/*
wechat official account : edanote
github : https://github.com/edanote/ODE
lint score : 100

*/


procedure(ODEplotHilight(coor layer)
let((cvId hlSetId)
    cvId = deGetEditCellView()
    hlSetId = geCreateHilightSet(cvId layer)
;    hlSetId = geCreateHilightSet(cvId '("y1" "drawing"))
    hlSetId->enable = t
    geAddHilightRectangle(hlSetId coor)
    geRefreshCellView(cvId)
    ;geDeleteAllHilightSet(cvId)
) ; end of let
) ; end of procedure

procedure(ODEclearHilight()
let((cvId)
    cvId = deGetEditCellView()
    geDeleteAllHilightSet(cvId)
    geRefreshCellView(cvId)
) ; end of let
) ; end of procedure

procedure(ODEclearHilightA(@key (hlSetId geCreateHilightSet(deGetEditCellView() '("y1" "drawing"))))
let(()
    geDeleteHilightSet(hlSetId)
    geRefreshCellView(deGetEditCellView())
) ; end of let
) ; end of procedure


