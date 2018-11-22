import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QThread, pyqtSlot
import time
import youtube_dl
from PyQt5 import QtCore, QtGui, QtWidgets
import sys



# hier kommen history und done liste rein?
class TaskQueueThread(QThread):

    myDownloadTaskSignal = pyqtSignal(list)
    myUpdatedTaskList = pyqtSignal(list)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.yt_task_queue = []
        self.yt_task_update = []

    def run(self):
        #wenn kein doing, emit erstes todo
        #emit auch immer die liste (2 Signale)
        #wie geht dann todo->done ?
        while True:

            # Download fertig? Setze status auf done oder failed
            running_task = False
            if (len(self.yt_task_update) != 0):
                for (idx, task) in enumerate(self.yt_task_queue):
                    if (self.yt_task_update[0] == task[0]):
                        self.yt_task_queue[idx][2] = self.yt_task_update[2]
                        self.yt_task_update = []
                        break

            # Laeuft gerade ein Download
            for task in self.yt_task_queue:
                if task[2]=='doing':
                    running_task = True
                    break

            # Wenn kein DL laeuft gibt neuen DL Auftrag
            if not running_task:
                for (idx, task) in enumerate(self.yt_task_queue):
                    if task[2] == 'todo':
                        self.yt_task_queue[idx][2] = 'doing'
                        self.myDownloadTaskSignal.emit(task) #um neue auftraege zu stellen
                        break
            self.myUpdatedTaskList.emit(self.yt_task_queue) #um das textfeld upzudaten
            time.sleep(0.5)
    
    #brauche ich nicht
    #@pyqtSlot(list)
    #def add_to_task_queue(self, yt_task):
    #    self.yt_task_queue.append(yt_task)
    
    #hier dockt der ytdlthread an
    @pyqtSlot(list)
    def update_task_status(self, yt_task):
        self.yt_task_update = yt_task


class YTDLThread(QThread):

    #braucht Signal, dass er fertig ist. Wird von TaskQueueThread.yt_task_queue aufgenommen
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
        #print(yt_task)
        title = yt_task[1]
        video_url = yt_task[0]
        #print(yt_task)

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
        
        return {
            'audio': open('{}.mp3'.format(title), 'rb'),
            'title': title,
        }








    @pyqtSlot(list)
    def yt_task_setter(self, yt_task):
        self.yt_task = yt_task

class Stream(QObject):
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))
    
    def flush(self):
        pass