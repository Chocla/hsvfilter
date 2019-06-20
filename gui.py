import sys
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget,QSlider,QFileDialog,QAction
from PyQt5.QtCore import QSize, QObject,QThread,pyqtSlot
from PyQt5.QtGui import QPixmap,QImage
from qrangeslider import QRangeSlider
import numpy as np
import cv2
#TODO: cleanup unneeded imports

class vidThread(QThread):
    changePixmap = QtCore.pyqtSignal(QImage)
    lBound = np.array([0,0,0])
    rBound = np.array([255,255,255])
    
    @pyqtSlot(np.ndarray,np.ndarray)
    def updateSliders(self,a,b):
        self.lBound = a
        self.rBound = b
        print(self.lBound,self.rBound)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret,frame = cap.read()
            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            if ret:
                mask = cv2.inRange(hsv, self.lBound, self.rBound)
                
                res = cv2.bitwise_and(frame,frame,mask=mask)
                h, w, ch = res.shape
                bytesPerLine = ch * w

                convertedToRGB = cv2.cvtColor(res,cv2.COLOR_BGR2RGB)
                converted = QImage(convertedToRGB.data, w,h,bytesPerLine,QtGui.QImage.Format_RGB888)
                
                final =  converted.scaled(640, 480, QtCore.Qt.KeepAspectRatio)

                self.changePixmap.emit(final)
                # cv2.imshow('res',res)

#TODO: Implement a save/import for initial range state.
#TODO: Add more documentation
class Window(QMainWindow):
    lBound = np.array([0,0,0])
    rBound = np.array([255,255,255])
    slidersChanged = QtCore.pyqtSignal(np.ndarray,np.ndarray)
    def __init__(self):
        QMainWindow.__init__(self)
        #Initialize Filter Range Arrays
        self.lBound = np.array([0,0,0])
        self.rBound = np.array([255,255,255])

        self.setMinimumSize(QSize(640,480))
        self.setWindowTitle("Test")
        
        c = QWidget(self)
        self.setCentralWidget(c)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("&File")

        importAction = QAction("&Import Settings",self)
        importAction.setStatusTip("Import HSV Tolerances")
        importAction.triggered.connect(self.importRanges)
        exportAction = QAction("&Export Settings",self)
        exportAction.setStatusTip("Export Current Tolerances")
        exportAction.triggered.connect(self.exportRanges)

        fileMenu.addAction(importAction)
        fileMenu.addAction(exportAction)

        gridLayout = QGridLayout(self)
        c.setLayout(gridLayout)
        self.frame = QLabel(self)
        self.frame.resize(640, 480)
        gridLayout.addWidget(self.frame,0,0,4,4)

        self.th = vidThread()
        self.th.changePixmap.connect(self.setImage)
        self.slidersChanged.connect(self.th.updateSliders)
        self.th.start()

        #Initialize Range Sliders
        self.slider1 = QRangeSlider()
        self.slider1.setFixedHeight(15)
        self.slider2 = QRangeSlider()
        self.slider2.setFixedHeight(15)
        self.slider3 = QRangeSlider()
        self.slider3.setFixedHeight(15)
        gridLayout.addLayout(self.setupSlider(self.slider1, QLabel("Hue"),self.updateRange),5,0)
        gridLayout.addLayout(self.setupSlider(self.slider2, QLabel("Saturation"),self.updateRange),5,1)
        gridLayout.addLayout(self.setupSlider(self.slider3, QLabel("Value"),self.updateRange),5,2)

    def setupSlider(self,slider, label,slot):
        slider.setMin(0)
        slider.setMax(255)
        slider.setEnd(255)
        slider.startValueChanged.connect(slot)
        slider.endValueChanged.connect(slot)
        tmp = QGridLayout(self)
        tmp.addWidget(label,0,0)
        tmp.addWidget(slider,1,0)
        return tmp

    #TODO: Change updateRange to only update the slider that is being changed instead of all of them.
    #TODO: Don't store range arrays in both the Window and vidThread
    def updateRange(self):
        self.lBound[0],self.rBound[0] = self.slider1.getRange()
        self.lBound[1],self.rBound[1] = self.slider2.getRange()
        self.lBound[2],self.rBound[2] = self.slider3.getRange()
        self.slidersChanged.emit(self.lBound,self.rBound)

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.frame.setPixmap(QPixmap.fromImage(image))


    #Sample Open/Save Code

    # def openFileNameDialog(self):
    #     options = QFileDialog.Options()
    #     options |= QFileDialog.DontUseNativeDialog
    #     fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
    #     if fileName:
    #         print(fileName)

    # def saveFileDialog(self):
    #     options = QFileDialog.Options()
    #     options |= QFileDialog.DontUseNativeDialog
    #     fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
    #     if fileName:
    #         print(fileName)

    #TODO: Import a json file to range values
    #TODO: Update Sliders to proper values
    def importRanges(self):
        pass

    #TODO: parse current settings into a json file
    #TODO: prompt user to save that file as whatever
    def exportRanges(self):
        pass

    def testFunc(self):
        print("test!")