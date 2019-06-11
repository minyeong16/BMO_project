import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import subprocess
import random
import time
import os

form_class1 = uic.loadUiType('main.ui')[0]
# form_class2 = uic.loadUiType('main.ui')[0]
CurrentIndex = 0

subprocess.Popen("googlesamples-assistant-hotword --project_id bmo-assistant-f4b98 --device_model_id bmo-assistant-f4b98-bmo-3x19ql", shell=True)

class MyWindow(QMainWindow, form_class1):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('BMO')
        self.resize(480, 320)
        self.center()
        self.imagelist = ['image/bmo3.png', 'image/bmoangry.png', 'image/bmoeyeclose.png', 'image/bmoholy.png', 'image/bmosmile.png']
        pixmap = QPixmap(self.imagelist[random.randint(0, 4)])
        self.label.setPixmap(pixmap)
        self.pushButton.clicked.connect(self.main_clicked)
        self.back_main.clicked.connect(self.back1_clicked)
        self.back_manu.clicked.connect(self.back2_clicked)
        self.setting.clicked.connect(self.setting_clicked)
        # self.game1.clicked.connect(self.g1_clicked)
        # self.game2.clicked.connect(self.g2_clicked)
        self.exit.clicked.connect(QCoreApplication.instance().quit)
        self.restart.clicked.connect(self.restart_clicked)
        self.sys_reboot.clicked.connect(self.reboot_clicked)
        self.sys_shutdown.clicked.connect(self.shutdown_clicked)

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
        subprocess.call("python3"+" testui.py", shell=True)

    def shutdown_clicked(self):
        os.system('sudo shutdown now')

    def reboot_clicked(self):
        os.system("sudo reboot")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.showFullScreen()
    sys.exit(app.exec_())
