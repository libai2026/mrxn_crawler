---
title: "虚拟机下centos不能自动获取ip地址解决办法"
source: https://mrxn.net/jswz/VMware-DHCP-ip.html
asset_dir: embedded-base64
---

刚刚的密码忘记了解决了，可是又出现问题了，不能联网，自动获取ip。。。。

虚拟机VM下安装装centos系统刚开始的时候还能自动获取到IP地址，突然有一天IP消失了，再怎么重启都无法获取IP地址。因为之前是可以获取IP，而且 VMware NAT Service 和 VMware DHCP Service 两个已启动，没做任何的改动，所以配置肯定是没问题的。

后来检查Edit--Virtual Network Editor...，进去以后看到VMnet0 Bridged Auto-bridging - - - ，点选VMnet0，在VMnet Information里面，点击“Bridged to: ”后面的“Automatic”下拉菜单，发现有两个网卡，一个是VPN的，一个物理网卡。果断将“Automatic”更换为物理网卡，重新启动Centos系统，久违的IP回来了。

注意：这里使用的物理网卡连接的网络是自动分配IP的。

CentOS配置网卡开机自动获取IP地址：

vi /etc/sysconfig/network-scripts/ifcfg-eth0

将 ONBOOT="no" 改为 ONBOOT="yes"

保存后： service network restart

查看IP： ifconfig

深入探索

编程

软件

防病毒程序与恶意软件

遇到同样CentOS配置网卡开机不能自动获取IP地址问题的朋友可以试下这个办法来解决。
