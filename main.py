from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import img_dr
import os
import random
import sys

MILLISEC = 1000

# number of seconds a photo is on screen before changing
PhotoChangeInterval = 30

class MainWindow(QMainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()

        self.app = app

        self.imgs = os.listdir(os.path.join(os.getcwd(), "img"))

        self.timer = QTimer()
        self.timer.setInterval(PhotoChangeInterval * MILLISEC)
        self.timer.timeout.connect(self.change_img)

        self.lbl_img = QLabel(self)
        self.lbl_img.move(0,0)

    def run(self):
        screenRes = self.app.primaryScreen().size()
        self.setGeometry(0, 0, screenRes.width(), screenRes.height())
        self.setStyleSheet("background-color: black;")
        self.setWindowTitle("RPI GUI")

        self.lbl_img.resize(screenRes.width(), screenRes.height())
        self.change_img()

        self.timer.start()

        self.showFullScreen()

    def change_img(self):
        img_path = os.path.join("img", random.choice(self.imgs))
        self.lbl_img.setPixmap(QPixmap(img_path))
        self.lbl_img.show()
        self.timer.start()

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Escape:
            self.app.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screenRes = app.primaryScreen().size()
    win = MainWindow(app)
    for img in win.imgs:
        img = os.path.join(os.getcwd(), "img", img)
        img_dr.convert_to_srgb(img)    # avoids a warning
        img_dr.stretch_to_fill(img, screenRes.width(), screenRes.height())
    win.run()
    sys.exit(app.exec_())

