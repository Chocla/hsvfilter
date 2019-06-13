import cv2
import sys
from PyQt5.QtWidgets import QApplication
import gui

#TODO: (Joe) Write HSV Filter (lol)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = gui.Window()
    mainWin.show()
    sys.exit(app.exec_() )