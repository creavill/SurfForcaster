from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

def makePoint(lon,lat,col,map):
    x,y = map(lon, lat)
    map.plot(x, y, 'bo', markersize=5, color=col)