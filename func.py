# -*- coding: utf-8 -*-ss
#自作モジュールのパスをsys.pathへ追加
#import sys
#sys.path.append(r'C:\Users\soraya-PC\OneDrive - awcc.uec.ac.jp\uec_doc\Mieuniv_Scope\experiment\lib')

import serial
import micropyGPS
import time
import binascii
import threading

'''
micropyGPSを用いたGPS信号受信プロセス
デーモンスレッドにより, GPSデータを中断することなく別スレッドで持続して取得
'''

def rungps(s_GPS, s_tx, gps, lock): # GPSモジュールを読み、GPSオブジェクトを更新する
    s_GPS.readline()  # 最初の1行は中途半端なデータが読めることがあるので、捨てる
    sentence = []
    while True:
        try:
            sentence = s_GPS.readline().decode('utf-8')  # GPSデーターを読み、文字列に変換する
        
            if sentence[0] != '$': # 先頭が'$'でなければその行をスキップする
                continue
            else:
                lock.acquire()
                for x in sentence: # 読んだ文字列を解析してGPSオブジェクトにデーターを追加、更新する
                    gps.update(x)
                lock.release()
                print('lat =','{:.16f}'.format(gps.latitude[0]))
                s_tx.flush()

                time.sleep(0.1)

        
        except UnicodeDecodeError:
            # でコードできないときはその行をスキップする
            s_GPS.readline()
            continue

        s_GPS.flushInput()
