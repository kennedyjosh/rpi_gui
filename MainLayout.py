from datetime import datetime
from StylizedClasses import Icon, PaddedLabel
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget
import constant
import os

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

        self.frame_outdoor_weather = QFrame()
        self.frame_outdoor_weather.setStyleSheet(constant.SS_BBOX)
        self.frame_outdoor_weather.setAttribute(Qt.WA_StyledBackground, True)
        self.layout_outdoor_weather = QHBoxLayout(self.frame_outdoor_weather)
        self.layout_outdoor_weather.setStretch(0, 1)
        self.layout_outdoor_weather.setStretch(1, 5)
        self.lbl_outdoor_weather_temp = QLabel()
        self.lbl_outdoor_weather_temp.setText("80°")
        self.lbl_outdoor_weather_temp.setStyleSheet(constant.SS_FONT + "background-color : rgba(0,0,0,0);")
        self.lbl_outdoor_weather_temp.adjustSize()
        temp_text_height = self.lbl_outdoor_weather_temp.fontMetrics().boundingRect(self.lbl_outdoor_weather_temp.text()).size().height()
        temp_text_width = self.lbl_outdoor_weather_temp.fontMetrics().boundingRect(self.lbl_outdoor_weather_temp.text()).size().width()
        self.lbl_outdoor_weather_icon = Icon(int(0.8 * temp_text_height), os.path.join(constant.ICON_FOLDER, "sun.png"))
        self.layout_outdoor_weather.addWidget(self.lbl_outdoor_weather_icon)
        self.layout_outdoor_weather.addWidget(self.lbl_outdoor_weather_temp)
        self.frame_outdoor_weather.setFixedSize(QSize(int(temp_text_width * 2.05), int(temp_text_height * 1.05)))

    def run(self):
        # set spacing ratios for rows
        # row 0:1:2 being 16:3:1 certifies 5% cushion at the bottom, 80% cushion on top
        # clock row has 15% of screen space (vertically)
        self.grid.setRowStretch(0, 16)
        self.grid.setRowStretch(1, 3)
        self.grid.setRowStretch(2, 1)

        # set spacing ratios for columns
        # spacing ratio is 1:1 for interior columns with padding on first and last col
        for col in range(1,4):
            self.grid.setColumnStretch(col, 6)
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(4, 1)

        # add children to grid layout
        self.grid.addWidget(self.frame_outdoor_weather, 1, 1, alignment=Qt.AlignLeft)
        self.grid.addWidget(self.lbl_clock, 1, 2, alignment=Qt.AlignHCenter)

        # update height of icons
        # self.lbl_outdoor_weather_icon.updateDim(
        #     self.lbl_outdoor_weather_temp.fontMetrics().boundingRect(self.lbl_outdoor_weather_temp.text()).size().height()
        # )

        # initialize update timers and run the update function to start things off
        self.clock_refresh.start()
        self.update_clock()

    def update_clock(self):
        time = datetime.now().time()
        curr_time_txt = time.strftime("%d:%%M%%p" % (time.hour % 12 if time.hour % 12 else 12)).lower()
        self.lbl_clock.setText(curr_time_txt)
        self.lbl_clock.adjustSize()
