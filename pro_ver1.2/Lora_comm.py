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
    s_GPS = serial.Serial('/dev/ttyUSB', 9600, timeout=10)
    s_GPS.readline() # 最初の1行は中途半端なデーターが読めることがあるので、捨てる
    while True:
        sentence = s_GPS.readline().decode('utf-8') # GPSデーターを読み、文字列に変換する
        if sentence[0] != '$': # 先頭が'$'でなければ捨てる
            continue
        for x in sentence: # 読んだ文字列を解析してGPSオブジェクトにデーターを追加、更新する
            gps.update(x)

gpsthread = threading.Thread(target=rungps, args=()) # 上の関数を実行するスレッドを生成
gpsthread.daemon = True 
gpsthread.start() # スレッドを起動

'''
LoRaを用いた通信
緯度, 軽度, 海抜情報をシリアルに流す
'''
s_lora = serial.Serial('/dev/ttyUSB', 19200)
try:
    while True:
        i=0
        if gps.clean_sentences > 20: # ちゃんとしたデーターがある程度たまったら出力する
            h = gps.timestamp[0] if gps.timestamp[0] < 24 else gps.timestamp[0] - 24
            lat = '{:.8f}'.format(gps.latitude[0])
            lon = '{:.8f}'.format(gps.longitude[0])
            time = h + gps.timestamp[1] + gps.timestamp[2]
            print('緯度経度: lat, lon')
            print('海抜: %f' % gps.altitude)
            TXDA = 's' + ',' +str(i) + ',' + 's' + ',' + time  + ',' + 's' + ',' + \
                    lat + ',' + 's' + ',' + lon + ',' + 's' + ',' + gps.altitude + ','
            print(TXDA)
            s_lora.write(b'TXDA' + binascii.b2a_hex(TXDA.encode('utf-8')) + b'\r\n')
            i=i+1
        time.sleep(3.0)
        
except KeyboardInterrupt:
    print('finish')