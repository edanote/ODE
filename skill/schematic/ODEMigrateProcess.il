/*
wechat official account : edanote
github : https://github.com/edanote/ODE
lint score : 100

migrate pdk cell in mapping file to new pdk cell
ODEMigrateProcess("test_library" "./mapping")

mapping file format
libold cellold libnew cellnew cdf1_old cdf1_new cdf2_old cdf2_new .....
lambda lib_new cell_new cdf_new floating_number
valMap lib_new cell_new cdf_new prop_old prop_new
*/

procedure(ODEMigrateProcess(library processMap )
let((mapPort lineList oldSymLib oldSymCell newSymLib newSymCell oldProp newProp libDB devicePropTable cv allProp tableType tableValue temp singlePropItem cellName lambdaKey lambdaTable newValue nextLine instName instOrient instxy symbolId deviceNameTable oldSymLibCell libName newSymProp newSymVal oldSymVal valMapKey valMapTable )
mapPort=infile(processMap)
unless(libDB=ddGetObj(library) error("Library %s does not exists\n" library))


lambdaTable=makeTable("lambdaValue" 0)
devicePropTable = makeTable("atable" 0)
valMapTable = makeTable("atable" 0)
deviceNameTable = makeTable("atable" 0)
;while( lineList = lineread(mapPort)
while( gets(nextLine mapPort)
    rexCompile( "\n" )
    nextLine = rexReplace( nextLine "" 0)
    lineList = simStringsToList(nextLine)
;    lineList = foreach(mapcar x lineList symbolToString(x))

    case(nthelem(1 lineList)
        ("lambda"
            libName = nthelem(2 lineList)
            cellName = nthelem(3 lineList)
            lambdaKey = strcat(libName "_" cellName "_" nthelem(4 lineList))
            lambdaTable[lambdaKey] = atof(nthelem(5 lineList))
        )
        ("valMap"
            newSymLib = nthelem(2 lineList)
            newSymCell = nthelem(3 lineList)
            newSymProp = nthelem(4 lineList)
            oldSymVal = nthelem(5 lineList)
            newSymVal = nthelem(6 lineList)
            valMapKey = strcat(newSymLib "_" newSymCell "_" newSymProp)
            valMapKey = strcat(newSymLib "_" newSymCell "_" newSymProp "_" oldSymVal)
;            if(not valMapTable[valMapKey] then
;                valMapTable[valMapKey]=makeTable()
;            )
;            valMapTable[valMapKey][oldSymVal] = newSymVal
            valMapTable[valMapKey] = newSymVal
        )
        ("#"
        )
        ( t
            oldSymLib       = nthelem(1 lineList)
            oldSymCell      = nthelem(2 lineList)
            newSymLib       = nthelem(3 lineList)
            newSymCell      = nthelem(4 lineList)
            oldSymLibCell = strcat(oldSymLib "_" oldSymCell)
            devicePropTable[oldSymLibCell] = makeTable("cell property mapping" 0)
            deviceNameTable[oldSymLibCell] = makeTable("library/cell name mapping" 0)
            deviceNameTable[oldSymLibCell]["newSymLib"] = newSymLib
            deviceNameTable[oldSymLibCell]["newSymCell"] = newSymCell
            for(i 5 length(lineList)
                if(oddp(i) then
                    oldProp     = nthelem(i lineList)
                    newProp     = nthelem(i+1 lineList)
                    devicePropTable[oldSymLibCell][oldProp]=newProp
                ) ; end of if
            ) ; end of for
        )
    )
)  ; end of while


foreach(cell libDB~>cells
    if(exists(x cell~>views~>name (x=="schematic"))
        then
        cv = dbOpenCellViewByType(library cell~>name "schematic" "schematic" "a")
        foreach( inst cv~>instances 
            oldSymLib = inst~>libName
            oldSymCell = inst~>cellName
            oldSymLibCell = strcat(inst~>libName "_" inst~>cellName)
            tableValue = makeTable("deviceValue" 0)
            tableType = makeTable("deviceValueType" 0)
            when(member(oldSymLibCell deviceNameTable~>?)
                allProp=inst~>prop~>??
                foreach(singleProp allProp
                    singlePropItem=car(singleProp)
                    oldProp =singlePropItem~>name
;                    foreach(key devicePropTable[oldSymLibCell]
                    if(member(oldProp devicePropTable[oldSymLibCell]~>?) then
                        temp = devicePropTable[oldSymLibCell][oldProp]
                        tableValue[temp]=singlePropItem~>value
                        tableType[temp]=singlePropItem~>valueType
                    )
;                    )
                )
                newSymLib = deviceNameTable[oldSymLibCell]["newSymLib"]
                newSymCell = deviceNameTable[oldSymLibCell]["newSymCell"]
                symbolId=dbOpenCellViewByType(newSymLib newSymCell "symbol")
                instName = inst~>baseName
                instxy = inst~>xy
                instOrient = inst~>orient
                schDelete(inst)
;                foreach(param cdfGetCellCDF(symbolId->cell)->parameters
;                    param->value = param->defValue
;                )
                inst = schCreateInst( cv symbolId instName instxy instOrient )
                foreach(newProp tableValue
                    lambdaKey = strcat(newSymLib "_" newSymCell "_" newProp)
                    if(member(lambdaKey lambdaTable~>?) then
                       newValue = cdfParseFloatString(tableValue[newProp]) * lambdaTable[lambdaKey]
                       newValue = aelSuffixNotation(newValue)
                    else
                       newValue = tableValue[newProp]
                    )
                    temp = strcat(lambdaKey "_" newValue)
                    if(member(temp valMapTable~>?) then
                        newValue = valMapTable[temp]
                    )
                    dbReplaceProp(inst newProp tableType[newProp] newValue)
                )
            )
        ) ; end of for instances
        schCheck(cv)
        dbSave(cv)
        dbClose(cv)
    )
) ; end of for cell

close(mapPort)
)  ; end of let
)  ; end of procedure


;sklint(?file "/home/study/project/xxxx/skill/ODEMigrateProcess.il")
;load "/home/study/project/xxxx/skill/ODEMigrateProcess.il"
;ODEMigrateProcess("migrate_test" "/home/study/project/xxxx/skill/mapping")
