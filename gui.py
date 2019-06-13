import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget,QSlider
from PyQt5.QtCore import QSize  

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

        #TODO: (Joe) Find double sided sliders to use instead of these
        #TODO: (Joe) Connect Sliders with variables that control HSV ranges
        #TODO: (Joe) Add Labels for the sliders
        slider1 = QSlider(QtCore.Qt.Horizontal)
        gridLayout.addWidget(slider1,1,0)
        slider2 = QSlider(QtCore.Qt.Horizontal)
        gridLayout.addWidget(slider2,1,1)
        slider3 = QSlider(QtCore.Qt.Horizontal)
        gridLayout.addWidget(slider3,1,2)