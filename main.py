# -*- coding: utf-8 -*-ss
from multiprocessing import Manager, Value, Process
import threading
import micropyGPS
import serial

from loracomm import trans, rec
from func import rungps

ttyUSB0 = '/dev/ttyUSB0'
ttyUSB1 = '/dev/ttyUSB1'
ttyUSB2 = '/dev/ttyUSB2'

if __name__ == "__main__":

    gps = micropyGPS.MicropyGPS(9, 'dd') # MicroGPSオブジェクトを生成する。
                                        # 引数はタイムゾーンの時差と出力フォーマット
    s_gps = serial.Serial(ttyUSB0, 9600, timeout=10)
    s_tx = serial.Serial(ttyUSB1, 19200)
    s_rx = serial.Serial(ttyUSB2, 19200)

    # ①ロックを作成
    lock = threading.Lock()
    gpsthread = threading.Thread(target=rungps, args=(s_gps, s_tx, gps, lock)) # 上の関数を実行するスレッドを生成
    gpsthread.daemon = True
    gpsthread.start() # スレッドを起動

    tx_thread = threading.Thread(target=trans, args=(s_tx, gps))
    tx_thread.start()

    rx_thread = threading.Thread(target=rec, args=(s_rx, gps))
    rx_thread.start()
