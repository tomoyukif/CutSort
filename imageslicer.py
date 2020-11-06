#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 10:18:43 2020

@author: ftom
"""

import os
import cv2
import csv
from skimage.io import imread

def imageslicer(in_file, out_dir, size_x, size_y, step_x, step_y):    
            
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    img = imread(in_file)
    root, ext = os.path.splitext(in_file)
    basename = os.path.basename(root)
    height, width, channels = img.shape[:3]

    slice_x0 = 0
    slice_y0 = 0
    slice_size_x = size_x
    slice_size_y = size_y
    slice_step_x = step_x
    slice_step_y = step_y

    cord_list = os.path.join(out_dir, "slice_coordinate.csv")  
    with open(cord_list, 'w') as f:
        tmp = ["image_file", "x0", "x1", "y0", "y1"]
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(tmp)
    
        while True:
            slice_x1 = slice_x0 + slice_size_x
            slice_y1 = slice_y0 + slice_size_y
            
            if slice_x1 > width:
                slice_x1 = width
                slice_x0 = slice_x1 - slice_size_x
            if slice_y1 > height:
                slice_y1 = height
                slice_y0 = slice_y1 - slice_size_y
    
            sliced_img = img[slice_y0:slice_y1, slice_x0:slice_x1]
            out_file = os.path.join(out_dir, basename + "_" + str(slice_y0) + "-" + str(slice_y1) + "_" + str(slice_x0) + "-" + str(slice_x1) + ext)
            cv2.imwrite(out_file, sliced_img)
            
            tmp = [out_file, slice_x0, slice_x1, slice_y0, slice_y1]
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(tmp)
            
            if slice_x1 == width:
                if slice_y1 == height:
                    break
                slice_x0 = 0
                slice_y0 = slice_y0 + slice_step_y
            else:
                slice_x0 = slice_x0 + slice_step_x