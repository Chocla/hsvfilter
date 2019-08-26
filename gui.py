from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget,QFileDialog,QAction
from PyQt5.QtCore import QSize, QThread,pyqtSlot
from PyQt5.QtGui import QPixmap,QImage
from qrangeslider import QRangeSlider
import numpy as np
import cv2
import json

#TODO: Add color filter object detection
#TODO: Draw a box around detected object
class vidThread(QThread):
    changePixmap = QtCore.pyqtSignal(QImage)

    lBound = np.array([0,0,0])
    rBound = np.array([255,255,255])
    
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
                
                res = cv2.bitwise_and(frame,frame,mask=mask)


                #cv2.rectangle(res, (50,50),(100,100), (255,0,0), 2)
                h, w, ch = res.shape
                bytesPerLine = ch * w

                convertedToRGB = cv2.cvtColor(res,cv2.COLOR_BGR2RGB)
                converted = QImage(convertedToRGB.data, w,h,bytesPerLine,QtGui.QImage.Format_RGB888)
                
                final =  converted.scaled(640, 480, QtCore.Qt.KeepAspectRatio)

                self.changePixmap.emit(final)
    #Return (x1,y1) (x2,y2) coordinates corresponding to the boundaries of the object
    def findBoundaries(self,image):
        h,w, ch = image.shape
        x1,y1 = h,w
        for i in np.arange(h, 0, -1):
            print(image[0][i])
            for j in np.arange(w,0, -1):
                if j < x1 and i < y1 and image[j,i].all() != np.array([0,0,0]).all():
                    x1,y1, = j,i
        print(x1,y1)

        #First idea:
        #find the minimum x and y val that aren't black
        #find the maximum x and y val that aren't black
        #use those as coords
        #Downsides:
        #doesn't take into account connectedness of pixels that correspond to an object
        #so 1 stray pixel screws up the box boundaries significantly
        #Somehow, I need to capture the idea of a region, regression?

        #Second Idea:
        #Just use an opencv function lole cv2.contour seems to be a good choice.
        pass

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
  