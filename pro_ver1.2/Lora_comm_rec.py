#自作モジュールのパスをsys.pathへ追加
import sys
sys.path.append(r'C:\Users\soraya-PC\OneDrive - awcc.uec.ac.jp\uec_doc\Mieuniv_Scope\experiment\lib')

import serial
import micropyGPS
import threading
import time
import binascii

event = threading.Event()

'''
IM920を用いた信号受信プロセス
デーモンスレッドにより, LoRaからの送信信号を中断することなく別スレッドで持続して取得
'''
def runlora(): # GPSモジュールを読み、GPSオブジェクトを更新する
    s_lora = serial.Serial('COM8', 19200)
    try:
        while True:
            print('waiting')
            print(s_lora.readline().decode('utf-8'))
    except KeyboardInterrupt:
        s_lora.close()
        print('finish')

gpsthread = threading.Thread(target=runlora, args=()) # 上の関数を実行するスレッドを生成
gpsthread.daemon = True 
gpsthread.start() # スレッドを起動

'''
受信信号に対する処理
'''
try:
    while True:
    print('waiting')
        text = text.replace("\r\n","")
        text = text.split(":")[1]
        text = text.split(",")

        for x in text:
            cngtext += chr(int(x,16))
except KeyboardInterrupt:
    print('finish')