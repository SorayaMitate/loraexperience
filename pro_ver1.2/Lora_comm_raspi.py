#自作モジュールのパスをsys.pathへ追加
import sys
sys.path.append(r'C:\Users\soraya-PC\OneDrive - awcc.uec.ac.jp\uec_doc\Mieuniv_Scope\experiment\lib')

import serial
import micropyGPS
import threading
import time
import binascii

'''
micropyGPSを用いたGPS信号受信プロセス
デーモンスレッドにより, GPSデータを中断することなく別スレッドで持続して取得
'''
gps = micropyGPS.MicropyGPS(9, 'dd') # MicroGPSオブジェクトを生成する。
                                     # 引数はタイムゾーンの時差と出力フォーマット

def rungps(): # GPSモジュールを読み、GPSオブジェクトを更新する
    s_GPS = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
    s_GPS.readline()  # 最初の1行は中途半端なデータが読めることがあるので、捨てる

    while True:
        sentence = None
        sentence = s_GPS.readline().decode('utf-8')  # GPSデーターを読み、文字列に変換する
        if sentence is None:
            print('None')
        else:
            if sentence[0] != '$': # 先頭が'$'でなければ捨てる
                continue
            for x in sentence: # 読んだ文字列を解析してGPSオブジェクトにデーターを追加、更新する
                gps.update(x)
        s_GPS.reset_input_buffer()

        time.sleep(0.01)

gpsthread = threading.Thread(target=rungps, args=()) # 上の関数を実行するスレッドを生成
gpsthread.daemon = True
gpsthread.start() # スレッドを起動


'''
LoRaを用いた通信
緯度, 軽度, 海抜情報をシリアルに流す
'''
s_lora = serial.Serial('/dev/ttyUSB0', 19200)
i=0
try:
    while True:
        if gps.clean_sentences > 20: # ちゃんとしたデーターがある程度たまったら出力する
            h = gps.timestamp[0] if gps.timestamp[0] < 24 else gps.timestamp[0] - 24
            lat = '{:.8f}'.format(gps.latitude[0])
            lon = '{:.8f}'.format(gps.longitude[0])
            lon = '0' + lon

            if len(str(i)) <= 4:
                index = '0'*( 4 - len(str(i))) + str(i)
            else :
                index = str(i)
            h = kisuu_str(str(h))
            minutes = kisuu_str(str(gps.timestamp[1]))
            second = kisuu_str(str(int(gps.timestamp[2])))

            jikan = h + minutes + second
            print(jikan)
            s_lora.write( nb'TXDA'+ jikan.encode('utf-8') + index.encode('utf-8') + lat.encode('utf-8') + lon.encode('utf-8')  + b'\r\n')
            print(jikan, index, lat, lon)
            i=i+1

except KeyboardInterrupt:
    print('finish')


def kisuu_str(str):
    if len(str) % 2 == 1 :
        return "0" + str
    else:
        return str
    return -1