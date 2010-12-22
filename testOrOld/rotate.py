import cv, math

def markPoint(img, pt, color=(0,0,255), width=20):
	polys = [[(pt[0]-width/2, pt[1]-width/2), (pt[0]+width/2, pt[1]-width/2), (pt[0]+width/2, pt[1]+width/2), (pt[0]-width/2, pt[1]+width/2)]]
	cv.FillPoly(img, polys, color)

img = cv.LoadImage('../../dat/raw/DSC05172.JPG', 1)
markPoint(img, (2816/2, 2112/2))
#newImg = cv.CreateImage((2816,2112), cv.IPL_DEPTH_8U, 3)
newImg = cv.CloneImage(img)
matrix = cv.CreateMat(2, 3, cv.CV_32FC1)
cv.GetRotationMatrix2D((2816/2+150, 2112/2-150), -32, 1.0, matrix)
cv.WarpAffine(img, newImg, matrix)

cv.SaveImage('rotated.jpg', newImg)
