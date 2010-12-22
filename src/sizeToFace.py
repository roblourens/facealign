#!/usr/bin/python
 
# sizeToFace.py
 
# Face Detection using OpenCV. Based on sample code from:
# http://python.pastebin.com/m76db1d6b
 
# Usage: python sizeToFace.py <image_directory>
# ffmpeg -r 15 -b 1800 -i %4d.JPG -i testSong.mp3 test1800.avi
 
#: The number of processing Threads to spawn
N_THREADS = 4

import FaceImage
from multiprocessing import Pool
import sys, os

def main():
    # Get input files, sort by last modified time
    files = sortedImages(sys.argv[1])
    
    i=0
    errors = []
    pool = Pool()

    # For every JPG in the given directory
    for file in files:
        filepath = file[1]
        print('Added to pool ' + filepath)
        i += 1
        
        savename = '/Users/rob/code/facealign/dat/outtest/%04d.jpg' % i
        pool.apply_async(FaceImage.runFaceImage, (filepath, savename))
 
    pool.close()
    pool.join()

def sortedImages(inputDir):
    files = []
    for file in os.listdir(inputDir):
        if file.upper().endswith('.JPG') or file.upper().endswith('.JPEG'):
            # If a jpeg file
            filePath = os.path.join(inputDir, file)
            files.append((os.stat(filePath).st_mtime, filePath))
    files.sort()
    return files

if __name__ == "__main__":
    main()

