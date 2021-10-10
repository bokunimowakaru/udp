#!/usr/bin/env python3
# coding: utf-8

# UDPを送信する
# Copyright (c) 2021 Wataru KUNINO

# UDPで温度値を送信します。(外付けセンサ不要)
# ./ex3_tx_temp.py

import socket                                               # ソケットの組み込み
from time import sleep                                      # スリープの組み込み
from lib_tempSensor import TempSensor                       # 温度センサ組み込み

port = 1024                                                 # ポート番号を代入
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     # ソケットを作成
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)   # ブロードキャスト

tempSensor = TempSensor()                                   # 温度センサの実体化
tempSensor.offset = 30                                      # 補正値30を設定

while True:                                                 # 繰り返し構文
    temp = round(tempSensor.get(), 1)                       # 温度値を取得
    udp = 'temp._1,' + str(temp) + '\n'                     # 送信文字列を生成
    sock.sendto(udp.encode(),('255.255.255.255',port))      # UDP送信
    print('send :', udp, end='')                            # 送信データを出力
    sleep(10)                                               # 10秒の待ち時間処理
sock.close()                                                # 切断(実行されない)

'''
pi@raspberrypi:~/udp/learning $ ./ex3_tx_temp.py
send : temp._1,25.5
send : temp._1,26.5
send : temp._1,25.5
send : temp._1,24.5
'''
