from datetime import datetime
from PyQt5.QtCore import Qt, QRect, QTimer
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

        self.clock_refresh = QTimer()
        self.clock_refresh.setInterval(constant.MILLISEC)
        self.clock_refresh.timeout.connect(self.update_clock)

        self.lbl_img = QLabel(self)
        self.lbl_img.move(0,0)

        self.lbl_clock = QLabel(self)
        # w >> 1 == w / 2 (or close enough)
        self.lbl_clock.setStyleSheet(constant.SS_FONT + constant.SS_BBOX)
        self.lbl_clock.setAlignment(Qt.AlignHCenter)


    def run(self):
        screenRes = self.app.primaryScreen().size()
        self.setGeometry(0, 0, screenRes.width(), screenRes.height())
        self.setStyleSheet("background-color: black;")
        self.setWindowTitle("RPI GUI")

        self.lbl_img.resize(screenRes.width(), screenRes.height())
        self.change_img()

        self.update_clock()

        self.timer.start()
        self.clock_refresh.start()

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

    def update_clock(self):
        time = datetime.now().time()
        curr_time_txt = time.strftime("%d:%%M%%p" % (time.hour % 12 if time.hour % 12 else 12)).lower()
        self.lbl_clock.setText(curr_time_txt)
        self.lbl_clock.adjustSize()
        # ensure label is centered
        self.lbl_clock.move((screenRes.width() >> 1) - # the subtracted amt is 1/2 * expected text width
                                (self.lbl_clock.fontMetrics().boundingRect(self.lbl_clock.text()).width() >> 1),
                            int(screenRes.height() * .85))
        # the background looked too tight horizontally,
        # this cmd increases the horizontal size by 3% and re-centers
        self.lbl_clock.setGeometry(QRect(
            int(self.lbl_clock.x() - (self.lbl_clock.size().width() * .04)),
            self.lbl_clock.y(),
            int(self.lbl_clock.size().width() * 1.04),
            self.lbl_clock.size().height()
        ))
        self.clock_refresh.start()

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
    win.run()
    sys.exit(app.exec_())

