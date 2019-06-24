import sys
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget,QSlider,QFileDialog,QAction
from PyQt5.QtCore import QSize, QObject,QThread,pyqtSlot
from PyQt5.QtGui import QPixmap,QImage
from qrangeslider import QRangeSlider
import numpy as np
import cv2
import json

#TODO: cleanup unneeded imports

class vidThread(QThread):
    changePixmap = QtCore.pyqtSignal(QImage)

    # def __init__(self):
    lBound = np.array([0,0,0])
    rBound = np.array([255,255,255])
    
    @pyqtSlot(int)
    def updateRange(self,n):
        sliderID = self.sender().ID
        self.lBound[sliderID],self.rBound[sliderID] = self.sender().getRange()

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


#TODO: Rethink how the range data is getting sent back and forth between the window and the thread

#TODO: Add more documentation
class Window(QMainWindow):
    # lBound = np.array([0,0,0])
    # rBound = np.array([255,255,255])

    def __init__(self):
        QMainWindow.__init__(self)
        #Initialize Filter Range Arrays
        # self.lBound = np.array([0,0,0])
        # self.rBound = np.array([255,255,255])

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
        # self.slidersChanged.connect(self.th.updateSliders)
        self.th.start()

        #Initialize Range Sliders
        self.slider1 = QRangeSlider()
        self.slider1.setFixedHeight(15)
        self.slider2 = QRangeSlider(None,1)
        self.slider2.setFixedHeight(15)
        self.slider3 = QRangeSlider(None,2)
        self.slider3.setFixedHeight(15)
        gridLayout.addLayout(self.setupSlider(self.slider1, QLabel("Hue"),self.th.updateRange),5,0)
        gridLayout.addLayout(self.setupSlider(self.slider2, QLabel("Saturation"),self.th.updateRange),5,1)
        gridLayout.addLayout(self.setupSlider(self.slider3, QLabel("Value"),self.th.updateRange),5,2)
        self.slider1.drawValues()

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

    # def updateRange(self):
    #     self.lBound[0],self.rBound[0] = self.slider1.getRange()
    #     self.lBound[1],self.rBound[1] = self.slider2.getRange()
    #     self.lBound[2],self.rBound[2] = self.slider3.getRange()
    #     self.slidersChanged.emit(self.lBound,self.rBound)

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.frame.setPixmap(QPixmap.fromImage(image))

    #TODO: Update Sliders to proper values
    def importRanges(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, tmp = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;JSON Files (*.json)", options=options)
        if filename != "":
            f = open(filename,'r')
            data = json.load(f)
        else:
            return

        try:
            self.lBound[0] = data['lower']['h']
            self.lBound[1] = data['lower']['s']
            self.lBound[2] = data['lower']['v']
            self.rBound[0] = data['upper']['h']
            self.rBound[1] = data['upper']['s']
            self.rBound[2] = data['upper']['v']

            print("Import Print 0", self.lBound,self.rBound)
            self.slidersChanged.emit(self.lBound,self.rBound)
            self.slider1.setRange(self.lBound[0],self.rBound[0])
            self.slider2.setRange(self.lBound[1],self.rBound[1])
            self.slider3.setRange(self.lBound[2],self.rBound[2])  
            self.slider1.drawValues()
            self.slider2.drawValues()
            self.slider3.drawValues()
            print("Import Print 1", self.lBound,self.rBound)
        except:
            print("Error Parsing JSON File, Values not imported")

    def exportRanges(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()","","All Files (*);;JSON Files (*.json)", options=options)
        if fileName != "":
            f = open(fileName,'w')
        l1,l2,l3 = self.lBound
        r1,r2,r3 = self.rBound
        print(l1,l2,l3,self.lBound)
        jString = "{{\"lower\": {{\"h\": \"{}\", \"s\": \"{}\", \"v\": \"{}\"}}, \"upper\": {{\"h\": \"{}\", \"s\": \"{}\", \"v\": \"{}\" }}}}".format(l1,l2,l3,r1,r2,r3)
        f.write(jString)
  