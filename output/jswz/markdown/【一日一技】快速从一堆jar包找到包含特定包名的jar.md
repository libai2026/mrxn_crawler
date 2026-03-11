---
title: "【一日一技】快速从一堆jar包找到包含特定包名的jar"
source: https://mrxn.net/jswz/find-class-in-multiple-jars.html
asset_dir: assets/【一日一技】快速从一堆jar包找到包含特定包名的jar
---

# 【一日一技】快速从一堆jar包找到包含特定包名的jar

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/19 19:26
- 763浏览
- [0评论](#comment)
- 16分钟阅读

深入探索

库

Apache Struts

find

---

在日常[java](https://mrxn.net/tag/Java)代码审计中，经常遇到项目包含一大堆jar包，全部放入库中会增加巨大的索引耗时，

软件

除了常见的spring struts2 等框架jar包可以放入库中，方便搜索相关路由外，我们只需要搜索到包含我们需要审计的jar包即可，方法也很简单，直接使用`jar tf`命令配合`grep -q`命令即可完成

这里以亿赛通为例，切到jar所在目录，或者直接写上完整路径也可以

> 搜索指定位置的jar
>
> 开发工具

```
for jar in ./*.jar; do
    if jar tf "$jar" | grep -q 'com/esafenet/'; then
        echo "$jar"
    fi
done
```

脚本大致逻辑: 使用 `jar tf` 命令列出 JAR 包中的文件，如果找到包含 `com/esafenet/` 的路径，则输出该 JAR 包的名称。

深入探索

漏洞预警服务

编程语言教程

JSON处理工具

[![【一日一技】快速从一堆jar包找到包含特定包名的jar](images/img-001-bf545e9898e9.webp)](https://image.mrxn.net/13faa623bc334d02bd12fb7903688dcf.webp)

即可快速筛选出我们需要的jar包，然后直接右键加入库即可开始正常[审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)。

[![【一日一技】快速从一堆jar包找到包含特定包名的jar](images/img-002-c5c0483b17e0.webp)](https://image.mrxn.net/31e1491ce9be47a09246bd58bbb93ffa.webp)

win参考如下（[AI](https://mrxn.net/tag/%E5%A4%A7%E6%A8%A1%E5%9E%8B)生成，自测）

软件

深入探索

网络安全会议

VPN服务

网络安全课程

```
Get-ChildItem -Filter *.jar | ForEach-Object {
    if (jar tf $_.FullName | Select-String -Quiet 'com/esafenet/') {
        $_.Name
    }
}
```

# 改进版本

搜索当前目录及其子目录下所有jar

```
find . -name "*.jar" | while read jar; do
    if jar tf "$jar" | grep -q 'nc/bs/oa/oaco/im/'; then
        echo "$jar"
    fi
done
```

深入探索

编码转换工具

安全认证考试

传输层安全性协议

win参考如下（[AI](https://mrxn.net/tag/%E5%A4%A7%E6%A8%A1%E5%9E%8B)生成，自测）

```
Get-ChildItem -Recurse -Filter *.jar | ForEach-Object {
    if (jar tf $_.FullName | Select-String -Quiet 'nc/bs/oa/oaco/im/') {
        $_.FullName
    }
}
```

比如今天有朋友问在[用友NC importExcelTemplate 任意文件上传漏洞](https://mrxn.net/jswz/yonyou-nc-importExcelTemplate-upload-rce.html) 文章下面问如何查看importExcelTemplate方法对应的jar包是哪一个，在nc的安装目录的`/home/modules`下使用如下命令查找包含`uap/lfw/dbl/cpdoc/impt/action` 包名的jar包

```
#modules find . -name "*.jar" | while read jar; do                           
    if jar tf "$jar" | grep -q 'uap/lfw/dbl/cpdoc/impt/action'; then
        echo "$jar"
    fi
done
./webdbl/lib/pubwebdbl_dblLevel-1.jar
```

成功获取到`uap/lfw/dbl/cpdoc/impt/action` 包名所在jar包`/home/modules/webdbl/lib/pubwebdbl_dblLevel-1.jar`

然后可以导入IDEA的库里用作类或者直接使用`jd-gui` 来查看

[![【一日一技】快速从一堆jar包找到包含特定包名的jar](images/img-003-9a1cbbd26b15.webp)](https://image.mrxn.net/4c3b10b9d0ef4c489d8aaad5e7025456.webp)

符合上面漏洞分析部分，对吧。

软件

其次是还可以使用批量反编译jar包成class，然后导入IDEA进行搜索，亦或者使用许少开发的`jar-analyzer`来进行处理后，再导入IDEA进行[代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)。

PS: 现在有[AI](https://mrxn.net/tag/%E5%A4%A7%E6%A8%A1%E5%9E%8B)辅助，代码审计、解释代码、写命令，写docker compose、写代码等等之前繁琐的工作变得更加方便快捷。

漏洞修复方案

- 标签：
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#大模型](https://mrxn.net/tag/%E5%A4%A7%E6%A8%A1%E5%9E%8B)

---

文章目录

- [1.改进版本](#toc-1-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
