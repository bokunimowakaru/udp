#!/usr/bin/env python3
# coding: utf-8

# UDPを受信し、受信時刻と紐づけてセンサ名毎に保存する
# Copyright (c) 2021 Wataru KUNINO

# UDPの待ち受けと、受信した文字列の表示を繰り返します。
# ex2_rx.pyとの違いは、一度、実行すると繰り返し動作し続ける点と、
# 受信時刻と紐づけてセンサ名毎にデータを保存する点です。
# ./ex4_rx_log

import socket                                               # ソケットの組み込み
import datetime                                             # 日時管理の組み込み

def save(filename, data):                                   # 関数(ファイル保存)
    try:                                                    # 例外処理の監視
        fp = open(filename, mode='a')                       # 書込ファイルを開く
    except Exception as e:                                  # 例外処理発生時
        print(e)                                            # エラー内容を表示
    fp.write(data + '\n')                                   # dataをファイルへ
    fp.close()                                              # ファイルを閉じる

port = 1024                                                 # ポート番号を代入
sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)       # ソケットを作成
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)   # オプション設定
print('Listening UDP port', port, '...')                    # ポート番号表示

sock.bind(('', port))                                       # ポート番号を設定
while True:                                                 # 繰り返し構文
    udp = sock.recvfrom(128)                                # UDPパケットを取得
    s=''                                                    # 文字列変数sを生成
    for b in udp[0]:                                        # UDPパケット内
        if b > ord(' ') and b <= ord('~'):                  # 表示可能文字
            s += chr(b)                                     # 文字列sへ追加
    if s[5] != '_' or s[7] != ',' or len(s) < 9:            # 形式が一致しない時
        continue                                            # whileの先頭に戻る
    dev = s[0:7]                                            # デバイス名をdevに
    csv = s[8:]                                             # データをcsvに代入
    date = datetime.datetime.today()                        # 日付を取得
    date = date.strftime('%Y/%m/%d %H:%M')                  # 日付を文字列に変更
    output_str = date + ', ' + dev + ', ' + csv             # 日付とデータを結合
    print(output_str)                                       # 結合データを表示
    save('log_all.csv', output_str)                         # 単一ファイルに保存
    save('log_' + dev + '.csv', output_str)                 # 機器毎に保存
sock.close()                                                # 切断(実行されない)

'''
Listening UDP port 1024 ...
2021/10/16 13:16, temp._3, 24.5
2021/10/16 13:16, temp._3, 25.0
2021/10/16 13:17, temp._3, 24.5
2021/10/16 13:17, temp._3, 25.5
'''
