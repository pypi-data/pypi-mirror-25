#!/usr/bin/python
""" this class deal with image normalizing process
v01 updates:
        - don't return the figure anymore
        - 
        
"""
__author__="carlos"
__date__ ="$ Fev/2017 $"


import numpy as np

import h5py as h5

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.patches as patches
from matplotlib.transforms import Bbox
from matplotlib.widgets import  RectangleSelector

import sys

from myRoll import myRoll

import tifffile as tf

class imageNorm(object):

    def __init__(self):

        self.roll = myRoll()
        
        # Global variables
        self.img_orig = None
        self.img = None
        self.imgplot = None
        self.caxes = None
        self.axes = None
        self.mouseispressed = None
        self.openfileformat = None
        self.ssvfpath = None
        
        self.fig = plt.figure()
        self.axes = self.fig.add_subplot(111)
        
        # Creates a patch to use as selection area and add it to the main axes
    ##                self.selection = patches.Rectangle((0,0), 0, 0)
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.list_rectangles = []
            

    def loadImage(self, fpath, fformat):
        if fformat == 'ssv':
##            print "open ssv"
            self.img = np.rot90(np.genfromtxt(fpath, dtype=np.int32))
            self.img_orig = np.genfromtxt(fpath, dtype=np.int32)
            self.transformation = np.zeros(self.img.shape[1], dtype=np.int16)
            self.imgplot = plt.imshow(self.img, cmap='gray', interpolation='none')
            return self.imgplot.figure
        elif fformat == 'jpg' or fformat == 'png':
##            print "open jpg, png"
            self.img = mpimg.imread(fpath)
            self.img_orig = mpimg.imread(fpath)
            self.transformation = np.zeros(self.img.shape[1], dtype=np.int16)
            self.imgplot = plt.imshow(self.img, cmap='gray', interpolation='none')
            return self.imgplot.figure
        elif fformat == 'tiff' or fformat == 'tif':
##            print "open tiff, tif"
            self.img = tf.imread(fpath)
            self.img_orig = tf.imread(fpath)
##            print "shape", self.img.shape
            self.transformation = np.zeros(self.img.shape[1], dtype=np.int16)
            self.imgplot = plt.imshow(self.img, cmap='gray', interpolation='none')
            return self.imgplot.figure
        elif fformat == 'h5' or fformat == 'hdf5':                        
##            print "open h5, hdf5"
            with h5.File(fpath, "r") as hf:
                self.img = hf["stxm"].value
                self.img_orig = hf["stxm"].value
                self.ssvfpath = hf["stxm"].attrs["filepath"]
                self.transformation = np.zeros(self.img.shape[1], dtype=np.int16)
                self.transformation = hf["transformation"].value                
                hf.close()
            self.img = self.roll.transfRoll(self.img, self.transformation, 0)
            self.imgplot = plt.imshow(self.img, cmap='gray', interpolation='none')
            return self.imgplot.figure
        else:            
            return False
        

    def saveProject(self, savename, fformat):
        if fformat == "ssv":           
            fpath = str(savename[0])
            name = fpath[fpath.rindex("/")+1::]
            fpath = fpath[0:fpath.rindex("/")+1]
            saveformat = str(savename[1])
            saveformat = saveformat[saveformat.rindex('.'):-1]                
            prefix = "imageNorm_"
            
            with h5.File(fpath + prefix + name + saveformat, "w") as hf:
                hf.create_dataset("stxm", data=self.img_orig, dtype=np.int32)
                hf["stxm"].attrs["filepath"] = self.fpath
                hf.create_dataset("transformation", data=self.transformation, dtype=np.int16)
                hf.close()
        elif fformat == "h5" or fformat == "hdf5":
            fpath = str(savename[0])
            name = fpath[fpath.rindex("/")+1::]
            fpath = fpath[0:fpath.rindex("/")+1]
            saveformat = str(savename[1])
            saveformat = saveformat[saveformat.rindex('.'):-1]                
            prefix = "imageNorm_"

            with h5.File(fpath + prefix + name + saveformat, "w") as hf:
                hf.create_dataset("stxm", data=self.img_orig, dtype=np.int32)                            
                hf["stxm"].attrs["filepath"] = self.ssvfpath
                hf.create_dataset("transformation", data=self.transformation, dtype=np.int16)
                hf.close()
        else:
            return False
        
                        
                
    def exportImage(self, exportname):
        fpath = str(exportname[0])
        fformat = str(exportname[1])
        fformat = fformat[fformat.rindex('.'):-1]
        exportname = fpath + fformat

        """Supported formats:
        eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff."""
##        
##        mpimg.imsave("test_mpsave_tif", self.img, cmap='gray', format="tif")
##        mpimg.imsave("test_mpsave_tiff", self.img, cmap='gray', format="tiff")
##        mpimg.imsave("test_mpsave_png", self.img, cmap='gray', format="png")
##        mpimg.imsave("test_mpsave_jpeg", self.img, cmap='gray', format="jpeg")
##        mpimg.imsave("test_mpsave_svg", self.img, cmap='gray', format="svg")
####        mpimg.imsave("test_mpsave_raw", self.img, cmap='gray', format="raw")
##        tf.imsave("test_tfsave", self.img)

        if fformat == ".tiff" or fformat == ".tif":
            tf.imsave(exportname, self.img)
        elif fformat == ".ssv":
            np.savetxt(exportname, self.img, fmt='%.7d', delimiter='  ')        
                        

    def resetImage(self, fpath, fformat):
        self.clearSelection(True)
        self.loadImage(fpath, fformat)
        

    def removeFigure(self):
        self.clearSelection(True)
                

    def axesAdjustment(self):
        # extent is a tuple (left, right, bottom, top)
        extent = self.imgplot.get_extent()        
        self.imgplot.set_extent((0.0, self.img.shape[1], self.img.shape[0], 0.0 ))

        # xlim and ylim
