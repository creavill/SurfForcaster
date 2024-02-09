import math
import matplotlib
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import statistics

from plotSurfBuoys import plotBuoys
from plotSurfSpots import plostSurfSpots
from infoExtractor import getBouyData

def main():
    map = Basemap(projection='merc',
        resolution = 'h', area_thresh = 1000.0,
        llcrnrlon=-122, llcrnrlat=34,
        urcrnrlon=-120, urcrnrlat=36)
    
    plotBuoys(map)
    plostSurfSpots(map)

    buoyData = getBouyData()

    buildMatrix(buoyData, map)

    map.drawcoastlines()
    map.drawcountries()
    map.fillcontinents(color='coral')
    map.drawmapboundary()
    
    map.drawmeridians(np.arange(0, 360, 30))
    map.drawparallels(np.arange(-90, 90, 30))

    plt.show()

    ''' 
    Quiver plot 
    https://www.geeksforgeeks.org/quiver-plot-in-matplotlib/
    https://www.geeksforgeeks.org/numpy-meshgrid-function/
    https://stackoverflow.com/questions/56046811/how-make-a-correct-gradient-map-using-numpy-gradient
    '''

def buildMatrix(buoyData, map):

    norm = matplotlib.colors.Normalize()
    norm.autoscale(100)
    cm = matplotlib.cm.jet
    colorTest = 0
    for i in np.arange(34,36,.15):
        for j in np.arange(-122,-120,.15):
            avgs = calcAvgs(buoyData, j,i)
            x,y = map(j, i)
            # 0 - 300 is the range
            map.quiver(x,y,-math.sin(math.radians(avgs[1])),-math.cos(math.radians(avgs[1])),color=cm(int(avgs[0]*20)))
            colorTest+=3
            map.plot(x, y, 'bo', markersize=1, color='grey')



def calcAvgs(buoyData, lon, lat):
    '''
    View https://math.stackexchange.com/questions/1968091/weight-of-a-point-based-on-its-distance-from-other-weighted-points
    for explination of math
    '''
    
    avgMWD = []
    avgSwH =0
    totalRk = 0
    for buoys in buoyData:
        tempRk = 1/((math.dist([lon,lat], [buoys[2],buoys[1]])))
        avgMWD+=([float(buoys[3].MWD)]*round(tempRk))
        avgSwH += tempRk*float(buoys[3].SwH)
        totalRk+=tempRk
 
    return([avgSwH/totalRk,statistics.mean(avgMWD)])


main()