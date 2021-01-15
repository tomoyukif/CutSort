# ImageSorter
ImageSorter is a GUI-based image processing tool which provides the following functions.
1. Generate sliced images from an input image.
2. Sort image files into separate folders based on annotation information generated via [RectLabel](https://rectlabel.com/).

# Installation
Download the file in thie repository and put "CutSort.app" somewhere you like.
"CutSort.app" is an executable file on Mac OS X 10.15 or later.

# Dependencies
ImageSorter is written in Python and requires libraries listed below.  
- cv2
- scikit-image
- scipy
- numpy
- pandas
- csv
- xml

All codes are only tested using Python3.7.

The executable file of ImageSorter (ImageSorter.app) is also found in this repository.
ImageSorter.app is expected to be able to run on Windows, Mac OS, and Linux machines.

# Usage
Execute ImageSorter.app or type 
```
python /path/to/imagesorter/mian.py
```

When you execute ImageSorter, you will see a window like shown below.  
<kbd>![top window](./images/topwindow.png)</kbd>  

Click the "Image Slicer" tab to slice a image into pieses.  
"File sorter" enable you to classify image files in an input folder into separate folders based on annotation information generated via [RectLabel](https://rectlabel.com/).  



## Image Slicer
<kbd>![slicer](./images/slicer.png)</kbd>  


## File Sorter
<kbd>![sorter](./images/sorter.png)</kbd>
