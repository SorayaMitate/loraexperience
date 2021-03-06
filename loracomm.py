# -*- coding: utf-8 -*-ss
import datetime
import binascii
import time
import micropyGPS
import serial
import sys
import logging
#sys.path.append(
#    r'C:\Users\soraya-PC\OneDrive - awcc.uec.ac.jp\uec_doc\Mieuniv_Scope\experiment\lib')

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

def rec(s_lora, gps):

    logging.debug('rec start')

    file_name = 'data.csv'

    try:
        while True:
            cngtext = ""
            rxda = s_lora.readline().decode('utf-8')
            rxda = rxda.replace('\r\n', '')
            rxda = rxda.replace(':', ',')
            rxda_split = rxda.split(",")

            if len(rxda_split) >= 3:

                if float('{:.16f}'.format(gps.latitude[0]))>0: # ちゃんとしたデーターがある程度たまったら出力する

                    h = gps.timestamp[0] if gps.timestamp[0] < 24 else gps.timestamp[0] - 24
                    lat = float('{:.16f}'.format(gps.latitude[0]))
                    lon = float('{:.16f}'.format(gps.longitude[0]))
                    lon = '0' + str(lon)
                    with open(file_name, 'a') as f:
                        f.write(rxda + ',' + str(lat) + ',' + str(lon) + ',' + '\n')
                        f.close()
                else:
                    continue
            else :
                continue

    except KeyboardInterrupt:
        s_lora.close()
        print('finish')

    logging.debug('end')

def trans(s_lora, gps):

    logging.debug('trans start')

    '''
    LoRaを用いた通信
    緯度, 軽度, 海抜情報をシリアルに流す
    '''
    # 奇数ならば"0"を追記する
    def kisuu_str(str):
        if len(str) % 2 == 1 :
            return "0" + str
        else:
            return str
        return -1

    try:
        while True:
            if float('{:.16f}'.format(gps.latitude[0]))>0: # ちゃんとしたデーターがある程度たまったら出力する
                h = gps.timestamp[0] if gps.timestamp[0] < 24 else gps.timestamp[0] - 24
                lat = '{:.16f}'.format(gps.latitude[0])
                lon = '{:.16f}'.format(gps.longitude[0])
                lon = '0' + lon

                h = kisuu_str(str(h))
                minutes = kisuu_str(str(gps.timestamp[1]))
                second = kisuu_str(str(int(gps.timestamp[2])))

                jikan = h + minutes + second
                s_lora.write(b'TXDA'+ jikan.encode('utf-8') + \
                    lat.encode('utf-8') + lon.encode('utf-8')  + b'\r\n')

    except KeyboardInterrupt:
        print('finish')