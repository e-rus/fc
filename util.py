import FreeCAD as App
from FreeCAD import Units
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
    AAd = App.ActiveDocument
    AAd.addObject('Sketcher::SketchObject',sketch)
    planecheck = [set([pt[j] for pt in points]) for j in [0,1,2]]
    print(points,planecheck)
    if planecheck[2]==set([0]):
        rot = App.Rotation(0.000000, 0.000000, 0.000000, 1.000000)
        plc = App.Placement(App.Vector(0.000000, 0.000000, 0.000000),rot)
        points = [[pt[0],pt[1],0] for pt in points]
    elif planecheck[1]==set([0]):
        rot = App.Rotation(-0.707107, 0.000000, 0.000000, -0.707107)
        plc = App.Placement(App.Vector(0.000000, 0.000000, 0.000000), rot)
        points = [[pt[0],pt[2],0] for pt in points]
    elif planecheck[0]==set([0]):
        rot = App.Rotation(0.500000, 0.500000, 0.500000, 0.500000)
        plc = App.Placement(App.Vector(0.000000, 0.000000, 0.000000), rot)
        points = [[pt[1],pt[2],0] for pt in points]
    else:
        print("Out of planes")
    AAd.getObject(sketch).Placement = plc
    AAd.recompute()

    if closed:
        points.append(points[0])
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

#"############################################################################"#
def revolution(gid,gidr,axis=(0,0,1),base=(1,0,0),angle=360,solid=True):
    AAd = App.ActiveDocument
    AAd.addObject("Part::Revolution",gidr)
    AAd.getObject(gidr).Source = AAd.getObject(gid)
    AAd.getObject(gidr).Angle = angle
    AAd.getObject(gidr).Axis = axis
    AAd.getObject(gidr).Base = base
    AAd.getObject(gidr).Solid = True

#"############################################################################"#
def fcnew():
    docs = App.listDocuments().keys()
    for doc in docs:
        App.closeDocument(doc)

    doc = App.newDocument()

    AAd = App.ActiveDocument
    return AAd

#"############################################################################"#
def as_mm(v):
    v = Units.Quantity('{}mm'.format(v))
    return v

#"############################################################################"#
def filletz(gid,r):
    AAd = App.ActiveDocument
    AAd.getObject(gid).recompute()
    gidf = gid+'_fl'
    AAd.addObject("Part::Fillet",gidf)
    AAd.getObject(gidf).Base = AAd.getObject(gid)
    edg = AAd.getObject(gid).Shape.Edges
    print('\n',gid,AAd.getObject(gid).Shape,'\n')
    fl = {j:[ev.Point.z for ev in edg[j].Vertexes] for j in range(len(edg))}
    fl = {j:abs(v[0]-v[1]) for j,v in fl.items() if abs(v[0]-v[1])>0.01}
    print('\n',gid,fl,'\n')
    __fillets__ = [(j+1,r,r) for j in fl.keys()]
    AAd.getObject(gidf).Edges = __fillets__
    AAd.getObject(gid).Visibility = False
    return
