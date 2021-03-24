from PyQt5.QtCore import QSize, Qt
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QLabel
import constant

class Icon(QSvgWidget):
    '''QLabel object which takes a dimension in its constructor and
    always remains a square of the given dimension'''
    def __init__(self, dim, img_path):
        super(Icon, self).__init__()
        self.setStyleSheet(constant.SS_NO_BACKGROUND)
        self.dim = dim
        self.img_path = img_path
        self.updateImg()

    def updateImg(self, img=None):
        self.load(self.img_path if not img else img)
        # setAspectRatioMode was added in Qt 5.15
        if constant.QT_VERSION[0] == 5 and constant.QT_VERSION[1] >= 15:
            self.renderer().setAspectRatioMode(Qt.KeepAspectRatio)
        self.show()

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
        return QSize(round(w * 1.1), round(h * 1.05))
