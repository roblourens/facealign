FaceAlign
========

FaceAlign is a tool that can be used to align a set of images containing faces. It is particularly useful for creating "time-lapse" face videos, such as this one: http://www.youtube.com/watch?v=iI8xVKO-kow

How it works
------------

FaceAlign is a Python script that uses [opencv python bindings](http://opencv.willowgarage.com/wiki/), which requires >= Python 2.6. It detects the location of the face in each image (opencv tends to err on the side of over-detection, and this tool will use the largest detected face) and will scale and offset the image so that the centers of the faces in all images will match up. This is based on parameters that can be easily set in config.py.

Usage
-----

Once python and opencv are installed, open config.py and set HCDIR to the folder containing your opencv installation's Haar cascade files.

Run sizeToFace.py. It takes a required input directory parameter, and an optional output directory parameter. The output directory will be created if it does not already exist. By default, images will be output to the current directory. Output file names will be numbered starting with 0001.jpg.

$ python src/sizeToFace.py ../in-images

$ python src/sizeToFace.py ../in-images ../out-images

Eventual plans
--------------

* Originally, I planned to detect each eye so that the image could be rotated in addition to scaled and translated. This was abandoned due to some complications including reflections in my glasses screwing up opencv's eye detection. I still hope to make this work, or at least detect a failure and fall back on face detection.
* Brightness/contrast normalization
* Integration with ffmpeg for automatic video generation
* A GUI

So what's up?
-------------

Feedback, ideas, issue reports, and contributions are invited. Welcomed. Demanded, even. FaceAlign is fairly simple at the moment but I would be interested to hear if you found it useful. 
