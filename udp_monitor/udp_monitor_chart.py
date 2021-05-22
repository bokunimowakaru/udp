#!/usr/bin/env python3
# coding: utf-8

################################################################################
# UDPで受信したIoTセンサ機器の値を棒グラフで表示します。
#
#                                               Copyright (c) 2021 Wataru KUNINO
################################################################################

# 初期設定
UDP_PORT = 1024             # UDP待ち受けポート番号(デフォルトは1024)
DEV_CHECK = False           # 未登録デバイス保存(True:破棄,False:UNKNOWNで保存)

# センサ機器用登録デバイス（UDPペイロードの先頭5文字）
sensors = [\
    'temp0','hall0','adcnv','btn_s','pir_s','illum',\
    'temp.','humid','press','envir','accem','rd_sw',\
    'press','e_co2',\
    'actap','awsin','count','esp32','ident','medal',\
    'meter','ocean','river','tftpc','timer','voice',\
    'xb_ac','xb_ct','xb_ev','xb_sw','xbbat','xbbel',\
    'xbgas','xbhum','xblcd','xbled','xbprs','xbrad',\
    'xbsen'\
]

# センサ機器用CSV形式データの項目（数値データ）
csvs = {\
    'pir_s':[('Wake up Switch',''),('PIR Switch','')],\
    'rd_sw':[('Wake up Switch',''),('Reed Switch','')],\
    'temp0':[('Temperature','deg C')],\
    'temp.':[('Temperature','deg C')],\
    'ocean':[('Temperature','deg C'),('RSSI','dBm')],\
    'humid':[('Temperature','deg C'),('Humidity','%')],\
    'press':[('Temperature','deg C'),('Pressure','hPa')],\
    'envir':[('Temperature','deg C'),('Humidity','%'),('Pressure','hPa')],\
    'e_co2':[('Temperature','deg C'),('Humidity','%'),('Pressure','hPa'),('CO2','ppm'),('TVOC','ppb'),('Counter','')],\
    #'accem':[('Accelerometer X','g'),('Accelerometer Y','g'),('Accelerometer Z','g')],\
    'accem':[('Accelerometer X','m/s2'),('Accelerometer Y','m/s2'),('Accelerometer Z','m/s2')],\
    'actap':[('Power','W'),('Cumulative','Wh'),('Time','Seconds')],\
    'meter':[('Power','W'),('Cumulative','Wh'),('Time','Seconds')],\
    'awsin':[('Participants',''),('Cumulative','')],\
    'xb_ac':[('Usage Time','h'),('Consumption','kWh'),('Prev. Usage Time','h'),('Consumption','kWh')],\
    'xb_ct':[('Power','W')],\
    'xb_ev':[('Illuminance','lx'),('Temperature','deg C'),('Humidity','%')],\
    'xb_sw':[('Reed Switch','')],\
    'xbbel':[('Ringing','')],\
    'xbgas':[('CO','ppm'),('CH4','ppm')],\
    'xbhum':[('Illuminance','lx'),('Temperature','deg C'),('Humidity','%')],\
    'xblcd':[('Illuminance','lx'),('Temperature','deg C')],\
    'xbled':[('Illuminance','lx'),('Temperature','deg C')],\
    'xbprs':[('Temperature','deg C'),('Pressure','hPa')],\
    'xbrad':[('Radiation','uSievert'),('Temperature','deg C'),('Voltage','V')],\
    'xbsen':[('Illuminance','lx'),('Temperature','deg C'),('Low Battery','')]\
}

# データ範囲
csvs_range = {\
    ('Wake up Switch',''):      (0,1),\
    ('PIR Switch',''):          (0,1),\
    ('Reed Switch',''):         (0,1),\
    ('Temperature','deg C'):    (0,40),\
    ('RSSI','dBm'):             (-100,0),\
    ('Humidity','%'):           (0,100),\
    ('Pressure','hPa'):         (1013.25 - 20, 1013.25 + 20),\
    ('CO','ppm'):               (0,2000),\
    ('CO2','ppm'):              (0,2000),\
    ('CH4','ppm'):              (0,2000),\
    ('TVOC','ppb'):             (0,5000),\
    ('Counter',''):             (0,10),\
    ('Accelerometer X','m/s2'): (-9.8,9.8),\
    ('Accelerometer Y','m/s2'): (-9.8,9.8),\
    ('Accelerometer Z','m/s2'): (-9.8,9.8),\
    ('Accelerometer X','g'):    (-1,1),\
    ('Accelerometer Y','g'):    (-1,1),\
    ('Accelerometer Z','g'):    (-1,1),\
    ('Power','W'):              (0,3000),\
    ('Cumulative','Wh'):        (0,3000),\
    ('Consumption','kWh'):      (0,3),\
    ('Time','Seconds'):         (0,3600),\
    ('Time','Hours'):           (0,8760),\
    ('Usage Time','h'):         (0,24),\
    ('Prev. Usage Time','h'):   (0,24),\
    ('Participants',''):        (0,100),\
    ('Cumulative',''):          (0,100000),\
    ('Illuminance','lx'):       (0,1000),\
    ('Ringing',''):             (0,1),\
    ('Radiation','uSievert'):   (0.04,0.23),\
    ('Voltage','V'):            (0,5),\
    ('Low Battery',''):         (0,1)\
}

