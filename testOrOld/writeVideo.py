#! /usr/bin/python

import cv

def CV_FOURCC( c1, c2, c3, c4 ) :
	return (((ord(c1))&255)     \
		+ (((ord(c2))&255)<<8)  \
		+ (((ord(c3))&255)<<16) \
		+ (((ord(c4))&255)<<24))

vw = cv.CreateVideoWriter('vwTest.mpg', CV_FOURCC('P','I','M','1'), 30, (300,400))
print(vw)
image = cv.LoadImage('in/01.JPG', 1)
print(cv.WriteFrame(vw, image))
