import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget,QSlider
from PyQt5.QtCore import QSize  
from qrangeslider import QRangeSlider

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.setMinimumSize(QSize(640,480))
        self.setWindowTitle("Test")
        
        c = QWidget(self)
        self.setCentralWidget(c)

        gridLayout = QGridLayout(self)
        c.setLayout(gridLayout)
        title = QLabel("Hello World ",self)
        title.setAlignment(QtCore.Qt.AlignCenter)
        gridLayout.addWidget(title,0,0)

        #TODO: (Joe) Connect Sliders with variables that control HSV ranges
        
        self.slider1 = QRangeSlider()
        self.slider1.setFixedHeight(15)
        self.slider2 = QRangeSlider()
        self.slider2.setFixedHeight(15)
        self.slider3 = QRangeSlider()
        self.slider3.setFixedHeight(15)
        gridLayout.addLayout(self.setupSlider(self.slider1, QLabel("Hue")),1,0)
        gridLayout.addLayout(self.setupSlider(self.slider2, QLabel("Saturation")),1,1)
        gridLayout.addLayout(self.setupSlider(self.slider3, QLabel("Value")),1,2)

    def setupSlider(self,slider, label):
        slider.setMin(0)
        slider.setMax(255)
        tmp = QGridLayout(self)
        tmp.addWidget(label,0,0)
        tmp.addWidget(slider,1,0)
        return tmp