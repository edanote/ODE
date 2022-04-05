/*
wechat official account : edanote
github : https://github.com/edanote/ODE
lint score : 100
*/

; These code are developed at home
; Copy Right Belong To Nan Chen


procedure(ENoptimizeLocation()
let((curSelections currentDB)
;    cv=hiGetCurrentWindow()
    curSelections = geGetSelectedSet()
    currentDB = geGetEditCellView()
;    curPoint = hiGetPoint(cv)
;    println(curPoint)
    foreach(item curSelections
        if(item~>objType == "stdVia"
            ENMoveStdVia(item currentDB)
        )
        if(item~>objType == "label"
            ENmoveLabel(item currentDB)
        )
        if(item~>objType == "pathSeg"
            ENmovePath(item currentDB)
        )
    )
) ; end of let
) ; end of procedure

hiSetBindKeys("Layout" list(
list("<Key>a"             "ENoptimizeLocation()")
;list("Shift<key>(2)a"             "ENtest()")
)
)

procedure(ENMoveStdVia(item currentDB)
let((viaLayer1 viaLayer2 viaBBox auxiliaryCenter layer1QueryDB layer1ptsList layer2QueryDB layer2ptsList viaLocationPts viaCenter direction newx newy pathTypepts)
    auxiliaryCenter = nil
    pathTypepts = nil
    direction = nil
    viaLayer1 = item~>viaHeader~>viaDef~>layer1~>name
    viaLayer2 = item~>viaHeader~>viaDef~>layer2~>name
    viaCenter = item~>origin
    viaBBox = item~>bBox
    layer1QueryDB = dbShapeQuery(currentDB viaLayer1 viaBBox)
    layer1ptsList = ENGetQueryPointList(layer1QueryDB ?ignoreDB item)
    layer2QueryDB = dbShapeQuery(currentDB viaLayer2 viaBBox)
    layer2ptsList = ENGetQueryPointList(layer2QueryDB ?ignoreDB item)

    if(layer1ptsList == nil && layer2ptsList then
        pathTypepts = car(ENGetQueryPointList(layer2QueryDB ?ptsType "beginEndPts" ?ignoreDB item))
    )
    if(layer1ptsList && layer2ptsList == nil then
        pathTypepts = car(ENGetQueryPointList(layer1QueryDB ?ptsType "beginEndPts" ?ignoreDB item))
    )
    if(pathTypepts then direction = ENdirection(pathTypepts))
    if(direction == "vertical" then
        newx = xCoord(lowerLeft(pathTypepts))
        auxiliaryCenter = list(newx yCoord(viaCenter))
        item~>origin= auxiliaryCenter
    )
    if(direction == "horizontal" then
        newy = yCoord(lowerLeft(pathTypepts))
        auxiliaryCenter = list(xCoord(viaCenter) newy)
        item~>origin= auxiliaryCenter
    )

    if(layer1ptsList && layer2ptsList then
        viaLocationPts = dbPointArrayAnd( geGetEditCellView() layer1ptsList layer2ptsList)
        auxiliaryCenter = centerBox(ENPtsToBox(car(viaLocationPts)))
        item~>origin= auxiliaryCenter
    )

    
) ; end of let
) ; end of procedure


procedure(ENGetQueryPointList(queryDBList @key (ptsType "boundary") (ignoreDB nil))
let((pts layerPts)
    layerPts = nil
    foreach(layerDB queryDBList
        pts = nil
        if(type(layerDB) == 'dbobject then
            if(ignoreDB != layerDB then
                if(ptsType == "boundary" then
                    pts = ENGetLayerBoundaryPoints(layerDB)
                )
                if(ptsType == "beginEndPts" then
                    pts = ENGetLayerBeginEndpts(layerDB)
                )
            )
        else
            if((not member(ignoreDB layerDB)) then
                if(ptsType == "boundary" then
                    pts = ENInstTransform(layerDB ENGetLayerBoundaryPoints(nthelem(length(layerDB) layerDB)))
                )
            )
        ) ; end of if
        if(pts then
            if(layerPts then
                layerPts = append(layerPts list(pts))
            else
                layerPts = list(pts)
            )
        )
    ) ; end of for
    layerPts
) ; end of let
) ; end of procedure

procedure(ENGetLayerBoundaryPoints(layerDB)
    case(layerDB~>objType
        ("rect"
            ENBoxToBoundary(layerDB~>bBox)
        ) ;rect
        ("path"
            dbGetPathBoundary(layerDB)
        )
        ("pathSeg"
            layerDB~>boundary
        )
        ("polygon"
            layerDB~>points
        )
    ) ; end of case
) ; end of procedure

procedure(ENGetLayerBeginEndpts(layerDB)
    case(layerDB~>objType
        ("path"
            dbGetPathBoundary(layerDB)
        )
        ("pathSeg"
            list(layerDB~>beginPt layerDB~>endPt)
        )
    ) ; end of case
) ; end of procedure

procedure(ENdirection(pts)
let((pt1x pt2x direction)
    pt1x = xCoord(lowerLeft(pts))
;    pt1y = yCoord(lowerLeft(pts))
    pt2x = xCoord(upperRight(pts))
;    pt2y = yCoord(upperRight(pts))
    if(pt1x == pt2x then
        direction = "vertical"
    else
        direction = "horizontal"
    )
    direction
) ; end of let
) ; end of procedure

