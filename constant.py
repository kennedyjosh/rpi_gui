'''This file holds constant variables'''
from PyQt5.QtCore import QT_VERSION_STR
import CONFIG as config
import secret
import os

'''Time constants'''
MILLISEC = 1000

'''Qt Version'''
QT_VERSION = [int(x) for x in QT_VERSION_STR.split(".")]

'''StyleSheet constants'''
SS_FONT = f"color: white; font-family: {config.Font}; font: {config.ClockFontSize}px;"
SS_RED_FONT = f"color: red; font-family: {config.Font}; font: {config.ClockFontSize}px;"
SS_BBOX = ("border-top-left-radius : 20px; border-top-right-radius : 20px; border-bottom-left-radius : 20px;"
           "border-bottom-right-radius : 20px; background-color : rgba(0,0,0,100);")
SS_NO_BACKGROUND = "background-color : rgba(0,0,0,0);"

'''Subfolders to hold background images'''
RAW_IMG_FOLDER = os.path.join(os.getcwd(), "img")
FIXED_IMG_FOLDER = os.path.join(os.getcwd(), ".img")

'''Folder for weather icons'''
WEATHER_ICON_FOLDER = os.path.join(os.getcwd(), "weather_icons", "color")

'''Weather Codes (ClimaCell)'''
WEATHER_CODES = {
    "0": "Unknown",
    "1000": "Clear",
    "1001": "Cloudy",
    "1100": "Mostly Clear",
    "1101": "Partly Cloudy",
    "1102": "Mostly Cloudy",
    "2000": "Fog",
    "2100": "Light Fog",
    "3000": "Light Wind",
    "3001": "Wind",
    "3002": "Strong Wind",
    "4000": "Drizzle",
    "4001": "Rain",
    "4200": "Light Rain",
    "4201": "Heavy Rain",
    "5000": "Snow",
    "5001": "Flurries",
    "5100": "Light Snow",
    "5101": "Heavy Snow",
    "6000": "Freezing Drizzle",
    "6001": "Freezing Rain",
    "6200": "Light Freezing Rain",
    "6201": "Heavy Freezing Rain",
    "7000": "Ice Pellets",
    "7101": "Heavy Ice Pellets",
    "7102": "Light Ice Pellets",
    "8000": "Thunderstorm"
    }

'''Secrets'''
COORDS = secret.Coords
WEATHER_API_KEY = secret.ClimaCellApiKey
HASS_URL = secret.HomeAssistantUrl
HASS_TOKEN = secret.HomeAssistantApiKey