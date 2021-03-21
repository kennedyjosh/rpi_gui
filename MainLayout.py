from datetime import datetime
from StylizedClasses import Icon, PaddedLabel
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QSizePolicy, QStackedWidget, QWidget
import constant
import os

class MainLayout(QWidget):
    def __init__(self, app):
        super(MainLayout, self).__init__()

        self.app = app

        self.grid = QGridLayout(self)

        self.init_clock()
        self.init_outdoor_weather()

    def init_clock(self):
        '''Initialize clock label and update timer'''
        self.clock_refresh = QTimer()
        self.clock_refresh.setInterval(constant.MILLISEC)
        self.clock_refresh.timeout.connect(self.update_clock)
        self.lbl_clock = PaddedLabel(self)
        self.lbl_clock.setStyleSheet(constant.SS_FONT + constant.SS_BBOX)
        # default constructor for QSizePolicy is Fixed for horiz and vertical
        # Fixed means it only uses sizeHint function to determine size
        self.lbl_clock.setSizePolicy(QSizePolicy())

    def init_outdoor_weather(self):
        '''Initialize outdoor weather display'''
        # QFrame holds the main layout for the weather display
        self.frame_outdoor_weather = QFrame()
        self.frame_outdoor_weather.setStyleSheet(constant.SS_BBOX)
        # HBox has weather icon in col 1, temperature in col 2
        self.hbox_outdoor_weather = QHBoxLayout(self.frame_outdoor_weather)
        # temperature label
        self.lbl_outdoor_weather_temp = QLabel()
        self.lbl_outdoor_weather_temp.setStyleSheet(constant.SS_FONT + "background-color : rgba(0,0,0,0);")
        # weather icons stored in a qstackedwidget and a dict
        self.dict_outdoor_weather_icons = {}
        self.qstack_outdoor_weather_icons = QStackedWidget()
        self.qstack_outdoor_weather_icons.setAttribute(Qt.WA_TranslucentBackground, True)
        icon_height = int(0.2 * self.app.primaryScreen().size().height())  #int(0.8 * temp_text_height)
        # TODO init all weather icons from climacell
        self.dict_outdoor_weather_icons['sun'] = Icon(icon_height, os.path.join(constant.ICON_FOLDER, "sun.png"))
        self.qstack_outdoor_weather_icons.addWidget(self.dict_outdoor_weather_icons['sun'])
        # add labels to HBox
        self.hbox_outdoor_weather.addWidget(self.qstack_outdoor_weather_icons)
        self.hbox_outdoor_weather.addWidget(self.lbl_outdoor_weather_temp)

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

        # add each display to grid layout
        self.grid.addWidget(self.frame_outdoor_weather, 1, 1, alignment=Qt.AlignLeft)
        self.grid.addWidget(self.lbl_clock, 1, 2, alignment=Qt.AlignHCenter)

        # start timers for info refresh and run the update functions for each display
        self.clock_refresh.start()
        self.update_clock()
        self.update_outdoor_weather()

    def update_clock(self):
        time = datetime.now().time()
        curr_time_txt = time.strftime("%d:%%M%%p" % (time.hour % 12 if time.hour % 12 else 12)).lower()
        self.lbl_clock.setText(curr_time_txt)
        self.lbl_clock.adjustSize()

    def update_outdoor_weather(self):
        # TODO call weather api
        # update temperature
        self.lbl_outdoor_weather_temp.setText("80°")
        self.lbl_outdoor_weather_temp.adjustSize()

        # need these to update icon and frame size
        temp_text_rect = self.lbl_outdoor_weather_temp.fontMetrics().boundingRect(self.lbl_outdoor_weather_temp.text())
        temp_text_height = temp_text_rect.size().height()
        temp_text_width = temp_text_rect.size().width()

        # update icon
        self.dict_outdoor_weather_icons['sun'].updateDim(int(0.8 * temp_text_height))
        self.qstack_outdoor_weather_icons.setCurrentWidget(self.dict_outdoor_weather_icons['sun'])

        # adjust size of frame to fit information + 5% padding
        self.frame_outdoor_weather.setFixedSize(QSize(int(temp_text_width * 2.05), int(temp_text_height * 1.05)))
