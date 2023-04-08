# udp: Sensor Data Transmission Format named "CSVxUDP" (CSV Cross UDP)

UDP Beacon (advertising) Transmitter and Receiver Examples for IoT Sensor Application.  

## Language

Select language to transrate this page:

* [Japanese(日本語)](https://translate.google.com/website?sl=en&tl=ja&hl&u=https://git.bokunimo.com/udp/)
* [English(英語)](https://git.bokunimo.com/udp/)

## About "CSVxUDP" (CSV Cross UDP)

CSVxUDP is a simple transmission format for sensor systems which I authored for "トランジスタ技術 2016年 9月号 CQ出版社".  
It is structed by the following format defined 5 bytes device name; 1 byte separator '_', 1 byte identification number, 1 byte comma for the separated code, CSV payload, and LF code.  

Fig. Sensor Data Transmission Format (bytes):  

|Sensor     |Device Name (5)  |Separator (1)|ID Number (1)|Separator (1)|Payload (variable)  |Line Feed (1)|
|-----------|-----------------|-------------|-------------|-------------|--------------------|-------------|
|Humidity   | H u m i d       | _           | 1 (1~9)     | ,           | 2 7 . 0 ,   7 5 . 0| \n          |
|Temperature| t e m p .       | _           | 1 (1~9)     | ,           | 2 7 . 0            | \n          |
|PIR        | p i r _ s       | _           | 1 (1~9)     | ,           | 1 , 1              | \n          |

![Sensor Data Transmission Format](https://bokunimo.net/blog/wp-content/uploads/2022/06/csv.jpg)

## Contents in this Repository

Python code examples of "CSVxUDP" (CSV Cross UDP) for Raspberry Pi:  

* learning: Contents for Raspberry Pi  
* udp_monitor: Monitoring Sensor Application example for "CSVxUDP"  
* udp_logger.py: Testing Tool for "CSVxUDP"  

### Learning Contents for Raspberry Pi

There are example codes for learning "CSVxUDP" written in Python:  
[https://github.com/bokunimowakaru/udp/tree/master/learning](https://github.com/bokunimowakaru/udp/tree/master/learning)

### Monitoring Sensor Application example

I developed a monitoring tool which displays sensor values and their bar graphs on a web browser.  
The figure below shows recieved results from 32 sensor devices in my home.  

![udp_monitor](https://bokunimo.net/blog/wp-content/uploads/2022/02/udp-768x406.jpg)

[https://github.com/bokunimowakaru/udp/tree/master/udp_monitor](https://github.com/bokunimowakaru/udp/tree/master/udp_monitor)

### udp_logger.py

There are some simple monitoring tools in the root directory of this repository "udp":  

* udp_logger_basic.py
* udp_logger.py
* udp_logger.sh

[https://github.com/bokunimowakaru/udp/](https://github.com/bokunimowakaru/udp/)

## Sensor Transmitters for CSVxUDP

The above picture shows Humidity Sensor which structed by Rasberry Pi, M5 ENV II or III sensor,
and Python code [ex3_tx_humi.py](https://github.com/bokunimowakaru/udp/blob/master/learning/ex3_tx_humi.py) in learning direcrory.  

![Humidity Sensor for Raspberry Pi](https://raw.githubusercontent.com/bokunimowakaru/udp/master/learning/humid_sesnor.jpg)

On the next picture, there are ESP8266 and a humidity sensor AE-SHT31 on a breadbord,
and the power is supplied 3 x AA alkaline batteries for it.

![Humidity Sensor](https://bokunimo.net/blog/wp-content/uploads/yahoo/blog_import_5c796d4c214c7.jpg)

### Links in English (Google Transrater)

Web sites about CSVxUDP sensors:
* [ボクにもわかる IoTモジュール ESP-WROOM-02 ESP32-WROOM-32](https://translate.google.com/website?sl=ja&tl=en&hl&u=https://git.bokunimo.com/esp/)
* [IoT Sensor Core for Ambient](https://translate.google.com/website?sl=ja&tl=en&hl&u=https://bokunimo.net/ambient/)

Books written in Japanese:
* [Pythonで作るIoTシステム プログラム・サンプル集 in Japanese](https://translate.google.com/website?sl=ja&tl=en&hl&u=https://amzn.to/3ls4Vx4)
* [超特急Web接続!ESPマイコン・プログラム全集 in Japanese](https://translate.google.com/website?sl=ja&tl=en&hl&u=https://amzn.to/3JWq78I)

### Links in 日本語サイト
* [ボクにもわかる IoTモジュール ESP-WROOM-02 ESP32-WROOM-32](https://git.bokunimo.com/esp/)
* [IoT Sensor Core for Ambient](https://bokunimo.net/ambient/)
* [Pythonで作るIoTシステム プログラム・サンプル集](https://amzn.to/3ls4Vx4)
* [超特急Web接続!ESPマイコン・プログラム全集](https://amzn.to/3JWq78I)

## Troubleshooting

### Problems Recieving CSVxUDP Packets

If you cannot receive UDP Packets, please check the following possible causes.

* Network Connection Error
* IP Address Setting Error
* Security Setting such as AP Isolation
* Broadcasting Problems
* Malfunction of Packet Discard Function

#### Network Connection Error  

Please check the network cables or Wi-Fi settings of the SSID and the password.  

#### IP Address Setting Error  

Plase check the DHCP server function on the router is enabled.  

#### AP Isolation Function  

If the devices are on your Wi-Fi LAN which structed by the router with the AP Isolation function, the pachet might not reach via the router. Please turn off the function, if the Wi-Fi LAN is not shared with other users.  
Note: AP Isolation Function separates the paccet transportation between the terminal devices in the router, but it pass the devices to WAN via the router.  

#### Broadcasting Problems

Also some Wi-Fi routers discard broadcasted packets between the tarminals. In the case, please turn off the filter on the router, or swich the broadcast IP address '255.255.255.255' to the unicast such as '192.168.1.XX'.  

#### Packet Discard Function  

Packet Discard Function may occur due to the malfunction of the network equipment's security function, isolation function, loop prevention function, or following Malfunction of Packet Discard Function:

As the unidirectional UDP communication, a bridge function of network equipments may mistakenly recognize it, as an unnecessary packet and discard it.  
In this case, it can be repaired by repeated works of two-way communication, using Ping is one of the solutions. So, please input Ping command like "ping 192.168.1.XX⏎" on the LXTerminal.
Or reboot your gateway, wireless access point, or switching hub. If you restart only a device that does not include a DHCP server, you need to run two-way communication such as ping after restarting.  
After repaired, if it continues only one-way communication continues, the bridge function will discard packets again. It needs some apps usinig two-way communication on a regular basis.  

## (Misc.) ICMP Ping

This repository also contains some ICMP Ping examples for leaning the protocol about it.  

* icmp_ping.py
* icmp_logger.py
* icmp_sender.py

These files are needed the super user privileges.  So, please add a "sudo" command to the beginning of these files to run.  

	pi@raspberry:~/udp $ sudo ./icmp_ping.py  
	ICMP Ping Sender Reciever  
	Usage: sudo ./icmp_ping.py [ip_address] [data...]  
	send Ping to 127.0.0.1  
	ICMP TX(08) : 08 00 93 c0 e5 b9 7e 85  
	ICMP RX(08) : 00 00 9b c0 e5 b9 7e 85  
	IP Version  = v4  
	IP Header   = 20  
	IP Length   = 28  
	Protocol    = 0x01  
	Source      = 127.0.0.1  
	Destination = 127.0.0.1  
	ICMP Length = 8  
	ICMP Type   = 00  
	ICMP Code   = 00  
	Checksum    = Passed  
	Identifier  = e5b9  
	Sequence N  = 7e85  

## GitHub Pages (This Document)

* [https://git.bokunimo.com/udp/](https://git.bokunimo.com/udp/)

by <https://bokunimo.net>


