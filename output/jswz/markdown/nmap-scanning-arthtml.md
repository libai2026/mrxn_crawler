---
title: "Scanning is art - Nmap 扫描的艺术之常见的基本操作"
source: https://mrxn.net/jswz/Nmap-Scanning-Art.html
---

# Scanning is art - Nmap 扫描的艺术之常见的基本操作

[Mrxn](https://mrxn.net/author/1)* 发表于2019/4/6 14:49
* 3253浏览
* [2评论](#comment)
* 2小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

[![Scanning is art - Nmap 扫描的艺术之常见的基本操作](https://mrxn.net/content/uploadfile/201904/c6981554533443.jpg "Nmap")](https://mrxn.net/content/uploadfile/201904/c6981554533443.jpg)


  

**Nmap**
---

软件名字
**Nmap**
是
**Network Mapper**
的简称，是
[渗透测试](https://mrxn.net/tag/%E6%B8%97%E9%80%8F)
过程中必不可少的
[黑客工具](https://mrxn.net/tag/%E9%BB%91%E5%AE%A2%E5%B7%A5%E5%85%B7)
之一，其他的更多的介绍请前往官网：
<https://nmap.org/>



或者是维基百科查看：
<https://zh.wikipedia.org/wiki/Nmap>

。在
[渗透](https://mrxn.net/tag/%E6%B8%97%E9%80%8F)
测试中，如果我们在 WEB 应用层没有找到有用的信息，那么此时 Nmap 就派上用场了，利用它我们可以对单个目标主机或者是目标群进行
[扫描](https://mrxn.net/tag/%E6%89%AB%E6%8F%8F)
以此来获取基于 IP 的服务器主机信息，这也是信息刺探中的一部分，不过在实际
[渗透测试](https://mrxn.net/tag/%E6%B8%97%E9%80%8F)
中，如果我们在 WEB 应用层找打了可以利用的点并且可以进一步获得权限足够大的时候我们就可以暂时不需要使用 Nmap ，转而在后期需要提权或者是横向移动的

时候我们再使用它。这篇文章主要是将在使用 Nmap 的日常使用中的一些基本操作，还有些骚操作，暂时不多(主要是博主太菜了,哈哈哈哈,欢迎有骚姿势的朋友分享
  

下载地址：
<https://nmap.org/download.html>

  
Github 项目主页地址：
<https://github.com/nmap/nmap>

  
Nmap
[渗透测试](https://mrxn.net/tag/%E6%B8%97%E9%80%8F)
思维导图(高清大图)：
[我的 GitHub 仓库地址](https://raw.githubusercontent.com/Mr-xn/BurpSuite-collections/master/books/Nmap%E6%B8%97%E9%80%8F%E6%B5%8B%E8%AF%95%E6%80%9D%E7%BB%B4%E5%AF%BC%E5%9B%BE.png)
  
我4年前还搞过CHM的手册：
[Nmap手册](https://mrxn.net/free/176.html)

## 初识Nmap

Nmap是被专业人员广泛使用的一款功能全面的
[端口扫描](https://mrxn.net/tag/%E6%89%AB%E6%8F%8F)
工具。它由Fyodor编写并维护。由 于Nmap品质卓越，使用灵活，它已经是
[渗透](https://mrxn.net/tag/%E6%B8%97%E9%80%8F)
测试人员必备的工具。

除了端口
[扫描](https://mrxn.net/tag/%E6%89%AB%E6%8F%8F)
外，Nmap还具备如下功能：

```
主机探测：Nmap可査找目标网络中的在线主机。默认情况下，Nmap通过4种方式—— ICMP echo请求（ping）、向443端口发送TCP、SYN 包、向80端口发送TCP、ACK 包和 ICMP 时间戳请求——发现目标主机。  
服务/版本检测：在发现开放端口后，Nmap可进一步检查目标主机的检测服务协议、应用 程序名称、版本号等信息。  
操作系统检测：Nmap 向远程主机发送一系列数据包，并能够将远程主机的响应与操作系统 指纹数据库进行比较。如果发现了匹配结果，它就会显示匹配的操作系统。它确实可能无法 识别目标主机的操作系统；在这种情况下，如果您知道目标系统上使用的何种操作系统，可 在它提供的URL里提交有关信息，更新它的操作系统指纹数据库。   
网络路由跟踪：它通过多种协议访问目标主机的不同端口，以尽可能访问目标主机。Nmap 路由跟踪功能从TTL的高值开始测试，逐步递减TTL，直到它到零为止。  
Nmap脚本引擎：这个功能扩充了Nmap的用途。如果您要使用Nmap实现它（在默认情况 下）没有的检测功能，可利用它的脚本引擎手写一个检测脚本。目前，Nmap可检査网络服务 的漏洞，还可以枚举目标系统的资源。
```

## 安装Nmap

nmap的安装很简单，Windows的话直接去官网下载安装包直接安装就行了->
[下载链接](https://nmap.org/download.html)

kali已经自带了nmap，centos如果没有安装的话，
`yum install nmap`

就直接安装了

## 入门Nmap

刚开始使用的时候可能会因为信息量太大无从下手，最简单的使用就是
`nmap your-ip（域名）`

就可以
[扫描](https://mrxn.net/tag/%E6%89%AB%E6%8F%8F)
出其对外开放的服务。

```
root@kali:~# nmap 192.168.31.13
Starting Nmap 7.70 ( https://nmap.org ) at 2018-08-12 23:02 CST
Nmap scan report for 192.168.31.13
Host is up (0.00038s latency).
Not shown: 998 closed ports
PORT      STATE SERVICE
8080/tcp  open  http-proxy
10010/tcp open  rxapi
MAC Address: 00:0C:29:99:D3:E6 (VMware)

Nmap done: 1 IP address (1 host up) scanned in 1.85 seconds
```

|  |
| --- |
|  |

可以看出只开放了8080端口和10010端口

nmap -p 端口 IP(域名)，判断ip是否开放指定端口

|  |
| --- |
| ``` ``` root@kali:~# nmap -p 8080 192.168.31.13 Starting Nmap 7.70 ( https://nmap.org ) at 2018-08-12 23:05 CST Nmap scan report for 192.168.31.13 Host is up (0.00045s latency).  PORT     STATE SERVICE 8080/tcp open  http-proxy MAC Address: 00:0C:29:99:D3:E6 (VMware)  Nmap done: 1 IP address (1 host up) scanned in 0.36 seconds ```    ``` root@kali:~# nmap -p 80 192.168.31.13 Starting Nmap 7.70 ( https://nmap.org ) at 2018-08-12 23:05 CST Nmap scan report for 192.168.31.13 Host is up (0.00049s latency).  PORT   STATE  SERVICE 80/tcp closed http MAC Address: 00:0C:29:99:D3:E6 (VMware)  Nmap done: 1 IP address (1 host up) scanned in 0.42 seconds ``` ``` |

可以看出8080端口开放，80端口没有开放

也可以增加端口和网段 ：

```
nmap  -p 22,21,80 192.168.31.13

nmap  -p 22,21,80 192.168.31.1-253
```

|  |
| --- |
|  |

nmap 192.168.31.1/24
[扫描](https://mrxn.net/tag/%E6%89%AB%E6%8F%8F)
整个子网(整个C段)的端口 ，这个过程可能会比较久

## 进阶Nmap

在继续讲之前，先介绍一下Nmap可以识别出的6种端口状态，默认情况下，Nmap会
[扫描](https://mrxn.net/tag/%E6%89%AB%E6%8F%8F)
1660个常用的端口，可以覆盖大多数基本应用情况。

```
开放（Open）：工作于开放端口的服务器端的应用程序可以受理TCP    连接、接收UDP数据包或者响 应SCTP（流控制传输协议）请求。

关闭（Closed）：虽然我们确实可以访问有关的端口，但是没有应用程序工作于该端口上。

过滤（Filtered）：Nmap不能确定该端口是否开放。包过滤设备屏蔽了我们向目标发送的探测包。

未过滤（Unfiltered）：虽然可以访问到指定端口，但Nmap不能确定该端口是否处于开放状态。 

开放｜过滤（Open|Filtered）：Nmap认为指定端口处于开放状态或过滤状态，但是不能确定处于两者之中的 哪种状态。在遇到没有响应的开放端口时，Nmap会作出这种判断。这可以是由于防火墙丢 弃数据包造成的。

关闭｜过滤（Closed|Filtered）：Nmap 认为指定端口处于关闭状态或过滤状态，但是不能确定处于两者之中的 哪种状态。
```

  

### 常用选项

1.服务版本识别（-sV），Nmap可以在进行端口
[扫描](https://mrxn.net/tag/%E6%89%AB%E6%8F%8F)
的时候检测服务端软件的版本信息。版本信息将使后续的漏 洞识别工作更有针对性。

```
root@kali:~# nmap -sV 192.168.31.13 -p 8080
Starting Nmap 7.70 ( https://nmap.org ) at 2018-08-13 00:02 CST
Nmap scan report for 192.168.31.13
Host is up (0.00076s latency).

PORT     STATE SERVICE VERSION
8080/tcp open  http    Apache Tomcat 8.5.14
MAC Address: 00:0C:29:99:D3:E6 (VMware)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.75 seconds
```

  

2.操作系统检测（-O），Nmap还能识别目标主机的操作系统。

```
root@kali:~# nmap -O 192.168.31.13 
Starting Nmap 7.70 ( https://nmap.org ) at 2018-08-13 00:03 CST
Nmap scan report for 192.168.31.13
Host is up (0.00072s latency).
Not shown: 998 closed ports
PORT      STATE SERVICE
8080/tcp  open  http-proxy
10010/tcp open  rxapi
MAC Address: 00:0C:29:99:D3:E6 (VMware)
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.2 - 4.9
Network Distance: 1 hop

OS detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 3.49 seconds
```

  

3.禁用主机检测（-Pn），如果主机屏蔽了ping请求，Nmap可能会认为该主机没有开机。这将使得Nmap无法进行进一 步检测，比如端口
[扫描](https://mrxn.net/tag/%E6%89%AB%E6%8F%8F)
、服务版本识别和操作系统识别等探测工作。为了克服这一问题，就 需要禁用Nmap的主机检测功能。在指定这个选项之后，Nmap会认为目标主机已经开机并会 进行全套的检测工作

4.强力检测选项（-A），启用-A选项之后，Nmap将检测目标主机的下述信息
  

服务版本识别（-sV）；
  

操作系统识别（-O）；
  

脚本扫描（-sC）；
  

Traceroute（–traceroute）。

### TCP扫描选项

1.TCP连接扫描（-sT）：指定这个选项后，程序将和目标主机的每个端口都进行完整的三次 握手。如果成功建立连接，则判定该端口是开放端口。由于在检测每个端口时都需要进行三 次握手，所以这种扫描方式比较慢，而且扫描行为很可能被目标主机记录下来。如果启动 Nmap的用户的权限不足，那么默认情况下Nmap程序将以这种模式进行扫描。

2.SYN扫描（-sS）：该选项也称为半开连接或者SYN stealth。采用该选项后，Nmap将使用 含有SYN标志位的数据包进行端口探测。如果目标主机回复了SYN/ACK包，则说明该端口处 于开放状态：如果回复的是RST/ACK包，则说明这个端口处于关闭状态；如果没有任何响应 或者发送了ICMP unreachable信息，则可认为这个端口被屏蔽了。SYN模式的扫描速度非常 好。而且由于这种模式不会进行三次握手，所以是一种十分隐蔽的扫描方式。如果启动Nmap 的用户有高级别权限，那么在默认情况下Nmap程序将以这种模式进行
[扫描](https://mrxn.net/tag/%E6%89%AB%E6%8F%8F)
。

3.TCP NULL（-sN）、FIN（-sF）及XMAS（-sX）扫描：NULL 扫描不设置任何控制位； FIN扫描仅设置FIN标志位：XMAS扫描设置FIN、PSH和URG的标识位。如果目标主机返回 了含有RST标识位的响应数据，则说明该端口处于关闭状态；如果目标主机没有任何回应， 则该端口处于打开｜过滤状态。

4.TCP Maimon扫描（-sM）：Uriel Maimon 首先发现了TCP Maimom扫描方式。这种模式的 探测数据包含有FIN/ACK标识。对于BSD衍生出来的各种操作系统来说，如果被测端口处于 开放状态，主机将会丢弃这种探测数据包；如果被测端口处于关闭状态，那么主机将会回复 RST。

5.TCPACK扫描（-sA）：这种扫描模式可以检测目标系统是否采用了数据包状态监测技术 （stateful）防火墙，并能确定哪些端口被防火墙屏蔽。这种类型的数据包只有一个ACK标识 位。如果目标主机的回复中含有RST标识，则说明目标主机没有被过滤。

6.TCP窗口扫描（-sW）：这种扫描方式检测目标返回的RST数据包的TCP窗口字段。如果目 标端口处于开放状态，这个字段的值将是正值；否则它的值应当是0。

7.TCP Idle扫描（-sI）：采用这种技术后，您将通过指定的僵尸主机发送扫描数据包。本机 并不与目标主机直接通信。如果对方网络里有IDS，IDS将认为发起扫描的主机是僵尸主机。

### UDP扫描选项

Nmap有多种TCP
[扫描](https://mrxn.net/tag/%E6%89%AB%E6%8F%8F)
方式，而UDP扫描仅有一种扫描方式（-sU）。虽然UDP扫描结果没有 TCP扫描结果的可靠度高，但
[渗透](https://mrxn.net/tag/%E6%B8%97%E9%80%8F)
测试人员不能因此而轻视UDP扫描，毕竟UDP端口代表着 可能会有价值的服务端程序。但是UDP扫描的最大问题是性能问题。由干Linux内核限制1秒内最多发送一次ICMP Port Unreachable信息。按照这个速度，对一台主机的65536个UDP端口进行
[完整扫描](https://mrxn.net/tag/%E6%89%AB%E6%8F%8F)
，总耗时必 定会超过18个小时。

优化方法主要是：

|  |  |
| --- | --- |
|  | ``` ``` 1.进行并发的UDP扫描； 2.优先扫描常用端口； 3.在防火墙后面扫描； 4.启用--host-timeout选项以跳过响应过慢的主机。 ``` ``` |

假如我们需要找到目标主机开放了哪些 UDP端口。为提高扫描速度，我们仅扫描 53端口 （DNS）和161端口（SNMP）。

可以使用命令
`nmap -sU 192.168.56.103 -p 53,161`

### 目标端口选项

默认情况下，Nmap将从每个协议的常用端口中随机选择1000个端口进行扫描。其nmapservices文件对端口的命中率进行了排名。

可以自定义端口参数：

|  |  |
| --- | --- |
|  | ``` ``` -p端口范围：只扫描指定的端口。扫描1〜1024号端口，可设定该选项为–p    1-1024。扫描1 〜65535端口时，可使用-p-选项。  -F（快速扫描）：将仅扫描100    个常用端口。  -r（顺序扫描）：指定这个选项后，程序将从按照从小到大的顺序扫描端口。   -top-ports ：扫描nmap-services 里排名前N的端口。 ``` ``` |

### 输出选项

Nmap可以把扫描结果保存为外部文件。在需要使用其他工具处理Nmap的扫描结果时，这一 功能十分有用。即使您设定程序把扫描结果保存为文件，Nmap还是会在屏幕上显示扫描结果。

```
Nmap支持以下几种输出形式。
正常输出（-oN）：不显示runtime信息和警告信息。

XML 文件（-oX）：生成的 XML 格式文件可以转换成   HTML    格式文件，还可被Nmap    的图 形用户界面解析，也便于导入数据库。本文建议您尽量将扫描结果输出为XML文件。

生成便于Grep使用的文件（-oG）：虽然这种文件格式已经过时，但仍然很受欢迎。这种格 式的文件，其内容由注释（由#开始）和信息行组成。信息行包含6个字段，每个字段的字段 名称和字段值以冒号分割，字段之间使用制表符隔开。这些字段的名称分别为Host、Ports、Protocols、Ignored State、OS、Seq Index、IP ID   Seq 和Status。这种格式的文件便于 grep或awk之类的UNIX指令整理扫描结果。

输出至所有格式(-oA)
为使用方便，利用-oA选项 可将扫描结果以标准格式、XML格式和Grep格式一次性输出。分别存放在.nmap，.xml和.gnmap文件中。
```

  

### 时间排程控制选项

Nmap可通过-T选项指定时间排程控制的模式。它有6种扫描模式。

```
paranoid（0）：每5分钟发送一次数据包，且不会以并行方式同时发送多组数据。这种模式 的扫描不会被IDS检测到。

sneaky（1）：每隔15秒发送一个数据包，且不会以并行方式同时发送多组数据。

polite（2）：每0.4  秒发送一个数据包，且不会以并行方式同时发送多组数据。

normal（3）：此模式同时向多个目标发送多个数据包，为   Nmap    默认的模式，该模式能自 动在扫描时间和网络负载之间进行平衡。

aggressive（4）：在这种模式下，Nmap   对每个既定的主机只扫描5    分钟，然后扫描下一 台主机。它等待响应的时间不超过1.25秒。

insane（5）：在这种模式下，Nmap   对每个既定的主机仅扫描75   秒，然后扫描下一台主 机。它等待响应的时间不超过0.3秒。
```

|  |
| --- |
|  |

默认的
[扫描](https://mrxn.net/tag/%E6%89%AB%E6%8F%8F)
模式通常都没有问题。除非您想要进行更隐匿或更快速的扫 描，否则没有必要调整这一选项。

### 扫描IPv6主机

启用Nmap的-6选项即可扫描IPv6的目标主机。当前，只能逐个指定目标主机的IPv6地址。

|  |  |
| --- | --- |
|  | ``` ``` nmap -6  fe80::a00:27ff:fe43:1518 ``` ``` |

同一台主机在IPv6网络里开放的端口比它在IPv4网络里开放的端口数量要 少。这是因为部分服务程序尚未支持IPv6网络。

### 脚本引擎功能（Nmap Scripting Engine，NSE）

最后但是同样重要的，Nmap本身已经很强大了，但是加上它的脚本引擎更加开挂了，NSE 可使用户的各种网络检査工作更为自动化，有助于识别应 用程序中新发现的漏洞、检测程序版本等Nmap原本不具有的功能。虽然Nmap软件包具有各 种功能的脚本，但是为了满足用户的特定需求，它还支持用户撰写自定义脚本。

```
auth：此类脚本使用暴力破解等技术找出目标系统上的认证信息。

default：启用--sC  或者-A    选项时运行此类脚本。这类脚本同时具有下述特点：执行速度快；输出的信息有指导下一步操作的价值；输出信息内容丰富、形式简洁；必须可靠；不会侵入目标系统；能泄露信息给第三方。

discovery：该类脚本用于探索网络。

dos：该类脚本可能使目标系统拒绝服务，请谨慎使用。

exploit：该类脚本利用目标系统的安全漏洞。在运行这类脚本之前，渗透测试人员需要获取 被测单位的行动许可。

external：该类脚本可能泄露信息给第三方。

fuzzer：该类脚本用于对目标系统进行模糊测试。

instrusive：该类脚本可能导致目标系统崩溃，或耗尽目标系统的所有资源。

malware：该类脚本检査目标系统上是否存在恶意软件或后门。

safe：该类脚本不会导致目标服务崩溃、拒绝服务且不利用漏洞。

version：配合版本检测选项（-sV），这类脚本对目标系统的服务程序进行深入的版本检 测。

vuln：该类脚本可检测检査目标系统上的安全漏洞。
在Kali   Linux系统中，Nmap脚本位于目录/usr/share/nmap/scripts。

-sC 或--script=default：启动默认类NSE  脚本。

--script    <filename>|<category>|<directories>：根据指定的文件名、类别名、目录名，执行 相应的脚本。

--script-args   <args>：这个选项用于给脚本指定参数。例如，在使用认证类脚本时，可通过 这个选项指定用户名和密码
```

  

### 规避检测的选项

在
[渗透测试](https://mrxn.net/tag/%E6%B8%97%E9%80%8F)
的工作中，目标主机通常处于防火墙或 IDS 系统的保护之中。在这种环境中使用 Nmap 的默认选项进行
[扫描](https://mrxn.net/tag/%E6%89%AB%E6%8F%8F)
，不仅会被发现，而且往往一无所获。此时，我们就要使用Nmap 规避检测的有关选项。

```
-f（使用小数据包）：这个选项可避免对方识别出我们探测的数据包。指定这个选项之后， Nmap将使用8字节甚至更小数据体的数据包。

--mtu：这个选项用来调整数据包的包大小。MTU（Maximum   Transmission    Unit，最大传输 单元）必须是8的整数倍，否则Nmap将报错。

-D（诱饵）：这个选项应指定假 IP，即诱饵的 IP。启用这个选项之后，Nmap    在发送侦测 数据包的时候会掺杂一些源地址是假IP（诱饵）的数据包。这种功能意在以藏木于林的方法 掩盖本机的真实 IP。也就是说，对方的log还会记录下本机的真实IP。您可使用RND生成随机 的假IP地址，或者用RND：number的参数生成<number>个假IP地址。您所指定的诱饵主机 应当在线，否则很容易击溃目标主机。另外，使用了过多的诱饵可能造成网络拥堵。尤其是 在扫描客户的网络的时候，您应当极力避免上述情况。
Kali    Linux   渗透测试的艺术（中文版）
151第 6章 服务枚举
--source-port   <portnumber>或-g（模拟源端口）：如果防火墙只允许某些源端口的入站流 量，这个选项就非常有用。

--data-length：这个选项用于改变Nmap  发送数据包的默认数据长度，以避免被识别出来是 Nmap的扫描数据。

--max-parallelism：这个选项可限制Nmap   并发扫描的最大连接数。

--scan-delay    <time>：这个选项用于控制发送探测数据的时间间隔，以避免达到IDS/IPS端 口扫描规则的阈值。
```


下面贴一些我们日常实际
[渗透测试](https://mrxn.net/tag/%E6%B8%97%E9%80%8F)
过程中高频率使用的一些用法：
  

```
nmap -sV -sT -Pn --open -v 192.168.3.23 //扫描常见端口服务
nmap --script=default 192.168.137.* 或者 nmap -sC 192.168.137.*
nmap --script=auth 192.168.0.1  //对目标或网段进行应用弱口令检测
nmap --script=brute 192.168.0.105  //对数据库、smb、snmp进行简单密码暴力猜解
nmap --script=vuln 192.168.0.1//检测常见漏洞
nmap --script=realvnc-auth-bypass 192.168.0.0 //扫描vnc服务 可扫mysql、telnet、Rsync
nmap -n -p 445 --script=broadcast 192.168.0.1 //探测局域网更多服务
nmap --script external.baidu.com //whois解析
nmap --script external 202.103.243.110 //跟whois解析同样的效果
nmap  --script=realvnc-auth-bypass 192.168.137.4   //检查vnc bypass
检查vnc认证方式
nmap  --script=vnc-auth  192.168.137.4  
获取vnc信息
nmap  --script=vnc-info  192.168.137.4  
smb破解
nmap  --script=smb-brute.nse 192.168.137.4  
smb字典破解
nmap --script=smb-brute.nse --script-args=userdb=/var/passwd,passdb=/var/passwd192.168.137.4  
smb已知几个严重漏洞
nmap  --script=smb-check-vulns.nse --script-args=unsafe=1 192.168.137.4 
nmap -p 445  --script smb-ls--script-args ‘share=e$,path=\,smbuser=test,smbpass=test’ 192.168.137.4    查看共享目录  
查询主机一些敏感信息（注：需要下载nmap_service）
nmap -p 445 -n –script=smb-psexec --script-args= smbuser=test,smbpass=test192.168.137.4   
nmap -n -p445 --script=smb-enum-sessions.nse --script-args=smbuser=test,smbpass=test192.168.137.4    查看会话
系统信息nmap -n -p445 --script=smb-os-discovery.nse --script-args=smbuser=test,smbpass=test192.168.137.4  
猜解mssql用户名和密码
nmap -p1433 --script=ms-sql-brute --script-args=userdb=/var/passwd,passdb=/var/passwd192.168.137.4    
xp_cmdshell 执行命令 
nmap -p 1433 --script ms-sql-xp-cmdshell --script-args mssql.username=sa,mssql.password=sa,ms-sql-xp-cmdshell.cmd="net user" 192.168.137.4   
dumphash值
nmap -p 1433 --script ms-sql-dump-hashes.nse --script-args mssql.username=sa,mssql.password=sa  192.168.137.4  Mysql扫描：
nmap -p3306 --script=mysql-empty-password.nse 192.168.137.4   扫描root空口令
列出所有mysql用户
nmap -p3306 --script=mysql-users.nse --script-args=mysqluser=root 192.168.137.4   
支持同一应用的所有脚本扫描
nmap --script=mysql-* 192.168.137.4  
Oracle扫描：
oracle sid扫描
nmap --script=oracle-sid-brute -p 1521-1560 192.168.137
```

PS：Nmap 在实际
[渗透测试](https://mrxn.net/tag/%E6%B8%97%E9%80%8F)
的时候还可以在MSF里面调用配合MSF一起有时候别有用处！
  

参考资料如下：
  

Nmap 官方的在线版 Nmap参考指南(Man Page)：
<https://nmap.org/man/zh/>


[Github仓库版(网络下载上传)](https://github.com/Mr-xn/BurpSuite-collections/blob/master/books/nmap-man-page.pdf)
  

Nmap 中文域名网站：
<http://www.nmap.com.cn/doc/manual.shtm>
  

GitBook 在线版 ：
<https://legacy.gitbook.com/book/wizardforcel/nmap-man-page/details>
  

看云在线版：
<https://www.kancloud.cn/wizardforcel/nmap-man-page/141685>
  

crayon-xin 博客文章：
[nmap超详细使用指南](https://crayon-xin.github.io/2018/08/12/nmap%E8%B6%85%E8%AF%A6%E7%BB%86%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97/)

GitHub erasin ：
<https://github.com/erasin/notes/blob/master/linux/safe/nmap.md>

* 标签：
* [#
  渗透测试](https://mrxn.net/tag/%E6%B8%97%E9%80%8F%E6%B5%8B%E8%AF%95)
* [#
  黑客工具](https://mrxn.net/tag/%E9%BB%91%E5%AE%A2%E5%B7%A5%E5%85%B7)
* [#
  扫描](https://mrxn.net/tag/%E6%89%AB%E6%8F%8F)
* [#
  nmap](https://mrxn.net/tag/nmap)

---


// 获取当前脚本所在的父容器
const parentContainer = document.currentScript.parentElement;
let searchContainer = parentContainer.querySelector('article') || parentContainer;
if (searchContainer) {
// 优先在 class 名为 prose 或 markdown 的容器内搜索 img 图片
let images = [];
const containers = searchContainer.querySelectorAll('.prose, .markdown');
containers.forEach(function(container) {
images = images.concat(Array.from(container.querySelectorAll('img')));
});
if (images.length === 0) {
images = searchContainer.querySelectorAll('img');
}
images.forEach(function(img) {
if (img.getAttribute('data-action') === 'zoom') {
const parentLink = img.parentNode;
if (parentLink.tagName === 'A') {
parentLink.setAttribute('data-fancybox', 'gallery');
}
} else {
const link = document.createElement('a');
link.setAttribute('data-fancybox', 'gallery');
link.setAttribute('href', img.getAttribute('src'));
img.parentNode.insertBefore(link, img);
link.appendChild(img);
}
});
// 初始化 Fancybox
Fancybox.bind("[data-fancybox]", {
// 您的自定义选项
});
}

文章目录

×



.x\_nav\_toc {
position: fixed;
top: 0;
right: -300px;
width: 280px;
height: 100%;
background-color: white;
box-shadow: -2px 0 15px rgba(0, 0, 0, 0.1);
z-index: 1000;
transition: right 0.3s ease;
display: flex;
flex-direction: column;
overflow: hidden;
padding-top: 10px;
}
.x\_nav\_toc.active {
right: 0;
}
.x\_toc\_header {
display: flex;
justify-content: space-between;
align-items: center;
padding: 15px 20px;
height: 48px;
border-bottom: 1px solid #eee;
}
.x\_toc\_title {
font-size: 18px;
font-weight: bold;
color: #333;
}
.x\_toc\_close {
background: none;
border: none;
font-size: 24px;
cursor: pointer;
color: #777;
transition: color 0.2s;
}
.x\_toc\_close:hover {
color: #333;
}
.x\_toc\_content {
flex: 1;
overflow-y: auto;
padding: 15px 20px;
padding-right: 10px;
}
.x\_anchor-list {
list-style-type: none;
padding: 0;
margin: 0;
}
/\* 减小目录项间距 \*/
.x\_anchor-list li {
margin-bottom: 4px; /\* 间距从8px减小到4px \*/
}
.x\_anchor-list a {
text-decoration: none;
color: #555;
display: block;
padding: 6px 10px; /\* 减少内边距 \*/
transition: all 0.2s;
font-size: 14px;
border-radius: 4px;
line-height: 1.4; /\* 减小行高 \*/
}
.x\_anchor-list a:hover,
.x\_anchor-list a:focus {
background-color: #f8f9fa;
color: #0068d6;
}
.toc-number {
font-weight: 600;
margin-right: 8px;
color: #495057;
display: inline-block;
min-width: 25px;
}
/\* 减小各级标题间距 \*/
.toc-h1 {
font-weight: 600;
font-size: 15px;
margin-top: 10px; /\* 上边距从15px减小到10px \*/
padding-left: 5px !important;
}
.toc-h2 {
font-size: 14px;
padding-left: 15px !important; /\* 缩进从20px减小到15px \*/
}
.toc-h3 {
font-size: 13px;
padding-left: 25px !important; /\* 缩进从30px减小到25px \*/
}
.toc-h4 {
font-size: 12px;
padding-left: 35px !important; /\* 缩进从40px减小到35px \*/
}
/\* 修改后的切换按钮样式 - 使用图标且位置下移 \*/
.x\_toc\_toggle {
position: fixed;
bottom:120px; right: 17px;width:40px;height:40px;background-color:white;
border-radius: 50%;
border: none;
cursor: pointer;
box-shadow: 0 4px 12px rgba(0,0,0,0.15);
z-index: 999;
transition: all 0.3s ease;
display: flex;
align-items: center;
justify-content: center;
padding: 0;
}
.x\_toc\_toggle svg {
width:24px;height:24px;stroke:#3d9bff;
}
.x\_toc\_toggle:hover {
#background-color: #0081f8;
transform: translateY(-3px);
box-shadow: 0 6px 15px rgba(0,0,0,0.2);
}
@media (max-width: 768px) {
.x\_nav\_toc {
width: 280px;
}
.x\_toc\_toggle {
bottom: 100px; /\* 手机端也下移位置 \*/
right: 30px;
width: 40px;
height: 40px;
}
.x\_toc\_toggle svg {
width: 20px;
height: 20px;
}
}

document.addEventListener('DOMContentLoaded', function() {
// 获取所有标题元素
var className = ".line-numbers";
var selectors = [];
for (var i = 1; i <= 6; i++) {
selectors.push(className + ' h' + i);
}
var headings = document.querySelectorAll(selectors.join(', '));
// 获取DOM元素
var tocContainer = document.querySelector('.x\_nav\_toc');
var toggleButton = document.querySelector('.x\_toc\_toggle');
var tocList = document.querySelector('.x\_anchor-list');
var closeButton = document.querySelector('.x\_toc\_close');
var currentHighlight = null;
// 检测是否为移动设备
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
// 如果没有标题，隐藏所有元素
if (headings.length === 0) {
tocContainer.style.display = 'none';
toggleButton.style.display = 'none';
return;
}
// 初始化层级计数器
var counters = [0, 0, 0, 0, 0, 0]; // h1-h6
var currentLevel = 0;
// 生成带数字编号的目录
headings.forEach(function(heading, index) {
var level = parseInt(heading.tagName[1]);
// 更新计数器
counters[level - 1] += 1; // 增加当前级别计数器
// 重置更低级计数器
for (var i = level; i < 6; i++) {
counters[i] = 0;
}
// 生成编号字符串（如"1.2.3"）
var numberParts = [];
for (var i = 0; i < level; i++) {
if (counters[i] > 0) {
numberParts.push(counters[i]);
}
}
var numberText = numberParts.join('.')+'.';
// 创建唯一ID
var id = 'toc-' + numberText.replace(/\./g, '-');
heading.id = id;
var listItem = document.createElement('li');
var anchor = document.createElement('a');
var numberSpan = document.createElement('span');
numberSpan.className = 'toc-number';
numberSpan.textContent = numberText;
anchor.appendChild(numberSpan);
anchor.innerHTML += heading.textContent;
anchor.href = '#' + id;
anchor.classList.add('toc-h' + level);
listItem.appendChild(anchor);
tocList.appendChild(listItem);
// 添加点击事件（不关闭目录）
anchor.addEventListener('click', function(e) {
e.preventDefault();
// 更新高亮状态
if (currentHighlight) {
currentHighlight.classList.remove('active');
}
this.classList.add('active');
currentHighlight = this;
// 滚动到对应位置
var targetId = this.getAttribute('href').substring(1);
var targetElement = document.getElementById(targetId);
if (targetElement) {
var header = document.querySelector("header");
var headerHeight = header ? header.offsetHeight : 0;
var elementPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
var offsetPosition = elementPosition - headerHeight - 20;
window.scrollTo({
top: offsetPosition,
behavior: 'smooth'
});
// 滚动到目录项的可视区域
this.scrollIntoView({behavior: 'smooth', block: 'nearest'});
// 点击事件中
if (isMobile) {
closeToc(); // 移动端点击后关闭目录
}
}
});
});
// 切换按钮点击事件
toggleButton.addEventListener('click', function() {
tocContainer.classList.add('active');
});
// 关闭按钮点击事件
closeButton.addEventListener('click', function(e) {
e.stopPropagation();
closeToc();
});
// 滚动时更新高亮状态
window.addEventListener('scroll', function() {
var fromTop = window.scrollY;
var header = document.querySelector("header");
var headerHeight = header ? header.getBoundingClientRect().height : 0; // 更精确的header高度
//console.log(headerHeight);
// 精准计算标题文档位置
var activeSection = null;
headings.forEach(function(heading) {
var section = document.getElementById(heading.id);
if (!section) return;
// 使用getBoundingClientRect获取精确位置
var rect = section.getBoundingClientRect();
var sectionTop = rect.top + fromTop; // 转换为文档顶部绝对位置
var sectionBottom = rect.bottom + fromTop + headerHeight;
// 增加20px激活区域缓冲
if (fromTop + headerHeight + 20 >= sectionTop && fromTop < sectionBottom) {
activeSection = heading;
}
});
// 更新高亮状态（新增精确边界判断）
if (activeSection) {
var tocLink = tocList.querySelector('a[href="#' + activeSection.id + '"]');
if (tocLink && currentHighlight !== tocLink) {
if (currentHighlight) {
currentHighlight.blur();
currentHighlight.classList.remove('active');
}
tocLink.classList.add('active');
tocLink.focus();
currentHighlight = tocLink;
// 平滑滚动到可视区域（改进触发条件）
var tocRect = tocLink.getBoundingClientRect();
var tocContainerRect = tocContainer.getBoundingClientRect();
if (tocRect.bottom > tocContainerRect.bottom || tocRect.top < tocContainerRect.top) {
tocLink.scrollIntoView({behavior: 'auto', block: 'nearest'});
}
}
}
});
// 关闭目录面板
function closeToc() {
tocContainer.classList.remove('active');
}
});

/\* 超小屏幕隐藏 \*/
@media (max-width: 768px) {
#qrcode-right {
display: none;
}
}

版权所有：
[Mrxn's Blog](https://mrxn.net/)
  
文章标题：
[Scanning is art - Nmap 扫描的艺术之常见的基本操作](https://mrxn.net/jswz/Nmap-Scanning-Art.html)
  
文章链接：
<https://mrxn.net/jswz/Nmap-Scanning-Art.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/Nmap-Scanning-Art.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});

### 📚 推荐阅读

* [深信服运维安全管理系统 install\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-install_patch-rce.html)
* [深信服运维安全管理系统 del\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-del_patch-rce.html)
* [深信服运维安全管理系统 upload\_file 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-cssp-app-upload_file-rce.html)
* [深信服运维安全管理系统 csspost/update 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-csspost-update-rce.html)
* [深信服运维安全管理系统 save\_SNMP 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-SNMP-save_SNMP-rce.html)
* [深信服运维安全管理系统 getLdap 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-getLdap-rce.html)
* [深信服运维安全管理系统 Jwt 密钥硬编码](https://mrxn.net/jswz/sangfor_osm-login-search_login-token-leak.html)
* [深信服运维安全管理系统 del\_route 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-del_route-rce.html)
* [深信服运维安全管理系统 del\_net 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-del_net-rce.html)
* [深信服运维安全管理系统 change\_net 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-change_net-rce.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 updateLoginName SQL注入漏洞](https://mrxn.net/jswz/bigant-user-updateLoginName-sqli.html)
* [九佳易管理系统 PrivilegedCodeDestroy.asmx SQL注入漏洞](https://mrxn.net/jswz/a8erp-Interface-licx-PrivilegedCodeDestroy-sqli.html)
* [九佳易管理系统 Ajax\_XT.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-Ajax_XT-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](https://mrxn.net/jswz/bigant-dept-moveDept-sqli.html)
* [青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞](https://mrxn.net/jswz/qinglong-auth-bypass-rce.html)
* [九佳易管理系统 picHY.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-HuiYuanDangAn-picHY-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](https://mrxn.net/jswz/bigant-install-config-rce.html)
* [东胜物流软件 MsChDuiController 多个SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsChDuiController-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](https://mrxn.net/jswz/bigant-Public-download.html)
* [东胜物流软件 MsAnnounceController SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsAnnounce-GetData-sqli.html)

/\* 底部展示样式 \*/
.qrcode-bottom-box {
margin: 40px auto;
text-align: center;
}
.qrcode-title {
font-size: 16px;
color: #666;
margin-bottom: 0px;
font-weight: bold;
text-align: center;
}
.qrcode-bottom-box img {
display: inline-block;
padding: 10px;
background: #fff;
border-radius: 8px;
margin: 10px auto;
}
/\* 悬浮展示样式 \*/
.qrcode-float {
position: fixed;
z-index: 9999;
background: rgba(255,255,255,0.98);
padding: 20px;
border-radius: 12px;
}
.qrcode-float:hover {
transform: scale(1.05);
}
/\* 移动端适配 \*/
@media (max-width: 1440px) {
.qrcode-float {
right: 2%;
transform: none;
}
}
/\* 超小屏幕隐藏 \*/
@media (max-width: 768px) {
.qrcode-float {
display: none;
}
}

手机扫码阅读



var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/Nmap-Scanning-Art.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});