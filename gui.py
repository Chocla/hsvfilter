from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget,QFileDialog,QAction
from PyQt5.QtCore import QSize, QThread,pyqtSlot
from PyQt5.QtGui import QPixmap,QImage
from qrangeslider import QRangeSlider
import numpy as np
import cv2
import json

class vidThread(QThread):
    changePixmap = QtCore.pyqtSignal(QImage)

    lBound = np.array([0,0,0])
    rBound = np.array([255,255,255])

    #Pixel Coordinates for drawing direction arrow
    # (a,a) - (b,a) - (c,a)
    #   |               |
    # (a,b)           (c,b)
    #   |               |
    # (a,c) - (b,c) - (c,c) 
    a,b,c = 40,55,70
    #Order:
    #Up Left, Up, Up Right, Right, Down Right, Down, Down Left, Right
    arrowStart = np.array([
        (c,c), (b,c), (a,c), (a,b), (a,a), (b,a), (c,a), (c,b)
    ])
    arrowEnd = np.array([
        (a,a), (b,a), (c,a), (c,b), (c,c), (b,c), (a,c), (a,b)
    ])

    @pyqtSlot(int)
    def updateRange(self,n):
        sliderID = self.sender().ID
        self.lBound[sliderID],self.rBound[sliderID] = self.sender().getRange()
        print("Range:", self.lBound,self.rBound)

    def run(self):
        flag = True
        cap = cv2.VideoCapture(0)
        while True:
            ret,frame = cap.read()
            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            if ret:
                mask = cv2.inRange(hsv, self.lBound, self.rBound)
                #Finds contours of all regions
                contours, h = cv2.findContours(mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                
                if len(contours) != 0:
                    #Gets the biggest contour and draws a bounding rectangle for it
                    maxContour = self.findBiggestContour(contours)
                    rx,ry,rw,rh = cv2.boundingRect(maxContour)
                    cv2.rectangle(frame,(rx,ry), (rx+rw,ry+rh),(0,0,255))
                region = self.calculateDirection(rx,ry,rw,rh,frame.shape)
                cv2.arrowedLine(frame, tuple(self.arrowStart[region]),tuple(self.arrowEnd[region]), (255,0,0),4)

                #Converting to Qt Image for displaying
                h, w, ch = frame.shape
                bytesPerLine = ch * w
                convertedToRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                converted = QImage(convertedToRGB.data, w,h,bytesPerLine,QtGui.QImage.Format_RGB888)
                final =  converted.scaled(640, 480, QtCore.Qt.KeepAspectRatio)

                self.changePixmap.emit(final)
    #Calculates which region the center of the boundary box is in
    def calculateDirection(self,x,y,h,w,shape):
        vec = (x + (w/2) - (shape[1]/2), -(y + (h/2)) +(shape[0]/2))
      
        theta = np.arctan2([vec[1]],[vec[0]])[0]*(180/np.pi)
        if theta < 0:
            theta += 360
        region = int( ((theta - 22.5) % 360) / 45 )
        
        return region
    def findBiggestContour(self, contours):
        maxArea = 0
        maxIndex = 0
        i = 0
        while i < len(contours):
            tmpArea = cv2.contourArea(contours[i])
            if tmpArea > maxArea:
                maxArea = tmpArea
                maxIndex = i
            i += 1
        return contours[maxIndex]

#TODO: Add more documentation
class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(640,480))
        self.setWindowTitle("Test")
        
        c = QWidget(self)
        self.setCentralWidget(c)
        #TODO: Add a Menu that allows user to select from certain preset filters (commonly used)
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

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.frame.setPixmap(QPixmap.fromImage(image))

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
            self.slider1.setRange(int(data['lower']['h']),int(data['upper']['h']))
            self.slider2.setRange(int(data['lower']['s']),int(data['upper']['s']))
            self.slider3.setRange(int(data['lower']['v']),int(data['upper']['v']))
        except:
            print("Error Parsing JSON File, Values not imported")

    def exportRanges(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()","","All Files (*);;JSON Files (*.json)", options=options)
        if fileName != "":
            f = open(fileName,'w')
        l1,l2,l3 = self.th.lBound
        r1,r2,r3 = self.th.rBound

        jString = "{{\"lower\": {{\"h\": \"{}\", \"s\": \"{}\", \"v\": \"{}\"}}, \"upper\": {{\"h\": \"{}\", \"s\": \"{}\", \"v\": \"{}\" }}}}".format(l1,l2,l3,r1,r2,r3)
        f.write(jString)
  