##        self.imgplot.axes.set_xlim(0, 250)
##        self.imgplot.axes.set_ylim(260, 0)

        # Scale
        self.imgplot.autoscale()                
        self.imgplot.axes.relim()
##        self.imgplot.axes.autoscale()
##        self.imgplot.axes.autoscale_view(tight=True, scalex=False, scaley=False)
        
        self.axes = self.imgplot.axes


    def onSelect(self, eclick, erelease):
        print eclick.button        
        self.x0 = eclick.xdata
        self.y0 = eclick.ydata
        
        self.x1 = erelease.xdata
        self.y1 = erelease.ydata

        print self.x0, self.x1, self.y0, self.y1
        

    def onPress(self, event):
        pass
                                            
                       
    def onRelease(self, event):
##        print "released"
        self.y0 = int(round(self.y0, 0))
        self.y1 = int(round(self.y1, 0))
        self.x0 = int(round(self.x0, 0))
        self.x1 = int(round(self.x1, 0))
        if self.y0 > self.y1:
                aux = self.y0
                self.y0 = self.y1
                self.y1 = aux
        if self.x0 > self.x1:
                aux = self.x0
                self.x0 = self.x1
                self.x1 = aux
##        print self.x0, self.x1, self.y0, self.y1
        
        if self.axes == self.caxes:
                self.selection = patches.Rectangle((self.x0, self.y0), self.x1 - self.x0, self.y1 - self.y0,
                                                   alpha=0.5, facecolor='red', edgecolor='black', linewidth=2)
##                        print self.selection.get_xy(), self.axes.patches[len(self.axes.patches)-1].get_xy()
                if self.selection.get_xy() != self.axes.patches[len(self.axes.patches)-1].get_xy():
                        self.axes.add_patch(self.selection)
                        self.list_rectangles.append([self.x0, self.x1, self.y0, self.y1])
                        print "list of rectangles", self.list_rectangles, "\n", len(self.list_rectangles)
                        print self.list_rectangles[0][0]
        print "len of patches list:", len (self.axes.patches)

        return self.y0, self.y1
        

    def onMotion(self, event):
        self.caxes = event.inaxes
        

    def normImage(self):
        """Single line based"""
##                whitespaceline = 80
##                nf = self.img[whitespaceline, :].mean() / self.img[whitespaceline, :]
##                self.img = self.img * nf
        
        """Multiple selections"""
        if len(self.axes.patches) < 3: # If there is only on selection drawed
                print "\none selection\n"
                x0, x1, y0, y1 = self.x0, self.x1, self.y0, self.y1
                nf_00 = self.img[y0:y1, :].mean(0).mean() / self.img[y0:y1, :].mean(0)
                nf_01 = self.img[y0:y1, x0:x1].mean(0).mean() / self.img[y0:y1, :].mean(0)

                nf_10 = self.img[y0:y1, :].mean(1).mean() / self.img[y0:y1, :].mean(0)
                nf_11 = self.img[y0:y1, x0:x1].mean(1).mean() / self.img[y0:y1, :].mean(0)

                print "nf00:", self.img[y0:y1, :].mean(0).mean(), " nf01:", self.img[y0:y1, x0:x1].mean(0).mean()
                print "nf10:", self.img[y0:y1, :].mean(1).mean(), " nf11:", self.img[y0:y1, x0:x1].mean(1).mean()

                print "nf_00", nf_00.mean(), "nf_01", nf_01.mean()
                print "nf_10", nf_10.mean(), "nf_11", nf_11.mean()
                
                print "width:", x1-x0, "lenght:", y1-y0
                nf = nf_00
##                        self.img = self.img * nf_00
##                        self.img = self.img * nf_10
##                        self.imgplot.set_data(self.img)
                print "shape of nf:", nf.shape
        else: # If there are more than one selection drawed
                print "\nmultiple selection\n"
                nfs = np.zeros((len(self.list_rectangles), self.img.shape[1]))
                i = 0
                for rec in self.list_rectangles:
                        x0, x1, y0, y1 = rec[0], rec[1], rec[2], rec[3]
                        print x0, x1, y0, y1
                        nf = self.img[y0:y1, :].mean(0).mean() / self.img[y0:y1, :].mean(0)
                        nfs[i,:] = nf
##                        nf = self.img[:, y0:y1].mean(0).mean() / self.img[:, y0:y1].mean(0)
##                        nfs[:,i] = nf
                        i += 1
                print nfs.mean(0).shape
                nf = nfs.mean(0)
                
        self.img = self.img * nf
        self.imgplot.set_data(self.img)
                

    def clearSelection(self, radio):            
        if len(self.axes.patches) > 1:
                self.axes.patches[len(self.axes.patches)-1].remove()
                del self.list_rectangles[-1]                
        if radio:
                [patch.remove() for patch in self.axes.patches[1:len(self.axes.patches)]]
                self.list_rectangles = []
                
                                
              

                























                
                
                
     
