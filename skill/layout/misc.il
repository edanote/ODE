/*
wechat official account : edanote
github : https://github.com/edanote/ODE
lint score : 100

*/


procedure(ODEAddInst(libName cellName viewName extraLib extraCell extraView @key (prompt nil))
let((cv instAdd)
    cv=dbOpenCellViewByType(libName cellName viewName "" "a")
    foreach(inst dbInstQuery(cv list(0:0 0:0) 0 0)
        if(inst~>cellName == extraCell dbDeleteObject(inst))
    )
    instAdd=dbOpenCellViewByType(extraLib extraCell extraView)
    dbCreateInst(cv instAdd strcat("IODE_" extraCell) 0.0:0.0 "R0")
    dbSave(cv)
    if(prompt then
        ODEMessageDialog(strcat("instance add to " libName "/" cellName "/" viewName))
        dbRefreshCellView(instAdd)
        dbRefreshCellView(cv)
    )
    dbClose(cv)
    dbClose(instAdd)
) ; end of let
) ; end of procedure

procedure( ODEMessageDialog( string_text )
prog( ()
        hiDisplayAppDBox(       
                ?name           gensym( 'TrDialogBox )
                ?dboxBanner     "ODE Info"                   
                ?dboxText       string_text
                ?dialogType     hicErrorDialog                  
                ?dialogStyle    'modal                          
                ?buttonLayout   'Close
        )
) ; end prog
) ; end procedure mgcMessageDialog

