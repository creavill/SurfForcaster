'''
National Bouy App
wget https://www.ndbc.noaa.gov/data/realtime2/{Location}.txt
'''
import datetime
import requests

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)

class hourlyReport:
    def __init__(self, data_spec):
        '''
        (WVHT) Significant Wave Height 
        (SwH)  Swell Height        
        (SwP)  Swell Period        	
        (WWH)  Wind Wave Height    
        (WWP)  Wind Wave Period    
        (WWD)  Wind Wave Direction 
        Wave Steepness      (STEEPNESS)
        (APD)  Average Wave Period 
        (MWD) Mean Wace Direction
        '''
        self.date=datetime.datetime(int(data_spec[0]), int(data_spec[1]), int(data_spec[2]),int(data_spec[3]),int(data_spec[4]))
        self.WVHT=round(float(data_spec[5])*3.280839895,1)
        self.SwH=round(float(data_spec[6])*3.280839895,1)
        self.SwP=data_spec[7]
        self.WWH=round(float(data_spec[8])*3.280839895,1)
        self.WWP=data_spec[9]
        self.WWD=data_spec[11]
        self.APD=data_spec[13]
        self.MWD=data_spec[14]

    def __str__(self):
        return f'{str(utc_to_local(self.date))[:-6]}\n{self.WVHT} ft  {self.SwH} ft  {self.SwP} s  {self.MWD} deg \n{self.WWH} ft  {self.WWP} s  {self.WWD} deg \n'

class buoyData:
    def __init__(self, name, code, lat, lon):
        self.name = name
        self.code = code
        self.lat = lat 
        self.lon = lon
        self.hourlyData = getReport(code)

    def __str__(self):
        return f'{self.name}:  lat: {self.lat}  lon: {self.lon} \n {self.hourlyData[0]}'

def getReport(code):
        data_spec = requests.get(f'https://www.ndbc.noaa.gov/data/realtime2/{code}.spec').text.split("\n")[2:]
        report = []
        for items in data_spec:
            if(len(items)>0):
                report.append(hourlyReport(items.split()))
        return report

def getBouyData():
    buoyList = [["Diablo", 46215, 35.204, -120.859],
                ["Santa Maria", 46011, 34.936, -120.998],
                ["Santa Lucia", 46259, 34.767, -121.498],
                ["Harvest", 46218, 34.452, -120.78],
                ["Cape San Martin", 46028, 35.770, -121.903]]
    
    newBuoyList = []
    for buoys in buoyList:
        newBuoyList.append(buoyData(buoys[0],buoys[1],buoys[2],buoys[3]))
   
    return newBuoyList
