from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QBoxLayout, QLabel
import constant
import os

class Icon(QLabel):
    '''QLabel object which takes a dimension in its constructor and
    always remains a square of the given dimension'''
    def __init__(self, dim, img_path):
        super(Icon, self).__init__()
        self.dim = dim
        # source: https://stackoverflow.com/a/37956012/11106258
        # enables transparency in pngs to work
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.img_path = img_path
        self.updateImg()

    def updateImg(self):
        icon = QPixmap(self.img_path)
        self.setPixmap(icon.scaled(self.sizeHint(),
                                   Qt.KeepAspectRatio,
                                   Qt.SmoothTransformation))

    def updateDim(self, dim):
        self.dim = dim
        self.updateImg()

    def sizeHint(self):
        return QSize(self.dim, self.dim)

class PaddedLabel(QLabel):
    '''QLabel object which defaults to AlignHCenter and resizes to fit
    the text with some slight padding'''
    def __init__(self, parent = None):
        super(PaddedLabel, self).__init__(parent)
        self.setAlignment(Qt.AlignHCenter)

    def sizeHint(self):
        # adjust to fit around boundingRect of font with added 5% padding
        w = self.fontMetrics().boundingRect(self.text()).width()
        h = self.fontMetrics().boundingRect(self.text()).height()
        return QSize(int(w * 1.05), int(h * 1.05))
