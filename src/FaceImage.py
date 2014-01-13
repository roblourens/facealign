from config import *
import cv2 as cv
import numpy
from operator import itemgetter
import os
import traceback
import math

HC_EYEPAIRPATH = os.path.join(HCDIR, HC_EYEPAIR_NAME)
HC_LEFTEYEPATH = os.path.join(HCDIR, HC_LEFTEYE_NAME)
HC_RIGHTEYEPATH = os.path.join(HCDIR, HC_RIGHTEYE_NAME)
HC_FACEPATH = os.path.join(HCDIR, HC_FACE_NAME)

class Point:
    def __init__(self, *args):
        if len(args) == 1:
            self.x = args[0][0]
            self.y = args[0][1]
        elif len(args) == 2:
            self.x = args[0]
            self.y = args[1]

    def dist(self, p1):
        """ Returns the pythagorean distance from this point to p1 """
        return pow(pow(self.x - p1.x, 2) + pow(self.y - p1.y, 2), .5)

    def toTuple(self):
        return (self.x, self.y)

    def __str__(self):
        return '({0}, {1})'.format(self.x, self.y)

    def __repr(self):
        return self.__str__()

class Size:
    def __init__(self, *args):
        if len(args) == 1:
            self.w = len(args[0][0])
            self.h = len(args[0])
        elif len(args) == 2:
            self.w = args[0]
            self.h = args[1]

    def toTuple(self):
        return (self.w, self.h)

    def __str__(self):
        return '({0}, {1})'.format(self.w, self.h)

    def __repr(self):
        return self.__str__()

class Rect:
    def __init__(self, array):
        self.x = array[0]
        self.y = array[1]
        self.w = array[2]
        self.h = array[3]
        self.a = self.w * self.h
        self.center = Point(self.x + self.w/2.0, self.y + self.h/2.0)

    def contains(self, p):
        return self.x <= p.x <= self.x + self.w and \
               self.y <= p.y <= self.y + self.h

    def vsplit(self):
        lRect = Rect((self.x, self.y, self.w/2.0, self.h))
        rRect = Rect((self.center.x, self.y, self.w/2.0, self.h))
        return lRect, rRect

    def __str__(self):
        return '({0}, {1}), ({2}, {3}), w = {4}, h = {5}, a = {6}'.format(
            self.x, self.y, self.x + self.w, self.y + self.h, self.w, self.h, self.a
        )

    def __repr(self):
        return self.__str__()

