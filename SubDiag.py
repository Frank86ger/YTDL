# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SubDiag.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import urllib.request
from bs4 import BeautifulSoup
import time
import pyperclip

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(861, 274)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(330, 220, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(30, 50, 801, 27))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(30, 150, 801, 27))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(100, 80, 61, 27))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 80, 61, 27))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 30, 151, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 130, 101, 17))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        
        Dialog.accepted.connect(self.create_yt_task)
        self.yt_task = []

        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton_2.clicked.connect(self.paste_from_clipboard)
        self.pushButton.clicked.connect(self.get_yt_title)

        self.yt_title = ''
        self.yt_url = ''

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "CHECK"))
        self.pushButton_2.setText(_translate("Dialog", "PASTE"))
        self.label.setText(_translate("Dialog", "YouTube URL"))
        self.label_2.setText(_translate("Dialog", "Audio Name"))

    # Paste clipboard to URL field.
    def paste_from_clipboard(self):
        self.lineEdit.setText(pyperclip.paste())

    #try and catch exceptions (no internet connection or invalid youtube url)
    def get_yt_title(self):
        try:
            url = self.lineEdit.text()
            self.yt_url = url
            if (self.yt_url.find('youtube') == -1):
                self.lineEdit_2.setStyleSheet("color: red;")
                self.lineEdit_2.setText('No YOUTUBE url has been entered!')
                self.yt_title = ''
            else:
                soup = BeautifulSoup(urllib.request.urlopen(url), 'lxml')
                self.lineEdit_2.setStyleSheet("color: black;")
                self.lineEdit_2.setText(soup.title.string[:-10])
                self.yt_title = soup.title.string[:-10]
        except:
            failedText = 'No connection to that website could be established.'
            self.lineEdit_2.setStyleSheet("color: red;")
            self.lineEdit_2.setText(failedText)
            self.yt_title = ''

    # clean/reinigen string of special chars
    def perhaps_some_regex_magix(self):
        pass

    # irgendwas nicht okay? return []. OK button ausgrauen solange keine passende URL eingefuegt? ... later dude
    def create_yt_task(self):
        self.yt_task = [self.yt_url, self.yt_title, 'todo']


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