# センサ機器以外（文字データ入り）の登録デバイス
notifyers = [\
    'adash','atalk','cam_a','ir_in','janke','sound',\
    'xb_ir','xbidt'\
]

# 特定文字列
pingpongs = [
    'Ping','Pong','Emergency','Reset'\
]

devices = list()
dev_vals = dict()

import os
import sys
import socket
import datetime
from wsgiref.simple_server import make_server       # WSGIサーバ
from getpass import getuser                         # ユーザ取得を組み込む
from time import time                               # 時間取得を組み込む
from time import sleep                              # スリープ機能を組み込む
import threading                                    # スレッド管理を組み込む

def get_dev_name(s):                                    # デバイス名を取得
    if s.strip() in pingpongs:                          # Ping または Pong
        return s.strip()
    if not s[0:8].isprintable():
        return None                                     # Noneを応答
    if s[5] == '_' and s[7] == ',':                     # 形式が一致する時
        if s[0:5] in sensors:                           # センサリストの照合
            return s[0:7]                               # デバイス名を応答
        if s[0:5] in notifyers:                         # センサリストの照合
            return s[0:7]                               # デバイス名を応答
    return None                                         # Noneを応答

def get_val(s):                                         # データを数値に変換
    s = s.replace(' ','')                               # 空白文字を削除
    try:                                                # 小数変換の例外監視
        val = float(s)                                  # 小数値に変換
    except ValueError:                                  # 小数変換失敗時
        return None                                     # Noneを応答
    if float(int(val)) == val:                          # valが整数のとき
        return int(val)                                 # 整数値を応答
    else:
        return val                                      # 小数値を応答

def save(filename, data):
    try:
        fp = open(filename, mode='a')                   # 書込用ファイルを開く
    except Exception as e:                              # 例外処理発生時
        print(e)                                        # エラー内容を表示
    fp.write(data + '\n')                               # dataをファイルへ
    fp.close()                                          # ファイルを閉じる

def barChartHtml(colmun, range, val, color='lightgreen'):    # 棒グラフHTMLを作成する関数
    html = '<td>' + colmun[0] + '(' + colmun[1] + ')</td>\n' # 棒グラフ名を表示
    html += '<td align="right">'+str(val)+'</td>\n' # 変数valの値を表示
    min = range[0]
    max = range[1]
    i= round(200 * (val - min) / (max - min))       # 棒グラフの長さを計算
    if val - min <= (max - min) * 0.2:              # 20％以下のとき
        color = 'lightblue'                         # 棒グラフの色を青に
    if val - min >= (max - min) * 0.8:              # 80％以上のとき
        color = 'lightpink'                         # 棒グラフの色をピンクに
    if val > max or val < min:                      # 最大値or最小値を超えた時
        color = 'red'                               # 棒グラフの色を赤に
        i = 200                                     # グラフ長を200ポイントに
    html += '<td><div style="background-color: ' + color
    html += '; width: ' + str(i) + 'px">&nbsp;</div></td>\n'
    return html                                     # HTMLデータを返却

def wsgi_app(environ, start_response):              # HTTPアクセス受信時の処理
    path  = environ.get('PATH_INFO')                # リクエスト先のパスを代入
    if path != '/':                                 # パスがルート以外のとき
        start_response('404 Not Found',[])          # 404エラー設定
        return ['404 Not Found'.encode()]           # 応答メッセージ(404)を返却
    html = '<html>\n<head>\n'                       # HTMLコンテンツを作成
    html += '<meta http-equiv="refresh" content="10;">\n'   # 自動再読み込み
    html += '</head>\n<body>\n'                     # 以下は本文
    html += '<table border=1>\n'                    # 作表を開始
    html += '<tr><th>デバイス名</th><th>項目</th><th width=50>値</th>' # 「項目」「値」を表示
    html += '<th width=200>グラフ</th>\n'           # 「グラフ」を表示
    for dev in devices:
        if dev[0:5] in sensors:
            colmuns = csvs.get(dev[0:5])
            if colmuns is None:
                print('[ERROR] founds no devices on csvs dictionary; dev =',dev[0:5])
                break
            i_max = min(len(colmuns), len(dev_vals[dev]))
            if dev[0:5] == 'actap':  # (筆者開発環境用の例外) 数が多いので電力のみを表示する
                i_max = 1
            for i in range(i_max):
                colmun = csvs[dev[0:5]][i]
                minmax = csvs_range.get(colmun)
                val = dev_vals[dev][i]
                if range is not None:
                    if i == 0:
                        html += '<tr><th rowspan = ' + str(i_max) + '>' + dev + '</th>'
                    else:
                        html += '<tr>'
                    html += barChartHtml(colmun, minmax, val)   # 棒グラフ化
    html += '</tr>\n</table>\n</body>\n</html>\n'   # 作表とhtmlの終了
    start_response('200 OK', [('Content-type', 'text/html; charset=utf-8')])
    return [html.encode('utf-8')]                   # 応答メッセージを返却

