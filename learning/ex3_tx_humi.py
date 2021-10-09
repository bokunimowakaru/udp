#!/usr/bin/env python3
# coding: utf-8

# UDPを送信する
# Copyright (c) 2021 Wataru KUNINO

# UDPで温度値と湿度値を送信します。(外付けセンサ = SHT30)
# ./ex3_tx_humi.py

import socket                                               # ソケットの組み込み
from time import sleep                                      # スリープの組み込み
from lib_humiSensorSHT import HumiSensor                    # 温度センサ組み込み

port = 1024                                                 # ポート番号を代入
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     # ソケットを作成
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)   # ブロードキャスト

humiSensor = HumiSensor()                                   # 温度センサの実体化

while True:                                                 # 繰り返し構文
    (temp, humi) = humiSensor.get()                         # 温度値を取得
    udp = 'humid_1,' + str(round(temp, 1)) + ', '           # 送信文字列を生成
    udp += str(round(humi, 2)) + '\n'                       # 
    sock.sendto(udp.encode(),('255.255.255.255',port))      # UDP送信
    print('send :', udp, end='')                            # 送信データを出力
    sleep(10)                                               # 10秒の待ち時間処理
sock.close()                                                # 切断(実行されない)

'''
pi@raspberrypi:~/udp/learning $ ./ex3_tx_humi.py
send : humid_1,29.7, 56.13
send : humid_1,29.7, 56.18
send : humid_1,29.7, 56.18
send : humid_1,29.7, 56.14
send : humid_1,29.7, 56.14
'''