class FaceImage:
    """ Represents an image with a face in it, and all the scaling/cropping that goes along with it. """

    def __init__(self, imagepath):
        self.filename = os.path.basename(imagepath)
        self.image = cv.imread(imagepath)
        self.origSize = Size(self.image)
        self.imagepath = imagepath
        self._finalImg = None
        self.log = ''

    def cropToFace(self):
        """ Finds the face position of the OpenCV image, scales so that the face is the 'ideal'
        size, then crops so that the face is in the center """
        self._log('Starting ' + self.imagepath)
        eyepair = None
        lEye = rEye = None

        if not FORCE_FULL_FACE:
            eyepair = self._getEyePair()
            lEye, rEye = self._getEyes(eyepair)

        # Find the middle of the eyes
        if lEye is not None and rEye is not None:
            mid = Point(rEye.center.x/2.0 + lEye.center.x/2.0,
                        rEye.center.y/2.0 + lEye.center.y/2.0)
            eyewidth = rEye.center.dist(lEye.center)
            eyeAngle = math.degrees(
                math.atan((rEye.center.y - lEye.center.y)/(rEye.center.x - lEye.center.x)))
        else:
            eyeAngle = 0
            if eyepair is not None:
                self._log('No individual eyes found, falling back on eyepair')
                mid = eyepair.center
                eyewidth = eyepair.w*EYEPAIR_WIDTH_TO_EYE_WIDTH
            else:
                self._log('No eyes found, falling back on face')
                face = self._getFace()
                mid = Point(face.center.x, face.h*FACE_HEIGHT_TO_EYE_MID + face.y)
                eyewidth = face.w*FACE_WIDTH_TO_EYE_WIDTH
                if MARKUSED or MARKALL:
                    self._markPoint(mid, MIDPOINT_COLOR)

        self._log('', 1)
        self._log('Eye mid at: ' + str(mid) + ', should be: ' + str(Point(MID_X_TARGET, MID_Y_TARGET)), 1)

        if NOTRANSFORM:
            self._finalImg = self.image
            return

        # Calculate scaling params
        scaleF = EYEW_TARGET/eyewidth
        scSize = Size(int(self.origSize.w*scaleF), int(self.origSize.h*scaleF))
        scMid = Point(mid.x*scaleF, mid.y*scaleF)
        self._log('Eye width: ' + str(eyewidth) + ', should be: ' + str(EYEW_TARGET), 1)
        self._log('Scale factor: ' + str(scaleF), 1)
        self._log('Pre-crop scaled size: ' + str(scSize), 1)

        # Scale image
        scImg = cv.resize(self.image, (scSize.w, scSize.h), interpolation=cv.INTER_LANCZOS4)

        # Determine translation. offset: (positive leaves a top/left border, negative doesn't)
        self._log('Scaled midpoint: ' + str(scMid), 1)
        self._log('Target midpoint: ' + str(Point(MID_X_TARGET, MID_Y_TARGET)), 1)
        offset = Point(int(MID_X_TARGET - scMid.x), int(MID_Y_TARGET - scMid.y))
        self._log("offset: " + str(offset), 1)
        translatedScaledImage = crop(scImg, offset, Size(WIDTH_TARGET, HEIGHT_TARGET))

        # Rotate
        if eyeAngle == 0:
            self._finalImg = translatedScaledImage
        else:
            self._log('Rotating to: ' + str(eyeAngle))
            rotMatrix = cv.getRotationMatrix2D((MID_X_TARGET, MID_Y_TARGET), eyeAngle, 1)
            self._finalImg = cv.warpAffine(translatedScaledImage, rotMatrix, (WIDTH_TARGET, HEIGHT_TARGET))

    def save(self, outputpath):
        """ Saves the final image to the specified output path. Creates the path if necessary """
        self._log('Saving as ' + outputpath)
        if self._finalImg == None:
            raise Exception('Final image is uninitialized- run cropToFace first')

        outdir = os.path.dirname(outputpath)
        try:
            if not os.path.exists(outdir):
                self._log('Creating directory ' + outdir)
                os.makedirs(outdir)
        except:
            print(outdir)

        cv.imwrite(outputpath, self._finalImg)

    def _getEyePair(self):
        cascade = cv.CascadeClassifier(HC_EYEPAIRPATH)
        minSize = (int(EYEPAIR_MIN_SIZE[0]*self.origSize.w),
                   int(EYEPAIR_MIN_SIZE[1]*self.origSize.h))
        maxSize = (int(EYEPAIR_MAX_SIZE[0]*self.origSize.w),
                   int(EYEPAIR_MAX_SIZE[1]*self.origSize.h))
        eyepairs = toRects(cascade.detectMultiScale(self.image, minSize=minSize, maxSize=maxSize))

        if not eyepairs:
            return None

        for eyepair in eyepairs:
            self._log('Eyepair found: ' + str(eyepair), 1)
            if MARKALL:
                self._markRect(eyepair, EYEPAIR_COLOR)

        # Find the largest eyepair
        largest = max(eyepairs, key=lambda e: e.a)

        if largest.w / largest.h < EYEPAIR_RATIO:
            return None
        else:
            if MARKUSED:
                self._markRect(largest, EYEPAIR_COLOR)
            return largest

    def _getEyes(self, eyepair):
        lEyeCascade = cv.CascadeClassifier(HC_LEFTEYEPATH)
        rEyeCascade = cv.CascadeClassifier(HC_RIGHTEYEPATH)

        lEyes = toRects(lEyeCascade.detectMultiScale(self.image))
        rEyes = toRects(rEyeCascade.detectMultiScale(self.image))

        # mark eyes if needed
        for eye in lEyes:
            self._log('Left eye found: ' + str(eye), 1)
            if MARKALL:
                self._markRect(eye, LEFT_EYE_COLOR)

        for eye in rEyes:
            self._log('Right eye found: ' + str(eye), 1)
            if MARKALL:
                self._markRect(eye, RIGHT_EYE_COLOR)

        if len(lEyes) == 0 or len(rEyes) == 0:
            self._log("Didn't find both left and right eyes")
            return (None, None)

        # Filter eye results by having centers in the correct half of the eyepair
        if eyepair:
            rightEyepair, leftEyepair = eyepair.vsplit()
            self._log(str(leftEyepair))
            self._log(str(rightEyepair))
            lEyes = filter(lambda e: leftEyepair.contains(e.center), lEyes)
            rEyes = filter(lambda e: rightEyepair.contains(e.center), rEyes)

            if (len(lEyes) == 0 or len(rEyes) == 0):
                self._log("Didn't find eyes in the correct half of the eyepair")
                return (None, None)

        lEye = max(lEyes, key=lambda e: e.a)
        rEye = max(rEyes, key=lambda e: e.a)

        # Throw out the eyes if they are too close
        eyeDist = lEye.center.dist(rEye.center)
        minEyeDist = EYE_MIN_DISTANCE*self.origSize.w
        if eyeDist < minEyeDist:
            self._log('Eyes too close, rejected - %d, should be %d' % (eyeDist, minEyeDist))
            return (None, None)

        # Throw out the eyes if they differ in size too much
        eyeSizeDiff = max(lEye.a, rEye.a)/min(lEye.a, rEye.a)
        if eyeSizeDiff >= EYE_MAX_SIZE_DIFFERENCE:
            self._log('Eyes too different in size, rejected - %d vs %d' % (lEye.a, rEye.a))
            return (None, None)

        if MARKUSED:
            self._markRect(lEye, LEFT_EYE_COLOR)
            self._markRect(rEye, RIGHT_EYE_COLOR)

        return (lEye, rEye)

    def _getFace(self):
        """ Returns coordinates of the face in this image """
        cascade = cv.CascadeClassifier(HC_FACEPATH)
        faces = toRects(cascade.detectMultiScale(self.image))

        for face in faces:
            self._log('Face found: ' + str(face), 1)
            if MARKALL:
                self._markRect(face, FACE_COLOR)

        if len(faces) > 0:
            bestFace = faces[0]
            for face in faces:
                bestFace = self._bestFace(bestFace, face)

            if MARKUSED:
                self._markRect(bestFace, FACE_COLOR)

            return bestFace
        else:
            return None

    def _bestFace(self, f1, f2):
        # if the sizes of these faces are within .5% of each other, take the 
        # one nearest midpoint
        p = .005
        deltaP = float(abs(f1.a - f2.a))/max(f1.a, f2.a)
        imageMidpoint = Point(self.origSize.w*MID_X_TARGET_RATIO, self.origSize.h*MID_Y_TARGET_RATIO)
        if deltaP < p:
            return f1 if f1.center.dist(imageMidpoint) < f2.center.dist(imageMidpoint) else f2
        else:
            return max(f1, f2, key=lambda f: f.a)

    def _markRect(self, rect, color):
        """ Marks the location of the given rect onto the image """
        cv.rectangle(self.image, (rect.x, rect.y), (rect.x + rect.w, rect.y + rect.h), color)
        self._markPoint(rect.center, MIDPOINT_COLOR)

    def _markPoint(self, p, color):
        pointSize = 10
        cv.rectangle(
            self.image,
            (int(p.x) - pointSize/2, int(p.y) - pointSize/2),
            (int(p.x) + pointSize/2, int(p.y) + pointSize/2),
            color,
            cv.cv.CV_FILLED)


    def _log(self, msg, level=0):
        if DEBUG:
            self.log += '  '*level + str(msg) + '\n'

