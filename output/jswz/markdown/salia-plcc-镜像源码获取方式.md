---
title: "Salia PLCC 镜像源码获取方式"
source: https://mrxn.net/jswz/salia-plcc-source-code-extraction.html
asset_dir: assets/salia-plcc-镜像源码获取方式
---

# Salia PLCC 镜像源码获取方式

[Mrxn](https://mrxn.net/author/1)- 发表于2025/6/8 08:34
- 702浏览
- [0评论](#comment)
- 20分钟阅读

深入探索

filesystem

firmware

固件

---

# 下载镜像

从官网下载镜像

`http://salia.echarge.de/firmware/`

[![Salia PLCC 镜像源码获取方式](images/img-001-6b449a9a7fe4.webp)](https://image.mrxn.net/00f39d8af68b45ea8ed62bb917727074.webp)

目前可以下载 1.50.0 以及 2.2.0 两个版本的镜像

深入探索

服务器安全服务

VPN服务

安全认证考试

`http://salia.echarge.de/firmware/firmware_2.2.0.image`

`http://salia.echarge.de/firmware/firmware_1.50.0.image`

# 剥离镜像

对下载下来的镜像使用 `binwalk` 的 `-e` 参数对镜像进行解压剥离

```
# binwalk -e firmware_1.50.0.image
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             Squashfs filesystem, little endian, version 4.0, compression:gzip, size: 65128626 bytes, 18 inodes, blocksize: 131072 bytes, created: 2021-10-15 17:56:28
65130496      0x3E1D000       Object signature in DER format (PKCS header length: 4, sequence length: 2439
65130554      0x3E1D03A       Certificate in DER format (x509 v3), header length: 4, sequence length: 1466
```

得到解压后的 ext4 文件系统镜像文件 `file _firmware_1.50.0.image.extracted/squashfs-root/core-image-minimal-tarragon.ext4`

# 提取源码

主要就是 创建一个挂载点目录后直接挂载上面得到 `ext4` 文件系统镜像文件

```
sudo mkdir /mnt/ext4image
sudo mount -o loop _firmware_1.50.0.image.extracted/squashfs-root/core-image-minimal-tarragon.ext4 /mnt/ext4image
cd /mnt/ext4image
# 访问文件后 卸载
sudo umount /mnt/ext4image
```

深入探索

授权

SQL

漏洞修复方案

然后再进入目录即可 得到完整的系统文件

```
总计 39
drwxr-xr-x  2 root root  3072 2022-02-03 21:27 bin
drwxr-xr-x  2 root root  1024 2022-02-03 21:27 boot
drwxr-xr-x  2 root root  1024 2021-11-30 17:50 dev
drwxr-xr-x 40 root root  3072 2021-10-16 01:55 etc
drwxr-xr-x  3 root root  1024 2022-02-03 21:26 home
drwxr-xr-x  9 root root  4096 2021-10-16 02:12 lib
drwx------  2 root root 12288 2022-02-03 21:28 lost+found
drwxr-xr-x  2 root root  1024 2021-11-30 17:50 media
drwxr-xr-x  2 root root  1024 2021-11-30 17:50 mnt
dr-xr-xr-x  2 root root  1024 2021-11-30 17:50 proc
drwxr-xr-x  2 root root  1024 2021-11-30 17:50 run
drwxr-xr-x  2 root root  3072 2021-10-16 02:10 sbin
dr-xr-xr-x  2 root root  1024 2021-11-30 17:50 sys
drwxrwxrwt  2 root root  1024 2021-11-30 17:50 tmp
drwxr-xr-x 11 root root  1024 2022-02-03 21:27 usr
drwxr-xr-x 10 root root  1024 2021-10-16 02:10 var
drwxrwxrwx 24 root root  3072 2021-10-16 01:47 www
```

- 标签：
- [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
- [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)

---

文章目录

- [1.下载镜像](#toc-1-)
- [2.剥离镜像](#toc-2-)
- [3.提取源码](#toc-3-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
