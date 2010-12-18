#!/usr/bin/python
 
# face_detect.py
 
# Face Detection using OpenCV. Based on sample code from:
# http://python.pastebin.com/m76db1d6b
 
# Usage: python face_detect.py <image_directory>
 
import sys, os
import cv
 
def detectObjects(image, i):
  """Saves the image with a red rectangle drawn around the faces detected"""
  cascade = cv.Load('/usr/share/opencv/haarcascades/haarcascade_righteye_2splits.xml')
  faces = cv.HaarDetectObjects(image, cascade, cv.CreateMemStorage())
 
  if faces:
    for (x,y,w,h),n in faces: # What is n? How does this work?
      cv.Rectangle(image, (x,y), (x+w,y+h), (255,0,0)) # BGR
      print("eye found from (" + str(x)+", "+str(y)+") to ("+str(x+w)+", "+str(y+h)+")")
      cv.SetImageROI(image, (x,y,w,h))
      cv.SaveImage("output"+str(x)+".jpg", image)
      cv.ResetImageROI(image)
      
    cv.SaveImage("output"+str(i)+".jpg", image)

def main():
  i=0
  for file in os.listdir(sys.argv[1]):
    if file.endswith('.JPG'):
      filePath = os.path.join(sys.argv[1], file)
      print('\nconverting ' + filePath)
      image = cv.LoadImage(filePath, 1) # Second argument 0 is for grayscale
      detectObjects(image, i)
      i += 1
 
if __name__ == "__main__":
  main()
