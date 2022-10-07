/*
wechat official account : edanote
github : https://github.com/edanote/ODE
lint score : 100

*/

procedure(ODECiwPullDownMenu()
let((ReloadODEenv checkODEenv numMenus ODEindexNum ciwMenus)

    ; with out this commmand,numMenus will be 0
    ; and ODE menu will not be inserted
    ciwMenuInit()

    ; create menu item
    ReloadODEenv = hiCreateMenuItem(
        ?name     'ReloadODEenv
        ?itemText "Reload ODE config"
        ?callback "ODEloadEnv()"
    )

    checkODEenv = hiCreateMenuItem(
        ?name     'checkODEenv
        ?itemText "Check ODE config"
        ?callback "ODECheckSetting()"
    )

    ; create pulldown menu
    hiCreateMenu(
        'ODEMenu
        "OD&E"
        list( ReloadODEenv checkODEenv)
    )

    ; delte ODE menu if exist
    ciwMenus = hiGetBannerMenus( hiGetCIWindow() )
    ODEindexNum = lindex(ciwMenus 'ODEMenu)
    if(ODEindexNum then 
        hiDeleteBannerMenu( hiGetCIWindow() ODEindexNum-1 )
    )

    ; insert ODE menu
    numMenus = hiGetNumMenus( hiGetCIWindow() )
    hiInsertBannerMenu( hiGetCIWindow() 'ODEMenu numMenus )
);let
);procedure

ODECiwPullDownMenu()
