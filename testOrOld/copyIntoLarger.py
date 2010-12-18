from PIL import Image
import cv

img = cv.LoadImage('/home/rob/facealign/dat/raw/DSC05172.JPG', 1)
cv.SetImageROI(img, (0,0,1800,1800))
newImg = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 3)

cv.CvtColor(img, newImg, cv.CV_BGR2RGB)
pi = Image.fromstring("RGB", cv.GetSize(newImg), newImg.tostring())

#pi2.putdata(pi.getdata())
pi = pi.transform((2200,1800), Image.AFFINE, (1,0,-200,0,1,0))
pi.show()
