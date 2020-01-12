import emailWatcher_config as cfg
import sys
import threading
from datetime import datetime
try:
    import qdarkstyle
    bDark = True
except:
    print("unable to load style")
    bDark = False

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel, QStyleFactory
from functools import partial
global iTimeSpent
global view
iTimeSpent = 0
__version__ = '0.1'
__author__ = 'Blanc Stéphane'

class PyEmailerUi(QMainWindow):
    def __init__(self, sPic):
        super().__init__()        
        self.pic = sPic           
        print(QStyleFactory.keys())        
        self.setWindowTitle(cfg.keyboard_title)
        self.generalLayout = QVBoxLayout()        
        self.showFullScreen()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)        
        self._centralWidget.setLayout(self.generalLayout)        
        self._centralWidget.setFixedSize(560,400)
        
        self._createDisplay()
        self._createButtons()
        global view
        view = self        
    # Snip
    def _createDisplay(self):
        
        self.display = QLineEdit() 
        self.display2 = QLabel()       
        self.display2.setText(cfg.keyboard_help)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display2)
        self.generalLayout.addWidget(self.display)
    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        return self.display.text()
    
    
    def _close_and_send(self): 
        global sPicture
        global iTimeSpent
        print("close and send")
        print(self.display.text())
        f= open(cfg.result_path,"a+")
        print(str(datetime.now()) + "#" + self.display.text() + "#" + self.pic + "\n")        
        f.write(str(datetime.now()) + "#" + self.display.text() + "#" + self.pic + "\n")
        f.close()
        self.hide()        
        self.setDisplayText('')
        iTimeSpent = 1000
        

    def _close(self):        
        global iTimeSpent
        self.setDisplayText('')
        self.hide()        
        iTimeSpent = 1000


    def clearDisplay(self):
        self.setDisplayText('')
    def _createButtons(self):
        self.buttons = {}
        buttonsLayout = QGridLayout()
        buttons = {
                   cfg.keyboard_short_1: (5, 1, 104),
                   cfg.keyboard_short_2: (5,3, 104),
                   cfg.keyboard_short_3: (5,5, 160),
                   cfg.keyboard_domain_1: (5,8, 50),
                   cfg.keyboard_domain_2: (5,9, 50),
                   cfg.keyboard_domain_3: (5,10, 50),
                   '1': (0, 1, 50),
                   '2': (0, 2, 50),
                   '3': (0, 3, 50),
                   '4': (0, 4, 50),
                   '5': (0, 5, 50),
                   '6': (0, 6, 50),
                   '7': (0, 7, 50),
                   '8': (0, 8, 50),
                   '9': (0, 9, 50),
                   '0': (0, 10,50),
                   'A': (1, 1, 50),
                   'B': (1, 2, 50),
                   'C': (1, 3, 50),
                   'D': (1, 4, 50),
                   'E': (1, 5, 50),
                   'F': (1, 6, 50),
                   'G': (1, 7, 50),
                   'H': (1, 8, 50),
                   'I': (1, 9, 50),
                   'J': (1, 10,50),
                   'K': (2, 1, 50),
                   'L': (2, 2, 50),
                   'M': (2, 3, 50),
                   'N': (2, 4, 50),
                   'O': (2, 5, 50),
                   'P': (2, 6, 50),
                   'Q': (2, 7, 50),
                   'R': (2, 8, 50),
                   'S': (2, 9, 50),
                   'T': (2, 10,50),
                   'U': (3, 1, 50),
                   'V': (3, 2, 50),
                   'W': (3, 3, 50),
                   'X': (3, 4, 50),
                   'Y': (3, 5, 50),
                   'Z': (3, 6, 50),
                   '!': (3, 7, 50),
                   ',': (3, 8, 50),
                   '.': (3, 9, 50),
                   '@': (3, 10,50),
                   '-': (4, 1, 50),
                   '_': (4, 2, 50),
                   '#': (4, 3, 50),
                   '$': (4, 4, 50),
                   '%': (4, 5, 50),
                   '^': (4, 6, 50),
                   '&&': (4, 7,50),
                   '*': (4, 8, 50),
                   '+': (4, 9, 50),
                   ';': (4, 10,50),
                   cfg.keyboard_clear: (6,1, 104),
                   cfg.keyboard_cancel: (6,3, 104),
                   cfg.keyboard_send: (6,5, 325),
                  }
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(pos[2], 40)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
            self.generalLayout.addLayout(buttonsLayout)

class PyEmailerCtrl:
    def __init__(self, view):
        self._view = view
        self._connectSignals()
        tik_tok()

    def _buildExpression(self, sub_exp):
        expression = self._view.displayText() + sub_exp
        expression = expression.replace("@@","@")
        self._view.setDisplayText(str(expression).lower())
        reset_timer()        

    def _connectSignals(self):
        for btnText, btn in self._view.buttons.items():
            if btnText not in {'Effacer','Annuler','Envoyer'}:
                btn.clicked.connect(partial(self._buildExpression, btnText.replace("&&","&")))

        self._view.buttons[cfg.keyboard_clear].clicked.connect(self._view.clearDisplay)
        self._view.buttons[cfg.keyboard_send].clicked.connect(self._view._close_and_send)
        self._view.buttons[cfg.keyboard_cancel].clicked.connect(self._view._close)



def reset_timer():
    global iTimeSpent
    iTimeSpent = 0
    print("resetting timer:" + str(iTimeSpent))


def tik_tok():    
    global view
    global iTimeSpent
    iTimeSpent +=1
    print("virtualkeyboard - timer:" + str(iTimeSpent))
    if(iTimeSpent >= cfg.keyboard_timer):
        try:
            print("virtualkeyboard timeout exceed - closing form")
            view._close()            
            iTimeSpent = 0
            
        except:
            print("exit1")
    else:
        threading.Timer(1.0, tik_tok).start()    
