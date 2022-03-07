
procedure(ODEStdoutHandler(ipcId data)
      printf("run ipc command:%s" data)
      evalstring(data)
;  if(rexMatchp("^oderun_" data) then
;      rexCompile("^oderun_")
;      data = rexReplace(data "" 0)
;      printf("run ipc command : %s" data)
;      evalstring(data)
;  else
;      printf("log from ipc : %s" data)
;  )
)

procedure(ODEStderrHandler(ipcId data)
  printf("log from ipc : %s" data)
)

; ODEIpc=ipcBeginProcess("shell_command" "" 'dibStdoutHandler 'dibStderrHandler)

