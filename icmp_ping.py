#!/usr/bin/env python3
# coding: utf-8
# ICMPを送信する
# Copyright (c) 2023 Wataru KUNINO

# ICMPを送信します。
# sudo ./icmp_ping.py

# 第1引数は宛先IPアドレスです。
# sudo ./icmp_ping.py 127.0.0.1

# 第2引数以降は送信データです。
# sudo ./icmp_ping.py 127.0.0.1 data1 data2...

import sys
import socket

adr = '127.0.0.1'
icm_type = b'\x08'      # header[0] Type = echo message
icm_code = b'\x00'      # header[1] Code
icm_csum = b'\x00\x00'  # header[2:4] Checksum
icm_idnt = b'\x00\x04'  # header[4:6] Identifier
icm_snum = b'\x00\x01'  # header[6:8] Sequence Number

def checksum(payload):
    if len(payload)%2 == 1:
        payload += b'\x00'  # total length is odd, padded with one octet of zeros
    sum = 0x0000
    for i in range(len(payload)//2):    #  1 の補数和
        sum += int(payload[i*2]) * 256
        sum += int(payload[i*2+1])
        if sum > 0xFFFF:
            sum += 1
            sum &= 0xFFFF
    payload[2] = ~(sum >> 8) & 0xFF
    payload[3] = ~(sum) & 0xFF
    return payload

argc = len(sys.argv)                                    # 引数の数をargcへ代入
print('ICMP Sender')                                    # タイトル表示
print('Usage: sudo',sys.argv[0],'ip_address [data...]') # 使用方法
if argc >= 2:                                           # 入力パラメータ数の確認
    adr = sys.argv[1]                                   # IPアドレスを設定
body = ''
if argc >= 3:
    for word in sys.argv[2:]:
        if len(body) > 0:
            body += ' '
        body += word

print('send Ping "'+body+'" to',adr)

header = bytearray(icm_type + icm_code + icm_csum + icm_idnt + icm_snum)
payload = bytearray(header + body.encode())
payload = checksum(payload)

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
except Exception as e:                                  # 例外処理発生時
    print(e)                                            # エラー内容を表示
    exit()                                              # プログラムの終了
if sock:                                                # 作成に成功したとき
    print('TX('+'{:02x}'.format(len(payload))+')',end=': ')
    for c in payload:
        print('{:02x}'.format(c), end=' ')             # 受信データを表示
    print()
    sock.sendto(payload,(adr,0))       # Ping送信
    sock.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1) #
    sock.settimeout(1)
    while sock:
        try:
            icmp = sock.recv(256)                                        # 受信データの取得
        except socket.timeout:
            break
        if icmp[3] == len(icmp):
            print('RX('+'{:02x}'.format(len(icmp))+')',end=': ')
            for i in range(len(icmp)-len(payload),len(icmp)):
                print('{:02x}'.format(icmp[i]), end=' ')               # 受信データを表示
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
# 参考文献 INTERNET CONTROL MESSAGE PROTOCOL (IETF RFC)
'''
    https://www.rfc-editor.org/rfc/rfc792


Echo or Echo Reply Message

    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |     Type      |     Code      |          Checksum             |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |           Identifier          |        Sequence Number        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |     Data ...
   +-+-+-+-+-

   IP Fields:

   Addresses

      The address of the source in an echo message will be the
      destination of the echo reply message.  To form an echo reply
      message, the source and destination addresses are simply reversed,
      the type code changed to 0, and the checksum recomputed.

   IP Fields:

   Type

      8 for echo message;

      0 for echo reply message.

   Code

      0

   Checksum

      The checksum is the 16-bit ones's complement of the one's
      complement sum of the ICMP message starting with the ICMP Type.
      For computing the checksum , the checksum field should be zero.
      If the total length is odd, the received data is padded with one
      octet of zeros for computing the checksum.  This checksum may be
      replaced in the future.

   Identifier

      If code = 0, an identifier to aid in matching echos and replies,
      may be zero.

   Sequence Number

      If code = 0, a sequence number to aid in matching echos and
      replies, may be zero.

   Description

      The data received in the echo message must be returned in the echo
      reply message.

      The identifier and sequence number may be used by the echo sender
      to aid in matching the replies with the echo requests.  For
      example, the identifier might be used like a port in TCP or UDP to
      identify a session, and the sequence number might be incremented
      on each echo request sent.  The echoer returns these same values
      in the echo reply.

      Code 0 may be received from a gateway or a host.
'''
###############################################################################
# 参考文献 python raw socket: Protocol not supported (stackoverflow)
'''
    https://stackoverflow.com/questions/19732145/python-raw-socket-protocol-not-supported
'''
