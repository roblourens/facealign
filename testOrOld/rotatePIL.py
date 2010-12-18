import math
from PIL import Image

def getRotMatrix():
	rad = math.radians(10)
	alpha = math.cos(rad)
	beta = math.sin(rad)
	
#	m = [[alpha, beta, (1 - alpha)*2816/2 - beta*2112/2], 
#	     [-beta, alpha, beta*2816/2 - (1 - alpha)*2816/2]]

	m = (alpha, beta, (1 - alpha)*2816/2 - beta*2112/2, 
	     -beta, alpha, beta*2816/2 - (1 - alpha)*2816/2)

	
	return m
	
img = Image.open('../dat/raw/DSC05172.JPG')

m = getRotMatrix()

#img = img.transform((2816,2112), Image.AFFINE, m)
img = img.transform((4500, 2112), Image.AFFINE, (1, 0, -1500, 0, 1, 0))
img = img.transform((2816, 2112), Image.AFFINE, (1, 0, 1500, 0, 1, 0))
img.show()
