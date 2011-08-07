import cv
import os
import traceback
from config import *

HCPATH = os.path.join(HCDIR, HCNAME)

class FaceImage:
    """ Represents an image with a face in it, and all the scaling/cropping that goes along with it. """

    def __init__(self, imagepath):
        self.filename = os.path.basename(imagepath)
        self.image = cv.LoadImage(imagepath, 1) # Second argument is for 0:grayscale, 1:color
        self.imagepath = imagepath
        self.finalImg = None
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
        if MARKPOINTS:
            self._markFace(face)

        # Calculate scaling params based on faceWidth
        faceWidth = float(face[2]) # Make faceWidth a float
        scaleF = FACEW_TARGET/faceWidth
        scSize = (int(origSize[0]*scaleF), int(origSize[1]*scaleF))
        scMid = (mid[0]*scaleF, mid[1]*scaleF)
        self._log('\tFace width: ' + str(faceWidth) + ', should be: ' + str(FACEW_TARGET))
        self._log('\tPre-crop scaled size: ' + str(scSize))

        # Scale image
        scImg = cv.CreateImage(scSize, cv.IPL_DEPTH_8U, 3)
        cv.Resize(self.image, scImg, cv.CV_INTER_CUBIC)

        # Determine translation. offset: (positive leaves a border, negative doesn't)
        offset = (int(MID_X_TARGET-scMid[0]), int(MID_Y_TARGET-scMid[1]))
        self._log("\toffset: " + str(offset))

        self.finalImg = crop(scImg, offset, (WIDTH_TARGET, HEIGHT_TARGET))

    def save(self, outputpath):
        """ Saves the final image to the specified output path. Creates the path if necessary """
        self._log('Saving as ' + outputpath)
        if self.finalImg == None:
            raise Exception('Final image is uninitialized- run cropToFace first')

        outdir = os.path.dirname(outputpath)
        if not os.path.exists(outdir):
            self._log('Creating directory ' + outdir)
            os.makedirs(outdir)

        cv.SaveImage(outputpath, self.finalImg)

       
    def _getFaceCoords(self): 
        """ Returns coordinates of the face in this image """
        cascade = cv.Load(HCPATH)
        faces = cv.HaarDetectObjects(self.image, cascade, cv.CreateMemStorage())

        # Several faces will be found. Pick the largest.
        if faces:
            largest = (0,0,0,0,0) # x, y, w, h, w*h of largest eyes
            for (x,y,w,h),n in faces:
                self._log("\t\tFace found from (" + str(x)+", "+str(y)+
                ") to ("+str(x+w)+", "+str(y+h)+"), A: "+str(w*h))
                if w*h > largest[4]:
                    largest = (x, y, w, h, w*h)

                if MARKALL:
                    self._markFace((x,y,w,h)) 

            return largest
        else:
            return None

    def _markFace(self, face, color = (255,0,0)):
        """ Marks the location of the given face onto the image """
        cv.Rectangle(self.image, (face[0], face[1]), (face[0]+face[2], face[1]+face[3]), color)

    def _faceMidpoint(self, face):
        """ Returns the middle of the face """
        return (face[0] + face[2]/2, face[1] + face[3]/2)

    def _log(self, msg, level=1):
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
        
        cv.CopyMakeBorder(image, finalImg, useOffset, GAP_BORDER) 

        return finalImg

    else:
        cv.SetImageROI(image, (-offset[0], -offset[1], w, h))
        return image


def runFaceImage(imagepath, outpath):
    # exceptions just disappear from multiprocessing.Pool, for some reason
    try:
        print('beginning FaceImage run for image path: ' + imagepath)
        fi = FaceImage(imagepath)
        fi.cropToFace()
        fi.save(outpath)
        print(fi.log)

    except Exception as e:
        # print all at once to keep imagepath and stack trace from getting separated by multithreading
        msg = '*** Incomplete: ' + imagepath + ' ***\n'
        msg += traceback.format_exc()
        print(msg)
