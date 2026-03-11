---
title: "利用python脚本实现Windows网卡叠加"
source: https://mrxn.net/jswz/python-improve-windows-netcard.html
asset_dir: assets/利用python脚本实现windows网卡叠加
---

# 利用python脚本实现Windows网卡叠加

[Mrxn](https://mrxn.net/author/1)- 发表于2016/3/28 09:21
- 5711浏览
- [0评论](#comment)
- 1小时阅读

深入探索

JSON处理工具

网络安全课程

网络安全培训

---

以前经常在网上找网卡叠加的小[软件](#)，找过很多个，有的用不来有的没效果，偶尔找到一个能用的批处理，于是根据这个脚本自己用python写了一个修改路由表的方案，这样一来下次就不用在网上找来找去了，简单实用（水平有限，还请在座各位多多指教）。

[[![利用python脚本实现Windows网卡叠加](images/img-001-182e51410f36.png "点击查看原图")](https://mrxn.net/content/uploadfile/201603/thum-9cfc1459128240.png)](https://mrxn.net/content/uploadfile/201603/9cfc1459128240.png)

废话不多说直接贴代码，送给需要的人

```
#coding:utf-8

#调用库
import sys,os,re

#函数
def pro_continue():
    input("按Enter键退出")

def nic_count(x):
    if   x<2:
         print("网络叠加需要两块或两块以上网卡")
         exit()
    elif x>4:
         print("该程序最多支持叠加四块网卡")
         exit()

def add_routetables2(i,g):
    net_1=[1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,47,49,51,53,55,57,59,61,63,65,67,69,71,73,75,77,79,81,83,85,87,89,91,93,95,97,99,101,103,105,107,109,111,113,115,117,119,121,123,125,129,131,133,135,137,139,141,143,145,147,149,151,153,155,157,159,161,163,165,167,171,173,175,177,179,181,183,185,187,189,191,193,195,197,199,201,203,205,207,209,211,213,215,217,219,221,223]
    net_2=[2,4,6,8,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,100,102,104,106,108,110,112,114,116,118,120,122,124,126,128,130,132,134,136,138,140,142,144,146,148,150,152,154,156,158,160,162,164,166,168,170,174,176,178,180,182,184,186,188,190,194,196,198,200,202,204,206,208,210,212,214,216,218,220,222]
    print("开始<span class='wp_keywordlink_affiliate'><a href="http://www.slll.info/archives/tag/%e8%b4%9f%e8%bd%bd%e5%9d%87%e8%a1%a1" title="View all posts in 负载均衡" target="_blank">负载均衡</a></span>")
    os.system("route delete 0.0.0.0")
    os.system("route add 0.0.0.0 mask 0.0.0.0 " + str(g[0]) + " metric 30 if " + str(i[0]))
    a=0
    for x in net_1:
        os.system ("route add " + str(x) + ".0.0.0 mask 255.0.0.0 "+ str(g[0]) +" metric 25 if " + str(i[0]))
    for x in net_2:
        os.system ("route add " + str(x) + ".0.0.0 mask 255.0.0.0 "+ str(g[1]) +" metric 25 if " + str(i[1]))
    print("双网卡叠加成功")

def add_routetables3(i,g):
    net_1=[1,4,7,13,16,19,22,25,28,31,34,37,40,43,46,49,52,55,58,61,64,67,70,73,76,79,82,85,88,91,94,97,100,103,106,109,112,115,118,121,124,130,133,136,139,142,145,148,151,154,157,160,163,166,175,178,181,184,187,190,193,196,199,202,205,208,211,214,217,220,223]
    net_2=[2,5,8,11,14,17,20,23,26,29,32,35,38,41,44,47,50,53,56,59,62,65,68,71,74,77,80,83,86,89,92,95,98,101,104,107,110,113,116,119,122,125,128,131,134,137,140,143,146,149,152,155,158,161,164,167,170,173,176,179,182,185,188,191,194,197,200,203,206,209,212,215,218,221]
    net_3=[3,6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57,60,63,66,69,72,75,78,81,84,87,90,93,96,99,102,105,108,111,114,117,120,123,126,129,132,135,138,141,144,147,150,153,156,159,162,165,168,171,174,177,180,183,186,189,195,198,201,204,207,210,213,216,219,222]
    print("开始<span class='wp_keywordlink_affiliate'><a href="http://www.slll.info/archives/tag/%e8%b4%9f%e8%bd%bd%e5%9d%87%e8%a1%a1" title="View all posts in 负载均衡" target="_blank">负载均衡</a></span>")
    os.system("route delete 0.0.0.0")
    os.system("route add 0.0.0.0 mask 0.0.0.0 " + str(g[0]) + " metric 30 if " + str(i[0]))
    a=0
    for x in net_1:
        os.system ("route add " + str(x) + ".0.0.0 mask 255.0.0.0 "+ str(g[0]) +" metric 25 if " + str(i[0]))
    for x in net_2:
        os.system ("route add " + str(x) + ".0.0.0 mask 255.0.0.0 "+ str(g[1]) +" metric 25 if " + str(i[1]))
    for x in net_3:
        os.system ("route add " + str(x) + ".0.0.0 mask 255.0.0.0 "+ str(g[2]) +" metric 25 if " + str(i[2]))
    print("三网卡叠加成功")

def add_routetables4(i,g):
    net_1=[1,5,9,13,17,21,25,29,33,37,41,45,49,53,57,61,65,69,73,77,81,85,89,93,97,101,105,109,113,117,121,125,129,133,137,141,145,149,153,157,161,165,173,177,181,185,189,193,197,201,205,209,213,217,221]
    net_2=[2,6,14,18,22,26,30,34,38,42,46,50,54,58,62,66,70,74,78,82,86,90,94,98,102,106,110,114,118,122,126,130,134,138,142,146,150,154,158,162,166,170,174,178,182,186,190,194,198,202,206,210,214,218,222]
    net_3=[3,7,11,15,19,23,27,31,35,39,43,47,51,55,59,63,67,71,75,79,83,87,91,95,99,103,107,111,115,119,123,131,135,139,143,147,151,155,159,163,167,171,175,179,183,187,191,195,199,203,207,211,215,219,223]
    net_4=[4,8,12,16,20,24,28,32,36,40,44,48,52,56,60,64,68,72,76,80,84,88,92,96,100,104,108,112,116,120,124,128,132,136,140,144,148,152,156,160,164,168,176,180,184,188,196,200,204,208,212,216,220]
    print("开始负载均衡")
    os.system("route delete 0.0.0.0")
    os.system("route add 0.0.0.0 mask 0.0.0.0 " + str(g[0]) + " metric 30 if " + str(i[0]))
    a=0
    for x in net_1:
        os.system ("route add " + str(x) + ".0.0.0 mask 255.0.0.0 "+ str(g[0]) +" metric 25 if " + str(i[0]))
    for x in net_2:
        os.system ("route add " + str(x) + ".0.0.0 mask 255.0.0.0 "+ str(g[1]) +" metric 25 if " + str(i[1]))
    for x in net_3:
        os.system ("route add " + str(x) + ".0.0.0 mask 255.0.0.0 "+ str(g[2]) +" metric 25 if " + str(i[2]))
    for x in net_4:
        os.system ("route add " + str(x) + ".0.0.0 mask 255.0.0.0 "+ str(g[3]) +" metric 25 if " + str(i[3]))
    print("四网卡叠加成功")

def check_ip(ip_str):
    pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
    if re.match(pattern, ip_str):
        return True
    else:
        return False

#主程序
os.system("title 网卡叠加-www.slll.info&&color 18")
net_count=int(input("请输入网卡数量(MAX:4,Min:2): "))
nic_count(net_count)
arr_1=[]
arr_2=[]
for x in range(1,net_count+1):
    temp=input("请输入第"+str(x)+"块需要叠加的网卡索引号 (cmd下面利用该命令查看:route print | find \"...\"[第一列即索引号]): ")
    arr_1.append(temp)
    temp=input("请输入网卡(" +str(x)+") 的网关: ")
    while True:
        if check_ip(temp):
            arr_2.append(temp)
            break
        else:
            temp=input("输入错误,请重新输入网卡(" +str(x)+") 的网关: ")
if net_count==2:
    add_routetables2(arr_1,arr_2)
elif net_count==3:
    add_routetables3(arr_1,arr_2)
elif net_count==4:
    add_routetables4(arr_1,arr_2)
pro_continue()
```

注：此文并非博主原创，文章很有实用性，转载之，原文请移步：http://www.slll.info/archives/2153.html

- 标签：
- [#脚本](https://mrxn.net/tag/%E8%84%9A%E6%9C%AC)
- [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
- [#windows](https://mrxn.net/tag/windows)

---

文章目录

  
  

![](data:image/png;base64,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)

手机扫码阅读
