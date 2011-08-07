#: The path to the opencv install's Haar cascade folder
HCDIR = '/opt/local/share/opencv/haarcascades/'

#: The name of the Haar cascade file to use 
HCNAME = 'haarcascade_frontalface_default.xml'

#: If True, print debug info
DEBUG = True

#: If true, will mark the largest face on the image
MARKPOINTS = False

#: If true, will mark all faces on the image
MARKALL = False

#: The final image height
HEIGHT_TARGET = 720;

#: The final image width
WIDTH_TARGET = 960;

#: The target faceWidth:imageHeight
FACEW_RATIO_TARGET = .6

#: The ideal distance between eyes
FACEW_TARGET = FACEW_RATIO_TARGET*HEIGHT_TARGET

#: The ideal x and y-components of the position of the midpoint of the face
MID_X_TARGET = WIDTH_TARGET*.5
MID_Y_TARGET = HEIGHT_TARGET*.5

#: What is used when the image must be offset too far? 0 for black border, 1 for stretch colors
GAP_BORDER = 1
