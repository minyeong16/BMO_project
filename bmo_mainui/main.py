import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import subprocess
import random
import time
import os

#QTdesigner를 통해 생성한 ui파일을 로드
form_class1 = uic.loadUiType('main2.ui')[0]
#현재 페이지를 기록하는 전역변수
CurrentIndex = 0
#프로그램 실행과 동시에 구글 어시스턴트를 서브프로세스로 실행
subprocess.Popen("googlesamples-assistant-hotword --project_id bmo-assistant-f4b98 --device_model_id bmo-assistant-f4b98-bmo-3x19ql", shell=True)

#gui의 메인 class
class MyWindow(QMainWindow, form_class1):
    def __init__(self):
        super().__init__()
        self.setupUi(self) #로드한 ui파일 셋팅
        self.setWindowTitle('BMO') #타이틀 설정
        self.resize(480, 320) #해상도 설정
        self.center() #화면 중앙정렬 함수 실행

        #imagelist에 배경그림을 넣어두고, QPixmap을 사용하여 랜덤으로 로드
        self.imagelist = ['image/bmo3.png', 'image/bmoangry.png', 'image/bmoeyeclose.png', 'image/bmoholy.png', 'image/bmosmile.png']
        pixmap = QPixmap(self.imagelist[random.randint(0, 4)])
        self.label.setPixmap(pixmap)

        #버튼과 리스트 등의 클릭 이벤트 함수 선언
        self.pushButton.clicked.connect(self.main_clicked)
        self.pushButton_2.clicked.connect(self.add_clicked)
        self.back_main.clicked.connect(self.back1_clicked)
        self.back_manu.clicked.connect(self.back2_clicked)
        self.setting.clicked.connect(self.setting_clicked)
        self.listWidget.itemClicked.connect(self.game_clicked)
        self.restart.clicked.connect(self.restart_clicked)
        self.sys_reboot.clicked.connect(self.reboot_clicked)
        self.sys_shutdown.clicked.connect(self.shutdown_clicked)
        #bmo exit 버튼을 누를 경우 프로그램 종료
        self.exit.clicked.connect(QCoreApplication.instance().quit)

        #gui 실행
        self.show()

    #화면을 중앙정렬해주는 함수
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    #키보드 입력을 받아오는 함수
    def keyPressEvent(self, e):
        #만일 현재 페이지가 0번째 페이지라면 키 입력을 받았을 때 1번째 페이지로 이동
        if(CurrentIndex == 0):
            self.stackedWidget.setCurrentIndex(1)

    #0번째 페이지의 버튼을 눌렀을 경우 발생하는 이벤트 함수
    def main_clicked(self):
        #1번째 페이지로 이동하고 페이지를 기록하는 전역변수의 값을 1로 변경한다.
        self.stackedWidget.setCurrentIndex(1)
        CurrentIndex = 1

    #1번째 페이지에서 +버튼을 눌렀을 경우 발생하는 이벤트 함수
    def add_clicked(self):
        #파일을 불러오는 다이얼로그를 실행하고 그 파일의 경로를 리스트 항목에 추가
        fname = QFileDialog.getOpenFileName(self)
        self.listWidget.addItem(fname[0])

    #1번째 페이지의 리스트를 클릭했을 때 발생하는 이벤트 함수
    def game_clicked(self, item):
        #각 항목을 클릭하면 경로에 있는 프로그램을 서브프로세스로 실행시킨다.
        #1번째와 2번째 항목의 경우 기본항목이므로 경로를 직접 정해준다.
        if(item.text()=="- game1.py"):
            subprocess.call("python3"+" /home/pi/BMO_project/pygame/pygame_pyflying/pyflying.py", shell=True)
        elif(item.text()=="- game2.py"):
            subprocess.call("python3"+" /home/pi/BMO_project/bmoGame_project/game.py", shell=True)
        else:
            #여기서부터는 +버튼을 이용하여 직접 추가해준 프로그램을 실행하기 위한 경로 설정 코드이다.
            #파이썬 파일의 경우 파이썬 셀로 실행시키고, 나머지 경우에는 직접 실행시키는 방식을 사용한다.
            if(os.path.splitext(item.text())[1] == ".py"):
                subprocess.call("python3"+" {}".format(item.text()), shell=True)
                #print("python3"+" {}".format(item.text()))
            else:
                subprocess.call("cd {}".format(os.path.split(item.text())[0]) + "&&./{}".format(os.path.split(item.text())[1]), shell=True)
                #print("{}".format(os.path.split(item.text())[0]))

    #1번째 페이지에서 구석의 비모 본체 버튼을 눌렀을 경우 발생하는 이벤트 함수
    def back1_clicked(self):
        #QPixmap을 사용하여 imagelist에 저장해둔 배경그림을 랜덤으로 로드
        pixmap = QPixmap(self.imagelist[random.randint(0, 4)])
        self.label.setPixmap(pixmap)
        self.stackedWidget.setCurrentIndex(0)
        CurrentIndex = 0

    #1번째 페이지에서 SETTING버튼을 눌렀을 경우 발생하는 이벤트 함수
    def setting_clicked(self):
        #2번째 페이지로 이동하고 페이지를 기록하는 전역변수의 값을 2로 변경한다.
        self.stackedWidget.setCurrentIndex(2)
        CurrentIndex = 2

    #2번째 페이지에서 back버튼을 눌렀을 경우 발생하는 이벤트 함수
    def back2_clicked(self):
        #1번째 페이지로 이동하고 페이지를 기록하는 전역변수의 값을 1로 변경한다.
        self.stackedWidget.setCurrentIndex(1)
        CurrentIndex = 1
       
    #2번째 페이지의 restart버튼을 누를 경우 발생하는 이벤트 함수
    def restart_clicked(self):
        #현재 실행되고 있는 gui창을 종료하고 자기자신의 서브프로세스를 불러온다.
        self.close()
        subprocess.call("python3"+" main.py", shell=True)

    #2번째 페이지의 shutdown버튼을 누를 경우 발생하는 이벤트 함수
    def shutdown_clicked(self):
        #라즈베리파이를 종료시킨다.
        os.system('sudo shutdown now')

    #2번째 페이지의 reboot버튼을 누를 경우 발생하는 이벤트 함수
    def reboot_clicked(self):
        #라즈베리파이를 재시작한다.
        os.system("sudo reboot")

if __name__ == '__main__':
    app = QApplication(sys.argv) #프로그램 실행
    mywindow = MyWindow() #gui 창 실행
    mywindow.showFullScreen() #전체 화면으로 실행
    sys.exit(app.exec_()) #프로그램 종료시 처리되는 구문