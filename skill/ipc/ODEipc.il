/*
wechat official account : edanote
github : https://github.com/edanote/ODE
lint score : 100

procedure to run log as command or print as log

*/

;procedure(ODEStdoutHandler(ipcId data)
;      printf("run ipc command:%s" data)
;      evalstring(data)
;)

procedure(ODEStdoutHandler(ipcId data)
    foreach(line parseString(data "\n")
        printf("run ipc command:%s\n" line)
        evalstring(line)
    )
)

procedure(ODEStderrHandler(ipcId data)
  printf("log from ipc : %s" data)
)

procedure(ODEStdoutText(ipcId data)
    foreach(line parseString(data "\n")
        printf("%s\n" line)
    )
)

procedure(ODEStderrText(ipcId data)
    foreach(line parseString(data "\n")
        printf("%s\n" line)
    )
)

; ODEIpc=ipcBeginProcess("shell_command" "" 'ODEStdoutHandler 'ODEStderrHandler)

