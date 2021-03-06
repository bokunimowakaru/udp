#!/usr/bin/env python3
# coding: utf-8

# UDPを送信する ユニキャスト対応版
# Copyright (c) 2018-2022 Wataru KUNINO

###############################################################################

# UDPをブロードキャストで送信します。
# echo "Ping" | ./udp_sender.py

# 整数の第1引数を入力した場合は、ポート番号と判定します。
# echo "Ping" | ./udp_sender.py 1024

# 文字列の第1引数を入力した場合は、IPアドレスと判定します。
# echo "Ping" | ./udp_sender.py 192.168.1.10 1024

import sys
import socket

sendto_ip = '255.255.255.255'                           # 初期値ブロードキャスト
port = 1024                                             # 初期値ポート番号1024

argc = len(sys.argv)                                    # 引数の数をargcへ代入
print('UDP Sender (usage: '+sys.argv[0]+' port < data)')# タイトル表示
if argc >= 2:                                           # 入力パラメータ数の確認
    try:
        port = int(sys.argv[1])                         # ポート番号を設定
    except ValueError:                                  # 入力が文字列の時
        sendto_ip = sys.argv[1]                         # IPアドレスとして保持
        if argc >= 3:                                   # 引数が2個以上の時
            port = int(sys.argv[2])                     # ポート番号を設定
    if port < 1 or port > 65535:                        # ポート1未満or65535超の時
        port = 1024                                     # UDPポート番号を1024に
else:
    port = 1024

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # ソケットを作成
    if sendto_ip == '255.255.255.255':                  # ブロードキャストの時
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
except Exception as e:                                  # 例外処理発生時
    print(e)                                            # エラー内容を表示
    exit()                                              # プログラムの終了
if sock:                                                # 作成に成功したとき
    for line in sys.stdin:                              # 標準入力から変数lineへ
        udp = line.strip('\r\n')                        # 改行を削除してudpへ
        print('send : ' + udp)                          # 受信データを出力
        udp=(udp + '\n').encode()                       # 改行追加とバイト列変換
        sock.sendto(udp,(sendto_ip,port))               # UDPブロードキャスト送信
    sock.close()                                        # ソケットの切断
