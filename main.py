# -*- coding: utf-8 -*-

import multiprocessing as mp
from Lora_trans import trans
from Lora_receive import rec

ttyUSB0 = '/dev/ttyUSB0'
ttyUSB1 = '/dev/ttyUSB1'
ttyUSB2 = '/dev/ttyUSB2'

def main():

    #送信プロセス
    process_trans = mp.Process(target=trans, args=(ttyUSB0, ttyUSB1,))
    process_trans.start()
    
    #受信プロセス
    process_rec = mp.Process(target=rec, args=(ttyUSB2,))
    process_rec.start()

    process_rec.join()
    process_trans.join()

if __name__ == "__main__":
    main()