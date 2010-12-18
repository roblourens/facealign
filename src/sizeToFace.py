#!/usr/bin/python
 
# face_detect.py
 
# Face Detection using OpenCV. Based on sample code from:
# http://python.pastebin.com/m76db1d6b
 
# Usage: python detectEyes.py <image_directory>
# ffmpeg -r 15 -b 1800 -i %2d.JPG -i testSong.mp3 test1800.avi
# Original pic size: 2816x2112
 
import sys, os, cv, math
from PIL import Image

debug = True
markPoints = False
#: The final image height
HEIGHT_TARGET = 480;
#: The final image width
WIDTH_TARGET = 720;
#: The target faceWidth:imageHeight
FACEW_RATIO_TARGET = .6
#: The ideal distance between eyes
FACEW_TARGET = FACEW_RATIO_TARGET*HEIGHT_TARGET
#: The ideal x-component of the position of the midpoint of the face
MID_X_TARGET = WIDTH_TARGET*.5
#: The ideal y-component of the position of the midpoint of the face
MID_Y_TARGET = HEIGHT_TARGET*.5

""" Takes an openCV image and a haarcascade XML file, returns coords of the face """
def getFaceCoords(image, haarFile):
    if debug: print('\tgetFaceCoords')
    cascade = cv.Load(haarFile)
    faces = cv.HaarDetectObjects(image, cascade, cv.CreateMemStorage())

    # Several faces will be found. Pick the largest.
    if faces:
        largest = (0,0,0,0,0) # x, y, w, h, w*h of largest eyes
        for (x,y,w,h),n in faces: # What is n? How does this work?
            if debug: print("\t\tFace found from (" + str(x)+", "+str(y)+") to ("+str(x+w)+", "+str(y+h)+"), A: "+str(w*h))
            
            # max1 will be the largest, max2 second largest
            if w*h > largest[4]:
                largest = (x, y, w, h, w*h)

        return largest
    else:
        return None
        
    
def cropImg(img, newSize, newCorner=(0,0)):
    size = cv.GetSize(img)
    m = [[1, 0, size[0]/2 + newCorner[0]], 
         [0, 1, size[1]/2 + newCorner[1]]]
    transl = cv.CreateMat(2, 3, cv.CV_32FC1)
    
    cv.mSet(transl, 0, 0, m[0][0])
    cv.mSet(transl, 1, 1, m[1][1])
    cv.mSet(transl, 0, 1, m[0][1])
    cv.mSet(transl, 0, 2, m[0][2])
    cv.mSet(transl, 1, 2, m[1][2])
    cv.mSet(transl, 1, 0, m[1][0])
    
    newImg = cv.CloneImage(img)
    cv.GetQuadrangleSubPix(img, newImg, transl)
    return newImg
    
