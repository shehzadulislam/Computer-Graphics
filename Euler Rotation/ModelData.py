# Islam, Shehzad ul.
# sxi5356
# 2018-10-20

import sys
import numpy as np

class ModelData() :
    def __init__( self, inputFile = None ) :
        self.m_Vertices = []
        self.m_Faces    = []
        self.m_Window   = []
        self.m_Viewport = []
        self.m_BoundingBox = []
        self.xmin = float('inf')
        self.xmax = float('-inf')
        self.ymin = float('inf')
        self.ymax = float('-inf')
        self.zmin = float('inf')
        self.zmax = float('-inf')
        self.ax = 0.0
        self.ay = 0.0
        self.sx = 0.0
        self.sy = 0.0
        self.distance = 1.0
        self.center = (0.0,0.0,0.0)
        self.r00 = 0.0
        self.r01 = 0.0
        self.r02 = 0.0
        self.r10 = 0.0
        self.r11 = 0.0
        self.r12 = 0.0
        self.r20 = 0.0
        self.r21 = 0.0
        self.r22 = 0.0
        self.tx = 0.0
        self.ty = 0.0
        self.tz = 0.0
        self.ex = 0.0
        self.ey = 0.0
        self.ez = 0.0

        if inputFile is not None :
            # File name was given.  Read the data from the file.
            self.loadFile( inputFile )

    def loadFile( self, inputFile ) :
        with open(inputFile, 'r') as fp :
            lines = fp.read().replace('\r', '').split('\n')
        m_valuelist = []
        for (index, line) in enumerate(lines, start = 1) :
            line = line.strip()
            m_valuelist = []
            if len(line) > 0 :
                if line[0]=="#":
                    continue

                elif line[0]=="f":
                    number = ""
                    line = line[:1].replace('f', '') + line[1:] + " "
                    # print('\n')
                    for item in line :
                        if item != " ":
                            number = number + item                            
                            if item == "." :
                                print("Line " + str(index) + " is a malformed face spec.")
                                m_valuelist = []
                                number = ""
                                break
                        else:
                            if number != "":
                                value = int(number) - 1
                                # print("Num:",number)
                                # print("Value:",number)
                                m_valuelist.append(value)
                                # print("List:",m_valuelist)
                                if (len(line.split()) > 3) :
                                    m_valuelist = []
                                    print("Line " + str(index) + " is a malformed face spec.")
                                    break
                                number = ""
                    if len(m_valuelist) > 0:
                        tupvalue = tuple(m_valuelist)
                        self.m_Faces.append(tupvalue)

                elif line[0]=="v":
                    line = line[:1].replace('v', '') + line[1:] + " "
                    number = ""
                    for item in line :
                        if item != " ":
                            number = number + item
                        else:
                            if number != "":
                                valfloat = float(number)
                                value = round(valfloat, 2)
                                m_valuelist.append(value)
                                if len(m_valuelist) > 3:
                                    m_valuelist = []
                                    print("Line " + str(index) + " is a malformed vertex spec.")
                                    break
                                number = ""
                    if len(m_valuelist) > 0:
                        if m_valuelist[0] <= self.xmin:
                            self.xmin = m_valuelist[0]
                        else:
                            if(self.xmax <= m_valuelist[0]):
                                self.xmax = m_valuelist[0]
                        if m_valuelist[1] <= self.ymin:
                            self.ymin = m_valuelist[1]
                        else:
                            if(self.ymax <= m_valuelist[1]):
                                self.ymax = m_valuelist[1]
                        if m_valuelist[2] <= self.zmin:
                            self.zmin = m_valuelist[2]
                        else:
                            if(self.zmax <= m_valuelist[2]):
                                self.zmax = m_valuelist[2]
                    tupvalue = tuple(m_valuelist)
                    self.m_Vertices.append(tupvalue)
                elif line[0]=="w":
                    line = line[:1].replace('w', '') + line[1:] + " "
                    number = ""
                    if self.m_Window:
                        print("Line " + str(index) + " is a duplicate window spec.")
                    for item in line :
                        if item != " ":
                            if item.isalpha() == True:
                                print("Line " + str(index) + " is a malformed window spec.")
                                m_valuelist = []
                                break
                            else:
                                number = number + item
                        else:
                            if number != "":
                                valfloat = float(number)
                                value = round(valfloat, 2)
                                m_valuelist.append(value)
                                number = ""
                    if len(m_valuelist) > 0:
                        tupvalue = tuple(m_valuelist)
                        self.m_Window = tupvalue
                elif line[0]=="s":
                    line = line[:1].replace('s', '') + line[1:] + " "
                    number = ""
                    if self.m_Viewport:
                        print("Line " + str(index) + " is a duplicate viewport spec.")
                    for item in line :
                        if item != " ":
                            if item.isalpha() == True:
                                print("Line " + str(index) + " is a malformed viewport spec.")
                                m_valuelist = []
                                break
                            else:
                                number = number + item
                        else:
                            if number != "":
                                valfloat = float(number)
                                value = round(valfloat, 2)
                                m_valuelist.append(value)
                                number = ""
                    if len(m_valuelist) > 0:
                        tupvalue = tuple(m_valuelist)
                        self.m_Viewport = tupvalue
        boundingval = []
        boundingval.append(self.xmin)
        boundingval.append(self.xmax)
        boundingval.append(self.ymin)
        boundingval.append(self.ymax)
        boundingval.append(self.zmin)
        boundingval.append(self.zmax)
        self.m_BoundingBox = tuple(boundingval)

        #################################################
        # TODO: Put your version of loadFile() from HMWK 01
        # here.  Enhance this routine to do a running computation
        # of the bounding box.
        ##################################################

    def getBoundingBox( self ) :
        return self.m_BoundingBox
    ##################################################
    # TODO: Put your code to return the bounding box here.
    # Your routine should return a tuple with six
    # elements:
    #   ( xmin, xmax, ymin, ymax, zmin, zmax )
    ##################################################

    def specifyTransform( self, ax, ay, sx, sy, distance = 1.0 ) :
         self.ax = ax
         self.ay = ay
         self.sx = sx
         self.sy = sy
         self.distance = distance
    ##################################################
    # TODO: Put your code to remember the transformation here.
    ##################################################

    def getTransformedVertex( self, vNum, doPerspective=False, doEuler=False ) :
        vertex = self.m_Vertices[vNum]
        transformedvertex = []
        xcomp = vertex[0]
        ycomp = vertex[1]
        zcomp = vertex[2]
        xvalue = 0.0
        yvalue = 0.0
        zvalue = 0.0

        if doEuler == True:
            xp = self.r00 * xcomp + self.r01 * ycomp + self.r02 * zcomp + self.ex
            yp = self.r10 * xcomp + self.r11 * ycomp + self.r12 * zcomp + self.ey
            zp = self.r20 * xcomp + self.r21 * ycomp + self.r22 * zcomp + self.ez

            xcomp,ycomp,zcomp = xp,yp,zp

            xvalue = float(self.sx) * float(xcomp) + float(self.ax)
            yvalue = float(self.sy) * float(ycomp) + float(self.ay)

        if doPerspective == True:
            if zcomp >= self.distance:
                xvalueper = 0.0
                yvalueper = 0.0
            else:
                xvalueper = (self.sx * (xcomp / (1 - (zcomp/self.distance)))) + self.ax
                yvalueper = (self.sy * (ycomp / (1 - (zcomp/self.distance)))) + self.ay
        
            xvalue,yvalue = xvalueper,yvalueper
        else:
            xvalue = float(self.sx) * float(xcomp) + float(self.ax)
            yvalue = float(self.sy) * float(ycomp) + float(self.ay)

        transformedvertex.append(xvalue) 
        transformedvertex.append(yvalue)
        transformedvertex.append(float(0.0))
        return tuple(transformedvertex)

    def getCenter( self ) :
        self.tx = self.xmin + ((self.xmax - self.xmin) / 2)
        self.ty = self.ymin + ((self.ymax - self.ymin) / 2)
        self.tz = self.zmin + ((self.zmax - self.zmin) / 2)
        self.center = (self.tx,self.ty,self.tz)
        return self.center

    def specifyEulerAngles( self, roll, pitch, yaw ) :
        rollrad = np.radians(roll)
        pitchrad = np.radians(pitch)
        yawrad = np.radians(yaw)


        cosPhi,   sinPhi   = np.cos( rollrad ),   np.sin( rollrad )
        cosTheta, sinTheta = np.cos( pitchrad ), np.sin( pitchrad )
        cosPsi,   sinPsi   = np.cos( yawrad ),   np.sin( yawrad )

        # Now, compute the nine r values.
        # These four factors get used twice, so reuse them to save
        # four multiplications.
        cPhiXcPsi = cosPhi*cosPsi
        cPhiXsPsi = cosPhi*sinPsi
        sPhiXcPsi = sinPhi*cosPsi
        sPhiXsPsi = sinPhi*sinPsi

        # The r00 through r22 values.
        self.r00 = round(cosPsi * cosTheta,3)
        self.r01 = round(-cosTheta * sinPsi,3)
        self.r02 = round(sinTheta,3)

        self.r10 = round(cPhiXsPsi + sPhiXcPsi*sinTheta,3)
        self.r11 = round(cPhiXcPsi - sPhiXsPsi*sinTheta,3)
        self.r12 = round(-cosTheta*sinPhi,3)

        self.r20 = round(-cPhiXcPsi*sinTheta + sPhiXsPsi,3)
        self.r21 = round(cPhiXsPsi*sinTheta + sPhiXcPsi,3)
        self.r22 = round(cosPhi*cosTheta,3)

        self.ex  = round(-self.r00*self.tx - self.r01*self.ty - self.r02*self.tz + self.tx,3)
        self.ey  = round(-self.r10*self.tx - self.r11*self.ty - self.r12*self.tz + self.ty,3)
        self.ez  = round(-self.r20*self.tx - self.r21*self.ty - self.r22*self.tz + self.tz,3)

        print('r00 ',self.r00)
        print('r01 ',self.r01)
        print('r02 ',self.r02)
        print('r10 ',self.r10)
        print('r11 ',self.r11)
        print('r12 ',self.r12)
        print('r20 ',self.r20)
        print('r21 ',self.r21)
        print('r22 ',self.r22)
        print('ex ',self.ex)
        print('ey ',self.ey)
        print('ez ',self.ez)
        print('rollrad ',np.rad2deg(rollrad))
        print('yawrad ',np.rad2deg(yawrad))
        print('pitchrad ',np.rad2deg(pitchrad))


    ##################################################
    # TODO: Put your code to return a transformed version of
    # vertex n here.  Remember, vNum goes 0 .. n-1,
    # where n is the number of vertices.
    # Your routine should return a tuple with three
    # elements:
    #   ( x', y', z' )
    ##################################################

    def getFaces( self )    : return self.m_Faces
    def getVertices( self ) : return self.m_Vertices
    def getViewport( self ) : return self.m_Viewport
    def getWindow( self )   : return self.m_Window

