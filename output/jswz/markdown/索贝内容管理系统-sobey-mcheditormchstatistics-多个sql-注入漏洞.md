---
title: "索贝内容管理系统 /sobey-mchEditor/mch/statistics 多个SQL 注入漏洞"
source: https://mrxn.net/jswz/sobey-statistics-wxarticleList-sqli.html
asset_dir: assets/索贝内容管理系统-sobey-mcheditormchstatistics-多个sql-注入漏洞
---

# 索贝内容管理系统 /sobey-mchEditor/mch/statistics 多个SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/18 08:21
- 1053浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

计算机安全

数据库

统计学

---

# 漏洞简介

索贝融媒体系统的 /sobey-mchEditor/mch/[statistics](#) 接口下多个方法如`wxarticleList`、`wxarticleTotalList`、`queryMultiArgListCreateNname`、`countWxarticleByChannel`、`articleList`、`articleListTotal`、`articleListId`、`articlePaymentList`、`countArticleByUser`、`queryArgList`、`countArticleBysubColumn`、`countArticleByBaobiaoUser`、`getCustomFieldByCodes`均存在多个[SQL 注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意SQL语句注入到该接口的多个参数中，进而实现任意SQL语句执行，可能导致数据库敏感信息泄露、数据篡改，甚至在部分情况下进一步获取系统控制权限。影响范围包括数据库的完整性、保密性及可用性，严重时可能危及整个系统安全。

内容管理

# 影响版本

# fofa语法

> app="SOBEY-融媒体"
>
> 统计信息

# 漏洞分析

深入探索

网络安全课程

编程语言教程

安全运维咨询

看下存在漏洞的`wxarticleList`方法是如何实现的吧

```
@RestController
@RequestMapping({"/mch/statistics"})
public class ArticleListController extends BaseController {
```

在该方法的顶部定义了路径前缀为 `/mch/statistics` ,接着是各种子方法，其中`wxarticleList`方法实现如下

SQL注入检测工具

[![索贝内容管理系统 /sobey-mchEditor/mch/statistics 多个SQL 注入漏洞](images/img-001-026f3c30ab25.webp)](https://image.mrxn.net/6aab9a51e9b94c73b8eca8baa2a50860.webp)

[![索贝内容管理系统 /sobey-mchEditor/mch/statistics 多个SQL 注入漏洞](images/img-002-5323b4c051f0.webp)](https://image.mrxn.net/2ddda8947fe54ecb9dd7339bf3570231.webp)

多个参数createUserCode**、**username**、**title、channelId以及id均没有采用其他参数类似的参数化绑定查询，而是直接格式化拼接进SQL语句中，然后直接用`queryBuilder1.executeOneValue`来执行组装完成的SQL语句，从而形成SQL注入漏洞。

代码安全审计

深入探索

授权

云安全解决方案

网络安全会议

其他方法如下

wxarticleTotalList

[![索贝内容管理系统 /sobey-mchEditor/mch/statistics 多个SQL 注入漏洞](images/img-003-74508fb7dcd4.webp)](https://image.mrxn.net/2c878837bba649bf92c316ba16ead189.webp)

也是多个参数被直接拼接进SQL语句执行造成SQL注入漏洞。

漏洞修复方案

queryMultiArgListCreateNname

[![索贝内容管理系统 /sobey-mchEditor/mch/statistics 多个SQL 注入漏洞](images/img-004-afa039a446a0.webp)](https://image.mrxn.net/af00ba9e34bc4c2ba0a2272b13a70410.webp)

[![索贝内容管理系统 /sobey-mchEditor/mch/statistics 多个SQL 注入漏洞](images/img-005-7f7970907bfe.webp)](https://image.mrxn.net/5dfef9d9f5ba465285120b039b0c51fc.webp)

当parameter=editor或者auditor时，channelId参数被直接拼接进SQL语句进行执行，从而造成了SQL注入漏洞。

编程

countWxarticleByChannel

[![索贝内容管理系统 /sobey-mchEditor/mch/statistics 多个SQL 注入漏洞](images/img-006-504aa28fb9f0.webp)](https://image.mrxn.net/8699443ac3eb4859bc5f076703fae551.webp)

还有其他多个方法就不一一列举了，太多了！

数据管理

# 漏洞复现

```
POST /sobey-mchEditor/mch/statistics/js/../wxarticleList HTTP/1.1
Host: sobey.mrxn.net
Content-Type: application/x-www-form-urlencoded

createUserCode=1'SQLI_POC--+-&token=1&siteCode=1
```

[![索贝内容管理系统 /sobey-mchEditor/mch/statistics 多个SQL 注入漏洞](images/img-007-26796bef6a0c.webp)](https://image.mrxn.net/94bcb9c3fbdf46ea8c5d78f47c41ef3d.webp)

通过报错注入，成功在响应里回显数据库版本信息

Windows安全工具

## wxarticleTotalList

[![索贝内容管理系统 /sobey-mchEditor/mch/statistics 多个SQL 注入漏洞](images/img-008-bde707dc65d1.webp)](https://image.mrxn.net/2fee03fde92c4f6c810ec2962da88285.webp)

## queryMultiArgListCreateNname

[![索贝内容管理系统 /sobey-mchEditor/mch/statistics 多个SQL 注入漏洞](images/img-009-86aa54ff6d8b.webp)](https://image.mrxn.net/8d2e6ca45b87429293bc126f9c180e43.webp)

## countWxarticleByChannel

[![索贝内容管理系统 /sobey-mchEditor/mch/statistics 多个SQL 注入漏洞](images/img-010-5756c5e0f73b.webp)](https://image.mrxn.net/57e1f35d1471484cad25f07d3c008785.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [5.1.wxarticleTotalList](#toc-5-1-)
- [5.2.queryMultiArgListCreateNname](#toc-5-2-)
- [5.3.countWxarticleByChannel](#toc-5-3-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALMklEQVR4Aeyai3bbOBJEdfP//5xNq3xpokmQUjSxdM7SZ7HFenQDRlOT2DO/brfb779Zv7++rP2i017P+rP8TK9z6Iml1ZJ3LK+Wej3vre7LRWs6V38GayB/8tf/PuUGloH8me7tkdUPbg1wAxZbXQG4++qi/gzNiT2nXtg9OWRvuVg1teQdy6sFqa/nWhAOwV4nr+wjy3zhMpAi13r/DWwGApk6jHh21P4mQOpnuv305SKkfsbVj9DeIqQnjGgPc3JIruudm58hpA+MuJffDGQvdGk/dwMvDwQy9X7k/hbBmINjbj0kN+PrfSFZCOpBuD3UO1cXz/xnc+aP8OWBHDW/vOdv4OWB+BZB3kKPAOEQVD9D+/UcjH0gHL6x18h7z84hPczPEMZc7zOre0Z/eSDPbHZlz29gMxCn3vG8VRLAjT8r7M+vAX7/Pvz5pufk4uwcXV9za0XImw3Brj/K3QPGPtbP0LqOe/nNQPZCl/ZzN7AMBDJ1OMZ+NEje6evLIb46vMbtI0L6AUpT7GeSWzDjwP23DOY6wr4P0eEY1/2WgazF6/l9N/DLt+JZ9MjWyc/wLN99OeQt6/31C7sHqSmvVvdnvLK19Ou5Vuew37+yf7uuT4i3/CG4GQhk6p4PwmHE7stFSH7G1TvCWKfvGyeH5GCLZnpN1yG1PQfRzUM4jKgvQnx5R9j3ITpw2wzkdn299QaWgUCm1N+Wfjp9SF4fwvXV/yuE/f7ut0b3hNTIRYhuDYRDUN28fIY9J+9oPWSf7hdfBlLkWu+/gc1AINODoFP1qDDq+qK5GULqIWgdjNx6iH673ZTuaN2dtP+beTD2gnDzYmt3/xkEWGRg0YBFf/YBuPdZ120Gsjav55+/gV+QKc3ejn4kc5A6CJqDcHMznOUf1XsOsi98oxmxn0VdhNR2bp262HVIPQTNwcit28PrE+KtfQhOB+L0+jlhnHb3Zxz26/o+kFzX5SIkt7efme5BaiBoDsLNw8jVz9B+5uCxPpAccP0ccvuwr+knBL6nBizH9i0QNYDN3xj0jhCO62D0Ibzvv7fHWQb2e/U6SA6C+hDe99bvaA7268qfDqTMa/38DSwDgUxtNlV1SM6jqnfUF/VnvOuQfayDcHOifqEa7Gf1K7teMOZh5OtsPUP8eq5lX4guF2HUq6YWjHrll4EUudb7b2AZSE2sFmyntj5mZWqttXqG/Tp4Tq9etWqPWpD6eq5V3myVv17mID3kInDjz1rX1LN+PdeC43o49u0nQvLVu69lIIYvfO8NbAbixGCcoseE6DOuLvZ+kHp10bwIY07dPMSHc5zV2ktfVIf0Vhf15R1hv+6R3GYgvejiP3sDy0Dgsan+7dvR62B/Pxh1CIfg0fX0Pcyqw34PGHUIt84+IsSX95xcNAdjXdeB6yf124d9LZ+Qfi6nC5kq7KN15kVIXh/C9bsOo29ONP8MWgvp/UztM1kY+0M4BD2HeNR7OpCjosv7dzew/HdZbgGZqtypniHs18Go27ej/eGxfK8vDse17iFWTS05HNdXdm9ZrycXYeyrbn6N1ydkfRsf8LwMxKmJng3G6UI4BM2JMOr2E811hNTNcuqQnPXqhWody6ulDukBI1amVs91Xpn10lcD7r/5hvTXh5GrW1e4DETzwvfewPLv1CHTgxFrarU8Zj3Xkncsr5Y6pF/nlVmv7sNx3V5ezb5ySC8Iqvdc12e+uRn2OrnY6yDnAq6fQ24f9rX8I8vpiZ4TvqcH38/dn3H7QWrNibCv97rOrd9DOO65V/OI5hnMQvaBfTzL6a9xGchavJ7fdwObgUCm3d8GeUePPtPP/LM66zv2ujWfZSHf26M+jHkIh+Csz/os9WyuntdLfY2bgazN6/nnb2AZCIxTh5F7NNjX9TtC8hDs/qsc0hfYtAJ2fx7wLbUAkuu6vqgvqneE9HtUt1/hMpBefPH33MA1kPfc+3TX5ZeL9XGptU7uPVemVvcgH1MIdr9qanUdkoegPoRXTS31juW5jrzKdF9eXi25WFotOeRM8vJqycXSaslnWJlaa//6hKxv4wOeNwOpia2XZ4S8HTCi/rqmniG5eq5lDqLLy6s14zDmzUF02GLPyGufWpAadRi5eseqrdV1OaQPjKg/Q/jObwYyK7r0n7mBzS8X3RYytXoj9pY5PUi+63LRvPxVtF+hvep5vWA8mzmIbrbr8kex95F37P3W/vUJ6bfzZr75WxaMbw2Ew4hn54b9PES3HsJ9SyBcf6brP4OQ3vbstRBfHUZ+puv3/pA+EDQnQnTg+vX77cO+Xv4zBDJd3woYef9+e04f9utg1K0XrV8jpGat1fOsBpLXn2H1qKUPqSutFoRDsLSjBdvc9WfI0Y29wdv8GeL0Z2eB7VQrC9Fn9RAfgubE6lEL9n2IXplaMPLSXL2n+gzNw9gTRn5Wf+a7zyxX+vUJqVv4oPXwQCBvy2zK6pAcBP1e9eUijDl1EUYfwu0H4YAlG+zZTeBLeDQH3H+t3/Pyr3YLQPKL8PVgfo0PD+SrxwX/+AZOBwKZrlOE8H4u2Nd7zj7qMw7pp9+x1699SK2ZRxH+rs69Yb/+zIfUAdfPIbcP+9r8HAKZVj8nRHfaj6J9IPUQVO8I+z6MOoTDFu0J8eSeWS5Ccvpi9+X6kDp1UV/eEVIHwbV/+o+sdfh6/vc3MP05pE9ZDuNUIRxG7Ee3Xuy+vPuQvvowcvNHCGMNjNxaGHX31JefIez3Oasr//qE1C180NoMBMbp9rej8/696EP6yM1B9M57Tl/UF9XFRxCytz1Ea+Uw5vRFGH0I1+8Io+8+5uSFm4EYuvA9N7AMBDLFmlItCIegx4ORV7aW/hlWthaMfSAcgpWpZT+ILt9DSAaCZqrPesHow8jNWg/HvnnROlFd7Lq8cBlIkWu9/waWgTg9yNsg94gw6hCuP0NIDkbsefcTIXm5eYjeOaC0IHD/nRMENXrPzuE4D6Nv3zOEsQ7C4RuXgZw1u/yfuYFlIJAp9belczjOQfx+fPvMcJZXt06+hz3TOeyfDfZ194Bj/ywHYz2E9/NVn2UgRa71/hvYDAQyPQh6RKcpwuhDuH5H+4iQPATVO0J8CHZ/zWHMQLhnMQvR5SJE7/lHfXMde78ZL30zkN7s4j97A8tve/u2Na1aXYe8RV2vbC2ID/toXWXXSx1SJzcj/y8Rxr3sDdEhqC7CqMPIew5GH0ZuvvD6hNQtfNCa/rZ3dkbfWBEybQiqWy8XITl9CIdgz8GoW2duD3sGxh69xrzYfXn35aK5jjMfci74xusT4m19CC5/hsD3lOD82fPP3gZ9SC+5eYguFyH6LK8uQvKA0oLA/Sf13huiL8H2AI/5sJ+Dfd1tYO5fnxBv6UNwGYhv0Rn2c0OmDSP2PjD69oF9Xf8M1/v0rB5kj+53bl4dUgfB7pvreJY78peB9KYXf88NbAYCeRtgxLPj9anDa/X2g/Tp+0N02GLP2ktdDqlVF/XlIiSvL3YfkoNg9+WifQo3AzF04Xtu4OWB1FRrQd6Geq41+3bKWy9zkPrOzarPuPoarYHHesOYW/daP/e+a2/9bE7U6xyyL3D9l4u3D/t6+RMCma7fF4T7Noj6Z9jzMPaDka/7Qby1Vs+9pxzGvHrVvLJg7Nt7wdx/eSB9s4u/dgObgfiWdJxtY677ML4Fs5y6CGNd7/sMh/SCoHvYo3P1jpB6dTjmva8cUjfjpW8G4qYXvucGloFApgfHODtmTXdvmYf0lXeE+Pbovlwfklcv1Kvn9VKH1MCIZmHUIbz79lPvXF2E9JnlID5w/S3r9mFfyyfkw871f3uc/wEAAP//AeKiYAAAAAZJREFUAwA/PWWw4XLZNAAAAABJRU5ErkJggg==)

手机扫码阅读
