; create shape by coordinate number and layer name
; two coordinate is rectangle
; more than two coordinate is polygon

; ------------ example -------------------
; let((cv layer purpose coor)
;     cv = dbOpenCellViewByType("test_lib" "createShape" "layout" "maskLayout" "a")
;     layer = "Metal1"
;     purpose = "drawing"
;     coor = list(0:0 1:0 1:1)
;     ODECreateShape(cv layer purpose coor)
;     dbSave(cv)
;     dbClose(cv)
; )
; ------------ end of example -------------------

procedure( ODECreateShape(cv layer purpose coor @key (color t))
let((arrayLength newShapeDB preExistShapeDB)
    preExistShapeDB = nil
    if(color then
        preExistShapeDB = car(dbShapeQuery(cv layer ENPtsToBox(coor)))
    )

    arrayLength = length(coor)
    if(arrayLength == 2 then
        newShapeDB = dbCreateRect( cv list(layer purpose) coor ) 
    )
    if(arrayLength > 2 then
        newShapeDB = dbCreatePolygon( cv list(layer purpose) coor ) 
    )
    if(type(preExistShapeDB) == 'list then
        preExistShapeDB = nthelem(length(preExistShapeDB) preExistShapeDB)
    )
    if((color && preExistShapeDB) then
        ODECopyMPT(preExistShapeDB newShapeDB)
    )
) ; end of leg
) ; end of procedure

