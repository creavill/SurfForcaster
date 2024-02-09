'''
Weather app
https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid=f5c624515764759503fa025c5a408bb7

key = f5c624515764759503fa025c5a408bb7

National Bouy App
wget https://www.ndbc.noaa.gov/data/realtime2/{Location}.txt

Diablo = 46215
SANTA MARIA = 46011
Santa Lucia Escarpment = 46259
Harvest, CA = 46218
CAPE SAN MARTIN = 46028

Notes :: good idea, but far too much work to predict all swells and stuff. Revisit down the line maybe
'''

import datetime
import requests

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
#YY  MM DD hh mm Sep_Freq  < spec_1 (freq_1) spec_2 (freq_2) spec_3 (freq_3) ... >
data_spec = requests.get("https://www.ndbc.noaa.gov/data/realtime2/46215.data_spec").text.split("\n")[1:]
#YY  MM DD hh mm alpha1_1 (freq_1) alpha1_2 (freq_2) alpha1_3 (freq_3) ... >
swdir  = requests.get("https://www.ndbc.noaa.gov/data/realtime2/46215.swdir").text.split("\n")[1:]
#YY  MM DD hh mm alpha2_1 (freq_1) alpha2_2 (freq_2) alpha2_3 (freq_3) ... >
swdir2 = requests.get("https://www.ndbc.noaa.gov/data/realtime2/46215.swdir2").text.split("\n")[1:]
#YY  MM DD hh mm r1_1 (freq_1) r1_2 (freq_2) r1_3 (freq_3) ... >
swr1 = requests.get("https://www.ndbc.noaa.gov/data/realtime2/46215.swr1").text.split("\n")[1:]
#YY  MM DD hh mm r1_1 (freq_1) r1_2 (freq_2) r1_3 (freq_3) ... >
swr2 = requests.get("https://www.ndbc.noaa.gov/data/realtime2/46215.swr1").text.split("\n")[1:]



def extractRawData(rows,n):
    finalOutput = []
    for row in rows[1::]:  
        rowOutput=[]
        temp = row.split()
        i = n
        while i < len(temp):
            if float(temp[i])>-1:
                seconds = int(float(temp[i+1].strip('(').strip(')'))*100)
                dt =  datetime.datetime(int(temp[0]), int(temp[1]), int(temp[2]),int(temp[3]),int(temp[4]), seconds)
                rowOutput.append((str(utc_to_local(dt))[:-6],temp[i]))
            i+=2
        finalOutput+=rowOutput[::-2]

    for item in finalOutput:
        f.write(item[0] +"  " + item[1] + "\n")
    return finalOutput

def extractRawData2(data_spec,swdir,swdir2,swr1,swr2):
    upperBound=min(len(data_spec),len(swdir),len(swdir2),len(swr1),len(swr2))
    for n in range(0,upperBound):
        rowOutput=[]
        tempDS = data_spec[n].split()[6:]
        tempSD = swdir[n].split()[5:]
        tempSD2 = swdir2[n].split()[5:]
        tempSWR1 = swr1[n].split()[5:]
        tempSWR2 = swr2[n].split()[5:]
        date = data_spec[n].split()[0:6]
        i=0
        while i < min(len(tempDS),len(tempSWR1),len(tempSD),len(tempSD2),len(tempSWR2)):
            if float(tempDS[i])>-1:
                seconds = int(float(tempDS[i+1].strip('(').strip(')'))*100)
                dt =  datetime.datetime(int(date[0]), int(date[1]), int(date[2]),int(date[3]),int(date[4]), seconds)
                rowOutput.append((utc_to_local(dt), tempDS[i], tempSD[i], tempSD2[i] ,tempSWR1[i],str(tempSWR2[i])))

            i+=2
        for item in rowOutput[::]:
            f.write(str(item[0])[:-6] +",   " + item[1] + ",   " + item[2] +",   " + item[3] + ",   " + item[4] + ",   " + item[5] + " ,\n")

f = open("demofile2.txt", "w")
extractRawData2(data_spec,swdir,swdir2,swr1,swr2)
f.close()


'''
#print(rows[0])
#print(rows[1])
#print(rows[2])
class hourlyDiablo:
  def __init__(self, date, WH, DWP ,AP , MWD , WT   ):
    
    WH = Wave Height (ft)
    DWP = Dominant Wave Period (s) 
    AP = Average Period (s)
    MWD = Mean Wave Direction (deg)
    WT = Water Temp (DegC)
    
    self.date=datetime.datetime(rowInfo[0], rowInfo[1], rowInfo[2],rowInfo[3],rowInfo[4])
    self.WH = rowInfo[8]
    self.DWP = rowInfo[9]
    self.AP = rowInfo[10]
    self.MWD = rowInfo[11]
    self.WT = rowInfo[14]
'''
