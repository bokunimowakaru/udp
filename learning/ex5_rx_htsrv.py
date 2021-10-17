#!/usr/bin/env python3
# coding: utf-8

# UDPを受信し、センサ値をHTTPサーバでLAN内に情報共有する
# Copyright (c) 2021 Wataru KUNINO

# ./ex5_rx_htsrv.py

import socket                                               # ソケットの組み込み
import datetime                                             # 日時管理の組み込み
from wsgiref.simple_server import make_server               # HTTPサーバ組み込み
import threading                                            # スレッドを組み込む

def wsgi_app(environ, start_response):                      # (関数)HTTP受信処理
    path  = environ.get('PATH_INFO')                        # リクエストのパスが
    if path != '/':                                         # ルート以外のとき
        start_response('404 Not Found',[])                  # 404エラー設定
        return ['404 Not Foundt\r\n'.encode()]              # 応答メッセージ返却
    html = '<html>\n<head>\n'                               # HTMLコンテンツ
    html += '<meta http-equiv="refresh" content="10;URL=/">\n' # 自動更新
    html += '</head>\n<body>\n'                             # HTML本文
    global output_dict                                      # CSVデータ読み込み
    if len(output_dict) == 0:                               # データ件数が0の時
        html += 'データ受信待ち<br>\n'                      # '受信待ち'を追記
    else:                                                   # 1件以上の時
        for dev in output_dict:                             # デバイス名毎に
            html += output_dict[dev] + '<br>\n'             # データを追記
    html += '</body>\n</html>\n'                            # htmlの終了
    start_response('200 OK', [('Content-type', 'text/html; charset=utf-8')])
    return [html.encode('utf-8')]                           # 応答メッセージ返却

def httpd():                                                # (関数)HTTPサーバ
    htserv = make_server('', 8080,wsgi_app)                 # サーバ実体化
    try:                                                    # 例外処理の監視
        htserv.serve_forever()                              # HTTPサーバを起動
    except KeyboardInterrupt as e:                          # キー割り込み発生時
        raise e                                             # 例外を発生

output_dict = dict()                                        # CSVデータ保存用
thread = threading.Thread(target=httpd, daemon=True)        # httpdの実体化
thread.start()                                              # httpdの起動

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
    output_dict[dev] = output_str                           # データの更新

'''
Listening UDP port 1024 ...
2021/10/16 14:55, temp._1, 25.5
192.168.1.3 - - [16/Oct/2021 14:55:05] "GET / HTTP/1.1" 200 124
192.168.1.3 - - [16/Oct/2021 14:55:05] "GET /favicon.ico HTTP/1.1" 404 16
2021/10/16 14:55, temp._1, 26.0
192.168.1.3 - - [16/Oct/2021 14:55:15] "GET / HTTP/1.1" 200 124
2021/10/16 14:55, temp._1, 25.0
192.168.1.3 - - [16/Oct/2021 14:55:26] "GET / HTTP/1.1" 200 124
2021/10/16 14:55, temp._1, 25.5
192.168.1.3 - - [16/Oct/2021 14:55:36] "GET / HTTP/1.1" 200 124
'''
