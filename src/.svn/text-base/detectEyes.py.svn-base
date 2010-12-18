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
#: The ideal image height
HEIGHT_TARGET = 480;
#: The ideal image width
WIDTH_TARGET = 720;
#: The ideal eyeWidth:imageHeight
EYEW_RATIO_TARGET = .1135
#: The ideal distance between eyes
EYEW_TARGET = EYEW_RATIO_TARGET*HEIGHT_TARGET
#: The ideal x-component of the position of the midpoint between the eyes
MID_X_TARGET = WIDTH_TARGET*.5
#: The ideal y-component of the position of the midpoint between the eyes
MID_Y_TARGET = HEIGHT_TARGET*.4

""" Takes an openCV image, a haarcascade XML file, and an int for right(0) or 
	left(1) eye (image's l/r not yours), returns coords of the eye """
def getEyeCoords(image, haarFile, side):
	if debug: print("\tgetEyeCoords, side = " + str(side))
	cascade = cv.Load(haarFile)
	eyes = cv.HaarDetectObjects(image, cascade, cv.CreateMemStorage())

	# Several eyes will probably be found. Look at the largest two, if they are close in
	# size, pick the side=0:leftmost or side=1:rightmost one
	if eyes:
		max1 = max2 = (0,0,0,0,0) # x, y, w, h, w*h of largest eyes
		for (x,y,w,h),n in eyes: # What is n? How does this work?
			if debug: print("\t\tEye found from (" + str(x)+", "+str(y)+") to ("+str(x+w)+", "+str(y+h)+"), A: "+str(w*h))
			
			# max1 will be the largest, max2 second largest
			if w*h > max1[4]:
				max2 = max1
				max1 = (x, y, w, h, w*h)
			elif w*h > max2[4]:
				max2 = (x, y, w, h, w*h)
				
		if max1[4]-max2[4] < 20000 or max2[4]>=50000: # Mess around to figure out what works
			# If we're looking for right eyes, pick the leftmost, else pick the rightmost
			if side == 0:
				eye = max1 if max1[0] < max2[0] else max2
			elif side == 1:
				eye = max1 if max1[0] > max2[0] else max2
		else:
			eye = max1
		
		return eye
	else:
		return None
		
	
""" Rotates the given image by the given angle in radians """
def rotateImg(img, angle, pt):
	size = cv.GetSize(img)
	alpha = math.cos(angle)
	beta = math.sin(angle)
	m = [[alpha, beta, size[0]/2 + pt[0]], 
		 [-beta, alpha, size[1]/2 + pt[1]]]
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

