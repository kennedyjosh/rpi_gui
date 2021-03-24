from MainLayout import MainLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import CONFIG as config
import constant
import img_dr
import os
import random
import shutil
import sys

class MainWindow(QMainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()

        self.app = app

        self.imgs = os.listdir(constant.FIXED_IMG_FOLDER)
        self.img_index = -1

        self.timer = QTimer()
        self.timer.setInterval(config.PhotoChangeInterval * constant.MILLISEC)
        self.timer.timeout.connect(self.change_img)

        self.lbl_img = QLabel(self)
        self.lbl_img.move(0,0)

        self.setCentralWidget(MainLayout(self.app))

    def run(self):
        screenRes = self.app.primaryScreen().size()
        self.setGeometry(0, 0, screenRes.width(), screenRes.height())
        self.setStyleSheet("background-color: black;")
        self.setWindowTitle("RPI GUI")

        self.lbl_img.resize(screenRes.width(), screenRes.height())
        self.change_img()

        self.timer.start()

        self.centralWidget().run()

        self.showFullScreen()

    def change_img(self):
        self.img_index += 1
        self.img_index %= len(self.imgs)
        if self.img_index == 0:
            random.shuffle(self.imgs)
        img_path = os.path.join(constant.FIXED_IMG_FOLDER, self.imgs[self.img_index])
        self.lbl_img.setPixmap(QPixmap(img_path))
        self.lbl_img.show()
        self.timer.start()

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Escape:
            self.app.quit()

if __name__ == "__main__":
    # create .img folder for caching fixed imgs if it doesnt already exist
    if not os.path.exists(constant.FIXED_IMG_FOLDER):
        os.makedirs(constant.FIXED_IMG_FOLDER)

    app = QApplication(sys.argv)
    app.setOverrideCursor(Qt.BlankCursor)
    screenRes = app.primaryScreen().size()
    win = MainWindow(app)
    raw_imgs = os.listdir(constant.RAW_IMG_FOLDER)
    for img in raw_imgs:
        # only process new images
        if img not in win.imgs:
            win.imgs.append(img)
            shutil.copy(os.path.join(constant.RAW_IMG_FOLDER, img), constant.FIXED_IMG_FOLDER) # copy to .img folder
            img = os.path.join(constant.FIXED_IMG_FOLDER, img)
            img_dr.convert_to_srgb(img)    # avoids a warning
            img_dr.stretch_to_fill(img, screenRes.width(), screenRes.height())
    # remove imgs in .img that were removed from img
    for img in win.imgs:
        if img not in os.listdir(constant.RAW_IMG_FOLDER):
            os.remove(os.path.join(constant.FIXED_IMG_FOLDER, img))
            win.imgs.remove(img)
    try:
        win.run()
    except Exception as e:
        import traceback
        from datetime import datetime
        print(f"Error causing crash at {datetime.now()}")
        print(f"\t{e}")
        print(f"\t{repr(e)}")
        print(f"\t{traceback.print_exc()}")
    sys.exit(app.exec_())
