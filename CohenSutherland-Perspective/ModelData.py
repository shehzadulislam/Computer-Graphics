# Islam, Shehzad ul.
# sxi5356
# 2018-10-20

import sys

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
        self.ax = 0
        self.ay = 0
        self.sx = 0
        self.sy = 0
        self.distance = 1.0

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

    def getTransformedVertex( self, vNum, doPerspective=False ) :
        vertex = self.m_Vertices[vNum]
        transformedvertex = []
        xcomp = vertex[0]
        ycomp = vertex[1]
        zcomp = vertex[2]
        xvalue = 0.0
        yvalue = 0.0
        if doPerspective == True:
            if zcomp >= self.distance:
                xvalue = 0.0
                yvalue = 0.0
            else:
                xvalue = (self.sx * (xcomp / (1 - (zcomp/self.distance)))) + self.ax
                yvalue = (self.sy * (ycomp / (1 - (zcomp/self.distance)))) + self.ay
        else:
            xvalue = float(self.sx) * float(xcomp) + float(self.ax)
            yvalue = float(self.sy) * float(ycomp) + float(self.ay)
        transformedvertex.append(xvalue) 
        transformedvertex.append(yvalue)
        transformedvertex.append(float(0.0))
        return tuple(transformedvertex)
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

    ( ax, ay, sx, sy ) = constructTransform( w, v, width, height )
    print( f'Transform is {ax} {ay} {sx} {sy}' )

    model.specifyTransform( ax, ay, sx, sy )

    print( 'First 3 transformed vertices:' )
    for vNum in range( 3 ) :
        print( '     ', model.getTransformedVertex( vNum ) )

#---------#
if __name__ == '__main__' :
    _main()

#---------#---------#---------#---------#---------#--------#
