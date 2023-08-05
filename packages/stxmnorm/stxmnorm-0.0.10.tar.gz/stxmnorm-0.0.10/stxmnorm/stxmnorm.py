"""
***Source code of Normalizing STXM Project***

Using matplotlib inside QT

- Funtctions:
        - draw vertical lines (patches) on an plot
        - aplies a normalization function on the selected lines
        - using the numpy.mean() function as a first nonrmalization resource
        - 
        - 
        

"""

import os

from imageNorm import imageNorm # imports the module to normalize the image

from PyQt5 import QtCore, QtGui, uic, QtWidgets

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.widgets import  RectangleSelector
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

import sys


p = os.path.dirname(os.path.realpath(__file__))
qtDesignerFile = p + "/stxmnorm.ui" # Enter file created by QTDesigner here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtDesignerFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MyApp, self).__init__()

        self.imageNorm = imageNorm() # instanciates the class to use its modules
        
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.img_orig = None
        self.img = None
        self.imgplot = None
        self.caxes = None
        self.axes = None
        self.mouseispressed = None
        self.openfileformat = None
        

        self.canvas = None
        self.axes = None       
        self.figure = None                        
        self.fig_dict = {} # sets the list of figures of the GUI to empty

        self.fpath = ''
        self.fname = ''
        self.fformat = ''
        self.ssvfpath = ''

        self.y0 = int(0)
        self.y1 = int(0)
        
        # Menu bar actions
        fileOpen = self.file_open
        fileOpen.triggered.connect(self.openFile)        

        fileSave = self.file_save
        fileSave.triggered.connect(self.saveProject)

        fileExport = self.file_export
        fileExport.triggered.connect(self.exportImage)

        editRemoveFigure = self.edit_removefigure
        editRemoveFigure.triggered.connect(self.removeFigure)

        editResetImage = self.edit_resetimage
        editResetImage.triggered.connect(self.resetImage)

##        # Buttons from QT
        """Normalize Image"""
        self.normalize_image.clicked.connect(self.normImage)
        
        """Clear Selections"""
        self.clear_selection.clicked.connect(self.clearSelection)
        

    def openFile(self):
        if self.fpath != '' and self.figure != False:
            self.removeFigure()
        self.fpath = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '',\
                                                           "Images (*.png *.jpg *.tiff *.tif *.ssv);;HDF files (*.h5 *.hdf5);;All Files (*.*)")        
        self.fpath = self.fpath[0]
        self.fname = self.fpath[self.fpath.rindex('/')+1::]
        self.fformat = self.fpath[self.fpath.rindex('.')+1::]
        
        self.figure = self.imageNorm.loadImage(self.fpath, self.fformat) # always add 'self.' to call a member function (functions within a class)
        if self.figure == False:
            QtWidgets.QMessageBox.information(self, "Warning",
"""Unsupported file format!
""")   
        else:
            self.addFigure(self.fname)

     
    def addFigure(self, fname):
        self.canvas = FigureCanvas(self.figure) # send the figure as an argument to plot it        
        self.img_original_vl.addWidget(self.canvas) # add a figure to the vertical layout of the widget

        """ Creates the connections between the canvas, events and the funtions called"""
        self.canvas.figure.canvas.mpl_connect('button_press_event', self.onPress)
        self.canvas.figure.canvas.mpl_connect('button_release_event', self.onRelease)
        self.canvas.figure.canvas.mpl_connect('motion_notify_event', self.onMotion)

        self.selector = RectangleSelector(self.imageNorm.axes, self.imageNorm.onSelect, drawtype='box',
                             spancoords='data', button=1, minspanx=2, minspany=2)
        
        self.addNavigationToolbar()
        
        self.canvas.draw()
        self.canvas.update()        
        
        self.image_list.addItem(self.fname)


    def addNavigationToolbar(self):
        """
        self.toolbar = NavigationToolbar(self.canvas,\
                self, coordinates=True)
        self.addToolBar(self.toolbar)
        """
        # Personalization of Buttons in the NavigationToolbar
        NavigationToolbar.toolitems = ((u'Home', u'Reset original view', u'home', u'home'), (u'Back', u'Back to  previous view', u'back', u'back'),
                                       (u'Forward', u'Forward to next view', u'forward', u'forward'), (None, None, None, None),
                                       (u'Pan', u'Pan axes with left mouse, zoom with right', u'move', u'pan'), (u'Zoom', u'Zoom to rectangle', u'zoom_to_rect', u'zoom'),
                                       (None, None, None, None))
        
        
        # add fixed toolbar       
        self.toolbar = NavigationToolbar(self.canvas,\
                self.image_original, coordinates=True)        
        self.img_original_vl.addWidget(self.toolbar)


    def onPress(self, event):
        self.imageNorm.onPress(event)

        
    def onRelease(self, event):
        self.y0, self.y1 = self.imageNorm.onRelease(event)
        self.selection_y0.setValue(self.y0)
        self.selection_y1.setValue(self.y1)


    def onMotion(self, event):
        self.imageNorm.onMotion(event)
        

    def saveProject(self):
        savename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '',\
                                                         "(*.h5);; (*.hdf5)")
        save = self.imageNorm.saveProject(savename, self.fformat)
        if save == False:
            QtWidgets.QMessageBox.information(self, "Warning",
"""The file loaded must be of ssv or hdf5 type in order to Save a Project.
If you want ot export the image as tif, jpg, png, etc use the Export button.
""")   
            
        self.canvas.figure.canvas.draw()
        

    def exportImage(self):
        exportname = QtWidgets.QFileDialog.getSaveFileName(self, 'Export File', '',
                                                           "(*.png);;(*.tif);;(*.jpg);;(*.bmp);;(*.ico);;(*.jpeg);;(*.ppm);;(*.tiff);;(*.xbm);;(*.xpm);;(*.ssv)")
        self.imageNorm.exportImage(exportname)
        self.canvas.figure.canvas.draw()


    def resetImage(self):
        self.imageNorm.resetImage(self.fpath, self.fformat)
        self.canvas.figure.canvas.draw()
        
                
    def removeFigure(self):
        self.imageNorm.removeFigure()
        self.img_original_vl.removeWidget(self.canvas)
        self.canvas.close()
        self.img_original_vl.removeWidget(self.toolbar)
        self.toolbar.close()
        self.fig_dict.clear()
        self.image_list.clear()
        

    def normImage(self):
        self.imageNorm.normImage()
        self.canvas.figure.canvas.draw()
        

    def clearSelection(self):
        self.imageNorm.clearSelection(self.clear_all_selections.isChecked())
        self.canvas.figure.canvas.draw()
        
        
def gui():
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
    
              
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

