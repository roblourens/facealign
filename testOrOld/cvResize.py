import cv

img = cv.LoadImage('/home/rob/facealign/dat/raw/DSC05172.JPG', 1)
newImg = cv.CreateImage((1000,1000), cv.IPL_DEPTH_8U, 3)

cv.Resize(img, newImg, cv.CV_INTER_CUBIC)

cv.SaveImage('/home/rob/facealign/dat/raw/out/out.jpg', newImg)
