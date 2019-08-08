# 自作モジュールのパスをsys.pathへ追加
import binascii
import time
import threading
import micropyGPS
import serial
import sys
sys.path.append(
    r'C:\Users\soraya-PC\OneDrive - awcc.uec.ac.jp\uec_doc\Mieuniv_Scope\experiment\lib')


'''
micropyGPSを用いたGPS信号受信プロセス
デーモンスレッドにより, GPSデータを中断することなく別スレッドで持続して取得
'''
gps = micropyGPS.MicropyGPS(9, 'dd')  # MicroGPSオブジェクトを生成する。
# 引数はタイムゾーンの時差と出力フォーマット


def rungps():  # GPSモジュールを読み、GPSオブジェクトを更新する
    s_GPS = serial.Serial('/dev/ttyUSB1', 9600, timeout=10)
    s_GPS.readline()  # 最初の1行は中途半端なデーターが読めることがあるので、捨てる
    while True:
        try:
            sentence = s_GPS.readline().decode('utf-8')  # GPSデーターを読み、文字列に変換する
        except UnicodeDecodeError:
            s_GPS.readline()
            continue
        if sentence[0] != '$':  # 先頭が'$'でなければ捨てる
            continue
        for x in sentence:  # 読んだ文字列を解析してGPSオブジェクトにデーターを追加、更新する
            gps.update(x)


gpsthread = threading.Thread(target=rungps, args=())  # 上の関数を実行するスレッドを生成
gpsthread.daemon = True
gpsthread.start()  # スレッドを起動

'''
LoRaを用いた通信
緯度, 軽度, 海抜情報をシリアルに流す
'''
s_lora = serial.Serial('/dev/ttyUSB0', 19200)
i = 0
try:
    while True:
        if gps.clean_sentences > 20:  # ちゃんとしたデーターがある程度たまったら出力する
            h = gps.timestamp[0] if gps.timestamp[0] < 24 else gps.timestamp[0] - 24
            lat = '{:.8f}'.format(gps.latitude[0])
            lon = '{:.8f}'.format(gps.longitude[0])
            lon = '0' + lon
            if len(str(i)) <= 4:
                index = '0'*(4 - len(str(i))) + str(i)
            else:
                index = str(i)
            if len(str(h)) % 2 == 1:
                h = '0' + str(h)
            else:
                h = str(h)
            if len(str(gps.timestamp[1])) % 2 == 1:
                minutes = '0' + str(gps.timestamp[1])
            else:
                minutes = str(gps.timestamp[1])
            if len(str(int(gps.timestamp[2]))) % 2 == 1:
                second = '0' + str(int(gps.timestamp[2]))
            else:
                second = str(int(gps.timestamp[2]))

            jikan = h + minutes + second
            print(jikan)
            s_lora.write(b'TXDA'+jikan.encode('utf-8') + index.encode('utf-8') +
                         lat.encode('utf-8') + lon.encode('utf-8') + b'\r\n')
            print(jikan, index, lat, lon)
            i = i+1
        time.sleep(5.0)

except KeyboardInterrupt:
    print('finish')