""" Takes an openCV image, finds the eye positions, and sets ROI appropriately"""
def cropToFace(image, saveName):
    origSize = cv.GetSize(image)
    face = getFaceCoords(image, '/usr/local/share/opencv/haarcascades/haarcascade_frontalface_default.xml')
    if face == None: 
        print('No face found')
        raise Exception('No face found')
        
    if markPoints: cv.Rectangle(image, (face[0], face[1]), (face[0]+face[2], face[1]+face[3]), (0,0,255))
    
    mid = (face[0] + face[2]/2, face[1] + face[3]/2)            # The middle of the face
    if debug: print('\tFace at: ' + str(mid) + ', should be: (' + str(MID_X_TARGET) + ', ' + str(MID_Y_TARGET) + ')')
    if markPoints:
        markPoint(image, mid)
    
    # Calculate scaling params based on eyeWidth
    faceWidth = float(face[2]) # Make eyeWidth a double
    scaleF = FACEW_TARGET/faceWidth
    scSize = (int(origSize[0]*scaleF), int(origSize[1]*scaleF))
    scMid = (mid[0]*scaleF, mid[1]*scaleF)
    if debug: print('\tFace width: ' + str(faceWidth) + ' should be: ' + str(FACEW_TARGET))
    if debug: print('\tScaling to ' + str(scSize))
    
    # Scale image
    scImg = cv.CreateImage(scSize, cv.IPL_DEPTH_8U, 3)
    cv.Resize(image, scImg, cv.CV_INTER_CUBIC)
    
    # Determine translation
    newCorner = (int(scMid[0]-MID_X_TARGET), int(scMid[1]-MID_Y_TARGET))
    if debug: print("\tnewCorner: " + str(newCorner))
    
    # If any part of the image will be out of bounds, process as PIL
    if newCorner[0]<0 or newCorner[1]<0 or newCorner[0]>cv.GetSize(scImg)[0]-WIDTH_TARGET or newCorner[1]>cv.GetSize(scImg)[1]-HEIGHT_TARGET:
        rgbImg = cv.CreateImage(cv.GetSize(scImg), cv.IPL_DEPTH_8U, 3)             # Create new image with same size, hopefully same depth, 3 channels
        cv.CvtColor(scImg, rgbImg, cv.CV_BGR2RGB)                                 # Convert BGR to RGB
        
        pilImg = Image.fromstring("RGB", cv.GetSize(rgbImg), rgbImg.tostring()) # Create PIL image with same data
        pilImg = pilImg.transform((WIDTH_TARGET,HEIGHT_TARGET), Image.AFFINE, (1,0,newCorner[0],0,1,newCorner[1])) # Transform to final size, position
        
        # Save image
        print('Saving to ' + saveName + '\n')
        pilImg.save(saveName)
        
    else:
        # Set ROI for scaled image
        cv.SetImageROI(scImg, (newCorner[0],newCorner[1],WIDTH_TARGET,HEIGHT_TARGET)) # 2nd argument takes corner, w, h, not two points
        print('Saving to ' + saveName + '\n')
        cv.SaveImage(saveName, scImg)
    
    """
    scImg = cropImg(scImg, (HEIGHT_TARGET, WIDTH_TARGET), newCorner)
    cv.SetImageROI(scImg, (0, 0, WIDTH_TARGET,HEIGHT_TARGET)) # 2nd argument takes corner, w, h, not two points
    if markPoints: markPoint(scImg, (MID_X_TARGET, MID_Y_TARGET), (0,255,0))

    
    # Determine rotation
    angle = math.atan(float(midR[1]-midL[1])/float(midR[0]-midL[0]))
    if debug: print("\tRotating " + str(angle) + " radians")
    
    # Rotate about scMid
    scImg = rotateImg(scImg, angle, scMid)
    

    # Finally, save
    print('Saving to ' + saveName + '\n')
    cv.SaveImage(saveName, scImg)
    """
        
def markPoint(img, pt, color=(0,0,255), width=20):
    polys = [[(pt[0]-width/2, pt[1]-width/2), (pt[0]+width/2, pt[1]-width/2), (pt[0]+width/2, pt[1]+width/2), (pt[0]-width/2, pt[1]+width/2)]]
    cv.FillPoly(img, polys, color)

def main():
    # Get input files, sort by last modified time
    inputDir = sys.argv[1]
    
    files = []
    for file in os.listdir(inputDir):
        if file.upper().endswith('.JPG') or file.upper().endswith('.JPEG'):
            # If a jpeg file
            filePath = os.path.join(inputDir, file)
            files.append((os.stat(filePath).st_mtime, filePath))
    files.sort()
    
    i=0
    errors = []
    # For every JPG in the given directory
    for file in files:
        filePath = file[1]
        print('Processing ' + filePath)
        i = i + 1
        
        try:
            # Open the image, cropToEyes sets ROI wrt eyes
            image = cv.LoadImage(filePath, 1); # Second argument is for 0:grayscale, 1:color
            saveName = '/home/rob/facealign/dat/raw/outAnna/%04d.jpg' % i
            cropToFace(image, saveName)
            
        except Exception as e:
            print(type(e))
            print(e.args)
            print(e)
            errors.append(filePath)
            
    if errors: print("Incomplete: " + str(errors))
 
if __name__ == "__main__":
    main()
