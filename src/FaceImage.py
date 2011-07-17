import cv

DEBUG = True
markpoints = False
#: The final image height
HEIGHT_TARGET = 720;
#: The final image width
WIDTH_TARGET = 960;
#: The target faceWidth:imageHeight
FACEW_RATIO_TARGET = .6
#: The ideal distance between eyes
FACEW_TARGET = FACEW_RATIO_TARGET*HEIGHT_TARGET
#: The ideal x-component of the position of the midpoint of the face
MID_X_TARGET = WIDTH_TARGET*.5
#: The ideal y-component of the position of the midpoint of the face
MID_Y_TARGET = HEIGHT_TARGET*.5

class FaceImage:

    def __init__(self, imagepath):
        self.image = cv.LoadImage(imagepath, 1) # Second argument is for 0:grayscale, 1:color
        self.imagepath = imagepath
        self.hcpath = '/opt/local/share/opencv/haarcascades/haarcascade_frontalface_default.xml'
        self.log = ''

    def cropToFace(self):
        """ Takes an openCV image, finds the face position, scales so that the face is the 'ideal'
        size, then crops so that the face is in the center """
        self._log('Starting ' + self.imagepath)
        origSize = cv.GetSize(self.image)
        face = self._getFaceCoords()
        if face == None: 
            print('No face found')
            raise Exception('No face found')
            
        # Find the middle of the face, which will be at the center of the final image
        mid = self._faceMidpoint(face)
        self._log('\tFace at: ' + str(mid) + ', should be: (' + str(MID_X_TARGET) + ', ' + str(MID_Y_TARGET) + ')')
        if markpoints:
            self._markFace(face)
        
        # Calculate scaling params based on faceWidth
        faceWidth = float(face[2]) # Make faceWidth a float
        scaleF = FACEW_TARGET/faceWidth
        scSize = (int(origSize[0]*scaleF), int(origSize[1]*scaleF))
        scMid = (mid[0]*scaleF, mid[1]*scaleF)
        self._log('\tFace width: ' + str(faceWidth) + ', should be: ' + str(FACEW_TARGET))
        self._log('\tScaling to ' + str(scSize))
        
        # Scale image
        scImg = cv.CreateImage(scSize, cv.IPL_DEPTH_8U, 3)
        cv.Resize(self.image, scImg, cv.CV_INTER_CUBIC)
        
        # Determine translation. offset: (positive leaves a border, negative doesn't)
        offset = (int(MID_X_TARGET-scMid[0]), int(MID_Y_TARGET-scMid[1]))
        self._log("\toffset: " + str(offset))

        self.finalImg = crop(scImg, offset, (WIDTH_TARGET, HEIGHT_TARGET))


    def save(self, outputpath):
        self._log('Saving as ' + outputpath)
        if self.finalImg == None:
            raise Exception('Final image is uninitialized- run cropToFace first')

        cv.SaveImage(outputpath, self.finalImg)

       
    def _getFaceCoords(self): 
        """ Returns coordinates of the face in this image """
        cascade = cv.Load(self.hcpath)
        faces = cv.HaarDetectObjects(self.image, cascade, cv.CreateMemStorage())

        # Several faces will be found. Pick the largest.
        if faces:
            largest = (0,0,0,0,0) # x, y, w, h, w*h of largest eyes
            for (x,y,w,h),n in faces: # What is n? How does this work?
                self._log("\t\tFace found from (" + str(x)+", "+str(y)+
                ") to ("+str(x+w)+", "+str(y+h)+"), A: "+str(w*h))
                if w*h > largest[4]:
                    largest = (x, y, w, h, w*h)

            return largest
        else:
            return None

    def _markFace(self, face, color = (255,0,0)):
        """ Marks the location of the given face onto the image """
        cv.Rectangle(self.image, (face[0], face[1]), (face[0]+face[2], face[1]+face[3]), color)

    def _faceMidpoint(self, face):
        """ Returns the middle of the face """
        return (face[0] + face[2]/2, face[1] + face[3]/2)

    def _log(self, msg):
        if DEBUG:
            self.log += str(msg)+'\n'
            
def crop(image, offset, size):
    w, h = size

    # If there will be a border, use CopyMakeBorder. 
    # Setting ROI, no border is created and resulting image is smaller
    if offset[0]>0 or \
       offset[1]>0 or \
       offset[0]+cv.GetSize(image)[0]<w or \
       offset[1]+cv.GetSize(image)[1]<h:

        finalImg = cv.CreateImage((w, h), cv.IPL_DEPTH_8U, 3)

        # offset may have negative values, if there will be a right/bottom border
        useOffset = (max(0, offset[0]), max(0, offset[1]))

        # Need to crop first as CopyMakeBorder will complain if the source is too big for the destination
        # (The ROI is the opposite of the offset)
        cv.SetImageROI(image, (-offset[0], -offset[1], w, h))
        
        # 4th arg: 0 for black border, 1 for stretch colors
        cv.CopyMakeBorder(image, finalImg, useOffset, 1) 

        return finalImg

    else:
        cv.SetImageROI(image, (-offset[0], -offset[1], w, h))
        return image


def runFaceImage(imagepath, outpath):
    #try:
    fi = FaceImage(imagepath)
    fi.cropToFace()
    fi.save(outpath)
    print(fi.log)

    #except Exception as e:
     #   self._log('Incomplete: ' + self.imagepath)
      #  self._log(type(e))
       # self._log(e.args)
        #self._log(e)

