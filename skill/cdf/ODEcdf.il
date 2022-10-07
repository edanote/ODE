/*
wechat official account : edanote
github : https://github.com/edanote/ODE
lint score : 76(due to global variable ODEsetting/cdfgForm)

*/

procedure(ODEFormInitProc(cdfDataId )
let((cellList forbidcellList libName cellName cdfId baseInitProc baseInitProcCmd)
    cdfId = cdfGetBaseCellCDF(cdfDataId~>id)
    baseInitProc = cdfId~>formInitProc
    baseInitProcCmd = strcat(baseInitProc "(cdfDataId)")
    printf("----- begin to run base formInitProc command -----\n")
    printf("base formInitProc command is : %s\n" baseInitProcCmd)
    evalstring(baseInitProcCmd)
    printf("----- end of run base formInitProc command -----\n")
    libName = cdfgForm->libraryName->value
    cellName = cdfgForm->cellName->value

    case(cdfgForm->_formName
        ("Add Instance"
         printf("\n Schematic: Create Instance scenario")
         ; check ODEsetting["sch_deniedDev"]
;         foreach(libName ODEsetting["sch_deniedDev"]~>?
            if(ODEsetting["sch_deniedDev"][libName] && member(cellName ODEsetting["sch_deniedDev"][libName]) then
                warn("Library:%s / Cell:%s are not allowd to use"
                libName cellName) ;warn
                cdfgForm->libraryName->value = libName
                cdfgForm->cellName->value = "" else nil
            ) ;if
;         ) ; end of foreach
         ) ; end of Add Instance case
    ) ; end of case
) ; end of let
) ; end of procedure


procedure(ODEUpdateFormInitProc()
let((cellId cdfId )
    if(ODEsetting["sch_deniedDev"] then
        foreach(libName ODEsetting["sch_deniedDev"]~>?
            foreach(cellName ODEsetting["sch_deniedDev"][libName]
            cellId=ddGetObj(libName cellName)
            if(cellId then
                if( cdfId = cdfGetUserCellCDF( cellId ) then
                    cdfId->formInitProc = "ODEFormInitProc"
                else
                    cdfId = cdfCreateUserCellCDF(cellId)
                
                    cdfCreateParam( cdfId
                        ?name           "ODEdummyName"
                        ?prompt         "ODEdummyParam"
                        ?defValue       "ODEdefault"
                        ?type           "string"
                        ?display        "nil"
                        ?editable       "nil"
                        ?parseAsCEL     "yes"
                    )
                    cdfId->formInitProc = "ODEFormInitProc"
                ) ;if
            ) ; end of if cellId
            ); foreach
        ) ; end of foreach ODEsetting["sch_deniedDev"]~>?
    ) ; end of if
) ;let
) ;procedure ODEUpdateFormInitProc

; from manual
; The user-defined SKILL function is passed a tag value of 'cv or 'CDF to indicate that a list of database IDs has been provided to the function for the cellview or CDF IDs, respectively.
; looks like ODERefreshTrigger will run many times in a single refresh

; tag is : cv
; goodList is : nil
; badList is : nil
; tag in case is : cv
; .. refreshed CDF for cell "gpdk045 nmos1v".
; .. refreshed CDF for cell "gpdk045 pdio".
; .. refreshed CDF for cell "gpdk045 pmos1v".
; tag is : cdf
; goodList is : (dd:0x2bd467a0 dd:0x2bd466e0 dd:0x2bd463b0)
; badList is : nil
; tag in case is : cdf

procedure(ODERefreshCB( tag goodList badList )
;    printf("tag is : %s\n" tag)
;    printf("goodList is : %L\n" goodList)
;    printf("badList is : %L\n" badList)
    case( tag
        ('cv
;            printf("tag in case is : %s\n" tag)
            foreach( cv goodList
                info("CV **** %s %s %s was refreshed\n" cv~>libName cv~>cellName cv~>viewName)
            ) ;foreach
            foreach( cv badList
                info("CV ==== %s %s %s failed to refresh\n" cv~>libName cv~>cellName cv~>viewName)
            ); foreach
        ) ;cv
        ('cdf
;            printf("tag in case is : %s\n" tag)
            ODEUpdateFormInitProc()
        )
        (t
            info("**** Received unknown refresh tag - %L\n" tag)
        ) ;t
    ) ; end of case tag

) ;procedure ODERefreshCB

ODEUpdateFormInitProc()
ddsRegPostRefreshTrigger( "ODERefreshCB" )
