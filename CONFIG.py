'''Configurable variables'''
import secret

'''Number of seconds a photo is on screen before changing'''
PhotoChangeInterval = 30

'''Font type and sizes'''
Font = "pibotolt"
ClockFontSize = 84

'''Weather API info'''
# (lattitude, longitude) coordinates of location
Coords = secret.Coords
# ClimaCell API key as a string
ApiKey = secret.ClimaCellApiKey

'''Home Assistant url'''
# use http instead of https
HomeAssistantUrl = secret.HomeAssistantUrl
'''Home Assistant API key'''
HomeAssistantApi = secret.HomeAssistantApiKey
