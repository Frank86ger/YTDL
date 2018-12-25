# -*- coding: utf-8 -*-
"""
Small script, to download Youtube videos and convert to *.mp3s
"""
__author__ = "Frank Ehebrecht"
__copyright__ = "Copyright 2018"
__license__ = "GPL"

import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QThread, pyqtSlot
import time
import youtube_dl
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os

# Task Queue Thread: Update task queue and emit next download task
class TaskQueueThread(QThread):

    myDownloadTaskSignal = pyqtSignal(list)
    myUpdatedTaskList = pyqtSignal(list)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.yt_task_queue = []
        self.yt_task_update = []

    def run(self):
        # No 'doing'? -> emit first 'todo'
        while True:
            # Download done? Set status to 'done' or 'failed'
            running_task = False
            if (len(self.yt_task_update) != 0):
                for (idx, task) in enumerate(self.yt_task_queue):
                    if (self.yt_task_update[0] == task[0]):
                        self.yt_task_queue[idx][2] = self.yt_task_update[2]
                        self.yt_task_update = []
                        break

            # Is there a download running?
            for task in self.yt_task_queue:
                if task[2]=='doing':
                    running_task = True
                    break

            # If no download is running, emit next task.
            if not running_task:
                for (idx, task) in enumerate(self.yt_task_queue):
                    if task[2] == 'todo':
                        self.yt_task_queue[idx][2] = 'doing'
                        self.myDownloadTaskSignal.emit(task) #  To create new DL task.
                        break
            self.myUpdatedTaskList.emit(self.yt_task_queue) #  To update textfield.
            time.sleep(0.5)
    
    # Slot, the ytdlThread docks to.
    @pyqtSlot(list)
    def update_task_status(self, yt_task):
        self.yt_task_update = yt_task

# Download YoutubeVideo
class YTDLThread(QThread):

    # Signal for task queue, that download process has finished.
    job_done_signal = pyqtSignal(list)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.yt_task = []
    
    def run(self):
        while True:
            time.sleep(0.5)
            if (len(self.yt_task) != 0):
                try:
                    self.download_music(self.yt_task)
                    self.yt_task[2] = 'done'
                    self.job_done_signal.emit(self.yt_task)
                    self.yt_task = []
                except:
                    self.yt_task[2] = 'failed'
                    self.job_done_signal.emit(self.yt_task)
                    self.yt_task = []

    def download_music(self, yt_task):
        #title = yt_task[1]
        video_url = yt_task[0]

        f = open("outfolder.txt", 'rt')
        out_folder = f.readline()[:-1]
        f.close()
        title = os.path.join(out_folder, yt_task[1])

        ydl_opts = {
            'outtmpl': '{}.%(ext)s'.format(title),
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        #return {
        #    'audio': open('{}.mp3'.format(title), 'rb'),
        #    'title': title,
        #}

    # Slot to set yt_task.
    @pyqtSlot(list)
    def yt_task_setter(self, yt_task):
        self.yt_task = yt_task

# Helper for redirect of stdout.
class Stream(QObject):
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))
    
    def flush(self):
        pass
