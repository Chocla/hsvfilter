import cv2
import sys
from PyQt5.QtWidgets import QApplication
import gui

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = gui.Window()
    # print(mainWin.lBound,mainWin.rBound)
    mainWin.show()
    # cap = cv2.VideoCapture(0)

    # while True:
    #     #TODO: Put video frame into gui
    #     _, frame = cap.read()
    #     hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    #     lower = mainWin.lBound
    #     upper = mainWin.rBound
    #     mask = cv2.inRange(hsv, lower, upper)
    #     res = cv2.bitwise_and(frame,frame,mask=mask)
    #     cv2.imshow('res',res)
    #     k = cv2.waitKey(1)
    #     if k == ord('q'):
    #         break

    sys.exit(app.exec_() )