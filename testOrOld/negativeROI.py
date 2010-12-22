import cv

img = cv.LoadImage('../../dat/raw/DSC05172.JPG', 1)
cv.SetImageROI(img, (1000, 1000, 1000, 1000))
newImg = cv.CreateImage((1000, 1000), cv.IPL_DEPTH_8U, 3)
cv.CopyMakeBorder(img, newImg, (0, 0), 0)

cv.SaveImage('test.jpg', newImg)
