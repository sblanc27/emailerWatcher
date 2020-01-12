from VirtualKeyboard import PyEmailerUi, PyEmailerCtrl
import threading
import emailWatcher_config as cfg
import sys
import VirtualKeyboard
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtGui, QtCore

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSizeGrip, QPushButton
from PyQt5.QtCore import QSize, QRect
import sys

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


global ticIcon
ticIcon= 0

    
class MyHandler(FileSystemEventHandler):
    def __init__(self, iUI):
        self.iUI = iUI
    def on_created(self, event):        
        print(f'event type: {event.event_type}  path : {event.src_path}')        
        global sPicture
        sPicture = event.src_path
        
        self.iUI.showIcon()
        global ticIcon
        ticIcon= 0
        self.tick_timer()

    def tick_timer(self):                    
        global ticIcon
        ticIcon+=1
        
        print("icon_timer:" + str(ticIcon))
        if(ticIcon >=cfg.icon_timer):
            self.iUI.hideIcon()
        else:
            threading.Timer(1.0, self.tick_timer).start()    
        
        
class IconUi(QApplication):         
    
    def __init__(self):
        super().__init__(sys.argv)        
        app = QApplication(sys.argv)    
        iC = IconWidget()
        iC.buildIcon()
        event_handler = MyHandler(iC)
        observer = Observer()
        observer.schedule(event_handler, path=cfg.scan_folder_path, recursive=False)
        observer.start()
        try:
            sys.exit(app.exec_())
        except:
            print("ex")
        

class IconWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 image'
        self.left = cfg.icon_left
        self.top = cfg.icon_top
        self.width = 10#cfg.icon_width
        self.height = 10#cfg.icon_height        
        #self.initUI()

    def icon_click(self):
        print("click")    
        global iTimeSpent
        iTimeSpent = 0
        
        self.hide()
        global sPicture
        self.hide()
        view = PyEmailerUi(sPicture)
        view.show()
        PyEmailerCtrl(view=view)
        global ticIcon
        ticIcon=10000 

        #runK(self)
        #self.hide()
    
    def hideIcon(self):
        self.hide()

    def showIcon(self):
        self.show()

    def buildIcon(self):
        self.setWindowTitle(self.title)        
        self.setGeometry(self.left, self.top, self.width, self.height)    
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)
        self.button = QPushButton('', self)
        self.button.move(-6,-4)
        ico = QtGui.QPixmap('email.jpg')
        self.button.setIcon(QtGui.QIcon(ico))        
        self.button.setIconSize(QSize(ico.width(),ico.height()))
        self.resize(ico.width(),ico.height())        
        self.button.clicked.connect(self.icon_click)
        self.show()
        self.hideIcon()

def hide_icon(self):
    self.close()