---
title: "孚盟云CRM AjaxSendDingdingMessage.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-AjaxSendDingdingMessage-sqli.html
asset_dir: assets/孚盟云crm-ajaxsenddingdingmessage.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxSendDingdingMessage.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/22 08:26
- 613浏览
- [0评论](#comment)
- 28分钟阅读

深入探索

软件

软件即服务

鉴权

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxSendDingdingMessage.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

深入探索

编程语言教程

安全研究工具

Docker加速服务

直接看 AjaxSendDingdingMessage.ashx 对应的dll文件 FumaCRM\_BS.NewWeb.dll 里有关 **AjaxSendDingdingMessage** 方法的实现如下

```
try
{
  string empId = context.Request["empId"] == null ? "" : context.Request["empId"];
  if (string.IsNullOrWhiteSpace(empId))
  {
    o.Status = "E";
    o.Message = "empId is empty";
    context.Response.Write(JSON.Encode((object) o));
  }
  else
  {
    string str = context.Request["action"] == null ? "" : context.Request["action"];
    if (!string.IsNullOrWhiteSpace(str))
    {
      if (string.op_Equality(str, "SendDingMeg_Mail"))
        this.SendDingMeg_Mail(context, empId);
      else if (string.op_Equality(str, "StopSendDingdingMessage"))
        this.StopSendDingdingMessage(context, empId);
      else if (string.op_Equality(str, "GetSendDingdingMessageFlag"))
      {
        this.GetSendDingdingMessageFlag(context, empId);
      }
      else
      {
        if (!string.op_Equality(str, "SaveSendDingdingMessageFlag"))
          return;
        this.SaveSendDingdingMessageFlag(context, empId);
      }
    }
```

深入探索

文件大小转换

安全认证考试

文本剥离工具

当 **method=SendDingMeg\_Mail** 时，进入**SendDingMeg\_Mail**方法

```
private void SendDingMeg_Mail(HttpContext context, string empId)
{
  ResultMessage resultMessage = new ResultMessage();
  ResultMessage o = this.SendDingMeg_Mail(context.Request["agentId"] == null ? "" : context.Request["agentId"], context.Request["headText"] == null ? "" : context.Request["headText"], context.Request["bodyTitle"] == null ? "" : context.Request["bodyTitle"], context.Request["bodyContent"] == null ? "" : context.Request["bodyContent"], context.Request["bodyFormList"] == null ? "" : context.Request["bodyFormList"], context.Request["messageUrl"] == null ? "" : context.Request["messageUrl"], empId, context);
  context.Response.Write(JSON.Encode((object) o));
}
```

跟进 **SendDingMeg\_Mail** 方法

```
public ResultMessage SendDingMeg_Mail(
  string agentId,
  string headText,
  string bodyTitle,
  string bodyContent,
  string bodyForm,
  string messageUrl,
  string empId,
  HttpContext context = null)
{
  ResultMessage resultMessage = new ResultMessage();
  try
  {
    object single = this.dbHelper.GetSingle($"select SendCount from sySendDingdingMessage where EmpId = '{empId}' and SendDate = '{DateTime.Now.ToString("yyyy-MM-dd")}'");
```

最终可以看到，未经过滤或参数化绑定的参数 **empId** 被直接拼接进SQL语句中进行执行，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

其他当 action=**StopSendDingdingMessage**、**GetSendDingdingMessageFlag**和**SaveSendDingdingMessageFlag**时，均存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /m/Dingding/Ajax/AjaxSendDingdingMessage.ashx?method=SendDingMeg_Mail&empId=SQLI_POC HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM AjaxSendDingdingMessage.ashx SQL注入漏洞](images/img-001-eb88e358ac58.webp)](https://image.mrxn.net/d2fb6f8292614538a29fa33e438df803.webp)

成功通过报错注入在响应回显数据库版本信息

编程

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