def cropImg(img, newSize, newCorner=(0,0)):
	if debug: print('\tCropping w/corner: ' + str(newCorner))
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
def cropToEyes(image, saveName):
	origSize = cv.GetSize(image)
	rightEye = getEyeCoords(image, '/usr/share/opencv/haarcascades/haarcascade_righteye_2splits.xml', 0)
	leftEye = getEyeCoords(image, '/usr/share/opencv/haarcascades/haarcascade_lefteye_2splits.xml', 1)
	if rightEye == None: 
		print('No right eye found')
		return
	if leftEye == None: 
		print('No left eye found')
		return
	
	midR = (rightEye[0]+rightEye[2]/2, rightEye[1]+rightEye[3]/2)	# The midpoint of the right eye
	midL = (leftEye[0]+leftEye[2]/2, leftEye[1]+leftEye[3]/2)		# The midpoint of the left eye
	mid = (midL[0]/2 + midR[0]/2, midL[1]/2 + midR[1]/2)			# The point between the eyes
	if debug: print('\tEyes at: ' + str(midR) + ' and ' + str(midL))
	if markPoints:
		markPoint(image, midR)
		markPoint(image, midL)
	
	# Calculate scaling params based on eyeWidth
	eyeWidth = (midL[0]-midR[0])/2 + 0.0 # Make eyeWidth a double
	scaleF = EYEW_TARGET/eyeWidth
	scSize = (int(origSize[0]*scaleF), int(origSize[1]*scaleF))
	scMid = (mid[0]*scaleF, mid[1]*scaleF)
	if debug: print('\tScaling to ' + str(scSize))
	print(EYEW_TARGET)
	if debug: print('\tEye width: ' + str(eyeWidth))
	
	# Scale image
	scImg = cv.CreateImage(scSize, cv.IPL_DEPTH_8U, 3)
	cv.Resize(image, scImg, cv.CV_INTER_CUBIC)
	
	if markPoints: markPoint(scImg, scMid, (255,0,0))
	
	# Determine translation
	newCorner = (int(scMid[0]-MID_X_TARGET), int(scMid[1]-MID_Y_TARGET))
	if debug: print("\tnewCorner: " + str(newCorner))
	
	"""# If any part of the image will be out of bounds, process as PIL
	if newCorner[0]<0 or newCorner[1]<0 or newCorner[0]>cv.GetSize(scImg)[0]-WIDTH_TARGET or newCorner[1]>cv.GetSize(scImg)[1]-HEIGHT_TARGET:
		rgbImg = cv.CreateImage(cv.GetSize(scImg), cv.IPL_DEPTH_8U, 3) 			# Create new image with same size, hopefully same depth, 3 channels
		cv.CvtColor(scImg, rgbImg, cv.CV_BGR2RGB) 								# Convert BGR to RGB
		
		pilImg = Image.fromstring("RGB", cv.GetSize(rgbImg), rgbImg.tostring()) # Create PIL image with same data
		pilImg = pilImg.transform((WIDTH_TARGET,HEIGHT_TARGET), Image.AFFINE, (1,0,newCorner[0],0,1,newCorner[1])) # Transform to final size, position
		
		# Back to IPLImage
		scImg = cv.CreateImage(pilImg.size, cv.IPL_DEPTH_8U, 3)
		scImg.imageData = pilImg.tostring() # Doesn't work
		
	else:
		# Set ROI for scaled image
		cv.SetImageROI(scImg, (newCorner[0],newCorner[1],WIDTH_TARGET,HEIGHT_TARGET)) # 2nd argument takes corner, w, h, not two points
	"""

	scImg = cropImg(scImg, (HEIGHT_TARGET, WIDTH_TARGET), newCorner)
	cv.SetImageROI(scImg, (0, 0, WIDTH_TARGET,HEIGHT_TARGET)) # 2nd argument takes corner, w, h, not two points
	if markPoints: markPoint(scImg, (MID_X_TARGET, MID_Y_TARGET), (0,255,0))
		
	# Determine rotation
	angle = math.atan(float(midR[1]-midL[1])/float(midR[0]-midL[0]))
	if debug: print("\tRotating " + str(angle) + " radians")
	
	# Rotate about scMid
#	scImg = rotateImg(scImg, angle, scMid)
	
	# Finally, save
	print('Saving to ' + saveName + '\n')
	cv.SaveImage(saveName, scImg)
		
def markPoint(img, pt, color=(0,0,255), width=20):
	polys = [[(pt[0]-width/2, pt[1]-width/2), (pt[0]+width/2, pt[1]-width/2), (pt[0]+width/2, pt[1]+width/2), (pt[0]-width/2, pt[1]+width/2)]]
	cv.FillPoly(img, polys, color)

def main():
	# Get input files, sort
	inputDir = sys.argv[1]
	files = os.listdir(inputDir)
	files.sort()
	
	i=0
	# For every JPG in the given directory
	for file in files:
		# If a jpeg file
		if file.upper().endswith('.JPG') or file.upper().endswith('.JPEG'):
			filePath = os.path.join(inputDir, file)
			print('Processing ' + filePath)
			
			# Open the image, cropToEyes sets ROI wrt eyes
			image = cv.LoadImage(filePath, 1); # Second argument is for 0:grayscale, 1:color
			saveName = '/home/rob/facealign/dat/raw/out2/%04d.jpg' % i
			cropToEyes(image, saveName)
			
			i = i+1
 
if __name__ == "__main__":
	main()
