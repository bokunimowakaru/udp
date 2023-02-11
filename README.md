# udp: Sensor Data Transmission Format named "UDPxCSV" (UDP times CSV)

UDP Beacon (advertising) Transmitter and Receiver Examples for IoT Application.  

## About "UDPxCSV" (UDP times CSV)

This is a simple transmission format for sensor systems which I authored for "トランジスタ技術2016年9月号 (CQ出版社)".  
It has defined 5 bytes device name, 1 byte separator '_', 1 byte identification number, 1 byte comma for the separated code, CSV payload, and LF code.  


Fig. Sensor Data Transmission Format:  

|Sensor (bytes)  |Device Name (5)  |Separator (1)|ID Number (1)|Separator (1)|Payload (variable)  |Line Feed (1)|
|----------------|-----------------|-------------|-------------|-------------|--------------------|-------------|
|e.g. Humidity   | H u m i d       | _           | 1 (1~9)     | ,           | 2 7 . 0 ,   7 5 . 0| \n          |
|e.g. Temperature| t e m p .       | _           | 1 (1~9)     | ,           | 2 7 . 0            | \n          |
|e.g. PIR        | p i r _ s       | _           | 1 (1~9)     | ,           | 1 , 1              | \n          |

![Sensor Data Transmission Format](https://bokunimo.net/blog/wp-content/uploads/2022/06/csv.jpg)

## Contents for "UDPxCSV" (UDP times CSV)

* learning: Contents for Raspberry Pi  
* udp_monitor: Monitoring Sensor Application example for "UDPxCSV"  
* udp_logger.py: Testing Tool for "UDPxCSV"  

### Learning Contents for Raspberry Pi

There are example codes for learning "UDPxCSV" written in Python.  
[https://github.com/bokunimowakaru/udp/tree/master/learning](https://github.com/bokunimowakaru/udp/tree/master/learning)

### Monitoring Sensor Application example

I developed a monitoring tool which displays sensor values and their bar graphs on a web browser.  
The figure below shows recieved results from 32 sensor devices in my home.  

![udp_monitor](https://bokunimo.net/blog/wp-content/uploads/2022/02/udp-768x406.jpg)

[https://github.com/bokunimowakaru/udp/tree/master/udp_monitor](https://github.com/bokunimowakaru/udp/tree/master/udp_monitor)

### udp_logger.py

There are some simple monitoring tools in root directory of this repository "udp":  

* udp_logger_basic.py
* udp_logger.py
* udp_logger.sh

[https://github.com/bokunimowakaru/udp/](https://github.com/bokunimowakaru/udp/)

## Troubleshooting

### Trouble of Recieving UDPxCSV

If you cannot receive UDP, please check the following possible causes.

* Network Connection Error
* IP Address Setting Error
* Malfunction of Packet Discard Function

Packet Discard Function may occur due to the malfunction of the network equipment's security function, isolation function, loop prevention function, or following Malfunction of Packet Discard Function:

As the unidirectional UDP communication, a bridge function of network equipment may mistakenly recognize it as an unnecessary packet and discard it.  
In this case, it can be repaired by repeated works of two-way communication, using Ping is one of the solutions; please input Ping command like "ping 192.168.1.XX⏎" on the LXTerminal.
Or reboot your gateway, wireless access point, or switching hub. If you restart only a device that does not include a DHCP server, you need to run two-way communication such as ping after restarting.  
After repaired, if it continues only one-way communication continues, the bridge function will discard packets again. It needs some apps usinig two-way communication on a regular basis.  


## GitHub Pages (This Document)

* [https://git.bokunimo.com/udp/](https://git.bokunimo.com/udp/)

by <https://bokunimo.net>


