
procedure( ODEbutian()
let((cv libName cellName viewName pycmd rule_dir result_dir)
    cv = hiGetCurrentWindow()
    libName = cv~>cellView~>libName
    cellName = cv~>cellView~>cellName
    viewName = cv~>cellView~>viewName
    rule_dir = getShellEnvVar("BUTIAN_SOURCE_DIR")
    result_dir = getShellEnvVar("BUTIAN_RESULTS_DIR")
    pycmd = strcat("odebutian.py -laylib " libName " -laycell " cellName " -layview " viewName " -rule_dir " rule_dir " -result_dir " result_dir)
    println(pycmd)
    ipcBeginProcess(pycmd "" 'ODEStdoutHandler 'ODEStderrHandler)
) ; end of leg
) ; end of procedure

