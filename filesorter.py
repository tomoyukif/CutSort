#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 12:00:52 2020

@author: ftom
"""

import os
import cv2
import xml.etree.ElementTree as et
import glob
import csv
import pandas as pd
import numpy as np
import scipy.stats as stats
import colorcodes as cc
from skimage import io, draw

            
def make_object_list(in_dir, out_dir):
    out_list = os.path.join(out_dir, "object_list.csv")
    
    with open(out_list, 'w') as f_out:
        tmp = ["xml_file", "image_file", "annotation", "xmin", "ymin", "xmax", "ymax"]
        writer = csv.writer(f_out, lineterminator='\n')
        writer.writerow(tmp)
        
        for xml in glob.glob(os.path.join(in_dir, "*.xml")):
            xml_parsed = et.parse(xml)
            root = xml_parsed.getroot()
            img_file = root.find('filename').text
            
            for entry in root:
                if entry.tag =='object':
                    ano = entry.find('name').text
                    bndbox = entry.find('bndbox')
                    xmin = bndbox.find('xmin').text
                    ymin = bndbox.find('ymin').text
                    xmax = bndbox.find('xmax').text
                    ymax = bndbox.find('ymax').text
                    record = [xml, img_file, ano, xmin, ymin, xmax, ymax]
                    writer.writerow(record)
    return(out_list)

def clean_dup_objects(out_dir, object_list, threshold, voting):
    object_list = pd.read_csv(object_list)
    class_names = object_list.annotation.drop_duplicates().sort_values(ascending=True)
    class_names = class_names.reset_index(drop = True)
    updated_records = pd.DataFrame()
    
    if voting:
        xmin = np.array([object_list.xmin])
        xmax = np.array([object_list.xmax])
        ymin = np.array([object_list.ymin])
        ymax = np.array([object_list.ymax])
        box_size_x = xmax - xmin
        box_size_y = ymax - ymin
        x_dist = np.rot90(xmax, 3) - xmin
        x_dist_flip = x_dist > np.rot90(np.flipud(x_dist), 3)
        x_dist[x_dist_flip] = np.rot90(np.flipud(x_dist), 3)[x_dist_flip]        
        overlap_x = x_dist / box_size_x
        y_dist = np.rot90(ymax, 3) - ymin
        y_dist_flip = y_dist > np.rot90(np.flipud(y_dist), 3)
        y_dist[y_dist_flip] = np.rot90(np.flipud(y_dist), 3)[y_dist_flip]        
        overlap_y = y_dist / box_size_y
        invalid_x_y = np.logical_or(overlap_y < 0, overlap_x < 0)
        invalid_x_y = np.logical_or(invalid_x_y, np.rot90(np.flipud(invalid_x_y), 3))
        overlap_x[invalid_x_y] = 0
        overlap_y[invalid_x_y] = 0
        overlap_area = overlap_x * overlap_y
        valid_overlaps = overlap_area > threshold
        valid_overlaps = np.logical_or(valid_overlaps, np.rot90(np.flipud(valid_overlaps), 3))
        for record_i in valid_overlaps:
            valid_overlaps[record_i, :] = np.sum(valid_overlaps[record_i, :], axis = 0) != 0
        
        vote_annotation = valid_overlaps * np.array([object_list.annotation])
        mode_annotations = []
        for i in vote_annotation:
            tmp = i[i != '']
            mode_annotations = np.append(mode_annotations, stats.mode(tmp)[0])
        
        overlaps_xmin = valid_overlaps * xmin
        overlaps_xmin = overlaps_xmin.astype('float')
        overlaps_xmin[overlaps_xmin == 0] = np.nan
        overlaps_mean_xmin = np.nanmean(overlaps_xmin, 1).astype('int')
        overlaps_xmax = valid_overlaps * xmax
        overlaps_xmax = overlaps_xmax.astype('float')
        overlaps_xmax[overlaps_xmax == 0] = np.nan
        overlaps_mean_xmax = np.nanmean(overlaps_xmax, 1).astype('int')
        overlaps_ymin = valid_overlaps * ymin
        overlaps_ymin = overlaps_ymin.astype('float')
        overlaps_ymin[overlaps_ymin == 0] = np.nan
        overlaps_mean_ymin = np.nanmean(overlaps_ymin, 1).astype('int')
        overlaps_ymax = valid_overlaps * ymax
        overlaps_ymax = overlaps_ymax.astype('float')
        overlaps_ymax[overlaps_ymax == 0] = np.nan
        overlaps_mean_ymax = np.nanmean(overlaps_ymax, 1).astype('int')        
        updated_records = np.vstack([overlaps_mean_xmin, overlaps_mean_ymin, overlaps_mean_xmax, overlaps_mean_ymax])
        updated_records = pd.DataFrame(np.rot90(np.flipud(updated_records), 3))
        mode_annotations = mode_annotations.reshape(updated_records.shape[0])
        updated_records = pd.concat([updated_records, pd.Series(mode_annotations)], axis=1)
        updated_records = updated_records.drop_duplicates()
        updated_records = updated_records.reset_index(drop = True)
        
    else:
        for class_i in class_names:
            class_i_record = object_list.loc[object_list.annotation == class_i]
            xmin = np.array([class_i_record.xmin])
            xmax = np.array([class_i_record.xmax])
            ymin = np.array([class_i_record.ymin])
            ymax = np.array([class_i_record.ymax])
            box_size_x = xmax - xmin
            box_size_y = ymax - ymin
            x_dist = np.rot90(xmax, 3) - xmin
            x_dist_flip = x_dist > np.rot90(np.flipud(x_dist), 3)
            x_dist[x_dist_flip] = np.rot90(np.flipud(x_dist), 3)[x_dist_flip]        
            overlap_x = x_dist / box_size_x
            y_dist = np.rot90(ymax, 3) - ymin
            y_dist_flip = y_dist > np.rot90(np.flipud(y_dist), 3)
            y_dist[y_dist_flip] = np.rot90(np.flipud(y_dist), 3)[y_dist_flip]        
            overlap_y = y_dist / box_size_y
            invalid_x_y = np.logical_or(overlap_y < 0, overlap_x < 0)
            invalid_x_y = np.logical_or(invalid_x_y, np.rot90(np.flipud(invalid_x_y), 3))
            overlap_x[invalid_x_y] = 0
            overlap_y[invalid_x_y] = 0
            overlap_area = overlap_x * overlap_y
            valid_overlaps = overlap_area > threshold
            valid_overlaps = np.logical_or(valid_overlaps, np.rot90(np.flipud(valid_overlaps), 3))
            for record_i in valid_overlaps:
                valid_overlaps[record_i, :] = np.sum(valid_overlaps[record_i, :], axis = 0) != 0
            
            overlaps_xmin = valid_overlaps * xmin
            overlaps_xmin = overlaps_xmin.astype('float')
            overlaps_xmin[overlaps_xmin == 0] = np.nan
            overlaps_mean_xmin = np.nanmean(overlaps_xmin, 1).astype('int')
            overlaps_xmax = valid_overlaps * xmax
            overlaps_xmax = overlaps_xmax.astype('float')
            overlaps_xmax[overlaps_xmax == 0] = np.nan
            overlaps_mean_xmax = np.nanmean(overlaps_xmax, 1).astype('int')
            overlaps_ymin = valid_overlaps * ymin
            overlaps_ymin = overlaps_ymin.astype('float')
            overlaps_ymin[overlaps_ymin == 0] = np.nan
            overlaps_mean_ymin = np.nanmean(overlaps_ymin, 1).astype('int')
            overlaps_ymax = valid_overlaps * ymax
            overlaps_ymax = overlaps_ymax.astype('float')
            overlaps_ymax[overlaps_ymax == 0] = np.nan
            overlaps_mean_ymax = np.nanmean(overlaps_ymax, 1).astype('int')        
            mean_objects = np.vstack([overlaps_mean_xmin, overlaps_mean_ymin, overlaps_mean_xmax, overlaps_mean_ymax])
            mean_objects = pd.DataFrame(np.rot90(np.flipud(mean_objects), 3))
            mean_objects = mean_objects.drop_duplicates()
            mean_objects = mean_objects.reset_index(drop = True)
            updated_tmp = pd.concat([mean_objects, pd.Series([class_i] * mean_objects.shape[0])], axis=1)
            updated_records = pd.concat([updated_records, updated_tmp])
            
    updated_records.columns = ['xmin', 'ymin', 'xmax', 'ymax', 'annotation']
    annotation_counts = updated_records.annotation.value_counts()
    ann_counts_path = os.path.join(out_dir, 'annotation_counts.csv')
    annotation_counts.to_csv(ann_counts_path, header = False)
    out_record_path = os.path.join(out_dir, 'updated_list.csv')
    updated_records.to_csv(out_record_path)
    return(out_record_path)

        
def merge_slices(in_dir, out_dir, object_list):
    object_list = pd.read_csv(object_list)    
    
    slice_coordinate = os.path.join(in_dir, 'slice_coordinate.csv')
    slice_coordinate = pd.read_csv(slice_coordinate)
    img_width = slice_coordinate.x1.max()
    img_height = slice_coordinate.y1.max()
    ori_img = np.zeros((img_height, img_width, 3), np.uint8)
    
    for slice_file in slice_coordinate.image_file:
        tmp_img = cv2.imread(slice_file)
        record = slice_coordinate[slice_coordinate.image_file == slice_file]
        ori_img[int(record.y0):int(record.y1), int(record.x0):int(record.x1)] = tmp_img
        object_list.loc[object_list.image_file == os.path.split(slice_file)[1], ['xmin', 'xmax']] += int(record.x0)
        object_list.loc[object_list.image_file == os.path.split(slice_file)[1], ['ymin', 'ymax']] += int(record.y0)
    
    root, ext = os.path.splitext(slice_file)
    out_img_path = os.path.join(out_dir, 'original_image' + ext)
    io.imwrite(out_img_path, ori_img)
    out_list_path = os.path.join(out_dir, 'updated_list.csv')
    object_list.to_csv(out_list_path)
    return([out_img_path, out_list_path])

def overlay_annotations(img_file, object_list, out_dir, out_file):
    thickness = 10
    ori_img = io.imread(img_file)
    object_list = pd.read_csv(object_list)
    class_names = object_list.annotation.drop_duplicates().sort_values(ascending=True)
    n_class = class_names.shape[0]
    class_index = np.array(range(0, n_class, 1))
    n_color = n_class + 3 - (n_class % 3)
    for object_i in object_list.itertuples():
        ano = object_i.annotation
        ano_index = class_index[class_names == ano]
        if n_class == 1:
            rgb_color = (255, 255, 255)
        else:
            hex_color = cc.make_color_code(n_color, int(ano_index))
            rgb_color = (int(hex_color[1:3],16),int(hex_color[3:5],16),int(hex_color[5:7],16))
            
        for i in range(thickness):
            poly_x = np.array([object_i.ymin - 1 - i, object_i.ymin - 1 - i, object_i.ymax - 1 + i, object_i.ymax - 1 + i])
            poly_y = np.array([object_i.xmin - 1 - i, object_i.xmax - 1 + i, object_i.xmax - 1 + i, object_i.xmin - 1 - i])
            l1, l2 = draw.polygon_perimeter(poly_x, poly_y, shape=ori_img.shape)
            for j in range(3):
                ori_img[l1, l2, j] = rgb_color[j]
            
    root, ext = os.path.splitext(img_file)
    out_img_path = os.path.join(out_dir, out_file + ext)
    io.imsave(out_img_path, ori_img)
    
def get_slice_coordinate(in_dir, object_list):
    ol = pd.read_csv(object_list)
    xml_files = ol['xml_file']
    coordinate = xml_files.str.replace('.+/', '').str.replace('.xml', '').str.split('_', expand=True)
    x_coord = coordinate[2].str.split('-', expand=True)
    x0 = x_coord[0].astype('int') + ol['xmin']
    x1 = x_coord[1].astype('int') + ol['xmax']
    y_coord = coordinate[1].str.split('-', expand=True)
    y0 = y_coord[0].astype('int') + ol['ymin']
    y1 = y_coord[1].astype('int') + ol['ymax']
    image_file = ol['image_file']
    slice_coord = pd.concat([image_file, x0, x1, y0, y1], axis=1)
    slice_coord.columns = ['image_file', 'xmin', 'xmax', 'ymin', 'ymax']
    slice_coord.to_csv(os.path.join(in_dir, 'slice_cordinate.csv'), index=False)
    ol['xmin'] = x_coord[0].astype('int') + ol['xmin']
    ol['xmax'] = x_coord[0].astype('int') + ol['xmax']
    ol['ymin'] = y_coord[0].astype('int') + ol['ymin']
    ol['ymax'] = y_coord[0].astype('int') + ol['ymax']
    ol.to_csv(object_list, index=False)
    
def filesorter(in_dir, out_dir, data_type, ori_img, threshold, voting):
    list_path = make_object_list(in_dir, out_dir)
    
    if os.path.exists(os.path.join(in_dir, 'slice_coordinate.csv')):
        img_file_path, list_path = merge_slices(in_dir, out_dir, list_path)
    else:
        get_slice_coordinate(in_dir, list_path)
    
    
    if voting:
        out_file_name = 'annotated_image_before_cleanup'
        overlay_annotations(img_file_path, list_path, out_dir, out_file_name)
        list_path = clean_dup_objects(out_dir, list_path, threshold, voting)
        out_file_name = 'annotated_image_after_cleanup'
        overlay_annotations(img_file_path, list_path, out_dir, out_file_name)
    else:
        out_file_name = 'annotated_image'
        overlay_annotations(ori_img, list_path, out_dir, out_file_name)
    

