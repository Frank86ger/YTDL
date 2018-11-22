# -*- coding: utf-8 -*-
"""
Small script, to download Youtube videos and convert to *.mp3s
"""
__author__ = "Frank Ehebrecht"
__copyright__ = "Copyright 2018"
__license__ = "GPL"

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
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Redirect stdout to textBrowser_2.
        sys.stdout = Stream(newText=self.onUpdateText)

        # Define color schemes for processing history.
        self.color_scheme = {'todo': '676767', 'doing': '000000', 'done': '00ff00', 'failed': 'ff0000'}

        # Open the sub dialog on button clicked.
        self.pushButton.clicked.connect(self.openDiag)

        # Initialize TaskList-Thread and Download-Thread.
        self.taskQueueThread = TaskQueueThread()
        self.ytdlThread = YTDLThread()

        # Connect Signal and Slots of Threads
        # Update DONE of FAILED tasks: ytdlThread -> taskQueueThread
        self.ytdlThread.job_done_signal.connect(self.update_task_status)
        # Update Text Field.
        self.taskQueueThread.myUpdatedTaskList.connect(self.update_text_field)
        # Emit new Task from taskQueueThread to ytdlThread.
        self.taskQueueThread.myDownloadTaskSignal.connect(self.add_new_task_to_dl_thread)

        # Start Threads.
        self.taskQueueThread.start()
        self.ytdlThread.start()

    # Add task to taskQueue.
    def update_task_status(self, yt_task):
        if (len(yt_task[0]) > 0):
            self.taskQueueThread.update_task_status(yt_task)
    
    # Add task to downloader.
    def add_new_task_to_dl_thread(self, yt_task):
        self.ytdlThread.yt_task_setter(yt_task)
    
    # Update text of textBrowser.
    def update_text_field(self, yt_task_queue):
        self.textBrowser.setText(self.list2string(yt_task_queue))

    # Helper for redirect of stdout.
    def onUpdateText(self, text):
        cursor = self.textBrowser_2.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser_2.setTextCursor(cursor)
        self.textBrowser_2.ensureCursorVisible()
    
    # Helper for redirect of stdout.
    def __del__(self):
        sys.stdout = sys.__stdout__

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "YouTubeDownloader"))
        self.pushButton.setText(_translate("MainWindow", "ADD"))

    # Open dialog to enter URL and file name.
    def openDiag(self):
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()
        # Append task to task list.
        self.taskQueueThread.yt_task_queue.append(ui.yt_task)

    # Convert task list to layouted string
    def list2string(self, yt_task_queue):
        if len(yt_task_queue) == 0:
            return ' '
        else:
            mystr = ''
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
