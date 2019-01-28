# Islam, Shehzad ul
# sxi5356
# 2018-09-01

import sys

class ModelData() :
    def __init__( self, inputFile = None ) :
        self.m_Vertices = []
        self.m_Faces    = []
        self.m_Window   = []
        self.m_Viewport = []

        if inputFile is not None :
            # File name was given.  Read the data from the file.
            self.loadFile( inputFile )

    def getFaces( self )    :
        return self.m_Faces
    def getVertices( self ) :
        return self.m_Vertices
    def getViewport( self ) :
        return self.m_Viewport
    def getWindow( self )   :
        return self.m_Window

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
                    line = line[:1].replace('f', '').strip() + line[1:].strip()
                    line.strip()
                    for item in line :
                        if item != " ":
                            if item == "." :
                                print("Line " + str(index) + " is a malformed face spec.")
                                m_valuelist = []
                                break
                            else:
                                value = int(item) - 1
                                m_valuelist.append(value)
                                if len(m_valuelist) > 3 :
                                    m_valuelist = []
                                    print("Line " + str(index) + " is a malformed face spec.")
                                    break
                    if len(m_valuelist) > 0:
                        tupvalue = tuple(m_valuelist)
                        self.m_Faces.append(str(tupvalue))
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
                        tupvalue = tuple(m_valuelist)
                        self.m_Vertices.append(str(tupvalue))
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

##################################################
# Put your Python code for reading and processing the lines
# from the source file in the place of the comments below.
# (The comments give all the direction you should need to
#  write the code.  It's not all that difficult.)
##################################################

# Read each line of the file.

# Ignore any line that starts with a #.

# Ignore any blank line (or line that's only whitespace characters).

# For the remaining lines, if the line starts with:
#  f -- Append the three integers as a tuple to self.m_Faces.
#  v -- Append the three floats as a tuple to self.m_Vertices.
#  w -- Keep the four floats as a tuple in self.m_Window.
#  s -- Keep the four floats as a tuple in self.m_Viewport.

# Note that the above comments mention integers and floats.
# You must convert the string representation of the integers
# and floats into actual numbers.  There may be formatting
# errors in the file, so ensure you catch (and report)
# conversion errors.

# It is an error if a line starts with any other character.
# Print an error message for that line, but keep going and look
# at the rest of the lines.

# It is an error if the model file has more than one w line.
# Print an error message for this occurence, but keep going.

# It is an error if the model file has more than one s line.
# Print an error message for this occurence, but keep going.

# A model file may have any number of f and v lines.  In fact,
# some model files we will use will have thousands of v and f
# lines.

##################################################
# All the code you have to write should go above here in the
# body of the loadFile() routine.
##################################################

#---------#---------#---------#---------#---------#--------#
def _main() :
    # Get the file name to load.
    fName = sys.argv[1]

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

    print( 'Window line:', model.getWindow() )
    print( 'Viewport line:', model.getViewport() )

#---------#
if __name__ == '__main__' :
    _main()

#---------#---------#---------#---------#---------#--------#
