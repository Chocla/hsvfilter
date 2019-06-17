import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget,QSlider
from PyQt5.QtCore import QSize, QObject
from qrangeslider import QRangeSlider
import numpy as np

class Window(QMainWindow):
    lBound = np.array([0,0,0])
    rBound = np.array([255,255,255])
    def __init__(self):
        QMainWindow.__init__(self)
        #Initialize Filter Range Arrays
        self.lBound = np.array([0,0,0])
        self.rBound = np.array([255,255,255])

        self.setMinimumSize(QSize(640,480))
        self.setWindowTitle("Test")
        
        c = QWidget(self)
        self.setCentralWidget(c)

        gridLayout = QGridLayout(self)
        c.setLayout(gridLayout)
        title = QLabel("Video",self)
        title.setAlignment(QtCore.Qt.AlignCenter)
        gridLayout.addWidget(title,0,0,4,4)

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
    def updateRange(self):
        self.lBound[0],self.rBound[0] = self.slider1.getRange()
        self.lBound[1],self.rBound[1] = self.slider2.getRange()
        self.lBound[2],self.rBound[2] = self.slider3.getRange()
        print(self.lBound,self.rBound)