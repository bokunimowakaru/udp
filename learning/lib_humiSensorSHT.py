#!/usr/bin/env python3
# coding: utf-8

################################################################################
# 温湿度センサ SENSIRION SHT30 / SHT31 から温度と湿度を取得します。
#
#                                               Copyright (c) 2021 Wataru KUNINO
################################################################################

import smbus
from time import sleep

class HumiSensor:                                       # クラスHumiSensorの定義
    sht31 = 0x44                                        # 秋月=0x45,M5Stack=0x44
    try:                                                # 例外処理の監視を開始
        i2c = smbus.SMBus(1)                            # Iを開く
    except Exception as e:                              # 例外処理発生時
        raise Exception('SensorDeviceNotFound')         # 例外を応答
    def __init__(self):                                 # コンストラクタ作成
        self.temp = float()                             # 温度測定結果の保持用
        self.humi = float()                             # 湿度測定結果の保持用
    def word2uint(self,d1,d2):
        i = d1
        i <<= 8
        i += d2
        return i
    def get(self):                                      # 温度値取得用メソッド
        self.i2c.write_byte_data(self.sht31,0x24,0x00)
        sleep(0.018)
        data = self.i2c.read_i2c_block_data(self.sht31,0x00,6)
        if len(data) >= 5:
            i = self.word2uint(data[0],data[1])
            self.temp = float(i) / 65535. * 175. - 45.
            i = self.word2uint(data[3],data[4])
            self.humi  = float(i) / 65535. * 100.
        return (self.temp, self.humi)                   # 測定結果を応答
    def __del__(self):                                  # インスタンスの削除
        self.i2c.close()                                # ファイルを閉じる