#---------#---------#---------#---------#---------#--------#
def constructTransform( w, v, width, height ) :
    wxmin = float(w[0])
    wymin = float(w[1])
    wxmax = float(w[2])
    wymax = float(w[3])
    vxmin = float(v[0])
    vymin = float(v[1])
    vxmax = float(v[2])
    vymax = float(v[3])
    fx = -wxmin
    fy = -wymin
    gx = width * vxmin
    gy = height * vymin
    sx = (width * (vxmax - vxmin)) / (wxmax - wxmin)
    sy = (height * (vymax - vymin)) / (wymax - wymin)
    ax = fx * sx + gx
    ay = fy * sy + gy
    elem = []
    elem.append(ax)
    elem.append(ay)
    elem.append(sx)
    elem.append(sy)
    return tuple(elem)
##################################################
# TODO: Put your code to return the transform here.
# Your routine should use w, v, width, and height
# parameters according to the description in
#   "4303 Homework 02 Transform.pdf"
# to compute the transform.
# Your routine should return a tuple with four
# elements:
#   ( ax, ay, sx, sy )
##################################################

#---------#---------#---------#---------#---------#--------#
def _main() :
    # Get the file name to load and the canvas size.
    fName  = sys.argv[1]
    width  = int( sys.argv[2] )
    height = int( sys.argv[3] )
    roll = float(sys.argv[4])
    yaw = float(sys.argv[5])
    pitch = float(sys.argv[6])


    # Create a ModelData object to hold the model data from
    # the supplied file name.
    model = ModelData( fName )

    # Now that it's loaded, print out a few statistics about
    # the model data that we just loaded.
    print( "%s: %d vert%s, %d face%s" % (
        fName,
        len( model.getVertices() ), 'ex' if len( model.getVertices() ) == 1 else 'ices',
        len( model.getFaces() ), '' if len( model.getFaces() ) == 1 else 's' ))

    print( 'First 3 vertices:' )
    for v in model.getVertices()[0:3] :
        print( '     ', v )

    print( 'First 3 faces:' )
    for f in model.getFaces()[0:3] :
        print( '     ', f )

    w = model.getWindow()
    v = model.getViewport()
    print( 'Window line:', w )
    print( 'Viewport line:', v )
    print( 'Canvas size:', width, height )

    print( 'Bounding box:', model.getBoundingBox() )
    print( 'Center:', model.getCenter() )

    ( ax, ay, sx, sy ) = constructTransform( w, v, width, height )
    print( f'Transform is {ax} {ay} {sx} {sy}' )

    model.specifyTransform( ax, ay, sx, sy )

    model.specifyEulerAngles( roll, yaw, pitch )



    print( 'First 3 transformed vertices:' )
    for vNum in range( 3 ) :
        print( '     ', model.getTransformedVertex( vNum ) )

#---------#
if __name__ == '__main__' :
    _main()

#---------#---------#---------#---------#---------#--------#
