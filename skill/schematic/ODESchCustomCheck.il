/*
wechat official account : edanote
github : https://github.com/edanote/ODE
lint score : 94(due to ODEsetting global variable)

*/

procedure(ODESchCustomCheck(@optional (cv geGetEditCellView()) )
prog((count err_text libName cellName)
    count = 0
    printf("checking denied device in schematic\n")
    foreach( inst cv~>instances
        libName = inst~>libName
        cellName = inst~>cellName
        if( member(libName ODEsetting["sch_deniedDev"]~>?) && member(cellName ODEsetting["sch_deniedDev"][libName]) then
            err_text = sprintf(nil "library : %s / cell : %s is not allow to use" libName cellName)
;            warn(err_text)
            geCreateMarker( inst "error" "ODE" err_text "aaa")
            count = count + 1
        )
    )
    return(count)
) ; end of prog
) ; end of procedure

schRegPostCheckTrigger('ODESchSanityCheck)
 
 
procedure( ODESchSanityCheck(@optional (cv geGetEditCellView()) nErr nWarn "dxx" )
     let(( nUserErr nUserWarn)
              nErr nWarn
              nUserErr = ODESchCustomCheck(cv)
              nUserWarn = 0
              schUpdateUserSRCErrorAndWarn( nUserErr nUserWarn )
          );let
) ;procedure ODESchSanityCheck
