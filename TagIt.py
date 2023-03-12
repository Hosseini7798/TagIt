"""
TagIt.py       

The TagIt module allows users to easily label images with custom tags.
"""

# -----------------------------------------------------------------------
# Imports required packages 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob
import os
from natsort import natsorted
import pandas as pd
get_ipython().run_line_magic('matplotlib', 'notebook')

# -----------------------------------------------------------------------
class Tagger:
    """
    A class used to label images.

    ...

    Attributes
    ----------
    Images_dir (str): 
        The folder path of images have to be labeled.
        (e.g 'dir/to/images/folder') 
    BackUp_dir (str):
        The backup folder to write label information in csv format.
        (e.g 'dir/to/backup/folder')
        Note: 
            Please avoid using the `Images_dir`for storing backup csv file.
            Instead, consider using a seperate directory specifically for your data.
    classes_input (dict):
        A dictionary of defined key button and corresponding classes.
        (e.g {key_button:class}) 
    classes (list):
        A list of classes.
    key_button (list):
        A list of defined key button. 
    csv_path (str):
        The path to write label information in csv format.
    csv_backup_path (str):
        The path to write label information backup in csv foramt
    count (int):
        The number reflecting index of image.
    img_type (str):
        Images format.
        (e.g 'png', 'jpg', and ...) 
    figsize (tuple):
        The size of matplotlib canvas.
        (e.g. (7,7))
    len_imgs (int):
        The number of total images in `Images_dir`.
    font_size (float):
        The font size of legends(image path, image number, and image label).
    backup_rate (int):
        The frequency (in number of labeled images) at which to save a backup
        of the labeling progress. If set to 100, for example a backup of the
        labels will saved every 10 labeled images. 
        
    Methods
    -------
    onpress(event)
        Keep track of key press event.
    
    plot()
        Show the image with index of `count`.
    """
    def __init__(self, Images_dir: str, BackUp_dir: str,
                 classes_input: dict, count: int = None,
                 img_type: str = "png", figsize: tuple = (7,7),
                 backup_rate: int = 100):
        """
        Initializes a new Tagger object. 
        
        Args:
            Images_dir (str): 
                The folder path of images have to be labeled.
                (e.g 'dir/to/images/folder') 
            BackUp_dir (str):
                The backup folder to write label information in
                csv format.(e.g 'dir/to/backup/folder')
                Note: 
                    Please avoid using the `Images_dir`for storing
                    backup csv file. Instead, consider using a 
                    seperate directory specifically for your data.
            classes_input (dict):
                A dictionary of defined key button and 
                corresponding classes.(e.g {key_button:class})
            count (int):
                The number reflecting index of image.
            img_type (str):
                Images format. (e.g 'png', 'jpg', and ...) 
            figsize (tuple):
                The size of matplotlib canvas.(e.g. (7,7))
            backup_rate (int):
                The frequency (in number of labeled images) at
                which to save a backup of the labeling progress.
                If set to 100, for example a backup of the labels
                will saved every 100 labeled images.
        """
        # Attributes
        self.Images_dir = Images_dir                           # images directory 
        self.BackUp_dir = BackUp_dir                           # backup directory
        self.classes_input = classes_input                     # dictionary of defined keys and classes
        self.classes    = classes_input.values()               # list of classes
        self.key_button = classes_input.keys()                 # list of defined keys
        self.csv_path   = f"{Images_dir}/img_label.csv"        # path of label csv file 
        self.csv_backup_path = f"{BackUp_dir}/img_backup.csv"  # path of label backup csv file
        self.count      = count                                # index of image
        self.img_type   = img_type                             # imgage type (e.g. "png","jpg")
        self.figsize    = figsize                              # figure size: size of canvas
        self.font_size  = figsize[0]*(1.4)                     # font size of legend
        self.backup_rate = backup_rate                         # backup rate
        # If there were no CSV files, it create one otherwise continue to fill it
        if os.path.isfile(self.csv_path) is False:
            self.img_path = glob.glob(f"{Images_dir}/*.{self.img_type}")   # list of images in `Images_dir`
            self.img_path = natsorted(self.img_path) # sort `img_path` as the same as windows file explorer 
            self.img_info = pd.DataFrame({'img_path': pd.Series(data = self.img_path, dtype='str')}) # make image label dataframe
            self.img_info = self.img_info.assign(**dict.fromkeys(classes_input.values(),None)) # assign classes as column 
            self.img_info.to_csv(self.csv_path,index=False)    # save label dataframe as csv
            self.count = 0 

        else:
            self.img_info = pd.read_csv(self.csv_path, index_col=False) # read the existing csv file
            self.img_path = self.img_info.img_path
            # If count is not given, find the first row which is not labeled and set its index as count  
            if count is None:
                temp = self.img_info.iloc[:,1:].isnull().all(axis=1)
                self.count = temp[temp==True].first_valid_index()
                
        img = mpimg.imread(self.img_path[0])
        self.img_height, self.img_width, self.img_channel = img.shape
        
        self.len_imgs = len(self.img_path) # total number of images  
        
        fig = plt.figure(figsize=self.figsize) # plot 7 by 7 canvas 
        if self.count == None:
            self.count = self.len_imgs  
            plt.text(0.2, 0.5,
                     f"There is no images left.",
                     color='r', size=20)
            plt.show()
            cid = fig.canvas.mpl_connect('key_press_event',
                                         self.onpress) # keep track of key press event 
        else:
            self.plot()
            #Add an interactive widget to figure 
            cid = fig.canvas.mpl_connect('key_press_event',
                                         self.onpress) # keep track of key press event 
    
    def plot(self):
        self.path = self.img_path[self.count] # path of image which index=`count` 
        self.x = self.img_info.columns[self.img_info.iloc[self.count,].notnull()][1:].format() # list of defined label for this image
        self.img = mpimg.imread(self.path) # read the image 
        self.labels = plt.text(0, -0.015*self.img_height, f"{self.x}",
                               color='b',size=self.font_size) # show the list of defined label for this image
        self.paths = plt.text(0, -0.1*self.img_height, f"{self.path}",color='b',
                              size=self.font_size,rotation_mode="anchor") # show the path of this image 
        self.num = plt.text(self.img_width*0.8, -0.015*self.img_height,  f"{self.count}/{len(self.img_path)-1}",
                            color='r',size=self.font_size*2) # show the index(`count`) of this image 
        plt.imshow(self.img) # show the image 
        plt.show()
        
    def onpress(self, event):
        
        self.key = event.key # pressed key button on keyboard 
        
        # If pressed key button was in defined key button, add it to dataframe
        if self.key in self.key_button: 
            self.img_info.at[self.count, self.classes_input[self.key]] = 1 # fill corresponding column and row with 1 
            self.labels.remove() # remove old labels from canvas 
            self.x = self.img_info.columns[self.img_info.iloc[self.count,].notnull()][1:].format() # list of defined label for this image
            self.labels = plt.text(0, -0.015*self.img_height,
                                   f"{self.x}",color='b',size=self.font_size) # show the list of new defined label for this image
            plt.show()
            
        # If pressed key button was "enter" or "right", show the next image
        elif self.key in ["enter", "right"]:
            plt.clf() # clear the canvas 
            # The label data frame is saved if 100 images were labeled or images were finished
            if self.count % self.backup_rate == 0 :
                plt.text(0, -0.2*self.img_height,
                         f"Image label is backed up.",color='g',size=self.font_size) # inform the user that labels is backed up
                self.img_info.to_csv(self.csv_path,index=False) # save label dataframe in csv file 
                self.img_info.to_csv(self.csv_backup_path,index=False) # save label dataframe in backup csv file 
            elif self.count==len(self.img_path)-1:
                self.img_info.to_csv(self.csv_path,index=False) # save label dataframe in csv file 
                self.img_info.to_csv(self.csv_backup_path,index=False) # save label dataframe in backup csv file 
                plt.text(0.2, 0.5,
                         f"There is no images left.",
                         color='r', size=20)
                
            self.count += 1 # update count 
            
            # If there is an image left, show it 
            if len(self.img_path)>self.count:  
                self.plot()

        # If pressed key button was "backspace", delete defined label for current image
        elif self.key == "backspace":
            self.img_info.iloc[self.count, 1:] = None  # fill all columns of current image row in label dataframe with None 
            self.labels.remove() # remove old labels from canvas 
            self.x = self.img_info.columns[self.img_info.iloc[self.count,].notnull()][1:].format() # list of defined label for this image
            self.labels = plt.text(0, -0.015*self.img_height,
                                   f"{self.x}",color='b',size=self.font_size) # show the list of new defined label for this image
        
        # If pressed key button was "shift" or "left", show the previous image
        elif self.key in ["left", "shift"]:
            self.count -= 1 # update count
            plt.clf() # clear the canvas 
            self.plot()
        
        # If pressed key button was "s", save the label data frame 
        elif self.key == "s":
            self.img_info.to_csv(self.csv_path, index=False) # save label dataframe in csv file 
            self.img_info.to_csv(self.csv_backup_path,index=False) # save label dataframe in backup csv file 
            plt.text(0, -0.2*self.img_height,
                     f"Image label is saved.",color='g',size=self.font_size) # inform the user that labels is saved
