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
from skimage import io
import tkinter.messagebox
import threading as th
import imageslicer as isl
import filesorter as fs


class CutsortGUI(ttk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.configure(padding=50)
        self.pack()
        self.initial_menu()
        
    def initial_menu(self):
        # The initial appearance
        s = ttk.Style()
        s.configure('init.TButton', font=('Helvetica', '18'))
        self.filesorter_button = ttk.Button(self,
                                  text = "Image Slicer",
                                  style = 'init.TButton',
                                  command = self.open_slicer)
        self.filesorter_button.pack()
        
        self.imgslicer_button = ttk.Button(self,
                                  text = "File Sorter",
                                  style = 'init.TButton',
                                  command = self.open_sorter)
        self.imgslicer_button.pack(pady=(30, 0))

        
    def back_to_menu(self):
        children = self.winfo_children()
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
            img = io.imread(img_file)
            height, width, channels = img.shape[:3]
            img_h_text = 'Height = ' + str(height) + ' pixels'
            self.img_h.set(img_h_text)
            img_w_text = 'Width = ' + str(width) + ' pixels'
            self.img_w.set(img_w_text)       
        
    def open_slicer(self):
        children = self.winfo_children()
        for child in children:
            child.destroy()
            
        s = ttk.Style()
        s.configure('isl.TButton', font = ('Helvetica', '12', 'bold'))
        s.configure('small.TLabel', font = ('Helvetica', '10'))
        s.configure('regular.TLabel', font = ('Helvetica', '12'))
         
        back_button = ttk.Button(self,
                                 text = "Back to Menu",
                                 style = 'isl.TButton',
                                 command = self.back_to_menu)
        back_button.pack()


        in_file_button = ttk.Button(self,
                                  text = "Input image file",
                                  style = 'isl.TButton',
                                  command = self.in_file_dialog)
        in_file_button.pack(pady=(30, 10))
        
        self.in_file = tk.StringVar()
        self.in_file.set('Please select an input image file.')
        in_file_label = ttk.Label(self,
                                  textvariable = self.in_file,
                                  style = 'small.TLabel')
        in_file_label.pack(pady = (0, 5))
        
        self.img_h = tk.StringVar()
        self.img_h.set('NA')
        img_h_label = ttk.Label(self,
                                textvariable = self.img_h, 
                                style = 'small.TLabel')
        img_h_label.pack(pady = (0, 5))
    
        self.img_w = tk.StringVar()
        self.img_w.set('NA')
        img_w_label = ttk.Label(self,
                                textvariable = self.img_w, 
                                style = 'small.TLabel')
        img_w_label.pack(pady = (0, 10))
    
        size_x_label = ttk.Label(self,
                                 text='Set width of sliced images', 
                                 style = 'regular.TLabel')
        size_x_label.pack(pady = 0)
        self.size_x = ttk.Entry(self)
        self.size_x.insert(0, "500")
        self.size_x.pack(pady = (0, 10))
        
        size_y_label = ttk.Label(self,
                                 text='Set height of sliced images', 
                                 style = 'regular.TLabel')
        size_y_label.pack(pady = 0)
        self.size_y = ttk.Entry(self)
        self.size_y.insert(0, "500")
        self.size_y.pack(pady = (0, 10))
    
        step_x_label = ttk.Label(self,
                               text='Set step width of image slicing', 
                               style = 'regular.TLabel')
        step_x_label.pack(pady = 0)
        self.step_x = ttk.Entry(self)
        self.step_x.insert(0, "250")
        self.step_x.pack(pady = (0, 10))
        
        step_y_label = ttk.Label(self,
                               text='Set step height of image slicing', 
                               style = 'regular.TLabel')
        step_y_label.pack(pady = 0)
        self.step_y = ttk.Entry(self)
        self.step_y.insert(0, "250")
        self.step_y.pack(pady = (0, 10))

        out_dir_button = ttk.Button(self,
                                   text = "Output directory",
                                   style = 'isl.TButton',
                                   command = self.out_dir_dialog)
        out_dir_button.pack(pady=(0, 10))
        
        self.out_dir = tk.StringVar()
        self.out_dir.set ('Please select an output directory.')
        out_dir_label = ttk.Label(self,
                                  textvariable=self.out_dir,
                                 style = 'regular.TLabel')
        out_dir_label.pack(pady = 0)
        
        run_isl = ttk.Button(self,
                               text = "Run",
                               style = 'isl.TButton',
                               command = self.run_slicer)
        run_isl.pack(pady=(20, 0))
            
    def open_sorter(self):
        
        def show_type1():
            setting_frame.pack_forget()
            label1.grid_forget()
            widget1.grid_forget()
            widget2.grid_forget
            in_dir_button.pack_forget()
            in_dir_label.pack_forget()
            in_file_button.pack_forget()
            in_file_label.pack_forget()
            out_dir_button.pack_forget()
            out_dir_label.pack_forget()
            run_button.pack_forget()
            setting_frame.pack(pady = (30, 20))
            label1.grid(row = 0, column = 0)
            widget1.grid(row = 1, column = 0)
            widget2.grid(row = 4, column = 0)
            in_dir_button.pack(pady=(0, 10))
            in_dir_label.pack(pady = (0, 20))
            in_file_button.pack(pady=(0, 10))
            in_file_label.pack(pady = (0, 20))
            out_dir_button.pack(pady=(0, 10))
            out_dir_label.pack(pady = 0)
            run_button.pack(pady=(40,0))
            
        def show_type2():
            setting_frame.pack_forget()
            label1.grid_forget()
            widget1.grid_forget()
            widget2.grid_forget
            in_dir_button.pack_forget()
            in_dir_label.pack_forget()
            in_file_button.pack_forget()
            in_file_label.pack_forget()
            out_dir_button.pack_forget()
            out_dir_label.pack_forget()
            run_button.pack_forget()
            in_dir_button.pack(pady=(0, 10))
            in_dir_label.pack(pady = (0, 20))
            out_dir_button.pack(pady=(0, 10))
            out_dir_label.pack(pady = 0)
            run_button.pack(pady=(40,0))
            
        def show_type3():
            setting_frame.pack_forget()
            label1.grid_forget()
            widget1.grid_forget()
            widget2.grid_forget
            in_dir_button.pack_forget()
            in_dir_label.pack_forget()
            in_file_button.pack_forget()
            in_file_label.pack_forget()
            out_dir_button.pack_forget()
            out_dir_label.pack_forget()
            run_button.pack_forget()
            in_dir_button.pack(pady=(0, 10))
            in_dir_label.pack(pady = (0, 20))
            out_dir_button.pack(pady=(0, 10))
            out_dir_label.pack(pady = 0)
            run_button.pack(pady=(40,0))
                                           
        children = self.winfo_children()
        for child in children:
            child.destroy()
            
        s = ttk.Style()
        s.configure('fs.TButton', font = ('Helvetica', '12', 'bold'))
        s.configure('small.TLabel', font = ('Helvetica', '10'))
        s.configure('regular.TLabel', font = ('Helvetica', '12'))
        s.configure('regular.TLabelframe', font = ('Helvetica', '12'))
        s.configure('regular.TRadiobutton', font = ('Helvetica', '12'))
        s.configure('regular.TEntry', font = ('Helvetica', '12'))
         
        back_button = ttk.Button(self,
                                 text = "Back to Menu",
                                 style = 'fs.TButton',
                                 command = lambda:self.back_to_menu())
        back_button.pack()
        
        rb_frame = ttk.Labelframe(self,
                                  text = 'Input type', 
                                  padding = (10),
                                  style = 'regular.TLabelframe')
        rb_frame.pack(pady = (30, 20))
        self.type_val = tk.IntVar()
        self.type_val.set(1)
        rb1 = ttk.Radiobutton(rb_frame, 
                              text = 'Object detection on sliced images',
                              value = 1,
                              variable = self.type_val,
                              style = 'regular.TRadiobutton',
                              command = show_type1)
        rb2 = ttk.Radiobutton(rb_frame, 
                              text = 'Object detection on single images',
                              value = 2,
                              variable = self.type_val,
                              style = 'regular.TRadiobutton',
                              command = show_type2)
        rb3 = ttk.Radiobutton(rb_frame, 
                              text = 'Image classification',
                              value = 3,
                              variable = self.type_val,
                              style = 'regular.TRadiobutton',
                              command = show_type3)
        rb1.grid(row = 0, column = 0)
        rb2.grid(row = 1, column = 0)
        rb3.grid(row = 2, column = 0)
        
        setting_frame = ttk.Labelframe(self,
                                  text = 'Settings to summarize annotations', 
                                  padding = (10),
                                  style = 'regular.TLabelframe')
        setting_frame.pack(pady = (30, 20))
        self.threshold = tk.StringVar()
        self.voting = tk.BooleanVar()
        self.voting.set(False)
        label1 = ttk.Label(setting_frame, 
                              text = 'Percentage of overlaped area',
                               style = 'regular.TLabel')
        widget1 = ttk.Entry(setting_frame,
                              textvariable = self.threshold,
                              style = 'regular.TEntry')
        widget1.insert(0, "0")
        widget2 = ttk.Checkbutton(setting_frame, 
                              text = 'Vote to decide annotations',
                              variable = self.voting,
                              style = 'regular.TRadiobutton')
        label1.grid(row = 0, column = 0)
        widget1.grid(row = 1, column = 0)
        widget2.grid(row = 4, column = 0)
        
        in_dir_button = ttk.Button(self,
                                  text = "Input directory",
                                  style = 'fs.TButton',
                                  command = self.in_dir_dialog)
        in_dir_button.pack(pady=(0, 10))
        
        self.in_dir = tk.StringVar()
        self.in_dir.set('Please select an input directory.')
        in_dir_label = ttk.Label(self,
                                 textvariable=self.in_dir,
                                 style = 'regular.TLabel')
        in_dir_label.pack(pady = (0, 20))
        
        in_file_button = ttk.Button(self,
                                  text = "Original image file",
                                  style = 'isl.TButton',
                                  command = self.in_file_dialog)
        in_file_button.pack(pady=(0, 10))
        self.in_file = tk.StringVar()
        self.in_file.set('Please select the original image file of sclices.')
        in_file_label = ttk.Label(self,
                                  textvariable = self.in_file,
                                  style = 'regular.TLabel')
        in_file_label.pack(pady = (0, 20))
        
        
        out_dir_button = ttk.Button(self,
                                  text = "Output directory", 
                                  style = 'fs.TButton',
                                  command = self.out_dir_dialog)
        out_dir_button.pack(pady=(0, 10))
        
        self.out_dir = tk.StringVar()
        self.out_dir.set ('Please select an output directory.')
        out_dir_label = ttk.Label(self,
                                  textvariable=self.out_dir, 
                                  style = 'regular.TLabel')
        out_dir_label.pack(pady = 0)
        
        run_button = ttk.Button(self,
                               text = "Run",
                               style = 'fs.TButton',
                               command = self.run_sorter)
        run_button.pack(pady=(40,0))
        
    def run_slicer(self):
        def check_thread():
            if pb.winfo_exists():
                if t_slicer.is_alive():
                    self.after(20, check_thread)
                else:
                    pb_bar.stop()
                    pb.grab_release()
                    pb.destroy()
                    tk.messagebox.showinfo("Image Slicer", "Done!")
        
        pb = tk.Toplevel(self)
        pb.grab_set()
        pb.focus_force()
        pb.title('Running Image Slicer')
        pb_frame = ttk.Labelframe(pb, text = 'Running...')
        pb_frame.configure(padding=30)
        pb_frame.pack()
        pb_bar = ttk.Progressbar(pb_frame, orient='horizontal', length=200, mode='indeterminate')
        pb_bar.pack()
        
        in_file = self.in_file.get()
        out_dir = self.out_dir.get()
        size_x = int(self.size_x.get())
        size_y = int(self.size_y.get())
        step_x = int(self.step_x.get())
        step_y = int(self.step_y.get())
        
        check1 = in_file == 'Please select an input iamge.'
        check2 = out_dir == 'Please select an output directory.'
        if check1:
            tk.messagebox.showinfo("Image Slicer", "Invalid settings.\nPlease specify an input image.")
            pb.destroy()
        elif check2:
            tk.messagebox.showinfo("Image Slicer", "Invalid settings.\nPlease specify an output directory.")
            pb.destroy()
        else:
            t_slicer = th.Thread(target=isl.imageslicer, args=(in_file, out_dir, size_x, size_y, step_x, step_y, ))
            t_slicer.daemon = True
            pb_bar.start(10)
            t_slicer.start()
            self.after(20, check_thread)
            
    def run_sorter(self):
        def check_thread():
            if pb.winfo_exists():
                if t_sorter.is_alive():
                    self.after(20, check_thread)
                else:
                    pb_bar.stop()
                    pb.grab_release()
                    pb.destroy()
                    tk.messagebox.showinfo("File Sorter", "Done!")
                
        pb = tk.Toplevel(self)
        pb.grab_set()
        pb.focus_force()
        pb.title('Running Image Sorter')
        pb_frame = ttk.Labelframe(pb, text = 'Running...')
        pb_frame.configure(padding=30)
        pb_frame.pack()
        pb_bar = ttk.Progressbar(pb_frame, orient='horizontal', length=200, mode='indeterminate')
        pb_bar.pack()
        
        in_dir = self.in_dir.get()
        check1 = in_dir == 'Please select an input directory.'
        out_dir = self.out_dir.get()
        check2 = out_dir == 'Please select an output directory.'
        in_file = self.in_file.get()
        check3 = in_file == 'Please select the original image file of sclices.'
        
        data_type = self.type_val.get()
        check4 = data_type == 1
        threshold = float(self.threshold.get())
        voting = self.voting.get()
        if check1:
            tk.messagebox.showinfo("File Sorter", "Invalid settings.\nPlease specify an input directory.")
            pb.destroy()
        elif check2:
            tk.messagebox.showinfo("File Sorter", "Invalid settings.\nPlease specify an output directory.")
            pb.destroy()
        elif check3 and check4 and (not voting):
            tk.messagebox.showinfo("File Sorter", "Invalid settings.\nPlease specify the original image or turn on voting.")
            pb.destroy()
        else:
            t_sorter = th.Thread(target=fs.filesorter, args=(in_dir, out_dir, data_type, in_file, threshold, voting,))
            t_sorter.daemon = True
            pb_bar.start(10)
            t_sorter.start()
            self.after(20, check_thread)

if __name__ == '__main__':
    global root
    root = tk.Tk()
    root.title("Cut&Sort")
    CutsortGUI(master=root)
    root.mainloop()
