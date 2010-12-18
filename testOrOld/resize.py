import sys, os
from PIL import Image

inputDir = sys.argv[1]
files = os.listdir(inputDir)

for file in files:
	if file.upper().endswith('.JPG') or file.upper().endswith('.JPEG'):
		filePath = os.path.join(inputDir, file)
		print('Smallifying ' + filePath)
		img = Image.open(filePath)
		img = img.resize((640,480), Image.ANTIALIAS)
	
		img.save('/home/rob/facealign/dat/raw/out/small/'+file)