procedure(ENmoveLabel(item currentDB)
let((labelLayer labelxy pathDB realPathDB pathPts labelNewxy pt1x pt1y pt2x pt2y)
    labelLayer = item~>layerName
    labelxy = item~>xy
    pathDB = car(dbShapeQuery(currentDB labelLayer list(labelxy labelxy)))
    if(type(pathDB) == 'dbobject then
        realPathDB = pathDB
    else
        realPathDB = nthelem(length(pathDB) pathDB)
    ) ; end of if

    if(realPathDB~>objType == "pathSeg" then
        pathPts = list(realPathDB~>beginPt realPathDB~>endPt)
    ) ; end of if
    if(realPathDB~>objType == "path" then
        pathPts = realPathDB~>points
    )
    if(type(pathDB) == 'list then
        pathPts = ENInstTransform(pathDB pathPts)
    )
    if(pathPts then
        ; change orient/xy/height/justify
        labelNewxy = ENgetNeareest(labelxy pathPts)
        pt1x = xCoord(lowerLeft(pathPts))
        pt1y = yCoord(lowerLeft(pathPts))
        pt2x = xCoord(upperRight(pathPts))
        pt2y = yCoord(upperRight(pathPts))
        if(pt1x == pt2x then
        ; path is vertical
            if(yCoord(labelNewxy)*2 < pt1y+pt2y then
                item~>orient = "R90"
            else
                item~>orient = "R270"
            )
        else
        ; path is horizontal
            if(xCoord(labelNewxy)*2 < pt1x+pt2x then
                item~>orient = "R0"
            else
                item~>orient = "R180"
            )
        )
        item~>xy = labelNewxy
        item~>height = realPathDB~>width
        item~>justify = "centerLeft"
    )

) ; end of let    
) ; end of procedure

procedure(ENmovePath(item currentDB)
let((impPathLayer impPathbeginPt impPathendPt curWindowsPointArray itemPointArray usedPointArray refPathWidth refPathbeginPt refPathendPt nearestPointList transform hierRefPathDB refPathDB)
    impPathLayer = item~>lpp
    impPathbeginPt = item~>beginPt
    impPathendPt = item~>endPt
    curWindowsPointArray = list(ENBoxToBoundary(geGetWindowBox(hiGetCurrentWindow())))
    itemPointArray = list(item~>boundary)
    usedPointArray = dbPointArrayAnd(currentDB itemPointArray curWindowsPointArray)
    refPathDB = car(remove(item dbShapeQuery(currentDB impPathLayer list(nthelem(1 car(usedPointArray)) nthelem(3 car(usedPointArray))) )))
    if(refPathDB then
        if(type(refPathDB) == 'list then
            hierRefPathDB = nthelem(length(refPathDB) refPathDB)
            refPathWidth = hierRefPathDB~>width
            refPathbeginPt = hierRefPathDB~>beginPt
            refPathendPt = hierRefPathDB~>endPt
            refPathbeginPt = ENInstTransform(refPathDB refPathbeginPt)
            refPathendPt = ENInstTransform(refPathDB  refPathendPt)
        else
            refPathWidth = refPathDB~>width
            refPathbeginPt = refPathDB~>beginPt
            refPathendPt = refPathDB~>endPt
        ) ; end of if
        nearestPointList = ENgetNeareest2D(list(impPathbeginPt impPathendPt) list(refPathbeginPt refPathendPt))
        transform = list((xCoord(upperRight(nearestPointList))-xCoord(lowerLeft(nearestPointList))):(yCoord(upperRight(nearestPointList))-yCoord(lowerLeft(nearestPointList))) "R0" 1.0)
        dbMoveShape(item currentDB transform)
        item~>width = refPathWidth
    )
) ; end of let
) ; end of procedure

procedure(ENInstTransform(dbList ptOrPts)
let((instList instListLength )
    instList = reverse(setof(x dbList x~>objType == "inst"))
    instListLength = length(instList)
    for(inst 1 instListLength
        if(type(car(ptOrPts)) != 'list  then
            ptOrPts = dbTransformPoint(ptOrPts nthelem(inst instList)~>transform)
        else
            ptOrPts = dbTransformPointList(ptOrPts nthelem(inst instList)~>transform)
         )
    )
    ptOrPts
) ; end of let
) ; end of procedure

procedure(ENBoxToBoundary(bBox)
let((ll ur llx lly urx ury)
    ll = lowerLeft(bBox)
    ur = upperRight(bBox)
    llx = xCoord(ll)
    lly = yCoord(ll)
    urx = xCoord(ur)
    ury = yCoord(ur)
    list(llx:lly urx:lly urx:ury llx:ury)   
) ; end of let
) ; end of procedure

procedure( ENPtsToBox(pts)
let( (minX maxX minY maxY)
    when( pts
        minX = maxX = xCoord(car(pts))
        minY = maxY = yCoord(car(pts))
        foreach(point pts
            minX = min(minX xCoord(point))
            minY = min(minY yCoord(point))
            maxX = max(maxX xCoord(point))
            maxY = max(maxY yCoord(point))
        )
        list(minX:minY maxX:maxY) 
); end of when
); end of let
); end of procedure

procedure(ENgetNeareest(labelxy pointlist)
let((space itemSpace nearestPoint)
    space = 100000
    foreach(item pointlist
        itemSpace = ENspace(labelxy item)
        if(itemSpace < space then
            space = itemSpace
            nearestPoint = item
        )
    )
    nearestPoint
) ; end of let
) ; end of procedure

procedure(ENgetNeareest2D(pointlist1 pointlist2)
let((space itemSpace nearestPointList)
    space = 100000
    foreach(item1 pointlist1
        foreach(item2 pointlist2
            itemSpace = ENspace(item1 item2)
            if(itemSpace < space then
                space = itemSpace
                nearestPointList = list(item1 item2)
            )
        )
    )
    nearestPointList
) ; end of let
) ; end of procedure

procedure(ENspace(point1 point2)
    sqrt((xCoord(point1)-xCoord(point2))**2 + (yCoord(point1)-yCoord(point2))**2)
)
