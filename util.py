import FreeCAD as App
from StartPage import StartPage
from math import cos, sin
import Mesh, Part, Sketcher

def boold(A,B,C):
    AAd = App.ActiveDocument

    AAd.addObject("Part::Cut",C)
    AAd.getObject(C).Base = AAd.getObject(A)
    AAd.getObject(C).Tool = AAd.getObject(B)

    AAd.getObject(A).Visibility=False
    AAd.getObject(B).Visibility=False

    return

def boolu(obs,C):
    AAd = App.ActiveDocument

    AAd.addObject("Part::MultiFuse",C)

    obl = []
    for ob in obs:
        obl.append(AAd.getObject(ob))
        
    AAd.getObject(C).Shapes = obl

    for ob in obs:
        AAd.getObject(ob).Visibility=False
    return

def points_to_sketch(points,sketch,closed=True):
    pts = points
    sk = sketch
    n = len(pts)-1
    for i in range(n):
        x0=pts[i][0]
        y0=pts[i][1]
        z0=pts[i][2]
        x1=pts[i+1][0]
        y1=pts[i+1][1]
        z1=pts[i+1][2]
        
        lsg = Part.LineSegment(App.Vector(x0,y0,z0),App.Vector(x1,y1,z1))
        AAd.getObject(sk).addGeometry(lsg,False)

        if i>0:
            cst = Sketcher.Constraint('Coincident',i-1,2,i,1)
            AAd.getObject(sk).addConstraint(cst)
            AAd.recompute()

    if closed:
        cst = Sketcher.Constraint('Coincident',i,2,0,1)
        AAd.getObject(sk).addConstraint(cst)
    AAd.recompute()

    if AAd.getObject(sk).ViewObject.TempoVis:
        AAd.getObject(sk).ViewObject.TempoVis.restore()


################################################################################
def fcnew():
    docs = App.listDocuments().keys()
    for doc in docs:
        App.closeDocument(doc)

    doc = App.newDocument()

    AAd = App.ActiveDocument
    return AAd
