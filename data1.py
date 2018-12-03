import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#from mpl_toolkits.basemap import Basemap
#from shapely.geometry import Point, Polygon, MultiPoint, MultiPolygon
#from shapely.prepared import prep
#import fiona
from matplotlib.collections import PatchCollection
from descartes import PolygonPatch
import json
import datetime
from itertools import takewhile
import math
import collections
#Location storage
FILENAME='LocationHistory.json'
with open(FILENAME, 'r') as fh:
    raw = json.loads(fh.read())
#np.fliplr(raw)
ld = pd.DataFrame(raw['locations'])
del raw #free up some memory
# convert to typical units
ld['latitudeE7'] = ld['latitudeE7']/float(1e7) 
ld['longitudeE7'] = ld['longitudeE7']/float(1e7)
ld['timestampMs'] = ld['timestampMs'].map(lambda x: float(x)/1000) #to seconds
ld['datetime'] = ld.timestampMs.map(datetime.datetime.fromtimestamp)
ld.rename(columns={'latitudeE7':'latitude', 'longitudeE7':'longitude', 'timestampMs':'timestamp'}, inplace=True)
ld = ld[ld.accuracy < 1000] #Ignore locations with accuracy estimates over 1000m
ld.reset_index(drop=True, inplace=True) 
def timeRange(x,y,ld):
    ld = ld[ld.datetime>datetime.datetime(2016,12,x)]
    ld = ld[ld.datetime<datetime.datetime(2016,12,y)]
    return ld
ld = timeRange(11,12,ld)
#print (np.cos(1))
degrees_to_radians = np.pi/180.0 
ld['phi'] = (90.0 - ld.latitude) * degrees_to_radians 
ld['theta'] = (ld.longitude) * degrees_to_radians
# Compute distance between two GPS points on a unit sphere

ld['distance'] = np.arccos(
    np.sin(ld.phi)*np.sin(ld.phi.shift(-1)) * np.cos(ld.theta - ld.theta.shift(-1)) +
    np.cos(ld.phi)*np.cos(ld.phi.shift(-1))) * 6378.100 # radius of earth in km

ld['speed'] = ld.distance/(ld.timestamp - ld.timestamp.shift(-1))*3600 #km/hr
#def getConvert
#returns an array of all the time you are at home
def timeAtHome(ld):
    chargeable = ld[ld.speed==0]
    chargeable = chargeable[chargeable.latitude==chargeable.latitude.shift(-1)]
    chargeable = chargeable[chargeable.longitude==chargeable.longitude.shift(-1)]
    score= collections.Counter((chargeable['latitude']))
    #THING TO FIX probably won't work if you drive around the equator 
    home=chargeable[abs(chargeable.latitude-score.most_common(1)[0][0])<.05]
    return home
def chargeToats(ld):
    energyUsed=0.0
   # ld=ld[ld.distance0]
    ld=ld[ld.speed<10]
    for y in ld['longitude']:
        energyUsed=energyUsed+1
   # print(x)
    print('energy charged in seg')
    energyUsed=(energyUsed)
    print (energyUsed,"units")
    return energyUsed
def calcEnergy(ld):
    energyUsed=0.0
    ld=ld[ld.distance>0]
    ld=ld[ld.speed>10]
    for y in ld['distance']:
        energyUsed=energyUsed+y
   # print(x)
    print('energy used of day')
    energyUsed=(energyUsed*.621371)/3
    print (energyUsed,"killo watts")
    return energyUsed


    #print(home['datetime'])
def convertToTwenty(ld,i):
    calcEnergy(ld)
    chargeToats(ld)   
'''
for i in ld['datetime']:
    print (i.minute)
'''
state={"EVbat",time}
for i in range(1,72):
    x = math.floor(i/3)
    y = (i-x*3)*20
    a =math.floor((i-1)/3)
    b =(i-a*3)*20-1
    #print (b)
    ldi=ld[ld.datetime>datetime.datetime(2016,12,11,x,y)]
    ldi=ld[ld.datetime<datetime.datetime(2016,12,11,a,b)]
    print(i)
    convertToTwenty(ldi,i)

#print (chargeable['latitude'])
#print (chargeable['latitude':'longitude':'datetime'])


calcEnergy(ld)
