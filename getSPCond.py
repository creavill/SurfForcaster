from infoExtractor import getBouyData
import datetime
import requests
import json


class SurfSpot:
    def __init__(self,  name, lat, lon):
        self.name=name
        self.lat=lat
        self.lon=lon
        self.buoyData=getBouyData()
        self.Wind = getWindData(lat,lon)
        self.tideData=getTide()

def getSurfSpotData():
    #add animals and killers
    spotList =[["Rock", 35.372834,-120.867390],
               ["Pit", 35.377083, -120.867371],
               ["Studios", 35.419715, -120.880746],
               ["Yerb", 35.403359, -120.872336],
               ["Cayucos", 35.447924, -120.906409],
               ["Sanspit", 35.304456, -120.880269],
               ["Hazards", 35.291400, -120.886026],
               ["Beachcombers",35.168331, -120.697321],
               ["Sewers", 35.159157, -120.686966],
               ["Pismo", 35.138202, -120.646070]]
    
    tempSpot =[]
    for spots in spotList:
        tempSpot.append(SurfSpot(spots[0],spots[1],spots[2]))
    return tempSpot

def getKey():
    f = open("WeatherAppKey")
    return f.read()

def getWindData(lat,lon):
    #API KEY NOT PRIVATE
    key = getKey()
    data_spec = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=imperial&appid={key}').text
    y = json.loads(data_spec)
    wind=[]
    for data_item in y['list']:
        wind.append(data_item['wind'])
    return wind

def getTide():
    today = datetime.date.today()
    nextWeek = today + datetime.timedelta(days=7)
    tideData = requests.get(f'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date={str(today).replace("-","")}&end_date={str(nextWeek).replace("-","")}&station=9412110&product=ofs_water_level&datum=MLLW&time_zone=gmt&units=english&format=xml').text.replace("<wl","").replace("/>","").split("\n")
    return tideData

def consoludateData():
    spots =["Rock", 35.372834,-120.867390]
    rock = SurfSpot(spots[0],spots[1],spots[2])
    print(rock.buoyData[0 ])
    print(rock.Wind)
consoludateData()