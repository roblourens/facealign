import cv

image = cv.LoadImage('/home/rob/facealign/in/01.JPG', 1)
cv.Rectangle(image, (0,0), (20,20), (255,255,255))
win = 'test'
cv.NamedWindow(win, 1)
cv.ShowImage(win, image)
cv.SaveImage('/home/rob/facealign/out.jpg', image)
