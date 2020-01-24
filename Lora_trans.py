#自作モジュールのパスをsys.pathへ追加
#import sys
#sys.path.append(r'C:\Users\soraya-PC\OneDrive - awcc.uec.ac.jp\uec_doc\Mieuniv_Scope\experiment\lib')

import serial
import micropyGPS
import threading
import time
import binascii

'''
micropyGPSを用いたGPS信号受信プロセス
デーモンスレッドにより, GPSデータを中断することなく別スレッドで持続して取得
'''

# 奇数ならば"0"を追記する
def kisuu_str(str):
    if len(str) % 2 == 1 :
        return "0" + str
    else:
        return str
    return -1

def trans(ip):

    gps = micropyGPS.MicropyGPS(9, 'dd') # MicroGPSオブジェクトを生成する。
                                        # 引数はタイムゾーンの時差と出力フォーマット

    def rungps(): # GPSモジュールを読み、GPSオブジェクトを更新する
        s_GPS = serial.Serial('/dev/ttyUSB0', 9600, timeout=10)
        s_GPS.readline()  # 最初の1行は中途半端なデータが読めることがあるので、捨てる
        sentence = []
        while True:
            try:
                sentence = s_GPS.readline().decode('utf-8')  # GPSデーターを読み、文字列に変換する
            except UnicodeDecodeError:
                # でコードできないときはその行をスキップする
                s_GPS.readline()
                continue

            if sentence[0] != '$': # 先頭が'$'でなければその行をスキップする
                continue

            for x in sentence: # 読んだ文字列を解析してGPSオブジェクトにデーターを追加、更新する
                gps.update(x)

            s_GPS.flushInput()

    gpsthread = threading.Thread(target=rungps, args=()) # 上の関数を実行するスレッドを生成
    gpsthread.daemon = True
    gpsthread.start() # スレッドを起動


    '''
    LoRaを用いた通信
    緯度, 軽度, 海抜情報をシリアルに流す
    '''
    s_lora = serial.Serial('/dev/ttyUSB1', 19200)
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
                elif i >= 10000:
                    i = 0
                else :
                    index = str(i)
                h = kisuu_str(str(h))
                minutes = kisuu_str(str(gps.timestamp[1]))
                second = kisuu_str(str(int(gps.timestamp[2])))

                jikan = h + minutes + second
                s_lora.write(b'TXDA'+ jikan.encode('utf-8') + \
                    index.encode('utf-8') + lat.encode('utf-8') + lon.encode('utf-8')  + b'\r\n')
                i=i+1

    except KeyboardInterrupt:
        print('finish')
