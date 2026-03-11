---
title: "CentOS下安装netspeeder加速"
source: https://mrxn.net/jswz/net-speeder-vsp.html
asset_dir: assets/centos下安装netspeeder加速
---

# CentOS下安装netspeeder加速

[Mrxn](https://mrxn.net/author/1)- 发表于2015/10/18 22:47
- 36220浏览
- [7评论](#comment)
- 27分钟阅读

深入探索

在线安全工具

数据库

漏洞修复方案

---

1、作者项目主页，~~https://code.google.com/p/net-speeder/~~

已经迁移到github了：<https://github.com/snooda/net-speeder> （作者主页也有教程）

安装步骤如下：

Linux 与 Unix

安装[脚本](#)

获得安装包： wget http://[linux](#).linzhihao.cn/shell/netspeeder.sh

运行安装包：sh netspeeder.sh

然后再看看进程，如果能找到net\_speeder ，说明它正在运行，安装就成功了

使用方法(需要root权限启动）：

参数：./net\_speeder 网卡名 加速规则（bpf规则）

最简单用法： # ./net\_speeder venet0 "ip" 加速所有ip协议数据

关闭net\_speeder方法：killall net\_speeder

2、net-speeder是一个由snooda.com博主写的[Linux](#)脚本程序，主要目的是为了解决丢包问题，实现TCP双倍发送，即同一份数据包发送两份。这样的话在服务器带宽充足情况下，丢包率会平方级降低。

3、net-speeder对于不加速就可以跑满带宽的类型来讲（多线程下载），开启后反而由于多出来的无效流量，导致速度减半，性能开销稍大和自由度有损失。所以，如果你的VPS连接国内速度一切正常，请不要启用net-speeder。

操作系统

深入探索

Web安全书籍

漏洞预警服务

Windows安全工具

4、安装net-speeder的方法也很简单，这里提供由lazyzhu.com博主写的net-speeder一键安装包。执行以下命令：

```
 wget --no-check-certificate https://gist.github.com/LazyZhu/dc3f2f84c336a08fd6a5/raw/d8aa4bcf955409e28a262ccf52921a65fe49da99/net_speeder_lazyinstall.sh
sh net_speeder_lazyinstall.sh
```

[[![CentOS下安装netspeeder加速](images/img-001-724c3ddf3079.gif "点击查看原图")](https://mrxn.net/content/uploadfile/201510/52061445183476.gif)](https://mrxn.net/content/uploadfile/201510/52061445183476.gif)

深入探索

网络安全课程

安全工具开发

服务器安全服务

5、日后如果一键安装[脚本](#)下载链接失效了，这里给出脚本的具体内容，大家可以将将它保存为.sh文件，然后就可以执行了。

软件

```
#!/bin/sh

# Set Linux PATH Environment Variables
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

# Check If You Are Root
if [ $(id -u) != "0" ]; then
    clear
    echo -e "\033[31m Error: You must be root to run this script! \033[0m"
    exit 1
fi

if [ $(arch) == x86_64 ]; then
    OSB=x86_64
elif [ $(arch) == i686 ]; then
    OSB=i386
else
    echo "\033[31m Error: Unable to Determine OS Bit. \033[0m"
    exit 1
fi
if egrep -q "5.*" /etc/issue; then
    OST=5
    wget http://dl.fedoraproject.org/pub/epel/5/${OSB}/epel-release-5-4.noarch.rpm
elif egrep -q "6.*" /etc/issue; then
    OST=6
    wget http://dl.fedoraproject.org/pub/epel/6/${OSB}/epel-release-6-8.noarch.rpm
else
    echo "\033[31m Error: Unable to Determine OS Version. \033[0m"
    exit 1
fi

rpm -Uvh epel-release*rpm
yum install -y libnet libnet-devel libpcap libpcap-devel gcc

wget http://net-speeder.googlecode.com/files/net_speeder-v0.1.tar.gz -O -|tar xz
cd net_speeder
if [ -f /proc/user_beancounters ] || [ -d /proc/bc ]; then
    sh build.sh -DCOOKED
    INTERFACE=venet0
else
    sh build.sh
    INTERFACE=eth0
fi

NS_PATH=/usr/local/net_speeder
mkdir -p $NS_PATH
cp -Rf net_speeder $NS_PATH

echo -e "\033[36m net_speeder installed. \033[0m"
echo -e "\033[36m Usage: nohup ${NS_PATH}/net_speeder $INTERFACE \"ip\" >/dev/null 2>&1 & \033[0m"
```

5、安装完成后，会给出[脚本](#)用法，最简单的就是开启所有IP协议加速。执行以下命令：

```
nohup /usr/local/net_speeder/net_speeder venet0 "ip" >/dev/null 2>&1 &
```

6、net-speeder对于VPS速度有没有优化？就我自己的测试来看，速度和ping值都有所提升，但是流量也是双倍呀！所以对于流量吃紧的童鞋们来说，就别尝试了。。。当然，流量多的就无视。

脚本语言

- 标签：
- [#Linux](https://mrxn.net/tag/Linux)
- [#流量](https://mrxn.net/tag/%E6%B5%81%E9%87%8F)
- [#性能优化](https://mrxn.net/tag/%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96)
- [#vps](https://mrxn.net/tag/vps)
- [#运维](https://mrxn.net/tag/%E8%BF%90%E7%BB%B4)
- [#tcp](https://mrxn.net/tag/tcp)

---

文章目录

  
  

![](data:image/png;base64,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)

手机扫码阅读
