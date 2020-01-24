import datetime
import binascii
import time
import micropyGPS
import serial
import sys
#sys.path.append(
#    r'C:\Users\soraya-PC\OneDrive - awcc.uec.ac.jp\uec_doc\Mieuniv_Scope\experiment\lib')

def rec(arg):
    s_lora = serial.Serial(arg, 19200)

    try:
        while True:
            cngtext = ""
            rxda = s_lora.readline().decode('utf-8')
            rxda = rxda.replace('\r\n', '')
            rxda = rxda.replace(':', ',')
            rxda_split = rxda.split(",")

            if len(rxda_split) >= 1:
                file_name = rxda_split[1] + '_data.csv'
                with open(file_name, 'a') as f:
                    f.write(rxda + ',' + '\n')
                    f.close()
            else :
                continue

    except KeyboardInterrupt:
        s_lora.close()
        print('finish')
