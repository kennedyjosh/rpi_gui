from datetime import datetime
from PaddedLabel import PaddedLabel
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtWidgets import QGridLayout, QSizePolicy, QWidget
import constant

class MainLayout(QWidget):
    def __init__(self, app):
        super(MainLayout, self).__init__()

        self.app = app

        self.grid = QGridLayout(self)

        self.clock_refresh = QTimer()
        self.clock_refresh.setInterval(constant.MILLISEC)
        self.clock_refresh.timeout.connect(self.update_clock)
        self.lbl_clock = PaddedLabel(self)
        self.lbl_clock.setStyleSheet(constant.SS_FONT + constant.SS_BBOX)
        # default constructor for QSizePolicy is Fixed for horiz and vertical
        # Fixed means it only uses sizeHint function to determine size
        self.lbl_clock.setSizePolicy(QSizePolicy())

    def run(self):
        # set spacing ratios for rows
        # row 0:1:2 being 16:3:1 certifies 5% cushion at the bottom, 80% cushion on top
        # clock row has 15% of screen space (vertically)
        self.grid.setRowStretch(0, 16)
        self.grid.setRowStretch(1, 3)
        self.grid.setRowStretch(2, 1)

        # set spacing ratios for columns
        # spacing ratio is 1:1 for each of 3 columns
        for col in range(3):
            self.grid.setColumnStretch(col, 1)

        # add children to grid layout
        self.grid.addWidget(self.lbl_clock, 1, 1, alignment=Qt.AlignHCenter)

        # initialize update timers and run the update function to start things off
        self.clock_refresh.start()
        self.update_clock()

    def update_clock(self):
        time = datetime.now().time()
        curr_time_txt = time.strftime("%d:%%M%%p" % (time.hour % 12 if time.hour % 12 else 12)).lower()
        self.lbl_clock.setText(curr_time_txt)
        self.lbl_clock.adjustSize()
