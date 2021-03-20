'''This file holds constant variables'''
import CONFIG as config
import os

'''Time constants'''
MILLISEC = 1000

'''StyleSheet constants'''
SS_FONT = f"color: white; font-family: {config.Font}; font: {config.ClockFontSize}px;"
SS_BBOX = ("border-top-left-radius : 20px; border-top-right-radius : 20px; border-bottom-left-radius : 20px;"
           "border-bottom-right-radius : 20px; background-color : rgba(0,0,0,100);")

'''Subfolders to hold background images'''
RAW_IMG_FOLDER = os.path.join(os.getcwd(), "img")
FIXED_IMG_FOLDER = os.path.join(os.getcwd(), ".img")

'''Folder for icon images'''
ICON_FOLDER = os.path.join(os.getcwd(), ".icon")
