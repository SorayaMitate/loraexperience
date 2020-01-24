import multiprocessing as mp
from Lora_trans import trans
from Lora_receive import rec

ip = '190'
network_list = ['191','192']

def main():

    #送信プロセス
    process_trans = mp.Process(target=trans, args=ip)
    process_trans.start()
    
    #受信プロセス
    process_rec = mp.Process(target=rec, args=ip)
    process_rec.start()


if __name__ == "__main__":
    main()