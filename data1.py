import matplotlib.pyplot as plt
import numpy as np
import pandas as d
#from mpl_toolkits.basemap import Basemap
#from shapely.geometry import Point, Polygon, MultiPoint, MultiPolygon
#from shapely.prepared import prep
#import fiona
from matplotlib.collections import PatchCollection
from descartes import PolygonPatch
import json
import datetime
from itertools import takewhile

'''
with open('LocationHistoryM.json', 'r') as fh:
    raw = json.loads(fh.read())
#np.fliplr(raw)
lM = pd.DataFrame(raw['locations'])
del raw #free up some memory
# convert to typical units
lM['latitudeE7'] = lM['latitudeE7']/float(1e7) 
lM['longitudeE7'] = lM['longitudeE7']/float(1e7)
lM['timestampMs'] = lM['timestampMs'].map(lambda x: float(x)/1000) #to seconds
lM['datetime'] = lM.timestampMs.map(datetime.datetime.fromtimestamp)
# Rename fields based on the conversions we just did
lM.rename(columns={'latitudeE7':'latitude', 'longitudeE7':'longitude', 'timestampMs':'timestamp'}, inplace=True)
lM = lM[lM.accuracy < 1000] #Ignore locations with accuracy estimates over 1000m
lM.reset_index(drop=True, inplace=True) 
'''

with open('LocationHistory.json', 'r') as fh:
    raw = json.loads(fh.read())
#np.fliplr(raw)
ld = pd.DataFrame(raw['locations'])
del raw #free up some memory

# convert to typical units
ld['latitudeE7'] = ld['latitudeE7']/float(1e7) 
ld['longitudeE7'] = ld['longitudeE7']/float(1e7)
ld['timestampMs'] = ld['timestampMs'].map(lambda x: float(x)/1000) #to seconds
ld['datetime'] = ld.timestampMs.map(datetime.datetime.fromtimestamp)

# Rename fields based on the conversions we just did
ld.rename(columns={'latitudeE7':'latitude', 'longitudeE7':'longitude', 'timestampMs':'timestamp'}, inplace=True)
ld = ld[ld.accuracy < 1000] #Ignore locations with accuracy estimates over 1000m
ld.reset_index(drop=True, inplace=True) 
for x in ld['datetime']:
    if(x>datetime.datetime(2016,12,11)and x<datetime.datetime(2016,12,18)):
        print (x)
#print(takewhile(lambda ld: ld['datetime']>datetime.datetime(2016,12,17),ld))


#from_date =datetime.date(year=2015,mont=11,day=1)
#print (takewhile(lambda ld:ld['datetime']<=x,ld))
#all_points = MultiPoint(mapped_points)
