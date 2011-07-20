#!/usr/bin/python
 
# sizeToFace.py
 
# Face Detection using OpenCV
 
# Usage: python sizeToFace.py <image_directory> optional: <output_directory>
# ffmpeg -r 15 -b 1800 -i %4d.JPG -i testSong.mp3 test1800.avi
 
import FaceImage
from multiprocessing import Pool
import sys, os
from operator import itemgetter

def main():
    # Get input files, sort by last modified time
    files = sortedImages(sys.argv[1])

    if len(files) == 0:
        print('No jpg files found in ' + sys.argv[1])
        return

    if len(sys.argv) > 2:
        outdir = sys.argv[2]
    else:
        outdir = '.'
    
    i=0
    pool = Pool()

    # For every JPG in the given directory
    for file in files:
        filepath = file[1]
        i += 1
        savename = os.path.join(outdir, '%04d.jpg' % i)

        print('Added to pool: ' + filepath + ' with output path: ' + savename)
        pool.apply_async(FaceImage.runFaceImage, (filepath, savename))

    pool.close()
    pool.join()

def sortedImages(inputDir):
    files = []
    for dirpath, dirnames, filenames in os.walk(inputDir):
        for file in filenames:
            if file.upper().endswith('.JPG') or file.upper().endswith('.JPEG'):
                # If a jpeg file
                filePath = os.path.join(dirpath, file)
                files.append((os.stat(filePath).st_mtime, filePath))

    # Sort by last modified, then by path
    # (some old pics in my set have an equal recent modified time)
    files.sort()
    files.sort(key=itemgetter(1))
    return files

if __name__ == "__main__":
    main()

