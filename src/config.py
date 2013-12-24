#: The path to the opencv install's Haar cascade folder
HCDIR = 'C:/opencv/sources/data/haarcascades/'

#: The name of the eyepair Haar cascade file to use
HC_EYEPAIR_NAME = 'haarcascade_mcs_eyepair_big.xml'

#: The name of the left eye Haar cascade file to use
HC_LEFTEYE_NAME = 'haarcascade_lefteye_2splits.xml'

#: The name of the right eye Haar cascade file to use
HC_RIGHTEYE_NAME = 'haarcascade_righteye_2splits.xml'

#: The name of the face Haar cascade file to use
HC_FACE_NAME = 'haarcascade_frontalface_alt2.xml'

#: If True, print debug info
DEBUG = True

#: If true, will mark on the image the eyes/eyepairs which were selected to be used for calculations
MARKUSED = True

#: If true, will mark all eyes/eyepairs on the image
MARKALL = True

#: If true, don't perform the scale or offset (useful for debugging with MARKALL)
NOTRANSFORM = False

#: The final image height
HEIGHT_TARGET = 720

#: The final image width
WIDTH_TARGET = 960

#: What is used when the image must be offset too far? 0 for black border, 1 for stretch colors
GAP_BORDER = 1



# Feature marking colors

#: The color used to mark eyepairs
EYEPAIR_COLOR = (255, 0, 0)

#: The color used to mark left eyes
LEFT_EYE_COLOR = (0, 255, 0)

#: The color used to mark right eyes
RIGHT_EYE_COLOR = (0, 0, 255)

#: The color used to mark faces
FACE_COLOR = (0, 255, 255)

#: The color used to mark eye/eyepair center points
MIDPOINT_COLOR = (100, 100, 100)



# You probably don't need to change anything below this point

#: The target eyeWidth:imageHeight
EYEW_RATIO_TARGET = .25

#: The target distance between eyes
EYEW_TARGET = EYEW_RATIO_TARGET*HEIGHT_TARGET

#: The target face midpoint coords:image ratio
MID_X_TARGET_RATIO = .5
MID_Y_TARGET_RATIO = .4

#: The target x and y-components of the position of the midpoint of the face
MID_X_TARGET = WIDTH_TARGET*MID_X_TARGET_RATIO
MID_Y_TARGET = HEIGHT_TARGET*MID_Y_TARGET_RATIO

#: An eyepair is probably valid with this width/height ratio
EYEPAIR_RATIO = 2

#: Conversion factor between the width of an eyepair and the width between eyes, 
# used when valid eyes are not detected and the eyepair is used to calculate scaling factors
EYEPAIR_WIDTH_TO_EYE_WIDTH = .7

#: The minimum size detection threshold for eyepair
EYEPAIR_MIN_SIZE = (.15, .03)

#: The minimum distance threshold for left/right eye. Usually just necessary to
# ensure that detected left/right eyes w/o eyepair are not the same eye
EYE_MIN_DISTANCE = .05

#: The estimated y-coordinate of an eye on the face
# Used when we fall back on face detection from eye detection
EYE_FACE_RELATIVE_Y = .5

#: The estimated width of an eyepair relative to the face
# Used when we fall back on face detection from eye detection
EYE_FACE_RELATIVE_WIDTH = .8
