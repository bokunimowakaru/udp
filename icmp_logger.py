#!/usr/bin/env python3
# coding: utf-8
# ICMP Ping を受信する(応答はしない)
# Copyright (c) 2023 Wataru KUNINO

# ICMPを受信します。
# sudo ./icmp_logger.py

import sys
import socket
import ipaddress

filter = True # True ：IPv4と、IPヘッダ長20バイト、ICMP、パケット長、チェックサムを確認する
              # False：チェックサムのみを確認する

def checksum_calc(payload):
    if len(payload)%2 == 1:
        payload += b'\x00'  # total length is odd, padded with one octet of zeros
    sum = 0x0000
    for i in range(len(payload)//2):    #  1 の補数和
        sum += int(payload[i*2]) * 256
        sum += int(payload[i*2+1])
        if sum > 0xFFFF:
            sum += 1
            sum &= 0xFFFF
    sum = ~(sum) & 0xFFFF
    return sum.to_bytes(2, 'big')

print('ICMP Logger')                                    # タイトル表示
print('Usage: sudo',sys.argv[0])                        # 使用方法

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
except PermissionError:                                 # 例外処理発生時
    print('PermissionError, 先頭に sudo を付与して実行してください')
    exit()                                              # プログラムの終了
if sock:                                                # 作成に成功したとき
    sock.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
    while sock:
        try:
            icmp = sock.recv(256)                                        # 受信データの取得
        except Exception as e:
            print(e)
        length = int(256 * icmp[2] + icmp[3])
        header_length = int((icmp[0]%16)*4)
        protocol = icmp[9]
        source_adr = int.from_bytes(icmp[12:16], 'big')
        source_adr_s = str(ipaddress.IPv4Address(source_adr))
        dest_adr = int.from_bytes(icmp[16:20], 'big')
        dest_adr_s = str(ipaddress.IPv4Address(dest_adr))
        if filter == False or (icmp[0] == 0x45 and protocol == 0x01 and length == len(icmp)):
            icmp_len = length - header_length
            identifier = int.from_bytes(icmp[24:26], 'big')
            sequence = int.from_bytes(icmp[26:28], 'big')
            check = not int.from_bytes(checksum_calc(icmp[20:]),'big')
            if check:
                # icmp[0] == 0x45: IPv4と、IPヘッダ長20バイトに限定
                print('ICMP RX('+'{:02x}'.format(icmp_len)+')',end=' : ')
                for i in range(20,28):
                    print('{:02x}'.format(icmp[i]), end=' ')               # 受信データを表示
                print()
                print('IP Version  =','v'+str(int(icmp[0]>>4)))
                print('IP Header   =',header_length)
                print('IP Length   =',length)
                print('Protocol    =','0x'+('{:02x}'.format(protocol)))
                print('Source      =',source_adr_s)
                print('Destination =',dest_adr_s)
                print('ICMP Length =',icmp_len)
                print('ICMP Type   =','{:02x}'.format(icmp[20]))
                print('ICMP Code   =','{:02x}'.format(icmp[21]))
                print('Checksum    =', 'Passed' if check else 'Failed')
                print('Identifier  =','{:04x}'.format(identifier))
                print('Sequence N  =','{:04x}'.format(sequence))
                if icmp_len > 8:
                    try:
                        body = icmp[28:].decode()
                    except UnicodeDecodeError:
                        body = '\n'
                    if body.isprintable():
                        print('ICMP Data   =',body)
                    else:
                        print('ICMP Data   = ',end='')
                        for i in range(28,len(icmp)):
                            print('{:02x}'.format(icmp[i]), end=' ')     # 受信データを表示
                            if (i-28) % 8 == 7:
                                print('\n', end='              ')
                        if (len(icmp) - 28)%8 != 0:
                            print()
                print()
    sock.close()                                                # ソケットの切断

###############################################################################
# 参考文献 RAWソケットを利用したpingコマンド (Geekなページ)
'''
    https://www.geekpage.jp/programming/linux-network/book/12/12-1.php
'''

###############################################################################
# 参考文献 TCP/IP - ICMPとは (ネットワークエンジニアとして)
'''
    https://www.infraexpert.com/study/tcpip4.html
'''

###############################################################################
# 参考文献 INTERNET CONTROL MESSAGE PROTOCOL (IETF RFC 792)
'''
    https://www.rfc-editor.org/rfc/rfc792
'''

###############################################################################
# 参考文献 INTERNET PROTOCOL (IETF RFC 791)
'''
    https://www.rfc-editor.org/rfc/rfc791
'''
###############################################################################
# 参考文献 python raw socket: Protocol not supported (stackoverflow)
'''
    https://stackoverflow.com/questions/19732145/python-raw-socket-protocol-not-supported
'''
