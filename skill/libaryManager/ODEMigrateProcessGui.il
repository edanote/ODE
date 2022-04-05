
/*
wechat official account : edanote
github : https://github.com/edanote/ODE
lint score : 100

*/



procedure(ODEMigrateProcessGui(menuName lib cell view file cat)
let((libNameField ODEGuiList TOPForm)
    
    libNameField = hiCreateStringField(
        ?prompt     "library name"
        ?name       'libNameField
        ?defValue   lib
        ?callback   ""
        ?editable   nil
    )
    mapNameField = hiCreateStringField(
        ?prompt     "library name"
        ?name       'mapNameField
        ?defValue   "path to mapping file"
        ?callback   ""
        ?editable   t
    )

    ODEGuiList = list(libNameField mapNameField)

    TOPForm = hiCreateAppForm(
        ?name		'TOPForm
        ?formTitle	"migrate schematic in library to new process"
        ?fields		ODEGuiList
        ?callback	"ODEMigrateProcess(lib mapNameField->value)" 
        ?unmapAfterCB   t
        ?dialogStyle	'modeless
        ?buttonLayout	'OKCancel
    )
    if(lib != "" then
        hiDisplayForm(TOPForm)
    else
        ODEMessageDialog("please select library")
    )

; ODEMigrateProcess(library "./mapping")
) ; end of let
) ; end of procedure
