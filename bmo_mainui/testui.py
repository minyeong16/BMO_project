import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import subprocess
import random

form_class1 = uic.loadUiType('main.ui')[0]
# form_class2 = uic.loadUiType('main.ui')[0]
CurrentIndex = 0
 
class MyWindow(QMainWindow, form_class1):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Centering')
        self.resize(480, 320)
        self.center()
        self.imagelist = ['image/bmo3.png', 'image/bmoangry.png', 'image/bmoeyeclose.png', 'image/bmoholy.png', 'image/bmosmile.png']
        pixmap = QPixmap(self.imagelist[random.randint(0, 4)])
        self.label.setPixmap(pixmap)
        self.pushButton.clicked.connect(self.main_clicked)
        self.back_main.clicked.connect(self.back1_clicked)
        self.back_manu.clicked.connect(self.back2_clicked)
        self.setting.clicked.connect(self.setting_clicked)
        self.exit.clicked.connect(QCoreApplication.instance().quit)
        self.restart.clicked.connect(self.restart_clicked)
        
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, e):
        if(CurrentIndex == 0):
            self.stackedWidget.setCurrentIndex(1)
    
    def main_clicked(self):
        self.stackedWidget.setCurrentIndex(1)
        CurrentIndex = 1

    def back1_clicked(self):
        pixmap = QPixmap(self.imagelist[random.randint(0, 4)])
        self.label.setPixmap(pixmap)
        self.stackedWidget.setCurrentIndex(0)
        CurrentIndex = 0

    def back2_clicked(self):
        self.stackedWidget.setCurrentIndex(1)
        CurrentIndex = 1
        
    def setting_clicked(self):
        self.stackedWidget.setCurrentIndex(2)
        CurrentIndex = 2

    def restart_clicked(self):
        self.close()
        subprocess.call("python"+" testui.py", shell=True)
    
if __name__ =='__main__':
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    sys.exit(app.exec_())