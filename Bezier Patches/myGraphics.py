# Islam, Shehzad ul.
# sxi5356
# 2018-10-20

#----------------------------------------------------------------------
# This code was originally created by Prof. Farhad Kamangar.
# It has been significantly modified and updated by Brian A. Dalio for
# use in CSE 4303 / CSE 5365 in the 2018 Fall semester.

#----------------------------------------------------------------------

import CohenSutherland
from CohenSutherland import clipLine
import BézierPatch
from BézierPatch import resolve


#----------------------------------------------------------------------
class cl_world :
  def __init__( self, objects = [], canvases = [] ) :
    self.objects = objects
    self.canvases = canvases

  def add_canvas( self, canvas ) :
    self.canvases.append( canvas )
    canvas.world = self

  def reset( self ) :
    self.objects = []
    for canvas in self.canvases :
      canvas.delete( 'all' )

  def drawTriangle( self,canvas, v1, v2, v3, portal,doClip) :
    if doClip == True:
        doDraw, p1x, p1y, p2x, p2y = clipLine(v1[0],v1[1],v2[0],v2[1],portal)
        if(doDraw):
            self.objects.append(canvas.create_line(p1x, p1y, p2x, p2y))
        doDraw, p1x, p1y, p2x, p2y = clipLine(v2[0],v2[1],v3[0],v3[1],portal)
        if(doDraw):
            self.objects.append(canvas.create_line(p1x, p1y, p2x, p2y))
        doDraw, p1x, p1y, p2x, p2y = clipLine(v3[0],v3[1],v1[0],v1[1],portal)
        if(doDraw):
            self.objects.append(canvas.create_line(p1x, p1y, p2x, p2y))
    else:
        self.objects.append( canvas.create_line(v1[0], v1[1], v2[0], v2[1] ) )
        self.objects.append( canvas.create_line(v2[0], v2[1], v3[0], v3[1] ) )
        self.objects.append( canvas.create_line(v3[0], v3[1], v1[0], v1[1] ) )

  def create_graphic_objects( self, canvas, master ) :

    print( 'Resolution:', master.Resolution )
    resolution = master.Resolution

    # Create a rectangle of the viewport
    x1,y1,x2,y2 = master.model.getViewport()
    width = int(canvas.cget( 'width' ))
    height = int(canvas.cget( 'height' ))
    self.objects.append( canvas.create_rectangle(x1*width,y1*height,x2*width,y2*height,outline='black'))

    faces = master.model.getFaces()
    patches = master.model.getPatches()
    vertices = master.model.getVertices()
    doEuler = master.doEuler.get() == 1
    doPerspective = master.doPerspective.get() == 1
    doClip = master.doClip.get() == 1
    portal = x1 * width,y1 *height, x2*width, y2*height

    for face in faces:
      v1 = master.model.getTransformedVertex(face[0], doPerspective, doEuler)
      v2 = master.model.getTransformedVertex(face[1], doPerspective, doEuler)
      v3 = master.model.getTransformedVertex(face[2], doPerspective, doEuler)
      
      if master.doClip.get() == 1:
          doDraw, p1x, p1y, p2x, p2y = clipLine(v1[0],v1[1],v2[0],v2[1],portal)
          if(doDraw):
              self.objects.append(canvas.create_line(p1x, p1y, p2x, p2y))
          doDraw, p1x, p1y, p2x, p2y = clipLine(v2[0],v2[1],v3[0],v3[1],portal)
          if(doDraw):
              self.objects.append(canvas.create_line(p1x, p1y, p2x, p2y))
          doDraw, p1x, p1y, p2x, p2y = clipLine(v3[0],v3[1],v1[0],v1[1],portal)
          if(doDraw):
              self.objects.append(canvas.create_line(p1x, p1y, p2x, p2y))
      else:
          self.objects.append( canvas.create_line(v1[0], v1[1], v2[0], v2[1] ) )
          self.objects.append( canvas.create_line(v2[0], v2[1], v3[0], v3[1] ) )
          self.objects.append( canvas.create_line(v3[0], v3[1], v1[0], v1[1] ) )

    for patch in patches:
      points = resolve(resolution,patch,vertices)
      # print("Points",points)

      for row in range(0,resolution-1):
         rowStart = row * resolution
         for col in range(0,resolution-1):
           here = rowStart + col
           there = here + resolution

           triangleA = ( points[here], points[there], points[there+1] )
           v1 = master.model.transformXYZ(triangleA[0][0],triangleA[0][1],triangleA[0][2], doPerspective, doEuler)
           # print(v1)
           v2 = master.model.transformXYZ(triangleA[1][0],triangleA[1][1],triangleA[1][2], doPerspective, doEuler)
           # print(v2)
           v3 = master.model.transformXYZ(triangleA[2][0],triangleA[2][1],triangleA[2][2], doPerspective, doEuler)
           # print(v3)
           self.drawTriangle( canvas,v1,v2,v3,portal, doClip)

           triangleB = ( points[there+1], points[here+1], points[here] )
           v1 = master.model.transformXYZ(triangleB[0][0],triangleB[0][1],triangleB[0][2], doPerspective, doEuler)
           # print(v1)
           v2 = master.model.transformXYZ(triangleB[1][0],triangleB[1][1],triangleB[1][2], doPerspective, doEuler)
           # print(v2)
           v3 = master.model.transformXYZ(triangleB[2][0],triangleB[2][1],triangleB[2][2], doPerspective, doEuler)
           # print(v3)
           self.drawTriangle( canvas,v1,v2,v3,portal, doClip)
      

    # # 1. Create a line that goes from the upper left
    # #    to the lower right of the canvas.
    # self.objects.append( canvas.create_line(
    #   0, 0, canvas.cget( 'width' ), canvas.cget( 'height' ) ) )

    # # 2. Create a line that goes from the lower left
    # #    to the upper right of the canvas.
    # self.objects.append( canvas.create_line(
    #   canvas.cget( 'width' ), 0, 0, canvas.cget( 'height' ) ) )

    # # 3. Create an oval that is centered on the canvas and
    # #    is 50% as wide and 50% as high as the canvas.
    # self.objects.append( canvas.create_oval(
    #   int( 0.25 * int( canvas.cget( 'width' ) ) ),
    #   int( 0.25 * int( canvas.cget( 'height' ) ) ),
    #   int( 0.75 * int( canvas.cget( 'width' ) ) ),
    #   int( 0.75 * int( canvas.cget( 'height' ) ) ) ) )




  def redisplay( self, canvas, event ) :
    pass
    # if self.objects :
    #   canvas.coords(self.objects[ 0 ], 0, 0, event.width, event.height )
    #   canvas.coords(self.objects[ 1 ], event.width, 0, 0, event.height )
    #   canvas.coords(self.objects[ 2 ],
    #     int( 0.25 * int( event.width ) ),
    #     int( 0.25 * int( event.height ) ),
    #     int( 0.75 * int( event.width ) ),
    #     int( 0.75 * int( event.height ) ) )

#----------------------------------------------------------------------
