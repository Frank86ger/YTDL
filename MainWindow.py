# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from SubDiag import Ui_Dialog
from Worker import TaskQueueThread, YTDLThread, Stream
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(300, 30, 281, 21))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(30, 80, 741, 181))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(350, 270, 97, 27))
        self.pushButton.setObjectName("pushButton")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(30, 320, 741, 221))
        self.textBrowser_2.setObjectName("textBrowser_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        #TODO DUMB
        #dumb - vllt auch errors? was ist mit yt-dl msgs ?
        sys.stdout = Stream(newText=self.onUpdateText)


        #color schemes
        self.color_scheme = {'todo': '676767', 'doing': '000000', 'done': '00ff00', 'failed': 'ff0000'}

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Open the sub dialog on button clicked.
        self.pushButton.clicked.connect(self.openDiag)

        # Init TaskList and Download Threads
        self.taskQueueThread = TaskQueueThread()
        self.ytdlThread = YTDLThread()

        # Connect Signal and Slots of Threads
        # Update DONE of FAILED tasks: ytdlThread > ListThread
        self.ytdlThread.job_done_signal.connect(self.update_task_status)
        # Update Text Field. Brauche ich das? Ja! Immer wieder Textfeld neu (+methode)
        self.taskQueueThread.myUpdatedTaskList.connect(self.update_text_field)
        # Emit new Task to ytdl
        self.taskQueueThread.myDownloadTaskSignal.connect(self.add_new_task_to_dl_thread)

        # Start Threads
        self.taskQueueThread.start()
        self.ytdlThread.start()

    #remove else when tested on website
    def update_task_status(self, yt_task):
        if (len(yt_task[0]) > 0):
            self.taskQueueThread.update_task_status(yt_task)
        else:
            #self.taskQueueThread.update_task_status(yt_task)
            pass
    
    def add_new_task_to_dl_thread(self, yt_task):
        self.ytdlThread.yt_task_setter(yt_task)
    
    #needs change. currently for debug without internet
    def update_text_field(self, yt_task_queue):
        #outstr = r''
        #for task in yt_task_queue:
        #    outstr += task[2]
        #self.textBrowser.setText(outstr)
        self.textBrowser.setText(self.list2string(yt_task_queue))

    #TODO    
    #moredump
    def onUpdateText(self, text):
        cursor = self.textBrowser_2.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser_2.setTextCursor(cursor)
        self.textBrowser_2.ensureCursorVisible()
    
    def __del__(self):
        sys.stdout = sys.__stdout__
        


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "YouTubeDownloader"))
        self.pushButton.setText(_translate("MainWindow", "ADD"))

    def openDiag(self):
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()
        ui.yt_task # Diesen Task hinzufuergen
        self.taskQueueThread.yt_task_queue.append(ui.yt_task) # aaaaaber, wenn der append in der schleife stattfindet . ists okay
        #print(self.taskQueueThread.yt_task_queue) # kann auch ma wieder weg

    #puh aufgepasst, lieber die liste parsen
    def list2string(self, yt_task_queue):
        ##if len(self.yt_task_queue) == 0:
        if len(yt_task_queue) == 0:
            return ' '
        else:
            mystr = ''
            #for task in self.yt_task_queue:
            for task in yt_task_queue:
                word = '<span style=\" color: #%s;\">%s <br></span>' % (self.color_scheme[task[2]], task[1])
                mystr += word
            return mystr


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

