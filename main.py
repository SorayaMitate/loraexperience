# -*- coding: utf-8 -*-ss
from multiprocessing import Manager, Value, Process
import threading
import micropyGPS

from loracomm import trans, rec
from func import rungps

ttyUSB0 = '/dev/ttyUSB0'
ttyUSB1 = '/dev/ttyUSB1'
ttyUSB2 = '/dev/ttyUSB2'

if __name__ == "__main__":

    gps = micropyGPS.MicropyGPS(9, 'dd') # MicroGPSオブジェクトを生成する。
                                        # 引数はタイムゾーンの時差と出力フォーマット

    # ①ロックを作成
    lock = threading.Lock()
    gpsthread = threading.Thread(target=rungps, args=(gps, lock, ttyUSB0)) # 上の関数を実行するスレッドを生成
    gpsthread.daemon = True
    gpsthread.start() # スレッドを起動

    tx_thread = threading.Thread(target=trans, args=(gps, ttyUSB1))
    tx_thread.start()

    rx_thread = threading.Thread(target=rec, args=(gps, ttyUSB2))
    rx_thread.start()
