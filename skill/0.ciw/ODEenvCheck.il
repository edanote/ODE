/*
wechat official account : edanote
github : https://github.com/edanote/ODE
lint score : 72(due to global variable ODEsetting)

*/

procedure(ODEsettingGen(hier,key,value)
let((temp_point)
    temp_point = ODEsetting
    foreach(hier_key hier
        unless( member(hier_key temp_point~>?)
            temp_point[hier_key] = makeTable("table" 0)
        )
        temp_point = temp_point[hier_key]
    )
    temp_point[key] = value
) ; end of let
) ; end of procedure

; procedure(ODEsettingGen(key,value)
; let(()
;     if(! boundp('ODEsetting) then
;         ODEsetting = makeTable("ODEvar" 0)
;     )
;         ODEsetting[key] = value
; ) ; end of let
; ) ; end of procedure


procedure(ODEloadEnv()
let((ode_proj_setting_dir childPID ipcReturnCmd yaml_file)

    ODEsetting = makeTable("ODEvar" nil)
;    ODEsetting["schCheck"] = makeTable("schCheck" 0)
    
    
    ode_proj_setting_dir = getShellEnvVar("ODE_PROJ_SETTING_DIR")
    if( ! ode_proj_setting_dir then
        fprintf(woport "*WARN: shell environment ODE_PROJ_SETTING_DIR does not exist\n")
        fprintf(woport "*WARN: custom check will be missing\n")
    )
    if( ode_proj_setting_dir && ! isDir(ode_proj_setting_dir) then
        fprintf(woport "*WARN: ODE_PROJ_SETTING_DIR is not a directory\n")
        fprintf(woport "*WARN: custom check will missing\n")
    )
    if( ode_proj_setting_dir && isDir(ode_proj_setting_dir) then
        printf("ODE: shell env ODE_PROJ_SETTING_DIR is set to %s\n" ode_proj_setting_dir)
        printf("ODE: begin to read ODE custom environment\n")
        yaml_file = strcat(ode_proj_setting_dir "/project.yaml")
        if( yaml_file && isFile(yaml_file) then
;            childPID = ipcBeginProcess(strcat("odeyamltoskill.py -f " yaml_file) "" 'ODEStdoutHandler 'ODEStderrHandler)
            childPID = ipcBeginProcess(strcat("odeyamltoskill.py -f " yaml_file))
            ipcWaitForProcess( childPID )
            ipcReturnCmd = ipcReadProcess( childPID 10 )
;            println(ipcReturnCmd)
            foreach(cmd parseString(ipcReturnCmd "\n")
                evalstring(cmd)
            )
            ipcKillProcess( childPID )
        printf("ODE: end of read ODE custom environment\n")
        else
            fprintf(woport "%s did not exist or not a file\n" yaml_file)
        )
    )

) ; end of let
) ; end of procedure
ODEloadEnv()

; procedure(ODEsettingGen(hier,key,value)
; let((temp_point)
;     temp_point = ODEsetting
;     foreach(hier_key hier
;         if( ! member(hier_key temp_point~>?) then
;             temp_point[hier_key] = makeTable("table" 0)
;         )
;         temp_point = temp_point[hier_key]
;     )
;     temp_point[key] = value
; ) ; end of let
; ) ; end of procedure

; procedure(ODEsettingGen(key,value)
; let(()
;     if(! boundp('ODEsetting) then
;         ODEsetting = makeTable("ODEvar" 0)
;     )
;         ODEsetting[key] = value
; ) ; end of let
; ) ; end of procedure


;ODEloadEnv()


procedure(ODECheckSetting()
    printf("----------- begin of ODEsetting setting -----------\n")
    ODECheckItemSetting("sch_deniedDev" "denied device check will lost")
    printf("----------- end of ODEsetting setting -----------\n")
) ; end of procedure


procedure(ODECheckItemSetting(key comment)
        if(member(key ODEsetting~>?) then
            if(tablep(ODEsetting[key]) then
                printf("%s is defined as : %L\n" key ODEsetting[key]~>??)
            else
                printf("%s is defined as : %L\n" key ODEsetting[key])
            )
        else
            fprintf(woport "%s not defined,%s\n" key comment)
        )
) ; end of procedure

ODECheckSetting()
