from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QLabel

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
