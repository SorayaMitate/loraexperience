import math
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import simplekml
from vincenty import*

F = 920000000
f = '192_data.csv'
RSSI = 2 
TIME = 3
START_TX_LAT = 6
START_TX_LON = 15
RX_LAT = 25
RX_LON = 26

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

data = pd.read_csv(f,header=None, dtype=str)

l_time = []
l_tx_lat = []
l_tx_lon = []
l_rx_lat = []
l_rx_lon = []
l_rssi = []
for i, v in data.iterrows():

    for j in range(TIME, START_TX_LAT):
        if j == TIME:
            time = v[j]
        else:
            time = time + v[j]

    for j in range(START_TX_LAT, START_TX_LON):
        if j == START_TX_LAT:
            tx_lat = v[j] + '.'
        else:
            tx_lat = tx_lat + v[j]

    for j in range(START_TX_LON, RX_LAT):
        if j == START_TX_LON:
            tx_lon = v[j]
        elif j == START_TX_LON+1:
            tx_lon = tx_lon + v[j] + '.'
        else:
            tx_lon = tx_lon + v[j]

    l_time.append(time)
    l_tx_lat.append(float(tx_lat))
    l_tx_lon.append(float(tx_lon))
    l_rx_lat.append(float(v[RX_LAT]))
    l_rx_lon.append(float(v[RX_LON]))
    l_rssi.append(float(asccito10(v[RSSI])))


#データベース登録用
redata = pd.DataFrame({
    'time':l_time,
    'trans_lat':l_tx_lat,
    'trans_lon':l_tx_lon,
    'receive_lat':l_rx_lat,
    'receive_lon':l_rx_lon,
    'frequency':F,
    'rssi':l_rssi   
})
print(redata)