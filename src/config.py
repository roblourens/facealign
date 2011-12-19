#: The path to the opencv install's Haar cascade folder
HCDIR = '/opt/local/share/opencv/haarcascades/'

#: The name of the Haar cascade file to use 
HCNAME = 'haarcascade_frontalface_alt2.xml'

#: If True, print debug info
DEBUG = True

#: If true, will mark the largest face on the image
MARKFACE = False

#: If true, will mark all faces on the image
MARKALL = True

#: If true, don't perform the scale or offset (useful for debugging with MARKALL)
NOTRANSFORM = True

#: The final image height
HEIGHT_TARGET = 720;

#: The final image width
WIDTH_TARGET = 960;


# You probably don't need to change anything below this point

#: The target faceWidth:imageHeight
FACEW_RATIO_TARGET = .6

#: The target distance between eyes
FACEW_TARGET = FACEW_RATIO_TARGET*HEIGHT_TARGET

#: The target face midpoint coords:image ratio
MID_X_TARGET_RATIO = .5
MID_Y_TARGET_RATIO = .5

#: The target x and y-components of the position of the midpoint of the face
MID_X_TARGET = WIDTH_TARGET*MID_X_TARGET_RATIO
MID_Y_TARGET = HEIGHT_TARGET*MID_Y_TARGET_RATIO

#: What is used when the image must be offset too far? 0 for black border, 1 for stretch colors
GAP_BORDER = 1
