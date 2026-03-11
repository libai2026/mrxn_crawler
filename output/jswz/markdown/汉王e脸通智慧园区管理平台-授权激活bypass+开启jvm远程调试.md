---
title: "汉王e脸通智慧园区管理平台 授权激活bypass+开启JVM远程调试"
source: https://mrxn.net/jswz/efacego-auth-bypass.html
asset_dir: assets/汉王e脸通智慧园区管理平台-授权激活bypass+开启jvm远程调试
---

# 汉王e脸通智慧园区管理平台 授权激活bypass+开启JVM远程调试

[Mrxn](https://mrxn.net/author/1)- 发表于2025/6/27 08:20
- 1025浏览
- [5评论](#comment)
- 22分钟阅读

深入探索

debug

server

JVM

---

# 开启调试总体流程

- 卸载服务
- 修改服务
- 安装并启动服务
- 检查端口

## 卸载服务

```
net stop Tomcat8
# 或者 直接杀死进程
service.bat remove
@echo 【卸载Tomcat】
cd %installPath%\Tomcat8\bin
taskkill /F /IM tomcat8.exe /T
taskkill /F /IM tomcat8s.exe /T
call service.bat remove
```

## 修改服务

修改 `service.bat` 找到 `--JvmOptions` 增加 jvm 调试配置端口信息

编程

深入探索

服务器安全服务

Nessus

传输层安全性协议

```
--JvmOptions "-Dcatalina.home=%CATALINA_HOME%;-Dcatalina.base=%CATALINA_BASE%;-D%ENDORSED_PROP%=%CATALINA_HOME%\endorsed;-Djava.io.tmpdir=%CATALINA_BASE%\temp;-Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager;-Djava.util.logging.config.file=%CATALINA_BASE%\conf\logging.properties;-Dfile.encoding=UTF-8;-XX:PermSize=512M;-XX:MaxPermSize=1024M;%JvmArgs%" ^
```

修改成如下

网络安全

```
--JvmOptions "-Dcatalina.home=%CATALINA_HOME%;-Dcatalina.base=%CATALINA_BASE%;-D%ENDORSED_PROP%=%CATALINA_HOME%\endorsed;-Djava.io.tmpdir=%CATALINA_BASE%\temp;-Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager;-Djava.util.logging.config.file=%CATALINA_BASE%\conf\logging.properties;-Dfile.encoding=UTF-8;-XX:PermSize=512M;-XX:MaxPermSize=1024M;-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005;%JvmArgs%" ^
```

## 安装并启动服务

```
service.bat install
sc qc tomcat8
net start tomcat8
netstat -ano | findstr "5005"
```

[![汉王e脸通智慧园区管理平台 授权激活bypass+开启JVM远程调试](images/img-001-1dc37861bf1b.webp)](https://image.mrxn.net/36a9e15353b1461b9c917e7734fbb019.webp)

[![汉王e脸通智慧园区管理平台 授权激活bypass+开启JVM远程调试](images/img-002-75adbd236d2f.webp)](https://image.mrxn.net/931ff4cc02bb4b8d9f86a7f003e94ba5.webp)

就可以开始 debug 了

Java（编程语言）

# mysql 连接信息解密

使用 Tools 目录下的 `encrypt-gui.jar` 解密即可得到帐号密码 `root:kq_123654`

[![汉王e脸通智慧园区管理平台 授权激活bypass+开启JVM远程调试](images/img-003-adfdf4fce828.webp)](https://image.mrxn.net/a060d8e2bd14402984b0470b323914be.webp)

成功登录MySQL

软件

[![汉王e脸通智慧园区管理平台 授权激活bypass+开启JVM远程调试](images/img-004-25f9ababc881.webp)](https://image.mrxn.net/fe9993bfc9224597a97e1a2fa001e889.webp)

# 系统默认帐号

`admin:123654`

需要两次md5解密 `c2106dc9520c4edf378fd09732d2f87a1940062b`

[![汉王e脸通智慧园区管理平台 授权激活bypass+开启JVM远程调试](images/img-005-89e2396f8fdd.webp)](https://image.mrxn.net/5529c19310a646aa864bfec06c44bc3f.webp)

第一次解密

编程

[![汉王e脸通智慧园区管理平台 授权激活bypass+开启JVM远程调试](images/img-006-64f3697e1bf1.webp)](https://image.mrxn.net/4dd3b6b166db4c50acf90d9805c77edb.webp)

第二次解密

[![汉王e脸通智慧园区管理平台 授权激活bypass+开启JVM远程调试](images/img-007-ca9ac9bef37d.webp)](https://image.mrxn.net/132d0cdc7aee436089eb0eca9a3bef7e.webp)

# hook激活流程

> 仅测试了 1.6.x 版本，最新版2.0.x 没有测试

## 未hook之前

[![汉王e脸通智慧园区管理平台 授权激活bypass+开启JVM远程调试](images/img-008-6160dd4c546b.webp)](https://image.mrxn.net/a0e7f009cc864634990234d33110e81d.webp)

[![汉王e脸通智慧园区管理平台 授权激活bypass+开启JVM远程调试](images/img-009-ba849606fba2.webp)](https://image.mrxn.net/002c65c41d7242d58810f1f309bd7d05.webp)

最开始是Hook了启动时的授权校验，但是发现登录还有校验

网络安全

[![汉王e脸通智慧园区管理平台 授权激活bypass+开启JVM远程调试](images/img-010-dc348615d743.webp)](https://image.mrxn.net/e9569265bab74f2595852e1221fe7df0.webp)

[![汉王e脸通智慧园区管理平台 授权激活bypass+开启JVM远程调试](images/img-011-59fad57f8a44.webp)](https://image.mrxn.net/c4cd33d531d34af498612c917cab8fbf.webp)

[![汉王e脸通智慧园区管理平台 授权激活bypass+开启JVM远程调试](images/img-012-e93972c4f829.webp)](https://image.mrxn.net/a6d66582d50849308d0900ea3f2c9919.webp)

手动修改 state 值成功绕过校验进入后台

[![汉王e脸通智慧园区管理平台 授权激活bypass+开启JVM远程调试](images/img-013-8bfe2398c385.webp)](https://image.mrxn.net/57ba0429855f4846aea2a0f3f17c0687.webp)

## hook之后

[![汉王e脸通智慧园区管理平台 授权激活bypass+开启JVM远程调试](images/img-014-c9fc3bf8a4c5.webp)](https://image.mrxn.net/7a31b984c573444dacb752667308ef88.webp)

随便输入mac与key都可激活

[![汉王e脸通智慧园区管理平台 授权激活bypass+开启JVM远程调试](images/img-015-196182bf593e.webp)](https://image.mrxn.net/13e1628284264f36a2da1d2c6c5bd68e.webp)

### 如何hook？

选择hook `LoginController` 下的 `systemAuthorization.do` 方法里的`int state = Utils.`*`validSystemState`*`();` 部分

[![汉王e脸通智慧园区管理平台 授权激活bypass+开启JVM远程调试](images/img-016-cd6fc05137a9.webp)](https://image.mrxn.net/4f178c4eb65046f498b386006d9a777e.webp)

下载 `fuck-efacego-1.0-SNAPSHOT.jar` 然后复制到 应用 lib 目录下，然后修改 `catalina.bat` 如下

```
:execCmd
rem Get remaining unshifted command line arguments and save them in the
set CMD_LINE_ARGS=
set "CATALINA_OPTS=%CATALINA_OPTS% -javaagent:C:\EFaceGo\Tomcat8\webapps\manage\WEB-INF\lib\fuck-efacego-1.0-SNAPSHOT.jar -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005"
set "JAVA_OPTS=%JAVA_OPTS% -Dfile.encoding=UTF-8"
```

然后手动在命令行启动 `catalina.bat run`

出现 `MyAgent loaded!` 且没有报错就代表hook成功了

[![汉王e脸通智慧园区管理平台 授权激活bypass+开启JVM远程调试](images/img-017-99ddc69d42dc.webp)](https://image.mrxn.net/bd7636fa7d9e4185b099a2d3b3f1e061.webp)

最终完美搞定验证!

bypass jar文件下载 [fuck-efacego-1.0-SNAPSHOT](https://image.mrxn.net/f1fb6b7888dd4762a6da77e1e8e4bc98.jar)

文件SHA256: **1783bb952355f5a8933f869328bfb0de2cc706ced4d9d10c5e906376a449078d**

**下载完记得核对文件的hash值！**

- 标签：
- [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#工具](https://mrxn.net/tag/%E5%B7%A5%E5%85%B7)
- [#权限绕过](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)

---

文章目录

- [1.开启调试总体流程](#toc-1-)
- [1.1.卸载服务](#toc-1-1-)
- [1.2.修改服务](#toc-1-2-)
- [1.3.安装并启动服务](#toc-1-3-)
- [2.mysql 连接信息解密](#toc-2-)
- [3.系统默认帐号](#toc-3-)
- [4.hook激活流程](#toc-4-)
- [4.1.未hook之前](#toc-4-1-)
- [4.2.hook之后](#toc-4-2-)
- [4.2.1.如何hook？](#toc-4-2-1-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
