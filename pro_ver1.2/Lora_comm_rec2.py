#自作モジュールのパスをsys.pathへ追加
import sys
sys.path.append(r'C:\Users\soraya-PC\OneDrive - awcc.uec.ac.jp\uec_doc\Mieuniv_Scope\experiment\lib')

import serial
import micropyGPS
import threading
import time
import binascii
import datetime

s_lora = serial.Serial('COM5', 19200)
try:
    while True:
        cngtext = ""
        print('waiting')
        rxda = s_lora.readline().decode('utf-8')
        rxda = rxda.replace('\r\n', '')
        rxda = rxda.replace(':', ',')
        rxda_split = rxda.split(",")
        print(rxda_split)
        print(rxda_split[0])

        file_name = rxda_split[0] + '_data.csv'
        with open(file_name, 'a') as f:

            f.write(rxda + ',' + '\n')
            f.close()

except KeyboardInterrupt:
    s_lora.close()
    print('finish')