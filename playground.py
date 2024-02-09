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

def getReport(num):
    data_spec = requests.get(f'https://www.ndbc.noaa.gov/data/realtime2/{num}.spec').text.split("\n")
    report = []
    for items in data_spec:
        if(len(items)>0):
            report.append(hourlyReport(items.split()))
    return report

def getBouyData():
    Diablo = getReport(46215)[0]
    SantaMaria = getReport(46011)[0]
    SantaLucia = getReport(46259)[0]
    Harvest = getReport(46218)[0]
    CapeSanMartin = getReport(46028)[0]

    return([["Diablo", 35.204, -120.859, Diablo], 
            ["Santa Maria", 34.936, -120.998, SantaMaria], 
            ["Santa Lucia", 34.767, -121.498, SantaLucia], 
            ["Harvest", 34.452, -120.78, Harvest], 
            ["Cape San Martin", 35.770, -121.903, CapeSanMartin]])

getReport(46011)