def httpd(port = 80):
    htserv = make_server('', port, wsgi_app)        # HTTPサーバ実体化
    print('HTTP port', port)                        # ポート番号を表示
    htserv.serve_forever()                          # HTTPサーバを起動

buf_n= 128                                          # 受信バッファ容量(バイト)
argc = len(sys.argv)                                # 引数の数をargcへ代入
print('UDP Logger (usage: '+sys.argv[0]+' port)')   # タイトル表示
if argc >= 2:                                       # 入力パラメータ数の確認
    port = int(sys.argv[1])                         # ポート番号を設定
    if port < 1 or port > 65535:                    # ポート1未満or65535超の時
        port = UDP_PORT                             # UDPポート番号を1024に
else:
    port = UDP_PORT
print('Listening UDP port', port, '...')            # ポート番号表示
try:
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)# ソケットを作成
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)    # オプション
    sock.bind(('', port))                           # ソケットに接続
except Exception as e:                              # 例外処理発生時
    print(e)                                        # エラー内容を表示
    exit()                                          # プログラムの終了

thread = threading.Thread(target=httpd, daemon=True)# スレッドhttpdの実体化
thread.start()                                      # スレッドhttpdの起動

while thread.is_alive and sock:                     # 永久ループ(httpd,udp動作中
    udp, udp_from = sock.recvfrom(buf_n)                # UDPパケットを取得
    try:
        udp = udp.decode()                              # UDPデータを文字列に変換
    except Exception as e:                              # 例外処理発生時
        print(e)                                        # エラー内容を表示
        continue                                        # whileの先頭に戻る
    if len(udp) <= 4:
        continue
    dev = get_dev_name(udp)                             # デバイス名を取得
    if dev is None:                                     # 不適合
        if DEV_CHECK:                                   # デバイス選別モード時
            continue                                    # whileに戻る
        dev = 'UNKNOWN'                                 # 不明デバイス

    vals = list()
    if len(udp) > 8:
        vals = udp[8:].strip().split(',')               # 「,」で分割
    date = datetime.datetime.today()                    # 日付を取得
    date = date.strftime('%Y/%m/%d %H:%M')              # 日付を文字列に変更
    s = ''                                              # 文字列変数
    if dev[0:5] in sensors:
        for val in vals:                                # データ回数の繰り返し
            i = get_val(val)                            # データを取得
            s += ', '                                   # 「,」を追加
            if i is not None:                           # データがある時
                s += str(i)                             # データを変数sに追加
    else:
        s = ', '                                        # 文字列変数
        for c in udp:                                   # UDPパケット内
            if ord(c) >= ord(' ') and ord(c) <= ord('~'):   # 表示可能文字
                s += c                                  # 文字列sへ追加
    filename = 'log_' + dev + '.csv'                    # ファイル名を作成
    if dev not in devices:
        print('NEW Device,',dev)
        devices.append(dev)
        if not os.path.exists(filename):
            fp = open(filename, mode='w')               # 書込用ファイルを開く
            fp.write('YYYY/MM/dd hh:mm, IP Address')    # CSV様式
            column = csvs.get(dev[0:5])
            if column is not None:
                for col in column:
                    if col[1] == '':
                        fp.write(', ' + col[0])
                    else:
                        fp.write(', ' + col[0] + '(' + col[1] + ')')
            fp.write('\n')
            fp.close()                                  # ファイルを閉じる
    print(date + ', ' + dev + ', ' + udp_from[0], end = '')  # 日付,送信元を表示
    print(s, '-> ' + filename, flush=True)              # 受信データを表示
    save(filename, date + ', ' + udp_from[0] + s)       # ファイルに保存

    # 数値データの変数保持(HTML表示用)
    if dev[0:5] in sensors:                             # センサ(数値データ)のとき
            # (len(vals)>0だと値なし時に辞書追加されないのでsensorsかどうかで判定)
        dev_vals[dev] = list()                          # 数値データを保持
        for val in vals:
            dev_vals[dev].append(get_val(val))          # 数値に変換して追加
            # Noneは除去しない。Noneも代入
sock.close()                                            # ソケットの切断
