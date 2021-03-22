from datetime import datetime
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QSizePolicy, QStackedWidget, QWidget
from StylizedClasses import Icon, PaddedLabel
import CONFIG as config
import constant
import os
import requests

class MainLayout(QWidget):
    def __init__(self, app):
        super(MainLayout, self).__init__()

        self.app = app

        self.grid = QGridLayout(self)

        self.init_clock()
        self.init_outdoor_weather()

    def get_outdoor_weather(self):
        '''Use ClimaCell API to get weather information'''
        base_url = "https://data.climacell.co/v4/timelines"
        params = {
            "location": f"{config.Coords[0]},{config.Coords[1]}",
            "fields": "temperature,weatherCode",
            "timesteps": "current",
            "apikey": config.ApiKey
        }
        try:
            result = requests.get(base_url, params=params, timeout=30)
        except:
            return None
        if result.status_code == 200:
            result = result.json()['data']['timelines'][0]['intervals'][0]['values']
            return {
                "temp": (result['temperature'] * 1.8) + 32,
                "weather": constant.WEATHER_CODES[str(result['weatherCode'])]
            }
        else:
            print(result.json())
            return None

    def is_sun_up(self):
        '''Get sun data from local home assistant instance'''
        url = config.HomeAssistantUrl + "/api/states/sun.sun"
        headers = {
            "Authorization": f"Bearer {config.HomeAssistantApi}",
            "Content-Type": "application/json"
        }
        try:
            result = requests.get(url, headers=headers, timeout=15)
            if result.status_code == 200:
                result = result.json()
                if result['state'] == 'below_horizon':
                    return False
                else:
                    return True
            else:
                raise ValueError
        except:
            print("Using time of day instead of sun state")
            # if contacting home assistant fails, use rule:
            # if it is after 6am and before 6pm, the sun is up
            time = datetime.time(datetime.now())
            secs = time.hour * 3600 + time.minute * 60 + time.second
            if secs > (6 * 60 * 60) and secs < (18 * 60 * 60):
                return True
            else:
                return False

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
        # initialize update timer
        self.outdoor_weather_refresh = QTimer()
        self.outdoor_weather_refresh.setInterval(constant.MILLISEC * 60 * 3)   # 3 minutes
        self.outdoor_weather_refresh.timeout.connect(self.update_outdoor_weather)
        # QFrame holds the main layout for the weather display
        self.frame_outdoor_weather = QFrame()
        self.frame_outdoor_weather.setStyleSheet(constant.SS_BBOX)
        # HBox has weather icon in col 1, temperature in col 2
        self.hbox_outdoor_weather = QHBoxLayout(self.frame_outdoor_weather)
        # temperature label
        self.lbl_outdoor_weather_temp = QLabel()
        self.lbl_outdoor_weather_temp.setText("80°")
        self.lbl_outdoor_weather_temp.setStyleSheet(constant.SS_FONT + constant.SS_NO_BACKGROUND)
        # weather icons stored in a qstackedwidget and a dict
        self.dict_outdoor_weather_icons = {}
        self.qstack_outdoor_weather_icons = QStackedWidget()
        self.qstack_outdoor_weather_icons.setAttribute(Qt.WA_TranslucentBackground, True)
        icon_height = int(0.2 * self.app.primaryScreen().size().height())  # a too-big guess of what icon height will be
        # init all weather icons from climacell
        for icon in os.listdir(constant.WEATHER_ICON_FOLDER):
            if icon.endswith(".svg"):
                icon_name = icon.split(".")[0]
                self.dict_outdoor_weather_icons[icon_name] = Icon(icon_height,
                                                                  os.path.join(constant.WEATHER_ICON_FOLDER, icon))
                self.qstack_outdoor_weather_icons.addWidget(self.dict_outdoor_weather_icons[icon_name])
        # add labels to HBox
        self.hbox_outdoor_weather.addWidget(self.qstack_outdoor_weather_icons)
        self.hbox_outdoor_weather.addWidget(self.lbl_outdoor_weather_temp)
        # initialize dict of weather values
        self.dict_outdoor_weather_values = {}

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
        self.outdoor_weather_refresh.start()
        self.update_clock()
        self.update_outdoor_weather()

    def update_clock(self):
        time = datetime.now().time()
        curr_time_txt = time.strftime("%d:%%M%%p" % (time.hour % 12 if time.hour % 12 else 12)).lower()
        self.lbl_clock.setText(curr_time_txt)
        self.lbl_clock.adjustSize()

    def update_outdoor_weather(self):
        # get results from weather api
        weather = self.get_outdoor_weather()
        if weather == None:
            # there was some error fetching the data so don't update the label
            # red font indicates an issue updating temperature
            self.lbl_outdoor_weather_temp.setStyleSheet(constant.SS_RED_FONT + constant.SS_NO_BACKGROUND)
            return
        # white font color indicates weather info is updating OK
        self.lbl_outdoor_weather_temp.setStyleSheet(constant.SS_FONT + constant.SS_NO_BACKGROUND)
        # update temperature
        self.lbl_outdoor_weather_temp.setText(f"{round(weather['temp'])}°")
        self.lbl_outdoor_weather_temp.adjustSize()

        # need these to update icon and frame size
        temp_text_rect = self.lbl_outdoor_weather_temp.fontMetrics().boundingRect(self.lbl_outdoor_weather_temp.text())
        temp_text_height = temp_text_rect.size().height()
        temp_text_width = temp_text_rect.size().width()

        # update icon
        if weather['weather'].lower() + "_day.svg"  in os.listdir(constant.WEATHER_ICON_FOLDER):
            # day/night version of icon exists
            if self.is_sun_up():
                icon = weather['weather'].lower() + "_day"
            else:
                icon = weather['weather'].lower() + "_night"
        else:
            # day/night version of icon does not exist
            icon = weather['weather'].lower()
        self.dict_outdoor_weather_icons[icon].updateDim(int(0.8 * temp_text_height))
        self.qstack_outdoor_weather_icons.setCurrentWidget(self.dict_outdoor_weather_icons[icon])

        # adjust size of frame to fit information + 5% padding
        self.frame_outdoor_weather.setFixedSize(QSize(round(temp_text_width * 2.05), round(temp_text_height * 1.05)))
