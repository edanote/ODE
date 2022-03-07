procedure( ODECopyMPT(fromDB toDB)
let(()
    dbSetShapeColorLocked(toDB nil)
    dbSetShapeColor(toDB dbGetShapeColor(fromDB))
    dbSetShapeColorLocked(toDB dbIsShapeColorLocked(fromDB))
) ; end of let
) ; end of procedure
