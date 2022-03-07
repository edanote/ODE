# ODEThese code are developed at home,
copyright belong to Nan Chen
All rights reserved


setenv ODE_HOME /home/study/ODE
setenv BUTIAN_SOURCE_DIR path_to_pv_dir
setenv BUTIAN_RESULTS_DIR path_to_results_dir

add ${ODE_HOME}/bin to PATH variable

add below skill to .cdsinit
let((ODESkillPath)
ODESkillPath = strcat( getShellEnvVar("ODE_HOME") "/skill/loadme.skill")
load(ODESkillPath)
)


please make sure BUTIAN_RESULTS_DIR dir mode is 1777


