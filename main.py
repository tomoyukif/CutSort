#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 10:53:13 2020

@author: ftom
"""

import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog
import cv2
from skimage.io import imread
import tkinter.messagebox
import threading as th
import imageslicer as isl
import filesorter as fs


class Imagesorter(ttk.Frame):
    
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.create_widgets()
    
    def create_widgets(self):
        s = ttk.Style()
        s.configure('init.TFrame', background = 'white')
        self.frame = ttk.Frame(self, style = 'init.TFrame', padding = 10)
        self.frame.pack()
        self.initial_menu()
        
    def initial_menu(self):
        # The initial appearance
        s = ttk.Style()
        s.configure('init.TButton', font=('Helvetica', '12', 'bold'))
        self.filesorter_button = ttk.Button(self.frame,
                                  text = "Image Slicer",
                                  style = 'init.TButton',
                                  command = lambda:self.open_slicer())
        self.filesorter_button.pack(pady=(30, 0))
        
        self.imgslicer_button = ttk.Button(self.frame,
                                  text = "File Sorter",
                                  style = 'init.TButton',
                                  command = lambda:self.open_sorter())
        self.imgslicer_button.pack(pady=(30, 0))

        
    def back_to_menu(self):
        children = self.frame.winfo_children()
        for child in children:
            child.destroy()
        self.initial_menu()
            
            
    def in_dir_dialog(self):
        iDir = os.path.abspath(os.path.dirname(__file__))
        in_dir = tk.filedialog.askdirectory(initialdir=iDir)
        
        if len(in_dir) == 0:
            self.in_dir.set('Please select an input directory.')
        else:
            self.in_dir.set(in_dir)
            
    def out_dir_dialog(self):
        iDir = os.path.abspath(os.path.dirname(__file__))
        out_dir = tk.filedialog.askdirectory(initialdir=iDir)
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        if len(out_dir) == 0:
            self.out_dir.set('Please select an output directory.')
        else:
            self.out_dir.set(out_dir)
            
    def in_file_dialog(self):
        fTyp = [("image file", "*.jpg *.jpeg *.png *.tif *.tiff")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        in_file = tk.filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
        if len(in_file) == 0:
            self.in_file.set('Please select an input image file.')
        else:
            self.in_file.set(in_file)
            img_file = self.in_file.get()
            img = imread(img_file)
            height, width, channels = img.shape[:3]
            img_h_text = 'Height = ' + str(height) + ' pixels'
            self.img_h.set(img_h_text)
            img_w_text = 'Width = ' + str(width) + ' pixels'
            self.img_w.set(img_w_text)       
        
    def open_slicer(self):
        children = self.frame.winfo_children()
        for child in children:
            child.destroy()
            
        s = ttk.Style()
        s.configure('isl.TButton', font = ('Helvetica', '12', 'bold'))
        s.configure('small.TLabel', font = ('Helvetica', '10'), background = 'white')
        s.configure('regular.TLabel', font = ('Helvetica', '12'), background = 'white')
         
        back_button = ttk.Button(self.frame, 
                                 text = "Back to Menu",
                                 style = 'isl.TButton',
                                 command = lambda:self.back_to_menu())
        back_button.pack(pady=(10, 0))


        in_file_button = ttk.Button(self.frame,
                                  text = "Input image file",
                                  style = 'isl.TButton',
                                  command = lambda:self.in_file_dialog())
        in_file_button.pack(pady=(30, 10))
        
        self.in_file = tk.StringVar()
        self.in_file.set('Please select an input image file.')
        in_file_label = ttk.Label(self.frame, 
                                  textvariable = self.in_file,
                                  style = 'small.TLabel')
        in_file_label.pack(pady = (0, 5))
        
        self.img_h = tk.StringVar()
        self.img_h.set('NA')
        img_h_label = ttk.Label(self.frame,
                                textvariable = self.img_h, 
                                style = 'small.TLabel')
        img_h_label.pack(pady = (0, 5))
    
        self.img_w = tk.StringVar()
        self.img_w.set('NA')
        img_w_label = ttk.Label(self.frame,
                                textvariable = self.img_w, 
                                style = 'small.TLabel')
        img_w_label.pack(pady = (0, 10))
    
        size_x_label = ttk.Label(self.frame,
                                 text='Set width of sliced images', 
                                 style = 'regular.TLabel')
        size_x_label.pack(pady = 0)
        self.size_x = ttk.Entry(self.frame)
        self.size_x.insert(0, "500")
        self.size_x.pack(pady = (0, 10))
        
        size_y_label = ttk.Label(self.frame,
                                 text='Set height of sliced images', 
                                 style = 'regular.TLabel')
        size_y_label.pack(pady = 0)
        self.size_y = ttk.Entry(self.frame)
        self.size_y.insert(0, "500")
        self.size_y.pack(pady = (0, 10))
    
        step_x_label = ttk.Label(self.frame,
                               text='Set step width of image slicing', 
                               style = 'regular.TLabel')
        step_x_label.pack(pady = 0)
        self.step_x = ttk.Entry(self.frame)
        self.step_x.insert(0, "250")
        self.step_x.pack(pady = (0, 10))
        
        step_y_label = ttk.Label(self.frame,
                               text='Set step height of image slicing', 
                               style = 'regular.TLabel')
        step_y_label.pack(pady = 0)
        self.step_y = ttk.Entry(self.frame)
        self.step_y.insert(0, "250")
        self.step_y.pack(pady = (0, 10))

        out_dir_button = ttk.Button(self.frame,
                                   text = "Output directory",
                                   style = 'isl.TButton',
                                   command = lambda:self.out_dir_dialog())
        out_dir_button.pack(pady=(0, 10))
        
        self.out_dir = tk.StringVar()
        self.out_dir.set ('Please select an output directory.')
        out_dir_label = ttk.Label(self.frame,
                                  textvariable=self.out_dir,
                                 style = 'regular.TLabel')
        out_dir_label.pack(pady = 0)
        
        run_isl = ttk.Button(self.frame, 
                               text = "Run",
                               style = 'isl.TButton',
                               command = lambda:self.run_slicer())
        run_isl.pack(pady=(20, 0))
            
    def open_sorter(self):
                                           
        children = self.frame.winfo_children()
        for child in children:
            child.destroy()
            
        master.geometry("360x680")
        s = ttk.Style()
        s.configure('fs.TButton', font = ('Helvetica', '12', 'bold'))
        s.configure('small.TLabel', font = ('Helvetica', '10'), background = 'white')
        s.configure('regular.TLabel', font = ('Helvetica', '12'), background = 'white')
        s.configure('regular.TLabelframe', font = ('Helvetica', '12'), background = 'white')
        s.configure('regular.TRadiobutton', font = ('Helvetica', '12'), background = 'white')
        s.configure('regular.TEntry', font = ('Helvetica', '12'), background = 'white')
         
        back_button = ttk.Button(self.frame, 
                                 text = "Back to Menu",
                                 style = 'fs.TButton',
                                 command = lambda:self.back_to_menu())
        back_button.pack(pady=(10, 0))
        
        rb_frame = ttk.Labelframe(self.frame, 
                                  text = 'Input type', 
                                  padding = (10),
                                  style = 'regular.TLabelframe')
        rb_frame.pack(pady = (30, 20))
        self.rb_val = tk.IntVar()
        self.rb_val.set(1)
        rb1 = ttk.Radiobutton(rb_frame, 
                              text = 'Object detection on sliced images',
                              value = 1,
                              variable = self.rb_val,
                              style = 'regular.TRadiobutton')
        rb2 = ttk.Radiobutton(rb_frame, 
                              text = 'Object detection on single images',
                              value = 2,
                              variable = self.rb_val,
                              style = 'regular.TRadiobutton')
        rb3 = ttk.Radiobutton(rb_frame, 
                              text = 'Image classification',
                              value = 3,
                              variable = self.rb_val,
                              style = 'regular.TRadiobutton')
        rb1.grid(row = 0, column = 0)
        rb2.grid(row = 1, column = 0)
        rb3.grid(row = 2, column = 0)
        
        setting_frame = ttk.Labelframe(self.frame, 
                                  text = 'Settings to summarize annotations', 
                                  padding = (10),
                                  style = 'regular.TLabelframe')
        setting_frame.pack(pady = (30, 20))
        self.rb_val = tk.IntVar()
        self.threshold = tk.StringVar()
        self.voting = tk.BooleanVar()
        self.voting.set(True)
        label1 = ttk.Label(setting_frame, 
                              text = 'Percentage of overlaped area',
                               style = 'regular.TLabel')
        widget1 = ttk.Entry(setting_frame,
                              textvariable = self.threshold,
                              style = 'regular.TEntry')
        widget2 = ttk.Checkbutton(setting_frame, 
                              text = 'Vote to decide annotations',
                              variable = self.voting,
                              style = 'regular.TRadiobutton')
        label1.grid(row = 0, column = 0)
        widget1.grid(row = 1, column = 0)
        widget2.grid(row = 4, column = 0)
        
        in_dir_button = ttk.Button(self.frame,
                                  text = "Input directory",
                                  style = 'fs.TButton',
                                  command = lambda:self.in_dir_dialog())
        in_dir_button.pack(pady=(0, 10))
        
        self.in_dir = tk.StringVar()
        self.in_dir.set('Please select an input directory.')
        in_dir_label = ttk.Label(self.frame,
                                 textvariable=self.in_dir,
                                 style = 'regular.TLabel')
        in_dir_label.pack(pady = (0, 20))
        
        out_dir_button = ttk.Button(self.frame, 
                                  text = "Output directory", 
                                  style = 'fs.TButton',
                                  command = lambda:self.out_dir_dialog())
        out_dir_button.pack(pady=(0, 10))
        
        self.out_dir = tk.StringVar()
        self.out_dir.set ('Please select an output directory.')
        out_dir_label = ttk.Label(self.frame,
                                  textvariable=self.out_dir, 
                                  style = 'regular.TLabel')
        out_dir_label.pack(pady = 0)
        
        run_button = ttk.Button(self.frame,
                               text = "Run",
                               style = 'fs.TButton',
                               command = lambda:self.run_sorter())
        run_button.pack(pady=(40,20))                
        
    def run_slicer(self):          
        def check_thread():
            if t_slicer.is_alive():
                master.after(20, check_thread)
            else:
                pb_bar.stop()
                pb.grab_release()
                pb.destroy()
                tk.messagebox.showinfo("Image Slicer", "Done!")
        
        pb = tk.Toplevel(self.frame)
        pb.grab_set()
        pb.focus_force()
        pb.geometry('300x100')
        pb.title('Running Image Slicer')
        label = ttk.Label(pb, text = 'Running...')
        label.pack(side = 'left')
        pb_bar = ttk.Progressbar(pb, orient='horizontal', length=200, mode='indeterminate')
        pb_bar.pack(side = 'left')
        
        in_file = self.in_file.get()
        out_dir = self.out_dir.get()
        size_x = int(self.size_x.get())
        size_y = int(self.size_y.get())
        step_x = int(self.step_x.get())
        step_y = int(self.step_y.get())
        
        t_slicer = th.Thread(target=isl.imageslicer, args=(in_file, out_dir, size_x, size_y, step_x, step_y, ))
        t_slicer.daemon = True
        pb_bar.start(10)
        t_slicer.start()
        master.after(20, check_thread)
            
    def run_sorter(self):
        def check_thread():
            if t_sorter.is_alive():
                master.after(20, check_thread)
            else:
                pb_bar.stop()
                pb.grab_release()
                pb.destroy()
                tk.messagebox.showinfo("File Sorter", "Done!")
                
        pb = tk.Toplevel(self.frame)
        pb.grab_set()
        pb.focus_force()
        pb.geometry('300x100')
        pb.title('Running Image Sorter')
        label = ttk.Label(pb, text = 'Running...')
        label.pack(side = 'left')
        pb_bar = ttk.Progressbar(pb, orient='horizontal', length=200, mode='indeterminate')
        pb_bar.pack(side = 'left')
        
        in_dir = self.in_dir.get()
        out_dir = self.out_dir.get()
        threshold = float(self.threshold.get())
        voting = self.voting.get()
        t_sorter = th.Thread(target=fs.filesorter, args=(in_dir, out_dir, self.rb_val, threshold, voting,))
        t_sorter.daemon = True
        pb_bar.start(10)
        t_sorter.start()
        master.after(20, check_thread)
        

if __name__ == '__main__':
    global master
    master = tk.Tk()
    master.geometry("360x480")
    master.title("ImageSorter")
    master.configure(background = 'white')
    Imagesorter(master)
    master.mainloop()
