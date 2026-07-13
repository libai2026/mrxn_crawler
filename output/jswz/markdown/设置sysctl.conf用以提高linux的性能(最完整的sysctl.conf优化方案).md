---
title: "设置Sysctl.conf用以提高Linux的性能(最完整的sysctl.conf优化方案)"
source: https://mrxn.net/jswz/sysctl-vps-speeder.html
asset_dir: embedded-base64
---

Sysctl是一个允许您改变正在运行中的[Linux](https://mrxn.net/tag/Linux "标签：Linux")系统的接口。它包含一些 [tcp](https://mrxn.net/tag/tcp "标签：tcp")/IP 堆栈和虚拟内存系统的高级选项， 这可以让有经验的管理员提高引人注目的系统性能。用sysctl可以读取设置超过五百个系统变量。基于这点，sysctl(8) 提供两个功能：读取和修改系统设置。

软件实用程序

查看所有可读变量：

% sysctl -a

读一个指定的变量，例如 kern.maxproc：

% sysctl kern.maxproc kern.maxproc: 1044

要设置一个指定的变量，直接用 variable=value 这样的语法：

# sysctl kern.maxfiles=5000

kern.maxfiles: 2088 -> 5000

您可以使用sysctl修改系统变量，也可以通过编辑sysctl.conf文件来修改系统变量。sysctl.conf 看起来很像 rc.conf。它用 variable=value 的形式来设定值。指定的值在系统进入多用户模式之后被设定。并不是所有的变量都可以在这个模式下设定。

sysctl 变量的设置通常是字符串、数字或者布尔型。 (布尔型用 1 来表示’yes’，用 0 来表示’no’)。

sysctl -w kernel.sysrq=0

sysctl -w kernel.core\_uses\_pid=1

sysctl -w net.ipv4.conf.default.accept\_redirects=0

sysctl -w net.ipv4.conf.default.accept\_source\_route=0

sysctl -w net.ipv4.conf.default.rp\_filter=1

sysctl -w net.ipv4.tcp\_syncookies=1

Linux 与 Unix

sysctl -w net.ipv4.tcp\_max\_syn\_backlog=2048

sysctl -w net.ipv4.tcp\_fin\_timeout=30

sysctl -w net.ipv4.tcp\_synack\_retries=2

sysctl -w net.ipv4.tcp\_keepalive\_time=3600

sysctl -w net.ipv4.tcp\_window\_scaling=1

sysctl -w net.ipv4.tcp\_sack=1

深入探索

防病毒程序与恶意软件

编程

参考信息

配置sysctl

编辑此文件：

vi /etc/sysctl.conf

如果该文件为空，则输入以下内容，否则请根据情况自己做调整：

```
# Controls source route verification
# Default should work for all interfaces
net.ipv4.conf.default.rp_filter = 1
# net.ipv4.conf.all.rp_filter = 1
# net.ipv4.conf.lo.rp_filter = 1
# net.ipv4.conf.eth0.rp_filter = 1
# Disables IP source routing
# Default should work for all interfaces
net.ipv4.conf.default.accept_source_route = 0
# net.ipv4.conf.all.accept_source_route = 0
# net.ipv4.conf.lo.accept_source_route = 0
# net.ipv4.conf.eth0.accept_source_route = 0
# Controls the System Request debugging functionality of the kernel
kernel.sysrq = 0
# Controls whether core dumps will append the PID to the core filename.
# Useful for debugging multi-threaded applications.
kernel.core_uses_pid = 1
# Increase maximum amount of memory allocated to shm
# Only uncomment if needed!
# kernel.shmmax = 67108864
# Disable ICMP Redirect Acceptance
# Default should work for all interfaces
net.ipv4.conf.default.accept_redirects = 0
# net.ipv4.conf.all.accept_redirects = 0
# net.ipv4.conf.lo.accept_redirects = 0
# net.ipv4.conf.eth0.accept_redirects = 0
# Enable Log Spoofed Packets, Source Routed Packets, Redirect Packets
# Default should work for all interfaces
net.ipv4.conf.default.log_martians = 1
# net.ipv4.conf.all.log_martians = 1
# net.ipv4.conf.lo.log_martians = 1
# net.ipv4.conf.eth0.log_martians = 1
# Decrease the time default value for tcp_fin_timeout connection
net.ipv4.tcp_fin_timeout = 25
# Decrease the time default value for tcp_keepalive_time connection
net.ipv4.tcp_keepalive_time = 1200
# Turn on the tcp_window_scaling
net.ipv4.tcp_window_scaling = 1
# Turn on the tcp_sack
net.ipv4.tcp_sack = 1
# tcp_fack should be on because of sack
net.ipv4.tcp_fack = 1
# Turn on the tcp_timestamps
net.ipv4.tcp_timestamps = 1
# Enable TCP SYN Cookie Protection
net.ipv4.tcp_syncookies = 1
# Enable ignoring broadcasts request
net.ipv4.icmp_echo_ignore_broadcasts = 1
# Enable bad error message Protection
net.ipv4.icmp_ignore_bogus_error_responses = 1
# Make more local ports available
# net.ipv4.ip_local_port_range = 1024 65000
# Set TCP Re-Ordering value in kernel to ‘5′
net.ipv4.tcp_reordering = 5
# Lower syn retry rates
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_syn_retries = 3
# Set Max SYN Backlog to ‘2048′
net.ipv4.tcp_max_syn_backlog = 2048
# Various Settings
net.core.netdev_max_backlog = 1024
# Increase the maximum number of skb-heads to be cached
net.core.hot_list_length = 256
# Increase the tcp-time-wait buckets pool size
net.ipv4.tcp_max_tw_buckets = 360000
# This will increase the amount of memory available for socket input/output queues
net.core.rmem_default = 65535
net.core.rmem_max = 8388608
net.ipv4.tcp_rmem = 4096 87380 8388608
net.core.wmem_default = 65535
net.core.wmem_max = 8388608
net.ipv4.tcp_wmem = 4096 65535 8388608
net.ipv4.tcp_mem = 8388608 8388608 8388608
net.core.optmem_max = 40960
```

如果希望屏蔽别人 ping 你的主机，则加入以下代码：

字典与百科全书

# Disable ping requests

net.ipv4.icmp\_echo\_ignore\_all = 1

编辑完成后，请执行以下命令使变动立即生效：

/sbin/sysctl -p

/sbin/sysctl -w net.ipv4.route.flush=1

###################   
  
所有rfc相关的选项都是默认启用的，因此网上的那些还自己写rfc支持的都可以扔掉了:)   
  
