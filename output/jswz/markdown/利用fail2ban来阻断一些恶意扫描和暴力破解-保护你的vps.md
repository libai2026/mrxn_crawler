---
title: "利用fail2ban来阻断一些恶意扫描和暴力破解---保护你的VPS"
source: https://mrxn.net/jswz/use-fail2ban-to-protect-yourvps.html
asset_dir: assets/利用fail2ban来阻断一些恶意扫描和暴力破解-保护你的vps
---

# 利用fail2ban来阻断一些恶意扫描和暴力破解---保护你的VPS

[Mrxn](https://mrxn.net/author/1)- 发表于2018/6/23 13:33
- 15855浏览
- [17评论](#comment)
- 23分钟阅读

深入探索

漏洞预警服务

SQL注入防护

编程语言教程

---

**UPdate:使用效果很明显，就这么几天扫描快9W次，ban了八百多IP**

[[![利用fail2ban来阻断一些恶意扫描和暴力破解---保护你的VPS](images/img-001-13fe883476b3.png "点击查看原图_Mrxn")](../content/uploadfile/201807/16d91530537042.png)](../content/uploadfile/201807/16d91530537042.png)

简单介绍一下:

如果把vps的iptables比作是一把枪，那么fail2ban就是除了你之外的另一个忠心的手下，他可以拿着枪来枪毙或管理那些非法的探视，将他们拒之门外，将一些危险扼杀在萌芽阶段。但是，他也仅仅是个手下，不是超人，可况超人也不是万能的！所以也不要以为有了它就可以高枕无忧了，这就好比一个人在厉害，也不可能打过一群人。fail2ban可以防御一定范围的CC、暴力破解登录或者是恶意扫描等等。

安装：

推荐使用这个一键脚本（lnmp.org作者写的）：

wget <https://raw.githubusercontent.com/licess/lnmp/master/tools/fail2ban.sh> && ./fail2ban.sh

第二种方法就是自己手动去fail2ban的GitHub下载解压安装，地址：

<https://github.com/fail2ban/fail2ban>

最后一种就是直接通过包安装，但是可能不是最新的：

Debian/Ubuntu:apt install fail2ban

centos:yum install fail2ban

安装完来配置使其监控我们的nginx、apache或其他服务的日志，从日志中提取我们需要屏蔽的一些恶意请求，比如大量的404---通过扫描器扫描产生，ssh暴力破解，v2ray的暴力尝试爆破ID等等。

如果是通过第一种，使用一键脚本安装的话，我们只需要修改 /etc/fail2ban/jail.local 这个文件然后在 /etc/fail2ban/filter.d/中添加自己的规则文件即可。

比如我的在/etc/fail2ban/jail.local 中追加如下内容,下面使用cat命令直接追加：

cat >>/etc/fail2ban/jail.local<<EOF

[sshd]  
enabled = true  
port = ssh  
filter = sshd  
action = iptables[name=SSH, port=ssh, protocol=tcp]  
#mail-whois[name=SSH, dest=yourmail@mail.com]  
logpath = /var/log/auth.log  
maxretry = 5  
bantime = 604800

[deny-badcrawl]  
enabled = true  
port = http,https  
filter = deny-badcrawl  
action = iptables[name=Http, port=80, protocol=tcp]  
action = iptables[name=Https, port=443, protocol=tcp]  
logpath = /home/wwwlogs/\*.log  
maxretry = 4  
findtime = 3600  
bantime = 3600

[nginx-limit-req]  
enabled = true  
port = http,https  
logpath = /usr/local/nginx/conf/nginx.conf  
action = iptables[name=Http, port=80, protocol=tcp]  
action = iptables[name=Https, port=443, protocol=tcp]  
maxretry = 4  
findtime = 600  
bantime = 600

EOF

请注意SSH的port，如果你自己修改过端口号，那么请把port替换成你自己修改的端口号。nginx-limit-req需要你在你的nginx配置文件中配置了才能生效的。

深入探索

安全

文本剥离工具

恶意软件分析工具

因为nginx-limit-req新版本的fail2ban已经有了，具体的可以在 /etc/fail2ban/filter.d 目录下面查看。

好了，然后我们在 /etc/fail2ban/filter.d 目录下新建一个deny-badcrawl.conf：

touch deny-badcrawl.conf

然后将如下内容写进去（我依旧是使用的cat命令，你可以根据自己喜好，比如nano，vi等）：

cat >>/etc/fail2ban/filter.d/deny-badcrawl.conf<<EOF

[Definition]  
failregex = <HOST> -.\*- .\*HTTP/\*.\* 404 .\*$  
ignoreregex =

EOF

然后重启fail2ban即可:service fail2ban restart

然后查看状态：fail2ban-client status

查看某个规则的具体状态：fail2ban-client status deny-badcrawl

像我这里使用了几个小时后就封了好几个IP：

[[![利用fail2ban来阻断一些恶意扫描和暴力破解---保护你的VPS](images/img-002-88e669a7d457.png "点击查看原图_Mrxn")](../content/uploadfile/201806/1c7c1529735470.png)](../content/uploadfile/201806/1c7c1529735470.png)

注意：一般修改配置文件后，我们只需要重新载入即可，不需要重启fail2ban:

fail2ban-client reload nginx-limit-req 如果不生效，就强制重新加载service fail2ban force-reload nginx-limit-req

OK

具体的fail2ban用法和详细参数设置这些，早有前辈写过很多，不过最好是去官网看英文原版。

- 标签：
- [#攻击](https://mrxn.net/tag/%E6%94%BB%E5%87%BB)
- [#Linux](https://mrxn.net/tag/Linux)
- [#扫描](https://mrxn.net/tag/%E6%89%AB%E6%8F%8F)
- [#运维](https://mrxn.net/tag/%E8%BF%90%E7%BB%B4)

---

文章目录

  
  

![](data:image/png;base64,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)

手机扫码阅读
