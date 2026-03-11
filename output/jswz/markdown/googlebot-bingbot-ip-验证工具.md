---
title: "Googlebot | Bingbot IP 验证工具"
source: https://mrxn.net/jswz/Googlebot-Bingbot-IP-Check-Tools.html
asset_dir: assets/googlebot-bingbot-ip-验证工具
---

# Googlebot | Bingbot IP 验证工具

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/26 15:28
- 606浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

Googlebot

网络机器人

googlebot

---

# 开发目的

> 验证IP地址是否属于Google和Bing官方爬虫，支持批量处理、结果缓存和表格导出功能
>
> 搜索引擎

在网站运营中，识别真正的Google和Bing爬虫至关重要。恶意爬虫常伪装成Googlebot和Bingbot窃取数据，而官方推荐的验证方法繁琐且无法批量操作。为解决这一痛点，我们开发了这款工具，帮助网站管理员：

- 批量验证可疑IP的真实性
- 防止虚假爬虫引发的安全风险
- 优化服务器资源分配
- 满足SEO优化中的爬虫分析需求

# 基本功能

## 核心验证机制

1. **官方网段校验**  
   实时拉取Google和Bing官方公布的bot网段（来自多个JSON源），检查IP是否在授权范围内
2. **双重DNS验证**
   - PTR反向查询：解析IP对应的主机名
   - 正向A记录验证：检查主机名解析结果是否与原始IP一致
   - 后缀检测：验证主机名以`.googlebot.com.`或`.msn.com.`结尾
3. **智能批量处理**
   - 支持多种分隔符：换行/逗号/空格分隔的IP输入
   - 自动过滤无效地址：排除私有IP、保留地址等非常规IP
   - 异步队列处理：每个IP检测间隔0.5-1.5秒随机延迟，避免请求封锁

## 功能一览

深入探索

安全研究报告

传输层安全性协议

漏洞修复方案

[![Googlebot | Bingbot IP 验证工具](images/img-001-e7dccc5a370f.gif)](https://image.mrxn.net/aba3b5d2063b4c8fa14ae1ea391544a8.gif)

导出结果查看详细检查内容

互联网软件

[![Googlebot | Bingbot IP 验证工具](images/img-002-eb737e02db15.webp)](https://image.mrxn.net/b2f557adc6ef4cb2b393b495e851da14.webp)

# 开发设计

## 架构亮点

1. **分层验证逻辑**

   网络门户

   ```
   async function validateGooglebot(ip) {
    const cidrs = await getCachedCIDRs(); // 带缓存的网段获取
    const inRange = checkIPInCIDR(ip, cidrs);
    const ptrRecord = await dnsLookup(ip, "PTR");
    const aRecord = await dnsLookup(ptrHostname, "A");
    return inRange && validSuffix(ptrRecord) && aRecord.includes(ip);
   }
   ```
2. **性能优化设计**

   - **CIDR缓存**：网段数据本地存储24小时，减少90%冗余请求
   - **结果缓存**：IP验证结果存储7天，支持离线查看历史记录
   - **请求调度**：自动暂停/恢复机制防止资源过载
3. **容错机制**

   - 跨域代理：通过corsproxy.io解决官方数据源跨域限制
   - 重试策略：DNS查询失败时自动重试（最多3次）
   - 超时处理：所有网络请求设置5秒超时阈值

#### 数据流示意图

[![Googlebot | Bingbot IP 验证工具](images/img-003-54d373c72aa6.webp)](https://image.mrxn.net/390948d826d24238897df87300a6997a.webp)

其中实时检测部分有**四重校验逻辑**，如下图所示

网络安全

[![Googlebot | Bingbot IP 验证工具](images/img-004-ac46ba523096.webp)](https://image.mrxn.net/8d4162f29d5041d285ee77e4aa14b4c5.webp)

在线体验地址：<https://mrxn.net/botcheck/index.html>

# 参考

- <https://developers.google.com/search/docs/crawling-indexing/verifying-googlebot>
- <https://www.bing.com/toolbox/bingbot.json>

- 标签：
- [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
- [#网络安全](https://mrxn.net/tag/%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#html](https://mrxn.net/tag/html)
- [#JavaScript](https://mrxn.net/tag/JavaScript)
- [#工具](https://mrxn.net/tag/%E5%B7%A5%E5%85%B7)

---

文章目录

- [1.开发目的](#toc-1-)
- [2.基本功能](#toc-2-)
- [2.1.核心验证机制](#toc-2-1-)
- [2.2.功能一览](#toc-2-2-)
- [3.开发设计](#toc-3-)
- [3.1.架构亮点](#toc-3-1-)
- [3.1.1.数据流示意图](#toc-3-1-1-)
- [4.参考](#toc-4-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