###############################   
  
  
  
net.inet.ip.sourceroute=0   
  
net.inet.ip.accept\_sourceroute=0   
  
#############################   
  
通过源路由，攻击者可以尝试到达内部IP地址 --包括RFC1918中的地址，所以   
  
不接受源路由信息包可以防止你的内部网络被探测。   
  
#################################   
  
  
  
net.inet.[tcp](https://mrxn.net/tag/tcp "标签：tcp").drop\_synfin=1   
  
###################################   
  
安全参数，编译内核的时候加了options TCP\_DROP\_SYNFIN才可以用，可以阻止某些[OS](#)探测。   
  
##################################   
  
  
  
kern.maxvnodes=8446   
  
#################<http://www.bsdlover.cn#########&nbsp>;  
  
vnode 是对文件或目录的一种内部表达。 因此， 增加可以被[操作系统](#)利用的 vnode 数量将降低磁盘的 I/O。   
  
一般而言， 这是由操作系统自行完成的，也不需要加以修改。但在某些时候磁盘 I/O 会成为瓶颈，   
  
而系统的 vnode 不足， 则这一配置应被增加。此时需要考虑是非活跃和空闲内存的数量。   
  
要查看当前在用的 vnode 数量：   
  
# sysctl vfs.numvnodes   
  
vfs.numvnodes: 91349   
  
要查看最大可用的 vnode 数量：   
  
# sysctl kern.maxvnodes   
  
kern.maxvnodes: 100000   
  
如果当前的 vnode 用量接近最大值，则将 kern.maxvnodes 值增大 1,000 可能是个好主意。   
  
您应继续查看 vfs.numvnodes 的数值， 如果它再次攀升到接近最大值的程度，   
  
仍需继续提高 kern.maxvnodes。 在 top(1) 中显示的内存用量应有显著变化，   
  
更多内存会处于活跃 (active) 状态。   
  
####################################   
  
  
  
  
  
kern.maxproc: 964   
  
#################<http://www.bsdlover.cn#########&nbsp>;  
  
Maximum number of processes   
  
####################################   
  
kern.maxprocperuid: 867   
  
#################<http://www.bsdlover.cn#########&nbsp>;  
  
Maximum processes allowed per userid   
  
####################################   
  
因为我的maxusers设置的是256，20+16*maxusers＝4116。* *maxprocperuid至少要比maxproc少1，因为init(8) 这个系统程序绝对要保持在运作状态。   
  
我给它设置的2068。   
  
  
  
  
  
kern.maxfiles: 1928   
  
#################<http://www.bsdlover.cn#########&nbsp>;  
  
系统中支持最多同时开启的文件数量，如果你在运行[数据](#)库或大的很吃描述符的进程，那么应该设置在20000以上，   
  
比如kde这样的桌面环境，它同时要用的文件非常多。   
  
一般推荐设置为32768或者65536。   
  
####################################   
  
  
  
kern.argmax: 262144   
  
#################<http://www.bsdlover.cn#########&nbsp>;  
  
maximum number of bytes (or characters) in an argument list.   
  
命令行下最多支持的参数，比如你在用find命令来批量删除一些文件的时候   
  
find . -name "*.old" -delete，如果文件数超过了这个数字，那么会提示你数字太多的。   
  
可以利用find . -name "\*.old" -ok rm {} \;来删除。   
  
默认的参数已经足够多了，因此不建议再做修改。   
  
####################################   
  
  
  
kern.securelevel: -1   
  
#################<http://www.bsdlover.cn#########&nbsp>;  
  
-1：这是系统默认级别，没有提供任何内核的保护错误；    
  
0：基本上作用不多，当你的系统刚启动就是0级别的，当进入多用户模式的时候就自动变成1级了。    
  
1：在这个级别上，有如下几个限制：    
  
 a. 不能通过kldload或者kldunload加载或者卸载可加载内核模块；    
  
 b. 应用程序不能通过/dev/mem或者/dev/kmem直接写内存；    
  
 c. 不能直接往已经装在(mounted)的磁盘写东西，也就是不能格式化磁盘，但是可以通过标准的内核接口执行写操作；    
  
 d. 不能启动X-windows，同时不能使用chflags来修改文件属性；    
  
2：在 1 级别的基础上还不能写没装载的磁盘，而且不能在1秒之内制造多次警告，这个是防止DoS控制台的；    
  
3：在 2 级别的级别上不允许修改IPFW防火墙的规则。    
  
 如果你已经装了防火墙，并且把规则设好了，不轻易改动，那么建议使用3级别，如果你没有装防火墙，而且还准备装防火墙的话，不建议使用。   
  
我们这里推荐使用 2 级别，能够避免比较多对内核攻击。   
  
####################################   
  
  
  
kern.maxfilesperproc: 1735   
  
#################<http://www.bsdlover.cn#########&nbsp>;  
  
每个进程能够同时打开的最大文件数量，网上很多资料写的是32768   
  
除非用异步I/O或大量线程，打开这么多的文件恐怕是不太正常的。   
  
我个人建议不做修改，保留默认。   
  
####################################   
  
  
  
  
  
kern.ipc.maxsockbuf: 262144   
  
#################<http://www.bsdlover.cn#########&nbsp>;  
  
最大的套接字缓冲区，网上有建议设置为2097152（2M）、8388608（8M）的。   
  
我个人倒是建议不做修改，保持默认的256K即可，缓冲区大了可能造成碎片、阻塞或者丢包。   
  
####################################   
  
  
  
  
  
kern.ipc.somaxconn: 128   
  
#################<http://www.bsdlover.cn#########&nbsp>;  
  
最大的等待连接完成的套接字队列大小，即并发连接数。   
  
高负载服务器和受到Dos攻击的系统也许会因为这个队列被塞满而不能提供正常服务。   
  
默认为128，推荐在1024-4096之间，根据机器和实际情况需要改动，数字越大占用内存也越大。   
  
####################################   
  
  
  
  
  
kern.ipc.nmbclusters: 4800   
  
#################<http://www.bsdlover.cn#########&nbsp>;  
  
这个值用来调整系统在开机后所要分配给网络 mbufs 的 cluster 数量，   
  
由于每个 cluster 大小为 2K，所以当这个值为 1024 时，也是会用到 2MB 的核心内存空间。   
  
假设我们的网页同时约有 1000 个联机，而 TCP 传送及接收的暂存区大小都是 16K，   
  
则最糟的情况下，我们会需要 (16K+16K) \* 1024，也就是 32MB 的空间，   
  
然而所需的 mbufs 大概是这个空间的二倍，也就是 64MB，所以所需的 cluster 数量为 64MB/2K，也就是 32768。   
  
对于内存有限的机器，建议值是 1024 到 4096 之间，而当拥有海量存储器空间时，我们可以将它设定为 4096 到 32768 之间。   
  
我们可以使用 netstat 这个指令并加上参数 -m 来查看目前所使用的 mbufs 数量。   
  
要修改这个值必须在一开机就修改，所以只能在 /boot/loader.conf 中加入修改的设定   
  
kern.ipc.nmbclusters=32768   
  
####################################   
  
  
  
  
  
kern.ipc.shmmax: 33554432   
  
#################<http://www.bsdlover.cn#########&nbsp>;  
  
共享内存和信号灯("System VIPC")如果这些过小的话，有些大型的[软件](#)将无法启动   
  
安装xine和mplayer提示的设置为67108864，即64M，   
  
如果内存多的话，可以设置为134217728，即128M   
  
####################################   
  
  
  
  
  
kern.ipc.shmall: 8192   
  
#################<http://www.bsdlover.cn#########&nbsp>;  
  
共享内存和信号灯("System VIPC")如果这些过小的话，有些大型的软件将无法启动   
  
安装xine和mplayer提示的设置为32768   
  
####################################   
  
  
  
kern.ipc.shm\_use\_phys: 0   
  
#################<http://www.bsdlover.cn#########&nbsp>;  
  
如果我们将它设成 1，则所有 System V 共享内存 (share memory，一种程序间沟通的方式)部份都会被留在实体的内存 (physical memory) 中，  
  
而不会被放到硬盘上的 swap 空间。我们知道物理内存的存取速度比硬盘快许多，而当物理内存空间不足时，   
  
部份[数据](#)会被放到虚拟的内存上，从物理内存和虚拟内存之间移转的动作就叫作 swap。如果时常做 swap 的动作，   
  
则需要一直对硬盘作 I/O，速度会很慢。因此，如果我们有大量的程序 (数百个) 需要共同分享一个小的共享内存空间，   
  
或者是共享内存空间很大时，我们可以将这个值打开。   
  
这一项，我个人建议不做修改，除非你的内存非常大。   
  
####################################   
  
  
  
  
  
kern.ipc.shm\_allow\_removed: 0   
  
#################<http://www.bsdlover.cn#########&nbsp>;  
  
共享内存是否允许移除？这项似乎是在fb下装vmware需要设置为1的，否则会有加载SVGA出错的提示   
  
作为服务器，这项不动也罢。   
  
####################################   
  
  
  
kern.ipc.numopensockets: 12   
  
#################<http://www.bsdlover.cn#########&nbsp>;  
  
已经开启的socket数目，可以在最繁忙的时候看看它是多少，然后就可以知道maxsockets应该设置成多少了。   
  
####################################   
  
  
  
kern.ipc.maxsockets: 1928   
  
#################<http://www.bsdlover.cn#########&nbsp>;  
  
这是用来设定系统最大可以开启的 socket 数目。如果您的服务器会提供大量的 FTP 服务，   
  
而且常快速的传输一些小档案，您也许会发现常传输到一半就中断。因为 FTP 在传输档案时，   
  
每一个档案都必须开启一个 socket 来传输，但关闭 socket 需要一段时间，如果传输速度很快，   
  
而档案又多，则同一时间所开启的 socket 会超过原本系统所许可的值，这时我们就必须把这个值调大一点。   
  
除了 FTP 外，也许有其它网络程序也会有这种问题。   
  
然而，这个值必须在系统一开机就设定好，所以如果要修改这项设定，我们必须修改 /boot/loader.conf 才行   
  
kern.ipc.maxsockets="16424"   
  
####################################   
  
  
  
kern.ipc.nsfbufs: 1456   
  
#################<http://www.bsdlover.cn#########&nbsp>;  
  
经常使用 sendfile(2) 系统调用的繁忙的服务器，    
  
有必要通过 NSFBUFS 内核选项或者在 /boot/loader.conf (查看 loader(8) 以获得更多细节) 中设置它的值来调节 sendfile(2) 缓存数量。  
  
这个参数需要调节的普通原因是在进程中看到 sfbufa 状态。sysctl kern.ipc.nsfbufs 变量在内核配置变量中是只读的。    
  
这个参数是由 kern.maxusers 决定的，然而它可能有必要因此而调整。   
  
在/boot/loader.conf里加入   
  
kern.ipc.nsfbufs="2496"   
  
####################################   
  
  
  
  
  
kern.maxusers: 59   
  
#################<http://www.bsdlover.cn#########&nbsp>;  
  
maxusers 的值决定了处理程序所容许的最大值，20+16\*maxusers 就是你将得到的所容许处理程序。   
  
系统一开机就必须要有 18 个处理程序 (process)，即便是简单的执行指令 man 又会产生 9 个 process，   
  
所以将这个值设为 64 应该是一个合理的数目。   
  
如果你的系统会出现 proc table full 的讯息的话，可以就把它设大一点，例如 128。   
  
除非您的系统会需要同时开启很多档案，否则请不要设定超过 256。   
  
  
  
可以在 /boot/loader.conf 中加入该选项的设定，   
  
kern.maxusers=256   
  
####################################   
  
  
  
kern.coredump: 1   
  
#################<http://www.bsdlover.cn#########&nbsp>;  
  
如果设置为0，则程序异常退出时不会生成core文件，作为服务器，不建议这样。   
  
####################################   
  
  
  
kern.corefile: %N.core   
  
#################<http://www.bsdlover.cn#########&nbsp>;  
  
可设置为kern.corefile="/[data](#)/coredump/%U-%P-%N.core"   
  
其中 %U是UID，%P是进程ID，%N是进程名，当然/data/coredump必须是一个实际存在的目录   
  
####################################   
  
  
  
  
  
vm.swap\_idle\_enabled: 0   
  
vm.swap\_idle\_threshold1: 2   
  
vm.swap\_idle\_threshold2: 10   
  
#########################   
  
在有很多用户进入、离开系统和有很多空闲进程的大的多用户系统中很有用。   
  
可以让进程更快地进入内存，但它会吃掉更多的交换和磁盘带宽。   
  
系统默认的页面调度算法已经很好了，最好不要更改。   
  
########################   
  
  
  
  
  
vfs.ufs.dirhash\_maxmem: 2097152   
  
#########################   
  
默认的dirhash最大内存,默认2M   
  
增加它有助于改善单目录超过100K个文件时的反复读目录时的性能   
  
建议修改为33554432（32M）   
  
#############################   
  
  
  
  
  
vfs.vmiodirenable: 1   
  
#################   
  
这个变量控制目录是否被系统缓存。大多数目录是小的，在系统中只使用单个片断(典型的是1K)并且在缓存中使用的更小 (典型的是512字节)。   
  
当这个变量设置为关闭 (0) 时，缓存器仅仅缓存固定数量的目录，即使您有很大的内存。    
  
而将其开启 (设置为1) 时，则允许缓存器用 VM 页面缓存来缓存这些目录，让所有可用内存来缓存目录。   
  
不利的是最小的用来缓存目录的核心内存是大于 512 字节的物理页面大小(通常是 4k)。   
  
我们建议如果您在运行任何操作大量文件的程序时保持这个选项打开的默认值。    
  
这些服务包括 web 缓存，大容量邮件系统和新闻系统。   
  
尽管可能会浪费一些内存，但打开这个选项通常不会降低性能。但还是应该检验一下。   
  
####################   
  
  
  
  
  
vfs.hirunningspace: 1048576   
  
############################   
  
这个值决定了系统可以将多少[数据](#)放在写入储存设备的等候区。通常使用默认值即可，   
  
但当我们有多颗硬盘时，我们可以将它调大为 4MB 或 5MB。   
  
注意这个设置成很高的值(超过缓存器的写极限)会导致坏的性能。   
  
不要盲目的把它设置太高！高的数值会导致同时发生的读操作的迟延。   
  
#############################   
  
  
  
  
  
vfs.write\_behind: 1   
  
#########################   
  
这个选项预设为 1，也就是打开的状态。在打开时，在系统需要写入数据在硬盘或其它储存设备上时，   
  
它会等到收集了一个 cluster 单位的数据后再一次写入，否则会在一个暂存区空间有写入需求时就立即写到硬盘上。   
  
这个选项打开时，对于一个大的连续的文件写入速度非常有帮助。但如果您遇到有很多行程延滞在等待写入动作时，您可能必须关闭这个功能。   
  
############################   
  
  
  
net.local.stream.sendspace: 8192   
  
##################################   
  
本地套接字连接的数据发送空间   
  
建议设置为65536   
  
###################################   
  
net.local.stream.recvspace: 8192   
  
##################################   
  
本地套接字连接的数据接收空间   
  
建议设置为65536   
  
###################################   
  
  
  
  
  
net.inet.ip.portrange.lowfirst: 1023   
  
net.inet.ip.portrange.lowlast: 600   
  
net.inet.ip.portrange.first: 49152   
  
net.inet.ip.portrange.last: 65535   
  
net.inet.ip.portrange.hifirst: 49152   
  
net.inet.ip.portrange.hilast: 65535   
  
###################   
  
以上六项是用来控制TCP及UDP所使用的port范围，这个范围被分成三个部份，低范围、预设范围、及高范围。   
  
这些是你的服务器主动发起连接时的临时端口的范围，预设的已经1万多了，一般的应用就足够了。   
  
如果是比较忙碌的FTP server，一般也不会同时提供给1万多人访问的，   
  
当然如果很不幸，你的服务器就要提供很多，那么可以修改first的值，比如直接用1024开始   
  
#########################   
  
  
  
  
  
net.inet.ip.redirect: 1   
  
#########################   
  
设置为0，屏蔽ip重定向功能   
  
###########################   
  
  
  
net.inet.ip.rtexpire: 3600   
  
net.inet.ip.rtminexpire: 10   
  
########################   
  
很多apache产生的CL[OS](#)E\_WAIT状态，这种状态是等待客户端关闭，但是客户端那边并没有正常的关闭，于是留下很多这样的东东。   
  
建议都修改为2   
  
#########################   
  
  
  
  
  
net.inet.ip.intr\_queue\_maxlen: 50   
  
########################   
  
Maximum size of the IP input queue，如果下面的net.inet.ip.intr\_queue\_drops一直在增加，   
  
那就说明你的队列空间不足了，那么可以考虑增加该值。   
  
##########################   
  
net.inet.ip.intr\_queue\_drops: 0   
  
####################   
  
Number of packets dropped from the IP input queue,如果你sysctl它一直在增加，   
  
那么增加net.inet.ip.intr\_queue\_maxlen的值。   
  
#######################   
  
  
  
  
  
net.inet.ip.fastforwarding: 0   
  
#############################   
  
如果打开的话每个目标地址一次转发成功以后它的[数据](#)都将被记录进路由表和arp数据表，节约路由的计算时间   
  
但会需要大量的内核内存空间来保存路由表。   
  
如果内存够大，打开吧，呵呵   
  
#############################   
  
  
  
  
  
net.inet.ip.random\_id: 0   
  
#####################   
  
默认情况下，ip包的id号是连续的，而这些可能会被攻击者利用，比如可以知道你nat后面带了多少主机。   
  
如果设置成1，则这个id号是随机的，嘿嘿。   
  
#####################   
  
  
  
net.inet.icmp.maskrepl: 0   
  
############################   
  
防止广播风暴，关闭其他广播探测的响应。默认即是，无须修改。   
  
###############################   
  
  
  
net.inet.icmp.icmplim: 200   
  
##############################   
  
限制系统发送ICMP速率，改为100吧，或者保留也可，并不会给系统带来太大的压力。   
  
###########################   
  
net.inet.icmp.icmplim\_output: 1   
  
###################################   
  
如果设置成0，就不会看到提示说Limiting icmp unreach response from 214 to 200 packets per second 等等了  
  
不过禁止输出容易让我们忽视攻击的存在。这个自己看着办吧。   
  
######################################   
  
  
  
net.inet.icmp.drop\_redirect: 0   
  
net.inet.icmp.log\_redirect: 0   
  
###################################   
  
设置为1，屏蔽ICMP重定向功能   
  
###################################   
  
net.inet.icmp.bmcastecho: 0   
  
############################   
  
防止广播风暴，关闭广播ECHO响应，默认即是，无须修改。   
  
###############################   
  
  
  
  
  
net.inet.tcp.mssdflt: 512   
  
net.inet.tcp.minmss: 216   
  
###############################   
  
[数据](#)包数据段最小值，以上两个选项最好不动！或者只修改mssdflt为1460，minmss不动。   
  
原因详见http://www.bsdlover.cn/security/2007/1211/article\_4.html   
  
#############################   
  
  
  
  
  
net.inet.tcp.keepidle: 7200000   
  
######################   
  
TCP的套接字的空闲时间，默认时间太长，可以改为600000（10分钟）。   
  
##########################   
  
  
  
net.inet.tcp.sendspace: 32768   
  
#################<http://www.bsdlover.cn#########&nbsp>;  
  
最大的待发送TCP数据缓冲区空间，应用程序将数据放到这里就认为发送成功了，系统TCP堆栈保证数据的正常发送。   
  
####################################   
  
net.inet.tcp.recvspace: 65536   
  
###################################   
  
最大的接受TCP缓冲区空间，系统从这里将数据分发给不同的套接字，增大该空间可提高系统瞬间接受数据的能力以提高性能。   
  
###################################   
  
这二个选项分别控制了网络 TCP 联机所使用的传送及接收暂存区的大小。预设的传送暂存区为 32K，而接收暂存区为 64K。   
  
如果需要加速 TCP 的传输，可以将这二个值调大一点，但缺点是太大的值会造成系统核心占用太多的内存。   
  
如果我们的机器会同时服务数百或数千个网络联机，那么这二个选项最好维持默认值，否则会造成系统核心内存不足。   
  
但如果我们使用的是 gigabite 的网络，将这二个值调大会有明显效能的提升。   
  
传送及接收的暂存区大小可以分开调整，   
  
例如，假设我们的系统主要做为网页服务器，我们可以将接收的暂存区调小一点，并将传送的暂存区调大，如此一来，我们就可以避免占去太多的核心内存空间。   
  
  
  
net.inet.udp.maxdgram: 9216   
  
#########################   
  
最大的发送UDP[数据](#)缓冲区大小，网上的资料大多都是65536，我个人认为没多大必要，   
  
如果要调整，可以试试24576。   
  
##############################   
  
net.inet.udp.recvspace: 42080   
  
##################   
  
最大的接受UDP缓冲区大小，网上的资料大多都是65536，我个人认为没多大必要，   
  
如果要调整，可以试试49152。   
  
#######################   
  
以上四项配置通常不会导致问题，一般说来网络流量是不对称的，因此应该根据实际情况调整，并观察其效果。   
  
如果我们将传送或接收的暂存区设为大于 65535，除非服务器本身及客户端所使用的[操作系统](#)都支持 TCP 协议的 windows scaling extension (请参考 RFC 1323 文件)。  
  
FreeBSD默认已支持 rfs1323 (即 sysctl 的 net.inet.tcp.rfc1323 选项)。   
  
###################################################   
  
  
  
  
  
net.inet.tcp.log\_in\_vain: 0   
  
##################   
  
记录下任何TCP连接，这个一般情况下不应该更改。   
  
####################   
  
  
  
net.inet.tcp.blackhole: 0   
  
##################################   
  
建议设置为2，接收到一个已经关闭的端口发来的所有包，直接drop，如果设置为1则是只针对TCP包   
  
#####################################   
  
  
  
net.inet.tcp.delayed\_ack: 1   
  
###########################   
  
当一台计算机发起TCP连接请求时，系统会回应ACK应答[数据](#)包。   
  
该选项设置是否延迟ACK应答数据包，把它和包含数据的数据包一起发送。   
  
在高速网络和低负载的情况下会略微提高性能，但在网络连接较差的时候，   
  
对方计算机得不到应答会持续发起连接请求，反而会让网络更加拥堵，降低性能。   
  
因此这个值我建议您看情况而定，如果您的网速不是问题，可以将封包数量减少一半   
  
如果网络不是特别好，那么就设置为0，有请求就先回应，这样其实浪费的网通、电信的带宽速率而不是你的处理时间:)   
  
############################   
  
  
  
  
  
net.inet.tcp.inflight.enable: 1   
  
net.inet.tcp.inflight.debug: 0   
  
net.inet.tcp.inflight.rttthresh: 10   
  
net.inet.tcp.inflight.min: 6144   
  
net.inet.tcp.inflight.max: 1073725440   
  
net.inet.tcp.inflight.stab: 20   
  
###########################   
  
限制 TCP 带宽延迟积和 NetBSD 的 TCP/Vegas 类似。    
  
它可以通过将 sysctl 变量 net.inet.tcp.inflight.enable 设置成 1 来启用。    
  
系统将尝试计算每一个连接的带宽延迟积，并将排队的数据量限制在恰好能保持最优吞吐量的水平上。   
  
这一特性在您的服务器同时向使用普通调制解调器，千兆以太网，乃至更高速度的光与网络连接 (或其他带宽延迟积很大的连接) 的时候尤为重要，   
  
特别是当您同时使用滑动窗缩放，或使用了大的发送窗口的时候。    
  
如果启用了这个选项，您还应该把 net.inet.tcp.inflight.debug 设置为 0 (禁用调试)，   
  
对于生产环境而言， 将 net.inet.tcp.inflight.min 设置成至少 6144 会很有好处。    
  
然而， 需要注意的是，这个值设置过大事实上相当于禁用了连接带宽延迟积限制功能。   
  
这个限制特性减少了在路由和交换包队列的堵塞[数据](#)数量，也减少了在本地主机接口队列阻塞的数据的数量。   
  
在少数的等候队列中、交互式连接，尤其是通过慢速的调制解调器，也能用低的 往返时间操作。   
  
但是，注意这只影响到数据发送 (上载/服务端)。对数据接收(下载)没有效果。   
  
调整 net.inet.tcp.inflight.stab 是 不 推荐的。   
  
这个参数的默认值是 20，表示把 2 个最大包加入到带宽延迟积窗口的计算中。    
  
额外的窗口似的算法更为稳定，并改善对于多变网络环境的相应能力，    
  
但也会导致慢速连接下的 ping 时间增长 (尽管还是会比没有使用 inflight 算法低许多)。    
  
对于这些情形， 您可能会希望把这个参数减少到 15， 10， 或 5；    
  
并可能因此而不得不减少 net.inet.tcp.inflight.min (比如说， 3500) 来得到希望的效果。   
  
减少这些参数的值， 只应作为最后不得已时的手段来使用。   
  
############################   
  
  
  
net.inet.tcp.syncookies: 1   
  
#########################   
  
SYN cookies是一种用于通过选择加密的初始化TCP序列号，可以对回应的包做验证来降低SYN'洪水'攻击的影响的技术。   
  
默认即是，不需修改   
  
########################   
  
  
  
  
  
net.inet.tcp.msl: 30000   
  
#######################   
  
这个值网上很多文章都推荐的7500，   
  
还可以改的更小一些(如2000或2500)，这样可以加快不正常连接的释放过程(三次握手2秒、FIN\_WAIT4秒)。   
  
#########################   
  
net.inet.tcp.always\_keepalive: 1   
  
###########################   
  
帮助系统清除没有正常断开的TCP连接，这增加了一些网络带宽的使用，但是一些死掉的连接最终能被识别并清除。   
  
死的TCP连接是被拨号用户存取的系统的一个特别的问题，因为用户经常断开modem而不正确的关闭活动的连接。   
  
#############################   
  
  
  
net.inet.udp.checksum: 1   
  
#########################   
  
防止不正确的udp包的攻击，默认即是，不需修改   
  
##############################   
  
  
  
net.inet.udp.log\_in\_vain: 0   
  
#######################   
  
记录下任何UDP连接,这个一般情况下不应该修改。   
  
#######################   
  
  
  
net.inet.udp.blackhole: 0   
  
####################   
  
建议设置为1，接收到一个已经关闭的端口发来的所有UDP包直接drop   
  
#######################   
  
  
  
  
  
net.inet.raw.maxdgram: 8192   
  
#########################   
  
Maximum outgoing raw IP [data](#)gram size   
  
很多文章建议设置为65536，好像没多大必要。   
  
######################################   
  
net.inet.raw.recvspace: 8192   
  
######################   
  
Maximum incoming raw IP datagram size   
  
很多文章建议设置为65536，好像没多大必要。   
  
#######################   
  
  
  
net.link.ether.inet.max\_age: 1200   
  
####################   
  
调整ARP清理的时间，通过向IP路由缓冲填充伪造的ARP条目可以让恶意用户产生资源耗竭和性能减低攻击。   
  
这项似乎大家都未做改动，我建议不动或者稍微减少，比如300（HP-UX默认的5分钟）   
  
#######################   
  
  
  
net.inet6.ip6.redirect: 1   
  
###############################   
  
设置为0，屏蔽ipv6重定向功能   
  
###########################   
  
  
  
  
  
net.isr.direct: 0   
  
#################<http://www.bsdlover.cn#########&nbsp>;  
  
所有MPSAFE的网络ISR对包做立即响应,提高网卡性能，设置为1。   
  
####################################   
  
  
  
  
  
hw.ata.wc: 1   
  
#####################   
  
这个选项用来打开 IDE 硬盘快取。当打开时，如果有[数据](#)要写入硬盘时，硬盘会假装已完成写入，并将数据快取起来。   
  
这种作法会加速硬盘的存取速度，但当系统异常关机时，比较容易造成数据遗失。   
  
不过由于关闭这个功能所带来的速度差异实在太大，建议还是保留原本打开的状态吧，不做修改。   
  
###################   
  
  
  
  
  
security.bsd.see\_other\_uids: 1   
  
security.bsd.see\_other\_gids: 1   
  
#####################   
  
不允许用户看到其他用户的进程,因此应该改成0， 

#######################

写得很好，自己亲自实践了，效果不错，感谢作者！原文地址：http://[blog](#).csdn.net/21aspnet/article/details/6584792

软件实用程序