def toRects(cvResults):
    return [Rect(result) for result in cvResults]

def crop(image, offset, size):
    imageSize = Size(image)

    # If there will be a border, use CopyMakeBorder. 
    # Setting ROI, no border is created and resulting image is smaller
    if offset.x > 0 or \
       offset.y > 0 or \
       offset.x + imageSize.w < size.w or \
       offset.y + imageSize.h < size.h:

        # offset may have negative values, if there will be a right/bottom border
        offsTop = offset.y
        offsBottom = -(offset.y + imageSize.h - size.h)
        offsLeft = offset.x
        offsRight = -(offset.x + imageSize.w - size.w)

        image = image[max(0, -offset.y):min(-offset.y + size.h, imageSize.h), max(0, -offset.x):min(-offset.x + size.w, imageSize.w)]
        offsTop = max(0, offsTop)
        offsBottom = max(0, offsBottom)
        offsLeft = max(0, offsLeft)
        offsRight = max(0, offsRight)

        finalImg = cv.copyMakeBorder(image, offsTop, offsBottom, offsLeft, offsRight, GAP_BORDER)

        return finalImg

    else:
        return image[-offset.y:-offset.y + size.h, -offset.x:-offset.x + size.w]

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
        if fi != None:
            print(fi.log)
        print(msg)
