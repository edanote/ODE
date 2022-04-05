/*
wechat official account : edanote
github : https://github.com/edanote/ODE
lint score : 100

create pull down menu in layout/layoutXL

*/


procedure( ODECreateLayoutPulldownMenu()
;  if( boundp( 'ODELayoutPulldownMenu )
;     then ODELayoutPulldownMenu
;  else
    hiCreatePulldownMenu(
       'ODELayoutPulldownMenu
       "ODE"
       list(
          hiCreateMenuItem( ; list of menu items
             ?name 'ODEbutian
             ?itemText "butian"
             ?callback   "ODEbutian()"
;             ?callback   "ipcBeginProcess(\"/home/study/run.py\" \"\" 'ODEStdoutHandler 'ODEStderrHandler)"
            )
       ) ; list
    ) ; hiCreatePulldownMenu
;  ) ; if
) ; procedure
 
procedure( ODEPostInstallTrigger(args)
   hiInsertBannerMenu(
        args->window
        ODECreateLayoutPulldownMenu()
        length( hiGetBannerMenus( args->window))
   )
) ; procedure
 
;; Triggers for adding to Layout Suite L, XL, EXL window
deRegUserTriggers("maskLayout" nil nil 'ODEPostInstallTrigger)
deRegUserTriggers("maskLayoutXL" nil nil 'ODEPostInstallTrigger)
 
