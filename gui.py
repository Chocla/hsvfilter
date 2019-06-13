import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
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