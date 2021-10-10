#!/usr/bin/env python3
# coding: utf-8

# UDPを受信する
# Copyright (c) 2021 Wataru KUNINO

# UDPの待ち受けと、受信した文字列の表示を繰り返します。
# ex2_rx.pyとの違いは、一度、実行すると繰り返し動作し続ける点と、
# Listening UDP portや、送信元を表示しない点です。
# ./ex2_rx_loop.py

# 受信データをファイルに保存し続けることも出来ます。
# ./ex2_rx_loop.py > log.csv &

import socket                                               # ソケットの組み込み

port = 1024                                                 # ポート番号を代入
sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)       # ソケットを作成
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)   # オプション設定
# print('Listening UDP port', port, '...')                  # ポート番号表示

sock.bind(('', port))                                       # ポート番号を設定
while True:                                                 # 繰り返し構文
    udp = sock.recvfrom(128)                                # UDPパケットを取得
    print(udp[0].decode())                                  # 受信データを表示
sock.close()                                                # 切断(実行されない)
