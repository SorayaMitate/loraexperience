import math
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import simplekml
from vincenty import*

F = 920000000
TRANS_LAT = 35.6584199999999996
TRANS_LON = 139.5439983333333203
DATE = '20200125'
START_TIME = '13502335'
FINISH_TIME = '15442035'

#実験開始時間 13502335
#実験終了時間 15442035
#'367B','3670'
file_name = '192_data.csv' 

data = pd.read_csv(file_name, header=None)
print(data)

data = []
with open(file_name, 'r') as f:
    data += [i.rstrip('\n').split(',') for i in f]
    f.close()

def make_time(data, start_index, num):
    time = '0'
    for i in range(start_index, start_index+num+1):
        time += data[i]
    return int(time)

def make_latlon(data , start_index, num, flag):
    result = '0'
    for i in range(start_index, start_index+num+1):
        result += data[i]
        if i == start_index and flag == 0:
            result += '.'
        if i == start_index+1 and flag == 1:
            result += '.'
    return float(result)

def asccito10(s):
    moji = bin(int(s, 16))
    tmp = '0'
    for i in range(len(moji)):
        if i >=3:
            if moji[i] == '1':
                tmp += '0'
            elif moji[i] == '0':
                tmp += '1'
    return (-1)*int(tmp,2)

def cal_rho(lon_a,lat_a,lon_b,lat_b):
    ra=6378.140  # equatorial radius (km)
    rb=6356.755  # polar radius (km)
    F=(ra-rb)/ra # flattening of the earth
    rad_lat_a=np.radians(lat_a)
    rad_lon_a=np.radians(lon_a)
    rad_lat_b=np.radians(lat_b)
    rad_lon_b=np.radians(lon_b)
    pa=np.arctan(rb/ra*np.tan(rad_lat_a))
    pb=np.arctan(rb/ra*np.tan(rad_lat_b))
    xx=np.arccos(np.sin(pa)*np.sin(pb)+np.cos(pa)*np.cos(pb)*np.cos(rad_lon_a-rad_lon_b))
    c1=(np.sin(xx)-xx)*(np.sin(pa)+np.sin(pb))**2/np.cos(xx/2)**2
    c2=(np.sin(xx)+xx)*(np.sin(pa)-np.sin(pb))**2/np.sin(xx/2)**2
    dr=F/8*(c1-c2)
    rho=ra*(xx+dr)
    return rho * 10**3


def distance_by_hubeny(p1, p2):
    a2 = 6378137.0 ** 2
    b2 = 6356752.314140 ** 2
    e2 = (a2 - b2) / a2

    def d2r(deg):
        return deg * (2 * math.pi) / 360
    (lon1, lat1, lon2, lat2) = map(d2r, p1 + p2)
    w = 1 - e2 * math.sin((lat1 + lat2) / 2) ** 2
    c2 = math.cos((lat1 + lat2) / 2) ** 2
    return math.sqrt((b2 / w ** 3) * (lat1 - lat2) ** 2 + (a2 / w) * c2 * (lon1 - lon2) ** 2)

data_tmp = [(int(DATE + str(make_time(i, 3, 2))), make_latlon(i, 6, 8, 0), make_latlon(i, 15, 9, 1),\
    asccito10(i[2]), ) for i in data if i[6] != '00' \
        and int(START_TIME) <= make_time(i, 3, 3) <= int(FINISH_TIME)]

redata = []
for i in data_tmp:
    dist, theta = vincenty_inverse(TRANS_LAT, TRANS_LON, i[1], i[2])
    #theta = azimuth(TRANS_LON, TRANS_LAT, i[2], i[1])
    #dist = distance_by_hubeny([TRANS_LON, TRANS_LAT], [i[2], i[1]])
    redata += [i + (dist, theta)]
print('The number of nodes =', len(redata))

time = [i[0] for i in redata] 
lat = [i[1] for i in redata]
lon = [i[2] for i in redata]
rssi = [i[3] for i in redata]
dist = [i[4] for i in redata]
theta = [i[5] for i in redata]

#データベース登録用
flame = pd.DataFrame({
    'time':time,
    'trans_lat':TRANS_LAT,
    'trans_lon':TRANS_LON,
    'receive_lat':lat,
    'receive_lon':lon,
    'frequency':F,
    'rssi':rssi,
    'dist':dist
})
flame.to_csv('redata.csv', index=None)

#simplekmlのkmlクラスを定義
kml = simplekml.Kml()

for i in redata:
    pnt=kml.newpoint(name= str(i[3]))
    pnt.coords=[(i[2],i[1])]
    pnt.style.labelstyle.scale = 1.5 # name 表示テキストの大きさ指定（周りの文字より大きくする）
    pnt.style.labelstyle.color = simplekml.Color.cyan  # name 表示色を cyan に指定
kml.save('test.kml')
