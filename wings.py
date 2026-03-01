from uminekofy import uminekofy
#from PyQt6 import QtWidgets
from PyQt6.QtWidgets import *
from PyQt6 import uic
import sys
import multiprocessing as mp

class MainWindow(QMainWindow):
    def __init__(self, pipe: mp.Pipe):
        super().__init__()
        uic.loadUi("ui/MainWindow.ui", self)
        #self.setWindowTitle("Wings - VnLive")

        #self.label = QLabel(self)
        #self.label.setText("meow~!")
        #self.label.move(50, 50)

        #self.b1 = QPushButton(self)
        #self.b1.setText("clicker training")
        #def on_click():
        #    print("Clicked")
        #    pipe.send("42")
        #self.b1.clicked.connect(on_click)

def main(queue: mp.Queue):
    x: int = "meow"
    app = QApplication(sys.argv)
    window = MainWindow(queue)
    window.show()
    sys.exit(app.exec())
