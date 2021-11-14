import sys

from config import buttonX, buttonY, minimFinestraX, minimFinestraY, normalFinestraX, normalFinestraY, maximFinestraX, maximFinestraY

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self, title="Exemple signals-slots 1"):
        super().__init__()

        self.setFixedSize(QSize(1200, 700))

        self.setWindowTitle(title)

        self.pybutton = QPushButton("Maximitza", self)
        
        #Connectem la senyal clicked a la ranura button_pressed
        self.pybutton.clicked.connect(self.button_pressed) 

        self.pybutton.resize(buttonX, buttonY)
        self.pybutton.move(250, 300)

        self.pybutton2 = QPushButton("Normalitza", self)
        
        #Connectem la senyal clicked a la ranura button_pressed
        self.pybutton2.clicked.connect(self.button_pressed2) 

        self.pybutton2.resize(buttonX, buttonY)
        self.pybutton2.move(550, 300)

        self.pybutton3 = QPushButton("Minimitza", self)
        
        #Connectem la senyal clicked a la ranura button_pressed
        self.pybutton3.clicked.connect(self.button_pressed3) 

        self.pybutton3.resize(buttonX, buttonY)
        self.pybutton3.move(850, 300)

    def button_pressed(self):
        print("S'ha maximitzat la finestra!")

        self.setWindowTitle("Maximitzat")

        self.setFixedSize(QSize(maximFinestraX, maximFinestraY))

        self.move(0, 0)

        self.pybutton.move(430, 440)
        self.pybutton2.move(910, 440)
        self.pybutton3.move(1390, 440)

        self.pybutton.setEnabled(False)
        self.pybutton2.setEnabled(True)
        self.pybutton3.setEnabled(True)

    def button_pressed2(self):
        print("S'ha normalitzat la finestra!")

        self.setWindowTitle("Normalitzat")

        self.setFixedSize(QSize(normalFinestraX, normalFinestraY))

        self.move(360, 178)

        self.pybutton.move(250, 300)
        self.pybutton2.move(550, 300)
        self.pybutton3.move(850, 300)

        self.pybutton.setEnabled(True)
        self.pybutton2.setEnabled(False)
        self.pybutton3.setEnabled(True)

    def button_pressed3(self):
        print("S'ha minimitzat la finestra!")

        self.setWindowTitle("Minimitzat")

        self.move(810, 486)

        self.setFixedSize(QSize(minimFinestraX, minimFinestraY))

        self.pybutton.move(0, 0)
        self.pybutton2.move(100, 0)
        self.pybutton3.move(200, 0)

        self.pybutton.setEnabled(True)
        self.pybutton2.setEnabled(True)
        self.pybutton3.setEnabled(False)

app = QApplication(sys.argv)

if (len(sys.argv) == 3):
    window = MainWindow(sys.argv[1], sys.argv[2])
else:
    window = MainWindow()

window.show()

app.exec()